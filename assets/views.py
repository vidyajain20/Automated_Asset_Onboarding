from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Asset
from .forms import AssetUploadForm
from .utils import generate_asset_id, generate_ci_name
import pandas as pd
import threading
import time

def dashboard(request):
    assets = Asset.objects.all()
    
    # KPIs
    total_assets = assets.count()
    active_assets = assets.filter(status='Active').count()
    maintenance_assets = assets.filter(status='Maintenance').count()
    decommissioned_assets = assets.filter(status='Decommissioned').count()

    context = {
        'assets': assets,
        'total_assets': total_assets,
        'active_assets': active_assets,
        'maintenance_assets': maintenance_assets,
        'decommissioned_assets': decommissioned_assets,
    }
    return render(request, 'assets/dashboard.html', context)

def mock_dmr_scan(asset_id, ip_address):
    """
    Simulates a DMR scan process.
    """
    print(f"Starting DMR scan for {asset_id} at {ip_address}...")
    time.sleep(5) # Simulate network delay
    try:
        from .models import Asset # Import locally to avoid circular import issues if any, though here it is fine
        asset = Asset.objects.get(asset_id=asset_id)
        asset.dmr_status = 'Scanned'
        asset.save()
        print(f"DMR scan complete for {asset_id}. Status updated.")
    except Asset.DoesNotExist:
        print(f"Asset {asset_id} not found during scan.")

def upload_asset(request):
    if request.method == 'POST':
        form = AssetUploadForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = request.FILES['file']
            try:
                # Read using pandas
                df = pd.read_excel(uploaded_file)
                
                # Normalize columns to handle case sensitivity
                df.columns = df.columns.str.strip()
                
                # Column mapping helper
                def get_col(row, *aliases):
                    val = None
                    for alias in aliases:
                        if alias in row:
                            val = row[alias]
                            break
                        # Try case insensitive match
                        if val is None:
                            for col in row.index:
                                if col.lower() == alias.lower():
                                    val = row[col]
                                    break
                        if val is not None:
                            break
                    
                    # Clean value
                    if pd.isna(val) or str(val).strip().lower() == 'nan':
                        return None
                    return str(val).strip()

                count = 0
                for index, row in df.iterrows():
                    # Generate ID
                    new_asset_id = generate_asset_id()
                    
                    # Extract fields with fallback
                    serial_number = get_col(row, 'Serial Number', 'Serial No', 'S/N') or ''
                    model_category = get_col(row, 'Model category', 'Category') or ''
                    ci_name = get_col(row, 'CI Name', 'Name')
                    
                    # Auto-generate CI Name if missing
                    if not ci_name:
                        ci_name_gen = generate_ci_name(model_category, serial_number)
                        if ci_name_gen:
                            ci_name = ci_name_gen
                    
                    # Clean IP and Mac
                    ip_addr = get_col(row, 'IP Address', 'IP')
                    mac_addr = get_col(row, 'Mac Address', 'MAC')
                    
                    # Create Asset
                    asset = Asset.objects.create(
                        asset_id=new_asset_id,
                        serial_number=serial_number,
                        asset_tag=get_col(row, 'Asset Tag', 'Tag') or '',
                        model_id=get_col(row, 'Model Id', 'Model ID', 'Model id') or '',
                        model_category=model_category,
                        location=get_col(row, 'Location') or '',
                        ci_name=ci_name or '',
                        ip_address=ip_addr, # Pass None if empty
                        mac_address=mac_addr # Pass None if empty
                    )
                    
                    # Trigger Mock DMR Scan (Background thread to not block UI)
                    if asset.ip_address and asset.ip_address != 'nan':
                         threading.Thread(target=mock_dmr_scan, args=(asset.asset_id, asset.ip_address)).start()
                    
                    count += 1
                
                messages.success(request, f'Successfully uploaded {count} assets.')
                return redirect('dashboard')
            except Exception as e:
                messages.error(request, f'Error processing file: {str(e)}')
    else:
        form = AssetUploadForm()
    
    return render(request, 'assets/upload.html', {'form': form})

from .forms import AssetForm
from django.shortcuts import get_object_or_404

def edit_asset(request, asset_id):
    asset = get_object_or_404(Asset, asset_id=asset_id)
    if request.method == 'POST':
        form = AssetForm(request.POST, instance=asset)
        if form.is_valid():
            form.save()
            messages.success(request, f'Asset {asset.asset_id} updated successfully.')
            return redirect('dashboard')
    else:
        form = AssetForm(instance=asset)
    
    return render(request, 'assets/edit_asset.html', {'form': form, 'asset': asset})
