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
    """Show user's emails."""
    
    template_name = 'backend/callback.html'

    def get_context_data(self, **kwargs):
        # IMPORT RROSETTA CORE PROGRAMME FILES
        from .rrosettacore import sent_mail as s
        from .rrosettacore.format_text import format_emails
        from .rrosettacore import text_sum
        from .rrosettacore import collect_content
        from .rrosettacore import send_email
        from .rrosettacore import pdf_maker

        """Finalise authentication process and retrieve emails."""
        # Finalise authentication
        credentials = FLOW.step2_exchange(self.request.GET['code'])
        # Retrieve emails using the credentials above
        http = credentials.authorize(httplib2.Http())
        service = discovery.build('gmail', 'v1', http=http)
        #--
        try: user = service.users().getProfile(userId='me').execute()['emailAddress']
        except: print('sorry'); return;
        #--
        if self.check_list(user):
            kwargs['ln0'] = 'Rrosetta has already learnt all about you.'
            kwargs['ln1'] = 'She would like to move on now,'
            kwargs['ln2'] = 'so kindly please close this tab.'
            return kwargs
        #--
        d = {}                    # Initialised dictionary for user data
        d['user'] = user          # Get user email address
        d['language'] = 'english' # For future functionality of user langauge
        #--
        ## Read User sent emails and store temporarily
        print(user, ": reading...")
        try: emails = s.read(credentials, service, 20)
        except: 
            print(user, ": failed")
            kwargs['ln0'] = 'Rrosetta has found you emails to be flawed.'
            kwargs['ln1'] = 'She would like to move on now,'
            kwargs['ln2'] = 'so kindly please close this tab.'
            return kwargs
        #--
        ## Format emails for processing and summerisation
        print(user, ": formatting...")
        try: formatted_emails = format_emails(emails)
        except: 
            print(user, ": failed")
            kwargs['ln0'] = 'Rrosetta has found you emails to be flawed.'
            kwargs['ln1'] = 'You are of no user to her,'
            kwargs['ln2'] = 'so kindly please close this tab.'
            return kwargs
        #--
        ## Summerise using Sumy, until only four sentences are returned
        print(user, ": summerising...")
        try: d['sentences'] = text_sum.summerise(formatted_emails, d['language'], _count=12)
        except:             
            print(user, ": failed")
            kwargs['ln0'] = 'Rrosetta has found your writing illegible.'
            kwargs['ln1'] = 'You are of no use to her,'
            kwargs['ln2'] = 'so kindly please close this tab.'
            return kwargs
        #--
        ## Do Google searches and webscraping for zine content
        print(user, ": collecting...")
        try: d = collect_content.scrape(d)
        except:             
            print(user, ": failed")
            kwargs['ln0'] = 'Rrosetta cannot find anything interesting about you.'
            kwargs['ln1'] = 'She would like to move on now,'
            kwargs['ln2'] = 'so kindly please close this tab.'
            return kwargs
        #--
        print(user, ": urls:", len(d['urls']), " img:", len(d['img'].keys()), " txt:", len(d['txt'].keys()))
        ## Save dictionary as json for debugging (non-sensitive user data only)
        #try: collect_content.create_json(d, d['user'])
        #except:             
#            print(user, ": failed")
#            kwargs['ln0'] = 'Rrosetta would like to forget about you.'
#            kwargs['ln1'] = 'She would like to move on now,'
#            kwargs['ln2'] = 'so kindly please close this tab.'
#            return kwargs
        #--
        ## Make PDF using Reportlab
        print(user, ": designing...")
        try:
            pdf_maker.make(d)
        except:             
            print(user, ": failed")
            kwargs['ln0'] = 'Rrosetta lost interest.'
            kwargs['ln1'] = 'She would like to move on now,'
            kwargs['ln2'] = 'so kindly please close this tab.'
            return kwargs
        #--
        ## Send to printer
        print(user, ": printing...")
        #win: os.startfile("{}.pdf".format(d['user']), "print")
        try: subprocess.run(["/usr/bin/lpr", "-o portrait", "-o media=A4", "-o number-up=2", "./pdfs/{}.pdf".format(d['user'])])
        except:
            print(user, ": failed")
            kwargs['ln0'] = 'Rrosetta doesn\'t want to print your zine right now.'
            kwargs['ln1'] = 'She will send you it as a pdf.'
            kwargs['ln2'] = 'Kindly please close this tab.'
            return kwargs
        #--
        # send_email
        #--
        print(user, ": done!")
        return kwargs
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
    def check_list(self, _user):
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
