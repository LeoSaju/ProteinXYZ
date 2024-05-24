# myapp/forms.py

from django import forms

class UploadPDBFileForm(forms.Form):
    pdb_file = forms.FileField(label='Upload PDB file', widget=forms.ClearableFileInput(attrs={'class': 'form-control-file'}))
