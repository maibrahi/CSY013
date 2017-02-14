from django import forms

class ModuleForm(forms.Form):
    code = forms.CharField(label='Module Code', max_length=200)
    name = forms.CharField(label='Module Name', max_length=200)
