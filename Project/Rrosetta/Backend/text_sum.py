from sumy.parsers.html import HtmlParser
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lex_rank import LexRankSummarizer as Summarizer
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words
import csv

LANGUAGE = 'english'
COUNT = 32

def from_url(_url):
    parser = HtmlParser.from_url(_url, Tokenizer(LANGUAGE))
    
    stemmer = Stemmer(LANGUAGE)

    summarizer = Summarizer(stemmer)
    summarizer.stop_words = get_stop_words(LANGUAGE)

    sents = []
    for sentence in summarizer(parser.document, COUNT):
        sents.append(sentence)
    
    # with open("testfile.csv","w", encoding='utf-8') as file:
    #     csvwriter = csv.writer(file, delimiter='|', )
    #     csvwriter.writerow(str(s) for s in sents)

    s = ''
    for sent in sents:
        s += (str(sent) + ' ')
    
    return s

def from_text(_text, ):
    parser = PlaintextParser.from_string(_text, Tokenizer(LANGUAGE))

    stemmer = Stemmer(LANGUAGE)

    summarizer = Summarizer(stemmer)
    summarizer.stop_words = get_stop_words(LANGUAGE)

    sents = []
    for sentence in summarizer(parser.document, COUNT):
        sents.append(sentence)
    
    # with open("testfile.csv","w", encoding='utf-8') as file:
    #     csvwriter = csv.writer(file, delimiter='|', )
    #     csvwriter.writerow(str(s) for s in sents)

    s = ''
    s += (str(sent).join(' ') for sent in sents)
    return s

def main(_text, _count=COUNT, _language=LANGUAGE):
    COUNT = _count
    LANGUAGE = _language

    s = _text
    while COUNT > 1:
        COUNT /= 2
        s = from_text(s)

    return s
    

if __name__ == "__main__":
    import sys
    url = sys.argv[1]

    s = from_url(url)
    while COUNT > 1:
        COUNT /= 2
        s = from_text(s)
        print(s)
        print()
