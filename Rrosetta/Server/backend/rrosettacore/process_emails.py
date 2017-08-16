#PY3#HPM#
# This script contains many functions for processing and formatting emails
#   in order to allow NLTK to correctly anaylse the content

#=========================

import json
import string

import nltk
from nltk.corpus import stopwords

#=========================

# A list of conditions for string formatting
conditions_list = [
    "token[:4] != 'http'",
    "'@' not in token",
    "token not in stopwords.words('english')",
    "token not in string.punctuation",
    "token != ' '",
    "token != ''"
]

#=========================


def import_json(_filepath):
    """
    Takes String
    Returns Dictionary
    """
    data = {}
    with open(_filepath, 'r') as file:
        data = json.load(file)
    return data
#-------------------------


def filter_list(_list, _removal_conditions=conditions_list):
    """
    Takes List of Strings, (List of Strings)
    Returns List of Strings
    --
    Formats the strings
    accoriding to parameters
    in conditions list
    """
    new_list = []
    for sentence in _list:
        for condition in _removal_conditions:
            sentence = remove_stuff(sentence, condition)
        new_list.append(sentence)
    return new_list
#-------------------------


def pos_dict(_postags):
    """
    Takes List of Tuples
    Returns Dictionary
    --
    Creates dictionary
    from a list of tuples
    consisting of words 
    paired with Part-Of-Speech (POS) tags 
    """
    d = {}
    for i in _postags:
        for (v, k) in i:
            d.setdefault(k, []).append(v)
    for k in d:
        _list = d[k]
        v = count_words(_list)
        d[k] = v
    return d
#-------------------------


def remove_stuff(_sentence, _condition):
    """
    Takes String, String
    Returns List of Strings
    --
    Formats a sentence 
    to remove unwanted elements
    in accordance with condition
    """
    tokens = [token for token in nltk.tokenize.casual_tokenize(
        _sentence) if eval(_condition)]
    tokens = [token.strip() for token in tokens]
    return make_sentence(tokens)
#-------------------------


def make_sentence(_list):
    """
    Takes List
    Returns String
    --
    Forms a list of words
    into a Sentence
    """
    new_sentence = ''
    for token in _list:
        new_sentence = new_sentence + str(token + ' ')
    return new_sentence
#-------------------------


def count_words(_list):
    """
    Takes a List
    Returns a Dictionary
    --
    Creates a dictionary
    containing word paired
    with a count-up of the words occurances
    """
    d = {}
    for word in set(_list):
        d.setdefault(_list.count(word), []).append(word)
    return d
#-------------------------


def count_cutoff(_dict, _threshold):
    """
    Takes Dictionary, Int
    Returns Dictionary
    --
    Removes words from dictionary
    that occur less than the threshold
    """
    small_keys = [k for k in _dict if k < _threshold]
    for k in small_keys:
        _dict.pop(k, None)
    return _dict
#-------------------------

# def make_pos_dict_with_word_freq(_filepath, _list=[], removal_conditions=conditions_list):
#     """
#     Takes a String (List, List of strings)
#     Returns
#     """
#     try:
#         data = import_json(_filepath)
#         for k in data:
#             _list = [nltk.tokenize.casual_tokenize(item) for item in data[k]]
#         pos_list = [nltk.pos_tag(item) for item in _list if len(item) > 0]
#         _dict = pos_dict(pos_list)
#     except:
#         print("no user, file or list given")
#         return
# #-------------------------


#=========================
if __name__ == '__main__':
    file = "./twit_json/nike.json"
    make_pos_dict_with_word_freq(file)
