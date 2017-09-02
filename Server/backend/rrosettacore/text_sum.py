#PY3#HPM#
# This performs a recursive sumerisation
#   of a body of text that seeks to produce
#   a single sentence with greater accuracy

#=========================

from sumy.nlp.stemmers import Stemmer
from sumy.nlp.tokenizers import Tokenizer
from sumy.parsers.html import HtmlParser
from sumy.parsers.plaintext import PlaintextParser
from sumy.summarizers.lex_rank import LexRankSummarizer as Summarizer
from sumy.utils import get_stop_words

#=========================

# LANGUAGE = 'english'
# COUNT = 12                 # No. of recursions

#=========================


def from_url(_url, _lang, _count):
    """
    Takes a String
    Returns a List of Sentence Objects
    --
    Gives a summerising sentence
    of all the text
    on any given webpage
    """
    parser = HtmlParser.from_url(_url, Tokenizer(_lang))
    stemmer = Stemmer(_lang)
    summarizer = Summarizer(stemmer)
    summarizer.stop_words = get_stop_words(_lang)
    return summarizer(parser.document, _count)
#-------------------------


def from_set(_set, _lang, _count):
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
        text += str(item)
        text += ' '
    return from_text(text, _lang, _count)
#-------------------------


def from_text(_text, _lang, _count):
    """
    Takes a String
    Returns a List of Sentence Objects
    --
    Gives a summerising sentence
    for any given string of text
    """
    parser = PlaintextParser.from_string(_text, Tokenizer(_lang))
    stemmer = Stemmer(_lang)
    summarizer = Summarizer(stemmer)
    summarizer.stop_words = get_stop_words(_lang)
    return set(summarizer(parser.document, _count))

#-------------------------


def summerise(_set, _lang, _count):
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
    ouroboros = 2**_count
    s = from_set(_set, _count=ouroboros, _lang=_lang)
    while ouroboros > 4:
        ouroboros /= 2
        s = from_set(s, _count=ouroboros, _lang=_lang)
    return list(s)
#-------------------------