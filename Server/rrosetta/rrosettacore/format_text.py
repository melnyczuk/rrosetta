import string
import re

def remove_symbols(_sentence):
    """
    Takes a String
    Returns a List of Strings
    ---
    Removes anything that is not part of the alphabets
    """
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
        email = str(email.decode('UTF-8', 'ignore')).lower()
        email.replace(r'(\\[a-z])+', " ")   # removes escape characters
        email.replace(r'\d', " ")           # removes digits
        email.replace(r'<.*>', " ")         # removes html tags
        email.replace(r'{.*}', " ")         # removes JSON
        email = email.partition('>')[0]     # removes email reply thread
        emails.append(email)
    return emails
#-------------------------

    









