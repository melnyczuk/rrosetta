# Most of this code is ammended from the Google example for Django

# I began implementing this to see if the authentication problem I'm having is because I'm trying to debug from powershell.

# https://github.com/google/google-api-python-client/blob/master/samples/django_sample/plus/views.py

#=========================

import logging
import os

import httplib2
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseBadRequest, HttpResponseRedirect
from django.shortcuts import render
from googleapiclient.discovery import build
from oauth2client.client import flow_from_clientsecrets
from oauth2client.contrib import xsrfutil
from oauth2client.contrib.django_util.storage import DjangoORMStorage

from server import settings

from .models import CredentialsModel
from .rrosettacore.sent_mail import get_page_tokens, get_sent_bodys

#=========================

# CLIENT_SECRETS, name of a file containing the OAuth 2.0 information for this
# application, including client_id and client_secret, which are found
# on the API Access tab on the Google APIs
# Console <http://code.google.com/apis/console>

FLOW = flow_from_clientsecrets(
    settings.GOOGLE_OAUTH2_CLIENT_SECRETS_JSON,
    scope='https://www.googleapis.com/auth/gmail.readonly',
    redirect_uri='http://127.0.0.1:8000/backend/welcome')       # IS THIS WRONG?

#=========================


@login_required
def index(request):
    storage = DjangoORMStorage(
        CredentialsModel, 'id', request.user, 'credential')
    credential = storage.get()
    if credential is None or credential.invalid == True:
        FLOW.params['state'] = xsrfutil.generate_token(settings.SECRET_KEY,
                                                       request.user)
        authorize_url = FLOW.step1_get_authorize_url()
        return HttpResponseRedirect(authorize_url)
    else:
        http = httplib2.Http()
        http = credential.authorize(http)
        service = build("gmail", "v1", http=http)
        tokens = get_page_tokens(credential._userID, service)
        bodies = get_sent_bodys(
            tokens, credential, credential._userID, service)

        # I could return this to master_control.py to perform the rest of the programme
        return render(request, 'backend/welcome.html', {
            'sent-emails': bodies,
        })
#-------------------------


@login_required
def auth_return(request):
    if not xsrfutil.validate_token(settings.SECRET_KEY, request.REQUEST['state'],
                                   request.user):
        return HttpResponseBadRequest()
    credential = FLOW.step2_exchange(request.REQUEST)
    storage = DjangoORMStorage(
        CredentialsModel, 'id', request.user, 'credential')
    storage.put(credential)
    return HttpResponseRedirect("/")
#-------------------------
