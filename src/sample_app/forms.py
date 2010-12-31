from django import forms
from masher import site
from sample_app import JS_DIR

class SampleForm(forms.Form):
    username = forms.CharField(max_length=50)
    password = forms.CharField(max_length=50)

    class Media:
        js = (site.mash(['%s/one.js' % JS_DIR,
                       '%s/two.js' % JS_DIR,
                       '%s/three.js' % JS_DIR]),)
