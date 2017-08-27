import json
import random
import string

import requests
from bs4 import BeautifulSoup

from . import googl
from . import txt_anal
from . import img_anal

#=========================


def pull(_url):
    """
    Takes a String
    Returns a Soup
    """
    page = requests.get(_url).content
    soup = BeautifulSoup(page, 'html.parser')
    return soup
#-------------------------


def catalog_url(_url):
    """
    Takes a String
    Returns a Dictionary
    --
    Dictionary contains
    all text and images 
    grouped as such.
    """
    soup = pull(_url)
    # Seperates images and text into internal nested dictionaries of each
    content = {'img': {}, 'txt': {}}
    # Updates nested dictionary of images
    content['img'].update(sort_img(soup, _url))
    # Updates nested dictionary of text
    content['txt'].update(sort_all_txt(soup, _url))
    return content
#-------------------------


def sort_txt(_soup, _url):
    """
    Takes a Soup, String
    Returns a Dictionary 
    --
    Dictionary contains 
    the text (if any) 
    from every <p> tag in a page
    """
    p_dict = {}
    # get all text for every p tag in the soup
    paragraphs = [p for p in _soup.find_all('p')]
    for p in paragraphs:
        # Checks to see if there is any text present
        if len(p) > 0:
            key = 'p_' + str(int(random.random() * 10**10))
            p_dict[key] = {
                'origin': _url,
                'text': p.text
            }
    return p_dict
# NEED TO SORT THIS OUT ^ THIS DOESNT TAKE ENOUGH, BUT IS IT TOO MUCH TO TAKE ALL TEXT?
#-------------------------


def sort_all_txt(_soup, _url):
    """
    Takes Soup, String
    Returns a Dictionary
    -- 
    Dictionary contains all the text on a webpage
    """
    p_dict = {}
    paragraphs = [p.text for p in _soup.find_all('p')]
    text = _soup.getText()
    key = 'p_' + str(int(random.random() * 10**10))
    p_dict[key] = {
        'origin': _url,
        'text': text
    }
    return p_dict
#-------------------------


def sort_img(_soup, _url):
    """
    Takes Soup, String
    Returns a Dictionary
    --
    Dictionary contains every image
    with as much information as possible
    """
    img_dict = {}
    imgs = [img for img in _soup.find_all('img')]
    print(len(imgs))
    for img in imgs:
        key = 'img_' + str(int(random.random() * 10**10))
        img_dict[key] = {
            'origin': _url,
            'src': img['src']
        }
    return img_dict
#-------------------------


def create_dict(_URLset):
    """
    Takes a Set containing Strings
    Returns a Dictionary 
    --
    combing all the text and all the image dictionaries 
    for all pages marked as a 'Reference'
    on a wikipedia page
    """
    c_dict = {'urls': set(), 'img': {}, 'txt': {}}
    for link in _URLset:
        print("url: ", link)
        try:   
            soup = pull(link)         
            c_dict['img'].update(sort_img(soup, link))
            c_dict['txt'].update(sort_txt(soup, link))
            c_dict['urls'].add(link)
            print('yes')
        except:
            print('retry')
            try: soup = pull(link) 
            except: pass 
            try: c_dict['img'].update(sort_img(soup, link))
            except: pass
            try: c_dict['txt'].update(sort_txt(soup, link))
            except: pass
            c_dict['urls'].add(link)
            print('yes')
        else:
            print('no')
            pass
        print()
    return c_dict
#-------------------------


def create_json(_dict, _name):
    """
    Takes Dictionary, String
    Saves a JSON file
    """
    with open("{}.json".format(_name), 'w', encoding='utf-8') as outfile:
        json.dump(_dict, outfile, skipkeys=False, ensure_ascii=False, sort_keys=True)
#-------------------------

def makepass():
    pass
#-------------------------

def google_search(_sentence):
    """
    Takes a String
    Returns a set of URLs
    --
    Runs a search for input sentence
    and collects all external links
    """
    # The line below uses a function ammended from the module Py_Web_Search that builds a google search url.
    # The module itself is broken.
    search_url = googl.generate_url(str(_sentence), num='10', start='0', recent=None, country_code=None)
    soup = pull(search_url)
    urls = set()
    for link in soup.find_all('h3', {'class': 'r'}):
        if link.find('a')['href'] != None and link.find('a')['href'].partition("/url?q=")[2] != None and link.find('a')['href'].partition("/url?q=")[2].partition("&sa=")[0] != None:
            urls.add(link.find('a')['href'].partition("/url?q=")[2].partition("&sa=")[0])
    return urls

#-------------------------


def from_list(_list, _limit=None):
    urls = []
    for item in _list:  # .partition(': ')[2]
        l = from_string(str(item))
        for url in l:
            print("urls: ", url)
            if url[-3:] != 'pdf':
                urls.append(url)
        print()
    return urls
#-------------------------


def from_string(_sentence):
    #sentence = "".join(x for x in _sentence if x not in string.punctuation)
    print("sentence from list: ", _sentence)
    search_results = google_search(_sentence)
    return search_results
#-------------------------


def scrape(_sentences, _name):
    sentences = []
    for sentence in _sentences:
        sentences.append("".join(s for s in str(sentence) if s not in string.punctuation))
    urls = from_list(sentences)
    d = create_dict(urls)
    d = txt_anal.analyse(d)
    d = img_anal.analyse(d)
    d['user'] = _name
    d['sentences'] = sentences
    d['urls'] = list(d['urls'])
    create_json(d, _name)
    return d
#-------------------------