from django.conf.urls import url
from . import views
from .views import GmailView, GmailCallbackView

# urlpatterns = [
#     # url(r'^index', views.index, name='index'),
#     # url(r'^debug', views.debug, name='test'),
#     url(r'^gmail', views.GmailView.get_redirect_url, name='authenticate'),
#     url(r'^gmailapproved', views.GmailCallbackView.get_context_data, name='test'),
#     #url(r'^citation/[a-z]*', views.citation),
# ]

urlpatterns = [
    url(r'^$', GmailView.as_view(), name='home'),
    url(r'^callback/$', GmailCallbackView.as_view(), name='gmail-callback'),
]