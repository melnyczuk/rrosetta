# This script was built from a proof of concept
# kindly put together for me by Fabio Natali of the CCS. 
# It would not have been possible without him.

#=========================

import os
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

class GmailView(RedirectView):
    """Request access to Gmail account."""

    def get_redirect_url(self, *args, **kwargs):
        """Start authentication process."""
        return FLOW.step1_get_authorize_url()
#-------------------------

favicon_view = RedirectView.as_view(url='favicon.ico', permanent=True)
    

class GmailCallbackView(TemplateView):
    """Show user's emails."""
    
    template_name = 'backend/callback.html'

    def get_context_data(self, **kwargs):
        from .rrosettacore import sent_mail as s
        from .rrosettacore.format_text import format_emails
        from .rrosettacore import text_sum
        from .rrosettacore import collect_content
        from .rrosettacore import send_email

        """Finalise authentication process and retrieve emails."""
        # Finalise authentication
        credentials = FLOW.step2_exchange(self.request.GET['code'])
        # Retrieve emails using the credentials above
        http = credentials.authorize(httplib2.Http())
        service = discovery.build('gmail', 'v1', http=http)
        #--
        d = {}
        user = service.users().getProfile(userId='me').execute()['emailAddress']
        d['user'] = user
        d['language'] = 'english'
        #--
        print(user, ": reading...")
        emails = s.read(credentials, service, 20)
        #--
        print(user, ": formatting...")
        formatted_emails = format_emails(emails)
        #--
        print(user, ": summerising...")
        d['sentences'] = text_sum.summerise(formatted_emails, d['language'], _count=12)
        #--
        print(user, ": collecting...")
        d = collect_content.scrape(d)
        #--
        print(user, ": urls:", len(d['urls']), " img:", len(d['img'].keys()), " txt:", len(d['txt'].keys()))
        collect_content.create_json(d, d['user'])
        #--
        print(user, ": designing...")
        self.try_pdf(d)
        #--
        [print(user, ": printing...")]
        os.startfile("{}.pdf".format(d['user']), "print")
        #--
        # send_email
        #--
        print(user, ": done!")
        kwargs['user'] = user
        return kwargs
        #--
#-------------------------
    def try_pdf(self, d):
        from .rrosettacore import pdf_maker
        try:
            pdf_maker.make(d)
            return
        except:
            self.try_pdf(d)