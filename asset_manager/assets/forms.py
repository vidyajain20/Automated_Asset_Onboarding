from django import forms

class AssetUploadForm(forms.Form):
    file = forms.FileField(label='Select Excel File', help_text='Upload .xlsx or .xls file containing asset data')
