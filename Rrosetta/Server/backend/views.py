# This script was built from a proof of concept
# kindly provided to me by Fabio Natali

import random

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
        from .rrosettacore.format_text import format_emails
        from .rrosettacore import text_sum
        from .rrosettacore import json_maker
        from .rrosettacore import send_email

        """Finalise authentication process and retrieve emails."""
        # Finalise authentication
        credentials = FLOW.step2_exchange(self.request.GET['code'])
        # Retrieve emails using the credentials above
        http = credentials.authorize(httplib2.Http())
        service = discovery.build('gmail', 'v1', http=http)
        #--
        user = service.users().getProfile(userId='me').execute()
        #--
        tokens = s.get_page_tokens(service)
        msgs = s.get_sent_msgs(tokens, credentials, service)
        ids = s.get_sent_ids(msgs, credentials, service)
        contents = s.get_sent_contents(ids, credentials, service)
        bodies = s.get_sent_bodys(contents, credentials, service)
        sent_mail = s.read_sent_content(bodies)
        #--
        formatted_emails = format_emails(sent_mail)
        sentence = text_sum.summerise(formatted_emails, _count=15)
        name = str(int(random.random() * (10**10)))
        json_maker.main(sentence, name)
        #--
        # pdf_maker.make(user['emailAddress'])
        #--
        # if user["messagesTotal"] > 100:
        #     user_message = str("Hi, Rrosetta has finished analysing your sent emails, and crafting the content of you unique zine. Please collect this from the Rrosetta space, upstairs in the St James Hatcham Building. Did you know you have {} emails in you account? If you would like to learn more about Rrosetta, please visit http://melnycz.uk. Rrosetta would like to thanks you for your cooperation. Getting to know you has been a very stimulating experience.").format(user["messagesTotal"])
        # else:
        #     user_message = str("Hi, Rrosetta has finished analysing your sent emails, and crafting the content of you unique zine. Please collect this from the Rrosetta space, upstairs in the St James Hatcham Building. Did you know you have {} emails in your account? This isnt very many. As a result, your zine is probably worthless. Did you really think you could trick Rrosetta with some fake account? If you would like to learn more about Rrosetta, please visit http://melnycz.uk.").format(user["messagesTotal"]).encode("rfc2822")
        # completion_email = send_email.CreateMessage(user['emailAddress'], user['emailAddress'], 'Your personalised zine is ready for you', str('hey').encode('ascii'))
        # hm_email = send_email.CreateMessage(user['emailAddress'], 'h.melnyczuk@gmail.com', "Rrosetta: {}".format(user['emailAddress']), "")
        # send_email.SendMessage(service, 'me', completion_email)
        # send_email.SendMessage(service, 'me', hm_email)
        # #--
        #kwargs['sentence'] = sentence
        kwargs['user'] = user
        return kwargs
        #--
