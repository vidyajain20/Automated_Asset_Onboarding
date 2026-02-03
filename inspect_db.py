import os
import django
import sys

# Setup Django environment
sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'asset_manager.settings')
django.setup()

from assets.models import Asset

def inspect_data():
    print("Checking for 'nan' values...")
    nan_ips = Asset.objects.filter(ip_address='nan').count()
    nan_macs = Asset.objects.filter(mac_address='nan').count()
    
    print(f"Assets with ip_address='nan': {nan_ips}")
    print(f"Assets with mac_address='nan': {nan_macs}")
    
    # Also check for empty strings in GenericIPAddressField which might be storing '' as string instead of None
    # Note: SQLite stores mixed types, so it might store empty string.
    # GenericIPAddressField should represent None as None.
    
    print("\nSample IP values:")
    for asset in Asset.objects.all()[:5]:
        print(f"ID: {asset.asset_id}, IP: {repr(asset.ip_address)}, Mac: {repr(asset.mac_address)}")

if __name__ == '__main__':
    inspect_data()
