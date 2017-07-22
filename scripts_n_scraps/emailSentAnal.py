## THIS SCRIPT CONTAINS METHODS TO BUILD A 

import sys, nltk, json, random, string
from nltk.corpus import stopwords

def count_words(_list):
    _dict = {}
    for word in set(_list): 
         _dict.setdefault(_list.count(word), []).append(word)
    return _dict

def get_types(_data):
    _list = []
    for sentence in _data:
        for token in nltk.tokenize.casual_tokenize(sentence):
            token = token.lower()
            if token[:] not in string.punctuation:
                _list.append(token)
    _list = remove_at(remove_url(remove_stops(_list)))
    return nltk.pos_tag(_list)

def type_dict(_data):
    _list = get_types(_data)
    _dict = {}
    for [v, k] in _list: 
        _dict.setdefault(k, []).append(v)
    for k in _dict:
        l = _dict[k]
        s = count_words(l)
        _dict[k] = s
    return _dict

def remove_url(_list):
    for item in _list:
        if item[:4] == 'http' or item[:4] == 'www.':
            _list.remove(item)
    return _list

def remove_at(_list):
    for item in _list:
        if str(item)[0] == 'U+0040'.encode('utf-8') or str(item)[0] == '@':
            _list.remove(item)
    return _list

def remove_stops(_list):
    for item in _list:
        if item in stopwords.words("english"):  
            _list.remove(item)
    return _list

def count_cutoff(_dict, threshold):
    small_keys = [k for k in _dict if k < threshold]
    for k in small_keys:
        _dict.pop(k, None)
    return _dict

if __name__ == '__main__':
    screenuser = str(sys.argv[1])

    data = {}
    with open("./twit_json/{}.json".format(screenuser), 'r') as file:
        data = json.load(file)
    
    # print(set(stopwords.words('english')))
    # print()

    d = type_dict(data[screenuser])
    d = count_cutoff(d['NN'], 2)
    print(d)