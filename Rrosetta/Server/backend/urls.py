from django.conf.urls import url
from . import views
from .views import GmailView, GmailCallbackView

urlpatterns = [
    url(r'^$', GmailView.as_view(), name='home'),
    url(r'^callback/$', GmailCallbackView.as_view(), name='gmail-callback'),
]