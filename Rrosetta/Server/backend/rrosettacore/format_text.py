import string
import re
import nltk
from nltk.corpus import stopwords

def remove_symbols(_sentence):
    tokens = [token for token in _sentence.split(sep=' ') if token.isalpha()]
#-------------------------
    
def format_emails(_emails):
    """
    Takes a Set/List of Strings
    Returns a List of Strings
    --
    Formats emails to remove unwanted characters etc.
    """
    emails = []
    for email in _emails:
        email = str(email.decode("utf-8", 'ignore')).lower()
        email.replace(r'(\\[a-z])+', " ")   # removes escape characters
        email.replace(r'\d', " ")           # removes digits
        email.replace(r'<.*>', " ")         # removes html tags
        email.replace(r'{.*}', " ")         # removes JSON
        emails.append(email)
    return emails
#-------------------------
        
    









