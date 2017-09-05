#PY3#HPM#
# This script analyses all the text paragraphs catalogued in a JSON file

#=========================

import re
from nltk.corpus import stopwords

#=========================


def contains(_text, _dict):
    """
    Takes a String, Dictionary
    Returns a List of Strings
    or
    Returns False
    ---
    Checks to see if 
    the text contains
    any of the words
    from the summerised sentences
    """
    words = [word for item in _dict['sentences'] for word in item.split(
        ' ') if word in _text and word not in (_dict['language'])]
    if len(words) > 1:
        return words
    else:
        return False
#-------------------------


def find_quotes(_text):
    """
    Takes a String
    Returns a List of Strings
    --
    Pulls out any blockquotes
    from a string of text

    Returns False if no quotes are found
    """
    if _text.count('\"') > 0 and _text.count('\"') % 2 == 0:
        quotes = [quote for quote in _text.split('\"') if quote.startswith(
            ' ') != True and quote.endswith(' ') != True and len(quote) > 1]
        return quotes
    else:
        return False
#-------------------------


def remove_unwanted(_text):
    """
    Takes String
    Returns String
    --
    Formats a string
    """
    return _text.replace('\n', ' ').replace('\r', ' ').replace('\t', ' ').replace(r' *', ' ').strip()
#-------------------------


def analyse(_dict):
    """
    Takes a Dictionary
    Returns a Dictionary
    --
    Perform analysis
    on Dictionary,
    then updates the Dictionary
    """
    d = {}

    for k in _dict['txt']:
        # remove duds
        if _dict['txt'][k] != False and len(_dict['txt'][k]['text']) > 1:
            d[k] = _dict['txt'][k]

    for k in d:
        text = d[k]['text']
        d[k]['text'] = remove_unwanted(text)
        d[k]['quotes'] = find_quotes(text)
        d[k]['contains'] = contains(text, _dict)
        d[k]['count'] = len(d[k]['text'])

    return d
#-------------------------
