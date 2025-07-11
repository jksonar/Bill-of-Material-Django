from django import forms
from .models import Style

class StyleForm(forms.ModelForm):
    class Meta:
        model = Style
        fields = ['code', 'name', 'category', 'image', 'sizes', 'colors']
        widgets = {
            'sizes': forms.CheckboxSelectMultiple,
            'colors': forms.CheckboxSelectMultiple,
        }

class ConsumptionUploadForm(forms.Form):
    file = forms.FileField()