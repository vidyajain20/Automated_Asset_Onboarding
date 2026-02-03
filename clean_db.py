import os
import django
import sys

# Setup Django environment
sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'asset_manager.settings')
django.setup()

from assets.models import Asset

def clean_data():
    print("Cleaning data...")
    
    # Fix 'nan' in ip_address
    assets_with_nan_ip = Asset.objects.filter(ip_address='nan')
    print(f"Found {assets_with_nan_ip.count()} assets with IP='nan'. Cleaning...")
    for asset in assets_with_nan_ip:
        asset.ip_address = None
        asset.save()
        
    # Fix 'nan' in mac_address
    assets_with_nan_mac = Asset.objects.filter(mac_address='nan')
    print(f"Found {assets_with_nan_mac.count()} assets with Mac='nan'. Cleaning...")
    for asset in assets_with_nan_mac:
        asset.mac_address = None
        asset.save()
        
    # Fix empty string in ip_address (GenericIPAddressField should be None)
    assets_with_empty_ip = Asset.objects.filter(ip_address='')
    print(f"Found {assets_with_empty_ip.count()} assets with IP=''. Cleaning...")
    for asset in assets_with_empty_ip:
        asset.ip_address = None
        asset.save()

    print("Data cleaning complete.")

if __name__ == '__main__':
    clean_data()
