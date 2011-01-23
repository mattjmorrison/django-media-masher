from django import forms
from sample_app import SCRIPT_ONE, STYLE_ONE

class SampleForm(forms.Form):
    username = forms.CharField(max_length=50)
    password = forms.CharField(max_length=50)

    class Media:
        css = {'all': (STYLE_ONE, )}
        js = (SCRIPT_ONE,)
