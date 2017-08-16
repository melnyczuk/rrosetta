#PY3#HPM#
# This script analyses all the text paragraphs catalogued in a JSON file

#=========================

import json
import re

import nltk

#=========================


def pull_json(_filepath):
	"""
	Takes a String
	Returns a Dictionary
	"""
    with open(_filepath, 'r', encoding='utf-8') as infile:
        return json.load(infile)
#-------------------------


def update_json(_filepath, _dict):
	"""
	Takes a String and a Dictionary
	Saves a JSON file
	"""
    with open(_filepath, 'w', encoding='utf-8') as outfile:
        json.dump(_dict, outfile, skipkeys=False,
                  ensure_ascii=True, sort_keys=True)
#-------------------------


def contains_noun(_text, _noun):
	"""
	Takes String, String
	Returns Boolean
	--
	Checks to see if a noun
	is in a string of text
	"""
    if _text.count(_noun) > 0:
        return True
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


def analyse(_json):
	"""
	Takes a String
	Saves a JSON
	--
	Perform analysis
	from JSON file,
	the updates JSON
	"""
    path = "citation_jsons/{}.json".format(_json)
    d = pull_json(path)
    for k in d['txt']:
        text = d['txt'][k]['text']
        d['txt'][k]['text'] = remove_unwanted(text)
        d['txt'][k]['contains'] = contains_noun(text, _json)
        d['txt'][k]['quotes'] = find_quotes(text)
        if len(d['txt'][k]['text']) < 1:
            d['txt'][k] = False
        else:
            d['txt'][k]['count'] = len(d['txt'][k]['text'])
    update_json(path, d)
#-------------------------


#=========================
if __name__ == '__main__':
    import sys
    analyse(sys.argv[1])
