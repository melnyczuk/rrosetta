from django.conf.urls import url
from django.views.generic import TemplateView
from .views import load

urlpatterns = [
    url(r'^$', load), 
]