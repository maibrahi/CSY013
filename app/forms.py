from django import forms
from .models import SheetImage

class SheetImageForm(forms.ModelForm):
    class Meta:
        model = SheetImage
        fields = ('image', )

class ModuleForm(forms.Form):
    code = forms.CharField(label='Module Code', max_length=200)
    name = forms.CharField(label='Module Name', max_length=200)
