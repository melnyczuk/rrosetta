## SENT FOLDER SCRAPER ##
## THIS CODE IS LARGELY TAKEN FROM A SCRIPT 
# FREELY PROVIDED GOOGLE AS PART OF THEIR API DOCUMENTATION ##
#-------------------------
from __future__ import print_function
from bs4 import BeautifulSoup
import os, base64, httplib2
#-------------------------
## GOOGLE API MODULES ## 
from apiclient import discovery, http
from oauth2client import client, tools
from oauth2client.file import Storage
#-------------------------
try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/gmail-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/gmail.readonly'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Gmail API Python Quickstart'

#-------------------------
def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'gmail-python-quickstart.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        #else: # Needed only for compatibility with Python 2.6
            #credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

#-------------------------
def get_service(_batch=False):
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    #if _batch: return discovery.build('gmail', 'v1')
    return discovery.build('gmail', 'v1', http=http)

#-------------------------
def get_page_tokens(_service=get_service(),  _userID='me'):
    sent_results = _service.users().messages().list(labelIds='SENT', userId=_userID).execute()
    newPT = sent_results.get('nextPageToken')
    pageTokens = set()
    pageTokens.add(newPT)
    while newPT != None:
        sent_results = _service.users().messages().list(labelIds='SENT', userId=_userID, pageToken=newPT).execute()
        newPT = sent_results.get('nextPageToken')
        pageTokens.add(newPT)    
    return pageTokens

#-------------------------
def single_access_msgs(_service=get_service(), _userID='me'):
    sent_results = _service.users().messages().list(labelIds='SENT', userId=_userID).execute()
    return sent_results.get('messages', [])

#-------------------------
def get_sent_bodys(_pageTokens, _service=get_service(), _userID='me'):
    
    if not _pageTokens:
        print('no pages')
        sentMSGs = single_access_msgs()
    else:
        sentMSGs = [] 
        for token in _pageTokens:
            sent_results = _service.users().messages().list(labelIds='SENT', userId=_userID, pageToken=token).execute()
            sentMSGs.append(sent_results.get('messages', []))
    
    if not sentMSGs:
        print('no sent messages')
    else:
        print('Pages: ', len(_pageTokens))
        sentIDs = []
        for page in sentMSGs:
            for MSG in page:
                sentIDs.append(MSG['id'])

    if not sentIDs:
        print('no sent IDs')
    else:
        print("IDs: ", len(sentIDs))
        sentContents = []
        for sentID in sentIDs:
            sentContents.append(_service.users().messages().get(userId=_userID,id=sentID).execute())
    
    if not sentContents:
        print('no sent msg content')
    else:
        print("contents: ", len(sentContents))
        bodys = []
        for sentContent in sentContents:
            if 'body' not in sentContent['payload'].keys():
                pass
            else:
                bodys.append(sentContent['payload']['body'])
    return bodys
#-------------------------
def read_sent_content(_bodys):
    print("bodies: ", len(_bodys))
    sent_emails = []
    if not _bodys:
        print('no MSG bodies')
    else:
        data64s = []
        for body in _bodys:
            if 'data' not in body.keys():
                pass
            else:
                try:
                    sent_emails.append(str(relaxed_decode_base64(body['data'])).encode('utf-8'))
                except:
                    pass
    return sent_emails
#-------------------------            
def relaxed_decode_base64(data):
    """
    This function was taken from Stack Overflow:
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
    return base64.b64decode(data)
#------------------------- 
def main():
    tokens = get_page_tokens()
    bodies = get_sent_bodys(tokens)
    sent_emails = read_sent_content(bodies)
    return sent_emails

#=========================
if __name__ == '__main__':
    l = main()
    for i in l:
        print(i)
