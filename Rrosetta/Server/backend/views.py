# This script was built from a proof of concept
# kindly put together for me by Fabio Natali of the CCS. 
# It would not have been possible without him.

#=========================

import random

import httplib2
from apiclient import discovery
from django.conf import settings
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.views.generic import RedirectView, TemplateView
from oauth2client.client import OAuth2WebServerFlow

#=========================

FLOW = OAuth2WebServerFlow(
    client_id=settings.GOOGLE_OAUTH_CLIENT_ID,
    client_secret=settings.GOOGLE_OAUTH_CLIENT_SECRET,
    scope=settings.GOOGLE_OAUTH_SCOPE,
    redirect_uri=settings.GOOGLE_OAUTH_REDIRECT_URI,
)

#=========================

class GmailView(RedirectView):
    """Request access to Gmail account."""

    def get_redirect_url(self, *args, **kwargs):
        """Start authentication process."""
        return FLOW.step1_get_authorize_url()
#-------------------------

class GmailCallbackView(TemplateView):
    """Show user's emails."""

    template_name = 'backend/callback.html'

    def get_context_data(self, **kwargs):
        from .rrosettacore import sent_mail as s
        from .rrosettacore.format_text import format_emails
        from .rrosettacore import text_sum
        from .rrosettacore import collect_content
        from .rrosettacore import send_email
        #from .rrosettacore import pdf_maker

        """Finalise authentication process and retrieve emails."""
        # Finalise authentication
        credentials = FLOW.step2_exchange(self.request.GET['code'])
        # Retrieve emails using the credentials above
        http = credentials.authorize(httplib2.Http())
        service = discovery.build('gmail', 'v1', http=http)
        #--
        d = {}
        user = service.users().getProfile(userId='me').execute()['emailAddress']
        print(user)
        d['user'] = user
        d['language'] = 'english'
        #--
        tokens = s.get_page_tokens(service)
        #print(user, "Pages: ", len(tokens))
        msgs = s.get_sent_msgs(tokens, service)
        ids = s.get_sent_ids(msgs)
        #print(user, "IDs: ", len(ids))
        contents = s.get_sent_contents(ids, service)
        #print(user, "contents: ", len(contents))
        bodies = s.get_sent_bodys(contents)
        #print(user, "bodies: ", len(bodies))
        sent_mail = s.read_sent_content(bodies)
        #print(user, "decoded: ", len(sent_mail))
        #--
        formatted_emails = format_emails(sent_mail)
        #print(user, "formatted: ", len(formatted_emails))
        d['sentences'] = text_sum.summerise(formatted_emails, d['language'], _count=15)
        #print(user, d['sentences'])
        d = collect_content.scrape(d)
        collect_content.create_json(d, d['user'])
        print(user, "urls: ", len(d['urls']), "img: ", len(d['img'].keys()), "txt: ", len(d['txt'].keys()))
        #--
        #pdf_maker.make(d)
        #--
        # send_email
        #--
        #kwargs['sentence'] = sentence
        kwargs['user'] = user
        return kwargs
        #--
#-------------------------