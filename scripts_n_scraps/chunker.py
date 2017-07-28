import nltk, re, sys
import process_file as pf
from nltk.corpus import conll2000

## LOAD NEGATIVE WORDS LIST/S ##
neg_words = []
with open("./bin/negative-words.txt", 'r') as negfile: 
    for line in negfile:
        neg_words.append(line.replace('\n', ''))

## LOAD POSTIVE WORDS LIST/S
pos_words = []
with open("./bin/positive-words.txt", 'r') as posfile: 
    for line in posfile:
        pos_words.append(line.replace('\n', ''))

## ALTER FORMATTING CONDITIONS
pf.conditions_list.remove("token not in stopwords.words('english')")

## SETUP
user = str(sys.argv[1])
data = pf.import_json("./twit_json/{}.json".format(user))
paragraphs = data[user]
sentences = [nltk.sent_tokenize(paragraph) for paragraph in paragraphs]
sentences = [item for sentence in sentences for item in pf.filter_list(sentence)]

## DEFINE CHUNK GRAMMAR RULES
chunk = r"""
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

        Noun: {<DT|PP\$>?<NN.?|PRP.?>+}

        Adj: {<DT|PP\$>?<RB.?.?>?<JJ.?>+<RB.?.?>?}
        """

# GET CHUNKS FROM SENTENCES #
def get_chunks(sentence):
    s = nltk.tokenize.casual_tokenize(sentence)
    s = pf.filter_list(s)
    # making it back into a sentence and parsing it again seems to greatly improve pos-tag accuracy
    s = pf.make_sentence(s)
    s = nltk.tokenize.casual_tokenize(sentence)
    s = nltk.pos_tag(s)
    return nltk.RegexpParser(chunk).parse(s)

# ANALYSE SENTIMENT OF CHUNKS #
# THIS IS DONE BY CHECKING ALL ADJECTIVES, VERBS AND ADVERBS AGAINST POSITIVE AND NEGATIVE LISTS
def sent_anal_chunks(chunks):
    nounjectives = []
    nounjectives.append([[noun for c in chunks if type(c) == nltk.tree.Tree and c.label() == 'AdjNoun' for noun, postag in c if postag == 'NN' or postag == 'NNS' or postag == 'NNP' or postag == 'NNPS'], [adj for c in chunks if type(c) == nltk.tree.Tree and c.label() == 'AdjNoun' for adj, postag in c if postag == 'JJ' or postag == 'JJR' or postag == 'JJS']])    
    noun_dict = {}
    for a, b in nounjectives:
        for noun in a:
            x = 0
            for adj in b:
                if adj in pos_words: x += 1
                if adj in neg_words: x -= 1
            noun_dict[noun] = x
    return noun_dict

# MAKE A DICTIONARY THAT STORES NOUNS WITH THE SENTIMENT ANALYSED FROM THE CHUNKS THEY ARE IN #
def make_sentiment_dict(_sentences):
    _dict = {}
    for sentence in _sentences:
        t_dict = sent_anal_chunks(get_chunks(sentence))
        for k in t_dict.keys():
            _dict.setdefault(k, []).append(t_dict[k])
    return _dict

# MAKE A DICTIONARY THAT COUNTS HOW MANY TIMES THE NOUN WAS USED #
def count_sentiment_dict(_sentences):
    s_d = make_sentiment_dict(_sentences)
    count_dict = {}
    for word, v in s_d.items():
        sentiment = 0
        counter = 0
        for x in v:
            sentiment += x
            counter += 1
        count_dict.setdefault(sentiment, {}).setdefault(counter, []).append(word)   # Change this line: atm={setiment-rating:{word-counter:[nouns]}} / to={word-counter:{setiment-rating:[nouns]}}
    return count_dict

c_d = count_sentiment_dict(sentences)
print([[k, c_d[k]] for k in c_d if k > 3])  # Prints the all words that have a sentiment-rating higher than 3 / could be used to print all words mentioned more than 10 times