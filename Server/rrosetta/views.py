# This script was built from a proof of concept
# kindly put together for me by Fabio Natali. 
# It would not have been possible without him.

#=========================

import os, subprocess
import random

import httplib2
from apiclient import discovery
from django.conf import settings
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.views.generic import RedirectView, TemplateView
from oauth2client.client import OAuth2WebServerFlow

import django_rq
from django_rq import job

#=========================

FLOW = OAuth2WebServerFlow(
    client_id=settings.GOOGLE_OAUTH2_CLIENT_ID,
    client_secret=settings.GOOGLE_OAUTH2_CLIENT_SECRET,
    scope=settings.GOOGLE_OAUTH2_SCOPE,
    redirect_uri=settings.GOOGLE_OAUTH2_REDIRECT_URI,
)

#=========================

## Send user to OAuth2 page
class GmailView(RedirectView):
    """Request access to Gmail account."""

    def get_redirect_url(self, *args, **kwargs):
        """Start authentication process."""
        return FLOW.step1_get_authorize_url()
#-------------------------

## Serve Favicon when requested
favicon_view = RedirectView.as_view(url='favicon.ico', permanent=True)
    
## Callback response that runs Rrosetta core programme
class GmailCallbackView(TemplateView):
    template_name = 'backend/callback.html'

    """Show user's emails."""
    
    def get_context_data(self, **kwargs):
        # IMPORT RROSETTA CORE PROGRAMME FILES
        c = self.request.GET['code']

        django_rq.get_queue('high', default_timeout=3600).enqueue(run, c)

        kwargs['ln0'] = 'Rrosetta is learning about you.'
        kwargs['ln1'] = 'Please take a seat,'
        kwargs['ln2'] = 'and kindly close this tab.'
        return kwargs
    #-------------------------
#-------------------------

def run(c):
    from .rrosettacore import sent_mail as s
    from .rrosettacore.format_text import format_emails
    from .rrosettacore import text_sum
    from .rrosettacore import collect_content
    from .rrosettacore import send_email
    from .rrosettacore import pdf_maker

    """Finalise authentication process and retrieve emails."""
    # Finalise authentication
    credentials = FLOW.step2_exchange(c)
    # Retrieve emails using the credentials above
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('gmail', 'v1', http=http)  

    user = service.users().getProfile(userId='me').execute()['emailAddress']
    if not user: print('sorry no access'); return;
    print(user)
    #--

    if check_list(user): return

    d = {}                    # Initialised dictionary for user data
    d['user'] = user          # Get user email address
    d['language'] = 'english' # For future functionality of user langauge
    #--

    ## Read User sent emails and store temporarily
    print(user, ": reading...")
    emails = s.read(credentials, service, 20) #20
    if not emails: 
        print(user, ": failed")
        return
    #--                 
    
    ## Format emails for processing and summerisation
    print(user, ": formatting...")
    formatted_emails = format_emails(emails)
    if not formatted_emails: 
        print(user, ": failed")
        return
    #--

    ## Summarise using Sumy, until only four sentences are returned
    print(user, ": summarising...")
    d['sentences'] = text_sum.summerise(formatted_emails, d['language'], _count=12) #12
    if not d['sentences']:             
        print(user, ": failed")
        return
    #--
    
    ## Do Google searches and webscraping for zine content
    print(user, ": collecting...")
    d = collect_content.scrape(d)
    #--
    
    print(user, ": urls:", len(d['urls']), " img:", len(d['img'].keys()), " txt:", len(d['txt'].keys()))
    ## Save dictionary as json for debugging (non-sensitive user data only)
    # try: collect_content.create_json(d, d['user'])
    # except: print(user, ": failed"); return;
    #--
    
    ## Make PDF using Reportlab
    print(user, ": designing...")
    pdf_maker.make(d)
    # except: print(user, ": failed"); return;
    #--
    
    ## Send to printer
    # print(user, ": printing...")
    # #win: os.startfile("{}.pdf".format(d['user']), "print")
    # #osx: subprocess.run(["/usr/bin/lpr", "-o portrait", "-o media=A4", "-o number-up=2", "./pdfs/{}.pdf".format(d['user'])])
    #--

    # print(user, ": uploading")
    # subprocess.run([
    #         "curl", 
    #         "--upload-file", 
    #         "./{}.pdf".format(d['user']), 
    #         "https://transfer.sh/{}.pdf".format(d['user'])
    #     ]) 
    #--

    # print(user, ": emailing...")
    # print('me')
    # mailme(d)
    # print('you')
    # mailyou(d)
    #--

    print(user, ": printing...")
    socket_to_me("print.pdf")
    #--
    
    print(user, ": done!")
    return
    #--
#-------------------------

def try_pdf(self, d):
    """
    Keep trying to make a pdf
    until you make a pdf
    BAD
    """
    from .rrosettacore import pdf_maker
    try:
        pdf_maker.make(d)
        return
    except:
        self.try_pdf(d)
#-------------------------

def check_list(_user):
    """
    Checks to see if the user has already been through
    to prevent clogging exhibition with repeat users
    """
    user_list = open('pastusers.txt', 'r')
    if (_user + ' \n') in user_list:
        return True
    else:
        f = open('pastusers.txt', 'a')
        f.writelines(_user + ' \n')
        f.close()
        return False
#-------------------------

def mailme(d):
    subprocess.run([    
            "curl", 
            "'smtps://smtp.gmail.com:465'",
            "--mail-from", 
            "'rrosetta.zine@gmail.com'",
            "--mail-rcpt", 
            "'h.melnyczuk@gmail.com'",
            "--user",
            "'rrosetta.zine@gmail.com':'1UDKVmSaYWQTnFP0VZDy'",
            "-v"
        ])
#-------------------------

def mailyou(d):
    subprocess.run([    
            "curl", 
            "smtps://smtp.gmail.com:465",
            "--mail-from 'rrosetta.zine@gmail.com'",
            "--mail-rcpt '{}'".format(d['user']),
            "--user",
            "'rrosetta.zine@gmail.com':'1UDKVmSaYWQTnFP0VZDy'",
            "-v"
        ])
#-------------------------

def scp_pdf(d):
    import pexpect
    t = pexpect.spawn("scp print.pdf alisablakeney@124.170.221.24:./Desktop".format(d['user']))
    try: t.expect('Password:', timeout=240)
    except: print(str(t))
    t.sendline(' k ')
#-------------------------

def socket_to_me(_pdf):
# https://stackoverflow.com/questions/27241804/sending-a-file-over-tcp-sockets-in-python
    import socket               # Import socket module

    s = socket.socket()          # Create a socket object
    print(socket.gethostbyname(socket.gethostname()))
    
    s.connect(('218.214.105.53', 55345))
    print('Sending {} to:'.format(_pdf), s.getsockname())
    f = open(_pdf,'rb')
    l = f.read(1024)

    while (l):
        s.send(l)
        l = f.read(1024)

    f.close()
    print("Done Sending")
    s.shutdown(socket.SHUT_WR)
    print(s.recv(1024))
    s.close                     # Close the socket when done
#-------------------------