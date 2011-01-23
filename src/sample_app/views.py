from django.shortcuts import render_to_response
from django.template.context import RequestContext
from sample_app import forms, STATIC_PATH

def index(request):
    return render_to_response("sample_app/index.html",
          {'form':forms.SampleForm(),
           'MEDIA_ROOT':STATIC_PATH},
          context_instance=RequestContext(request))