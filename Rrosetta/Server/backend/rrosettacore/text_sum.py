#PY3#HPM#
# This performs a recursive sumerisation
#   of a body of text that seeks to produce
#   a single sentence with greater accuracy

#=========================

import csv

from sumy.nlp.stemmers import Stemmer
from sumy.nlp.tokenizers import Tokenizer
from sumy.parsers.html import HtmlParser
from sumy.parsers.plaintext import PlaintextParser
from sumy.summarizers.lex_rank import LexRankSummarizer as Summarizer
from sumy.utils import get_stop_words

#=========================

LANGUAGE = 'english'
COUNT = 32                  # No. of recursions

#=========================


def from_url(_url):
    """
    Takes a String
    Returns a String
    --
    Gives a summerising sentence
    of all the text
    on any given webpage
    """
    parser = HtmlParser.from_url(_url, Tokenizer(LANGUAGE))

    stemmer = Stemmer(LANGUAGE)

    summarizer = Summarizer(stemmer)
    summarizer.stop_words = get_stop_words(LANGUAGE)

    sents = []
    for sentence in summarizer(parser.document, COUNT):
        sents.append(sentence)

    s = ''
    for sent in sents:
        s += (str(sent) + ' ')

    return s
#-------------------------


def from_set(_set):
    """
    Takes a Set of Strings
    Returns a String
    --
    Gives a summerising sentence
    for all the text 
    in any given set of strings
    """
    text = ''
    for item in _set:
        text += str(item).join(' ')
    return from_text(text)
#-------------------------


def from_text(_text):
    """
    Takes a String
    Returns a String
    --
    Gives a summerising sentence
    for any given string of text
    """
    parser = PlaintextParser.from_string(_text, Tokenizer(LANGUAGE))

    stemmer = Stemmer(LANGUAGE)

    summarizer = Summarizer(stemmer)
    summarizer.stop_words = get_stop_words(LANGUAGE)

    sents = []
    for sentence in summarizer(parser.document, COUNT):
        sents.append(sentence)

    s = ''
    s += (str(sent).join(' ') for sent in sents)
    return s
#-------------------------


def summerise(_set, _count=COUNT, _lang=LANGUAGE):
    """
    Takes Set/List, (Int, String)
    Returns String
    --
    Provides a summery sentences 
    for any given set of strings
    in any specified langugage,
    recursively to improve accuracy,
    recurring a specified of times
    """
    COUNT = _count
    LANGUAGE = _lang

    ouroboros = 2**COUNT

    s = _set
    while ouroboros > 1:
        ouroboros /= 2
        s = from_set(s)
    return s
#-------------------------


#=========================
if __name__ == "__main__":
    import sys
    url = sys.argv[1]

    s = from_url(url)
    while COUNT > 1:
        COUNT /= 2
        s = from_text(s)
        print(s)
        print()
