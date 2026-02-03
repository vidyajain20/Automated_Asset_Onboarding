from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Asset
from .forms import AssetUploadForm
from .utils import generate_asset_id
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
                
                # Expected columns mapping
                # Serial Number, Asset Tag, Model Id, Model category, Location, CI Name, IP Address, Mac Address
                
                count = 0
                for index, row in df.iterrows():
                    # Generate ID
                    new_asset_id = generate_asset_id()
                    
                    # Create Asset
                    asset = Asset.objects.create(
                        asset_id=new_asset_id,
                        serial_number=str(row.get('Serial Number', '')),
                        asset_tag=str(row.get('Asset Tag', '')),
                        model_id=str(row.get('Model Id', '')),
                        model_category=str(row.get('Model category', '')),
                        location=str(row.get('Location', '')),
                        ci_name=str(row.get('CI Name', '')),
                        ip_address=str(row.get('IP Address', '')),
                        mac_address=str(row.get('Mac Address', ''))
                    )
                    
                    # Trigger Mock DMR Scan (Background thread to not block UI)
                    if asset.ip_address:
                         threading.Thread(target=mock_dmr_scan, args=(asset.asset_id, asset.ip_address)).start()
                    
                    count += 1
                
                messages.success(request, f'Successfully uploaded {count} assets.')
                return redirect('dashboard')
            except Exception as e:
                messages.error(request, f'Error processing file: {str(e)}')
    else:
        form = AssetUploadForm()
    
    return render(request, 'assets/upload.html', {'form': form})
