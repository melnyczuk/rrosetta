## THIS BUILDS A NESTED DICTIONARY OF ALL WORDS & THEIR POPULARITY GROUPED BY POS-TAG ##
import json, string
import nltk 
from nltk.corpus import stopwords

conditions_list = [
    "token[:4] != 'http'", 
    "'@' not in token", 
    "token not in stopwords.words('english')", 
    "token not in string.punctuation",
    "token != ' '",
    "token != ''"
]
#################
# ~ FUNCTIONS ~ #
#################
# IMPORTS JSON FILE INTO A DICTIONARY #
def import_json(_file):
    _data = {}
    with open(_file, 'r') as file: _data = json.load(file)
    return _data
#--------------------------------------
# FILTERS A LIST AGAINST A LIST OF CONDITIONS STATED AS STRINGS #
def filter_list(_list, removable_conditions=conditions_list):
    new_list = []
    for sentence in _list:
        for condition in removable_conditions: 
            sentence = remove_stuff(sentence, condition)
        new_list.append(sentence)
    return new_list
#--------------------------------------
# BUILDS POS-TAG DICTIONARY CONTAINING ALL WORDS #
def pos_dict(pos_tuples):
    _dict = {}
    for i in pos_tuples:
        for (v, k) in i: 
            _dict.setdefault(k, []).append(v)
    for k in _dict:
        _list = _dict[k]
        v = count_words(_list)
        _dict[k] = v
    return _dict
#--------------------------------------
# REMOVES TOKENS FROM TOKENISED SENTENCES BASED ON GIVEN CONDITIONAL #
def remove_stuff(sentence, conditional):
    tokens = [token for token in nltk.tokenize.casual_tokenize(sentence) if eval(conditional)]
    tokens = [token.strip() for token in tokens]
    return make_sentence(tokens)
#--------------------------------------
# MAKES A SENTENCE FROM A LIST OF TOKENS #
def make_sentence(_list):
    new_sentence = ''
    for token in _list: 
        new_sentence = new_sentence + str(token + ' ')
    return new_sentence
#--------------------------------------
# COUNTS HOW MANY TIMES A WORD APPEARS #
def count_words(_list):
    _dict = {}
    for word in set(_list): 
         _dict.setdefault(_list.count(word), []).append(word)
    return _dict
#--------------------------------------
# ALLOWS THE DICTIONARY TO BE PURGED OF INFREQUENT WORDS #
def count_cutoff(_dict, threshold):
    small_keys = [k for k in _dict if k < threshold]
    for k in small_keys: _dict.pop(k, None)
    return _dict
#--------------------------------------
# MAKES A NESTED DICTIONARY INSIDE JSON FILE DICTIONARY, WITH POS TAGS AS KEYS #
def make_pos_dict_with_word_freq(_file, _list=[], removal_conditions=conditions_list):
    try:
        data = import_json(_file)
        for k in data: 
            _list = [nltk.tokenize.casual_tokenize(item) for item in data[k]]
        pos_list = [nltk.pos_tag(item) for item in _list if len(item) > 0]
        _dict = pos_dict(pos_list)
    except: 
        print("no user, file or list given")
        return
#--------------------------------------
#======================================
if __name__ == '__main__':
    file = "./twit_json/nike.json"
    make_pos_dict_with_word_freq(file)