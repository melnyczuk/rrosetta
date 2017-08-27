#PY3#HPM#
# THIS CODE IS LARGELY TAKEN FROM A SCRIPT
#   FREELY PROVIDED GOOGLE AS PART OF THEIR API DOCUMENTATION ##

# Pulls all the sent emails from a gmail user account

#=========================

import base64

import httplib2
from bs4 import BeautifulSoup

#=========================



def get_page_tokens(_service):
    """
    Takes Int, OAuth2 Service
    Returns Int
    --
    Get all the page tokens
    for all the sent emails
    for any given UserID
    """
    sent_results = _service.users().messages().list(
        labelIds='SENT', userId='me').execute()
    newPT = sent_results.get('nextPageToken')
    pageTokens = set()
    pageTokens.add(newPT)
    while newPT != None:
        sent_results = _service.users().messages().list(
            labelIds='SENT', userId='me', pageToken=newPT).execute()
        newPT = sent_results.get('nextPageToken')
        pageTokens.add(newPT)
    return pageTokens
#-------------------------


def single_access_msgs(_service):
    """
    Takes Int, OAuth2 Service
    Returns Gmail Object
    --
    Access just the first page
    of sent emails for any UserID
    """
    sent_results = _service.users().messages().list(
        labelIds='SENT', userId='me').execute()
    return sent_results.get('messages', [])
#-------------------------


def get_sent_msgs(_pageTokens, _service):
    """
    Takes Int, OAuth2 Credential, Int, OAuth2 Service
    Returns List of Strings
    --
    for any given UserID
    get the credentials and service,
    pull each page of sent emails,
    collect in list
    """
    if not _pageTokens or _pageTokens == None:
        print('no pages')
        sentMSGs = single_access_msgs(_service)
    else:
        sentMSGs = []
        for token in _pageTokens:
            sent_results = _service.users().messages().list(
                labelIds='SENT', userId='me', pageToken=token).execute()
            sentMSGs.append(sent_results.get('messages', []))
    return sentMSGs
#-------------------------


def get_sent_ids(_sentMSGs):
    if not _sentMSGs:
        print('no sent messages')
    else:
        sentIDs = []
        for i, page in enumerate(_sentMSGs):
            print('Page: ', i, ' MSGs: ', len(page))
            for MSG in page:
                sentIDs.append(MSG['id'])
        return sentIDs
#-------------------------


def get_sent_contents(_sentIDs, _service):
    if not _sentIDs:
        print('no sent IDs')
    else:
        sentContents = []
        for i, sentID in enumerate(_sentIDs):
            sentContents.append(_service.users().messages().get(
                userId='me', id=sentID, format='full').execute())
            if i % 100 == 0: print(i)
        return sentContents
#-------------------------


def get_sent_bodys(_sentContents):
    if not _sentContents:
        print('no sent msg content')
    else:
        bodys = []
        for sentContent in _sentContents:
            if 'body' not in sentContent['payload'].keys():
                pass
            else:
                # Pulls email bodys, even if email has attachment
                if sentContent['payload']['body']['size'] != 0:
                    bodys.append(sentContent['payload']['body'])
                elif 'parts' in sentContent['payload'].keys():
                    bodys.append(sentContent['payload']['parts'][0]['body'])
        return bodys
#-------------------------


def read_sent_content(_bodys):
    """
    Takes List of Strings
    Returns Set of Strings
    --
    Translate Base64 encoded sent emails
    into UTF-8 encoded strings
    collected in a list of sent emails
    """
    sent_emails = set()
    if not _bodys:
        print('no MSG bodies')
    else:
        for body in _bodys:
            if 'data' not in body.keys():
                pass
            else:
                email = ''
                try:
                    #email = base64.urlsafe_b64decode(body['raw'].encode('ASCII'))
                    #email = base64.urlsafe_b64decode(body['data'].encode('UTF-8'))
                    email = relaxed_decode_base64(body['data'])
                    sent_emails.add(email)
                except:
                    pass
    return sent_emails
#-------------------------


def relaxed_decode_base64(data):
    """
    Takes String
    Returns String
    --
    Credit: This function was taken from Stack Overflow:
    https://stackoverflow.com/questions/44164829/base64-decode-specific-string-incorrect-padding-with-correct-padding
    """
    # If there is already padding we strim it as we calculate padding ourselves.
    if '=' in data:
        data = data[:data.index('=')]

    # We need to add padding, how many bytes are missing.
    missing_padding = len(data) % 4

    # We would be mid-way through a byte.
    if missing_padding == 1:
        data += 'A=='
    # Jut add on the correct length of padding.
    elif missing_padding == 2:
        data += '=='
    elif missing_padding == 3:
        data += '='

    # Actually perform the Base64 decode.
    return base64.urlsafe_b64decode(data)
#-------------------------


def main(_credentials, _service):
    """
    Takes OAuth2 Credentials, OAuth2 Service
    Returns List of Bytes-string
    """

    if not _credentials and not _service:
        print('not authorised')
    else:
        tokens = get_page_tokens(_service)
        bodies = get_sent_bodys(tokens, _credentials, _service)
        sent_emails = read_sent_content(bodies)
        return sent_emails
#-------------------------
