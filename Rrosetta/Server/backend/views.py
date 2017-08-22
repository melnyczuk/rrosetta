## This script was built from a proof of concept
##  kindly provided to me by Fabio Natali

import httplib2
from apiclient import discovery
from django.conf import settings
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.views.generic import RedirectView, TemplateView
from oauth2client.client import OAuth2WebServerFlow

FLOW = OAuth2WebServerFlow(
    client_id=settings.GOOGLE_OAUTH_CLIENT_ID,
    client_secret=settings.GOOGLE_OAUTH_CLIENT_SECRET,
    scope=settings.GOOGLE_OAUTH_SCOPE,
    redirect_uri=settings.GOOGLE_OAUTH_REDIRECT_URI,
)

##
class GmailView(RedirectView):
    """Request access to Gmail account."""

    def get_redirect_url(self, *args, **kwargs):
        """Start authentication process."""
        print('hey')
        return FLOW.step1_get_authorize_url()


class GmailCallbackView(TemplateView):
    """Show user's emails."""

    template_name = 'backend/callback.html'

    def get_context_data(self, **kwargs):
        from .rrosettacore import sent_mail as s
        from .rrosettacore import get_sentiment
        from .rrosettacore import text_sum 
        from .rrosettacore import json_maker
        
        """Finalise authentication process and retrieve emails."""
        # Finalise authentication
        credentials = FLOW.step2_exchange(self.request.GET['code'])
        # Retrieve emails using the credentials above
        http = credentials.authorize(httplib2.Http())
        service = discovery.build('gmail', 'v1', http=http)
        #--
        tokens = s.get_page_tokens(service)
        c = len(tokens)
        msgs = s.get_sent_msgs(tokens, credentials, service)
        ids = s.get_sent_ids(msgs, credentials, service)
        contents = s.get_sent_contents(ids, credentials, service)
        bodies = s.get_sent_bodys(contents, credentials, service)
        sent_mail = s.read_sent_content(bodies)
        #--
        formatted_emails = get_sentiment.format_emails(sent_mail)
        sentence = text_sum.summerise(formatted_emails, _count=c)
        kwargs['sentence'] = sentence
        json_maker.main(sentence)
        #--
        return kwargs