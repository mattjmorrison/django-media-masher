from django.shortcuts import render_to_response
from sample_app import forms

def index(request):
    return render_to_response("sample_app/index.html",
                              {'form':forms.SampleForm()})