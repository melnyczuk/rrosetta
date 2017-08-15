## Gmail OAuth2 Jazz ##
# THIS CODE IS LARGELY TAKEN FROM A SCRIPT FREELY PROVIDED GOOGLE AS PART OF THEIR API DOCUMENTATION ##
#-------------------------
from __future__ import print_function

import base64
import logging
import os

import httplib2
from bs4 import BeautifulSoup
#-------------------------
## GOOGLE API MODULES ##
from googleapiclient import discovery, errors, http
from googleapiclient.discovery import build
from oauth2client import client
from oauth2client import tools
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage

from google.oauth2 import service_account

#-------------------------
#=========================

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/gmail-python-quickstart.json
CLIENT_SECRET_FILE = 'client_secret.json'
CLIENTSECRETS_LOCATION = 'C:/Users/HPM/.credential/'
APPLICATION_NAME = 'Rrosetta'

REDIRECT_URI = [
    "urn:ietf:wg:oauth:2.0:oob",
    "http://rrosetta.uk"
]
SCOPES = [
    'https://www.googleapis.com/auth/gmail.readonly',
    'https://www.googleapis.com/auth/userinfo.email',
    'https://www.googleapis.com/auth/userinfo.profile',
]

#=========================


def get__credentials():
    credentials = service_account.Credentials.from_service_account_file('client_secret.json')
    return credentials.with_scopes(SCOPES)
#-------------------------

def debug():
    from google.auth.transport.urllib3 import AuthorizedHttp
    """Shows basic usage of the Gmail API.

    Creates a Gmail API service object and outputs a list of label names
    of the user's Gmail account.
    """
    credentials = get__credentials()
    authed_http = AuthorizedHttp(credentials)
    response = authed_http.request(
    'GET', 'https://www.googleapis.com/storage/v1/b')

    return response

def get_credentials(authorization_code, state):
    """Retrieve credentials using the provided authorization code.

    This function exchanges the authorization code for an access token and queries
    the UserInfo API to retrieve the user's e-mail address.
    If a refresh token has been retrieved along with an access token, it is stored
    in the application database using the user's e-mail address as key.
    If no refresh token has been retrieved, the function checks in the application
    database for one and returns it if found or raises a NoRefreshTokenException
    with the authorization URL to redirect the user to.

    Args:
    authorization_code: Authorization code to use to retrieve an access token.
    state: State to set to the authorization URL in case of error.
    Returns:
    oauth2client.client.OAuth2Credentials instance containing an access and
    refresh token.
    Raises:
    CodeExchangeError: Could not exchange the authorization code.
    NoRefreshTokenException: No refresh token could be retrieved from the
                                                    available sources.
    """
    email_address = ''
    try:
        credentials = exchange_code(authorization_code)
        store = Storage(credentials)
        user_info = get_user_info(credentials)
        email_address = user_info.get('email')
        user_id = user_info.get('id')
        if credentials is not None:
            return credentials
        if credentials.refresh_token is not None:
            store = Storage(credentials)
            return credentials
        else:
            if credentials and credentials.refresh_token is not None:
                return credentials
    except errors.Error as error:
        logging.error('An error occurred during code exchange.')
        # Drive apps should try to retrieve the user and credentials for the current
        # session.
        # If none is available, redirect the user to the authorization URL.
        error.authorization_url = get_authorization_url(email_address, state)
        raise error
    except:  # NoUserIdException:
        logging.error('No user ID could be retrieved.')
        # No refresh token has been retrieved.
        authorization_url = get_authorization_url(email_address, state)
        # raise NoRefreshTokenException(authorization_url)
#-------------------------


def get_authorization_url(email_address, state):
    """Retrieve the authorization URL.

    Args:
    email_address: User's e-mail address.
    state: State for the authorization URL.
    Returns:
    Authorization URL to redirect the user to.
    """
    flow = flow_from_clientsecrets(CLIENTSECRETS_LOCATION, ' '.join(SCOPES))
    flow.params['access_type'] = 'offline'
    flow.params['approval_prompt'] = 'force'
    flow.params['user_id'] = email_address
    flow.params['state'] = state
    return flow.step1_get_authorize_url(REDIRECT_URI)
#-------------------------


def build_service(credentials):
    """Build a Gmail service object.

    Args:
    credentials: OAuth 2.0 credentials.

    Returns:
    Gmail service object.
    """
    http = httplib2.Http()
    http = credentials.authorize(http)
    return build('gmail', 'v1', http=http)
#-------------------------


def get_user_info(credentials):
    """Send a request to the UserInfo API to retrieve the user's information.

    Args:
    credentials: oauth2client.client.OAuth2Credentials instance to authorize the
                            request.
    Returns:
    User information as a dict.
    """
    user_info_service = build(
        serviceName='oauth2', version='v2', http=credentials.authorize(httplib2.Http()))
    user_info = None
    try:
        user_info = user_info_service.user_info().get().execute()
    except errors.HttpError as e:
        logging.error('An error occurred: %s', e)
    if user_info and user_info.get('id'):
        return user_info
    else:
        print('An error occurred')
        # raise NoUserIdException()
#-------------------------


def exchange_code(authorization_code):
    """Exchange an authorization code for OAuth 2.0 credentials.

    Args:
    authorization_code: Authorization code to exchange for OAuth 2.0
                                            credentials.
    Returns:
    oauth2client.client.OAuth2Credentials instance.
    Raises:
    CodeExchangeException: an error occurred.
    """
    flow = flow_from_clientsecrets(CLIENTSECRETS_LOCATION, ' '.join(SCOPES))
    flow.redirect_uri = REDIRECT_URI
    try:
        credentials = flow.step2_exchange(authorization_code)
        return credentials
    except Exception as error:  # FlowExchangeError as error:
        logging.error('An error occurred: %s', error)
        # raise CodeExchangeException(None)
#-------------------------
