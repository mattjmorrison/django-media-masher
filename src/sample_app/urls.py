from django.conf.urls.defaults import patterns
from sample_app import views

urlpatterns = patterns('',
    (r'^$', views.index),
)
