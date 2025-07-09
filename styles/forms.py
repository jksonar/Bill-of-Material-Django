from django import forms

class ConsumptionUploadForm(forms.Form):
    file = forms.FileField()