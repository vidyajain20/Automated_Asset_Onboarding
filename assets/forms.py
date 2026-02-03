from django import forms

class AssetUploadForm(forms.Form):
    file = forms.FileField(label='Select Excel File', help_text='Upload .xlsx or .xls file containing asset data')

from .models import Asset

class AssetForm(forms.ModelForm):
    class Meta:
        model = Asset
        fields = ['serial_number', 'asset_tag', 'model_id', 'model_category', 'location', 'ci_name', 'ip_address', 'mac_address', 'status', 'dmr_status']
        widgets = {
            'serial_number': forms.TextInput(attrs={'class': 'mt-1 focus:ring-primary focus:border-primary block w-full shadow-sm sm:text-sm border-gray-300 rounded-md'}),
            'asset_tag': forms.TextInput(attrs={'class': 'mt-1 focus:ring-primary focus:border-primary block w-full shadow-sm sm:text-sm border-gray-300 rounded-md'}),
            'model_id': forms.TextInput(attrs={'class': 'mt-1 focus:ring-primary focus:border-primary block w-full shadow-sm sm:text-sm border-gray-300 rounded-md'}),
            'model_category': forms.TextInput(attrs={'class': 'mt-1 focus:ring-primary focus:border-primary block w-full shadow-sm sm:text-sm border-gray-300 rounded-md'}),
            'location': forms.TextInput(attrs={'class': 'mt-1 focus:ring-primary focus:border-primary block w-full shadow-sm sm:text-sm border-gray-300 rounded-md'}),
            'ci_name': forms.TextInput(attrs={'class': 'mt-1 focus:ring-primary focus:border-primary block w-full shadow-sm sm:text-sm border-gray-300 rounded-md'}),
            'ip_address': forms.TextInput(attrs={'class': 'mt-1 focus:ring-primary focus:border-primary block w-full shadow-sm sm:text-sm border-gray-300 rounded-md'}),
            'mac_address': forms.TextInput(attrs={'class': 'mt-1 focus:ring-primary focus:border-primary block w-full shadow-sm sm:text-sm border-gray-300 rounded-md'}),
            'status': forms.Select(attrs={'class': 'mt-1 block w-full py-2 px-3 border border-gray-300 bg-white rounded-md shadow-sm focus:outline-none focus:ring-primary focus:border-primary sm:text-sm'}),
            'dmr_status': forms.Select(attrs={'class': 'mt-1 block w-full py-2 px-3 border border-gray-300 bg-white rounded-md shadow-sm focus:outline-none focus:ring-primary focus:border-primary sm:text-sm'}),
        }
