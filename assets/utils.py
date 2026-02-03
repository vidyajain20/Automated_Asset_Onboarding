from .models import Asset

def generate_asset_id():
    """
    Generates a sequential Asset ID in the format AST-XXXX.
    Example: AST-0001, AST-0001
    """
    last_asset = Asset.objects.all().order_by('id').last()
    if not last_asset:
        return 'AST-0001'
    
    # Extract the number part
    last_id = last_asset.asset_id
    try:
        prefix, number = last_id.split('-')
        new_number = int(number) + 1
        return f'{prefix}-{new_number:04d}'
    except ValueError:
        return 'AST-0001'

def generate_ci_name(model_category, serial_number):
    """
    Generates a CI Name if missing.
    Format: [Model Category]-[Serial Number]
    """
    if not model_category or not serial_number:
        return None
    
    # Clean inputs
    category = str(model_category).strip()
    serial = str(serial_number).strip()
    
    return f"{category}-{serial}"
