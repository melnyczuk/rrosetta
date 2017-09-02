# Collects content by running a google search on a number of sentences,
# then collecting the top results for each search,
# then scraping the img and p tags for each of those sites.

#=========================

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
    return BeautifulSoup(page, 'html.parser')
#-------------------------


def create_json(_dict, _name):
    """
    Takes Dictionary, String
    Saves a JSON file
    """
    with open("{}.json".format(_name), 'w', encoding='utf-8') as outfile:
        json.dump(_dict, outfile, skipkeys=False,
                  ensure_ascii=False, sort_keys=True)
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
        try:
            soup = pull(link)
            c_dict['img'].update(sort_img(soup, link))
            c_dict['txt'].update(sort_txt(soup, link))
            c_dict['urls'].add(link)
        except:
            try:
                soup = pull(link)
            except:
                pass
            try:
                c_dict['img'].update(sort_img(soup, link))
            except:
                pass
            try:
                c_dict['txt'].update(sort_txt(soup, link))
            except:
                pass
            c_dict['urls'].add(link)
        else:
            pass
    c_dict['urls'] = list(c_dict['urls'])
    return c_dict
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
    search_url = googl.generate_url(
        str(_sentence), num='10', start='0', recent=None, country_code=None)
    soup = pull(search_url)
    urls = set()
    for heads in soup.find_all('h3', {'class': 'r'}):
        for head in heads:
            if head.name == 'a' and head.has_attr('href'): 
                link = head['href']
                if link != None and link.partition("/url?q=")[2] != None and link.partition("/url?q=")[2].partition("&sa=")[0] != None:
                    urls.add(link.partition("/url?q=")[2].partition("&sa=")[0])
                else:
                    pass
            else:
                pass
    return urls
#-------------------------


def scrape(_dict):
    for i, sentence in enumerate(_dict['sentences']):
        s = [word for word in str(sentence).split(
            sep=' ') if word not in string.punctuation]
        _dict['sentences'][i] = " ".join(s).strip()

    urls = [url for item in _dict['sentences']
            for url in google_search(str(item)) if url[-3:] != 'pdf']
    _dict.update(create_dict(urls))
    _dict['img'] = img_anal.analyse(_dict['img'])
    _dict['txt'] = txt_anal.analyse(_dict)
    return _dict
#-------------------------
