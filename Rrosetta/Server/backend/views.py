import httplib2
from apiclient import discovery
from django.conf import settings
from django.http import HttpResponseRedirect, HttpResponse, HttpRequest
from django.views.generic import RedirectView, TemplateView
from oauth2client.client import OAuth2WebServerFlow

FLOW = OAuth2WebServerFlow(
    client_id=settings.GOOGLE_OAUTH_CLIENT_ID,
    client_secret=settings.GOOGLE_OAUTH_CLIENT_SECRET,
    scope=settings.GOOGLE_OAUTH_SCOPE,
    redirect_uri=settings.GOOGLE_OAUTH_REDIRECT_URI,
)

class GmailView(RedirectView):
    """Request access to Gmail account."""
    def get_redirect_url(self, *args, **kwargs):
        """Start authentication process."""
        return FLOW.step1_get_authorize_url()

class GmailCallbackView(TemplateView):
    """Show user's emails."""

    template_name = 'backend/callback.html'

    def get_context_data(self, **kwargs):
        from .rrosettacore.sent_mail import get_page_tokens
        """Finalise authentication process and retrieve emails."""
        # Finalise authentication
        credentials = FLOW.step2_exchange(self.request.GET['code'])
        # Retrieve emails using the credentials above
        http = credentials.authorize(httplib2.Http())
        service = discovery.build('gmail', 'v1', http=http)
        
        
        
        
        
        
        
        
        
        # results = service.users().messages().list(userId='me',maxResults=10).execute()
        # messages = []
        # for result in results['messages']:
        #     message = service.users().messages().get(userId='me',id=result['id']).execute()
        #     messages.append(message)
        # kwargs['messages'] = messages
        # return kwargs



#def citation(self, *args):
    
