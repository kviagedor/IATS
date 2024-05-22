from django import forms

class CSVUploadForm(forms.Form):
    file = forms.FileField(widget=forms.ClearableFileInput(attrs={'class': 'custom-file-input'}))
