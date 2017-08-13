from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<_noun>[a-z]+)$', views.make_json, name='make_json'),
]