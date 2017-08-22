#PY3#HPM#

# This programme takes a list of strings and produces a dictionary
#   containing important nouns alongside a the number of times they occur,
#   and a sentiment rating produced by analysing the adjectives, verbs and adverbs
#   in the sentences that contain the noun.

#=========================

import re

import nltk
from nltk.corpus import conll2000

from . import process_emails as pf

#=========================

## LOAD NEGATIVE WORDS LIST/S ##
neg_words = set()
with open("backend/rrosettacore/bin/negative-words.txt", 'r') as negfile:
    for line in negfile:
        neg_words.add(line.replace('\n', ''))

# LOAD POSTIVE WORDS LIST/S
pos_words = set()
with open("backend/rrosettacore/bin/positive-words.txt", 'r') as posfile:
    for line in posfile:
        pos_words.add(line.replace('\n', ''))

# ALTER FORMATTING CONDITIONS
#pf.conditions_list.remove("token not in stopwords.words('english')")

# DEFINE CHUNK GRAMMAR RULES
hunk = """
        AdjNoun: {<DT|PP\$>?<RB.?.?>?<JJ.?>+<RB.?.?>?<NN.?|PRP.?><PRP.?>?}
        AdjNoun: {<DT|PP\$>?<RB.?.?>?<JJ.?>+<RB.?.?>?<PRP.?>?<NN.?|PRP.?>}
        NounAdj: {<DT|PP\$>?<PRP.?>?<NN.?|PRP.?><RB.?.?>?<JJ.?>+<RB.?.?>?}
        NounAdj: {<DT|PP\$>?<NN.?|PRP.?><PRP.?>?<RB.?.?>?<JJ.?>+<RB.?.?>?}

        VerbNoun: {<RB.?.?>?<VB.?>+<NN.?|PRP.?><NN.?|PRP.?>?}
        NounVerb: {<RB.?.?>?<NN.?|PRP.?><NN.?|PRP.?>?<VB.?>+}

        AdvNoun: {<RB.?.?>+<NN.?|PRP.?><NN.?|PRP.?>?}
        NounAdv: {<NN.?|PRP.?><NN.?|PRP.?>?<RB.?.?>+}

        VerbNounAdv: {<RB.?.?>?<VB.?>+<NN.?|PRP.?><NN.?|PRP.?>?<RB.?.?>?}
        NounVerbAdv: {<RB.?.?>?<NN.?|PRP.?><NN.?|PRP.?>?<VB.?>+<RB.?.?>?}
        
        VerbAdv: {<VB.?>+<RB.?.?>+}
        AdvVerb: {<RB.?.?>+<VB.?>+}
        """

chunk = r"""
        Noun: {<DT|PP\$>?<NN.?|PRP.?>+}
        Adj: {<DT|PP\$>?<RB.?.?>?<JJ.?>+<RB.?.?>?}
        """


#=========================


def get_chunks(_sentence):
    """
    Takes a String
    Returns a List of Strings
    --
    Get chunks from sentences
    """
    s = nltk.tokenize.casual_tokenize(_sentence)
    s = pf.filter_list(s)
    # making it back into a sentence and parsing it again seems to greatly improve pos-tag accuracy
    s = pf.make_sentence(s)
    s = nltk.tokenize.casual_tokenize(_sentence)
    s = nltk.pos_tag(s)
    c = []
    if len(s) > 0:
        c = nltk.RegexpParser(chunk).parse(s)
    return c
#-------------------------


def sent_anal_chunks(_chunks):
    """
    Takes a List of Strings
    Returns a Dictionary
    --
    Analyse Sentiment of chunks
    This is done by checking all adjectives, verbs and adverbs
    against lists of positive and negative words
    """
    nounjectives = []
    nounjectives.append([
        [noun for c in _chunks if type(c) == nltk.tree.Tree for noun, postag in c if postag == r'<NN.?|PRP.?>+'], 
        [adj for c in _chunks if type(c) == nltk.tree.Tree for adj, postag in c if postag == r'<RB.?.?>?<JJ.?>+<RB.?.?>?']
    ])   
    noun_dict = {}
    for a, b in nounjectives:
        for noun in a:
            x = 0
            for adj in b:
                if adj in pos_words:
                    x += 1
                if adj in neg_words:
                    x -= 1
            noun_dict[noun] = x
    return noun_dict
#-------------------------


def get_nouns(_chunks):
    #return [noun for c in _chunks if type(c) == nltk.tree.Tree for noun, postag in c if len(noun) > 0 and postag == r'<NN.?|PRP.?>+']
    nouns = []
    for c in _chunks:
        if type(c) == nltk.tree.Tree:
            for noun, postag in c:
                nouns.append((noun, postag))
                # if postag == 'NN' or postag == 'NNP' or postag == 'NNS':
                #     if str(noun).isalpha():
                #         print("noun: ", noun)
                #         nouns.append(noun)
    return nouns
#-------------------------


def make_sentiment_dict(_sentences):
    """
    Takes a List of Strings
    Returns a Dictionary 
    --
    Dictionary stores a noun
    with the sentiment value
    of the chunk that contains the noun
    """
    _dict = {}
    for sentence in _sentences:
        t_dict = sent_anal_chunks(get_chunks(sentence))
        for k in t_dict.keys():
            if len(k) > 1 and k.isalpha:
                _dict.setdefault(k, []).append(t_dict[k])
    print('msd: ', _dict)
    return _dict
#-------------------------


def count_sentiment(_emails):
    """
    Takes a Set/List of Strings
    Returns a dictionary
    --
    Dictionary contains a count of every occurance
    and the sentiment value
    for all nouns that is sentimentally significant
    in a list of emails
    """
    #emails = format_emails(_emails)
    paragraphs = [nltk.sent_tokenize(email) for email in _emails]
    sentences = [
        item for sentence in paragraphs for item in pf.filter_list(sentence)]
    sentiment_dict = make_sentiment_dict(sentences)
    count_dict = {}
    for word, v in sentiment_dict.items():
        sentiment = 0
        counter = 0
        for x in v:
            sentiment += x
            counter += 1
        count_dict.setdefault(sentiment, {}).setdefault(counter, []).append(
            word)   # change to={word-counter:{setiment-rating:[nouns]}} ??
    print('cs: ', count_dict)
    return count_dict
#-------------------------


def get_links(_emails):
    """
    Takes a Set/List of Strings
    Returns a List of Strings
    --
    Returns a list of URLs
    from within the emails
    """
    emails = format_emails(_emails)
    paragraphs = [nltk.sent_tokenize(email) for email in emails]
    urls = [item for sentence in paragraphs for item in pf.filter_list(
        sentence, removable_conditions=["'http' in token;"])]
    return urls
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
