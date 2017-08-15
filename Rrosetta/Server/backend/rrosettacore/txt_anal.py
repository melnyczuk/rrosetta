import json, nltk, re

def pull_json(_path):
	with open(_path, 'r', encoding='utf-8') as infile:
		return json.load(infile)

def update_json(_path, _dict):
	with open(_path, 'w', encoding='utf-8') as outfile:
		json.dump(_dict, outfile, skipkeys=False, ensure_ascii=True, sort_keys=True) 

def contains_noun(_text, _noun):
	if _text.count(_noun) > 0:
		return True
	else: 
		return False

def find_quotes(_text):
	if _text.count('\"') > 0 and _text.count('\"') % 2 == 0:
		quotes = [quote for quote in _text.split('\"') if quote.startswith(' ') != True and quote.endswith(' ') != True and len(quote) > 1]
		return quotes
	else: 
		return False

def remove_unwanted(_text):
	return _text.replace('\n', ' ').replace('\r', ' ').replace('\t',' ').replace(r' *', ' ').strip()

def analyse(_json):
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

if __name__ == '__main__':
	import sys
	analyse(sys.argv[1])