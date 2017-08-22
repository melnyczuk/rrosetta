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
            'src': img['src'],
            'alt': img['alt'],
            'title': img['title'],
            #'dimensions': [img['width'], img['height']]
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
    c_dict = {'img': {}, 'txt': {}}
    for link in _URLset:
        print("c_d: ", link)
        try:
            soup = pull(link)
            c_dict['img'].update(sort_img(soup, link))
            c_dict['txt'].update(sort_txt(soup, link))
            print('yes')
        except:
            print('no')
            pass
        print()
    return c_dict
#-------------------------


def create_json(_dict, _name):
    """
    Takes Dictionary, String
    Saves a JSON file
    --
    Dictionary contains
    sub-dictionaries containing
    all the text and all the images
    for all pages marked as a 'Reference'
    on a wikipedia page
    """
    with open("{}.json".format(_name), 'w', encoding='utf-8') as outfile:
        json.dump(_dict, outfile, skipkeys=False,
                  ensure_ascii=True, sort_keys=True)
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
            urls.add(link.find('a')['href'].partition("/url?q=")[2].partition("&sa=")[0])
    return urls

#-------------------------


def from_list(_list, _limit=None):
    urls = []
    for sentence in _list:  # .partition(': ')[2]
        l = from_string(str(sentence))
        for url in l:
            print("urls: ", url)
            urls.append(url)
        print()
    return urls
#-------------------------


def from_string(_sentence):
    sentence = "".join(x for x in _sentence if x not in string.punctuation)
    print("sentence from list: ", sentence)
    search_results = google_search(sentence)
    return search_results
#-------------------------


def main(_urls):
    urls = from_list(_urls)
    # print('urls: ', urls)
    # print()
    temp = create_dict(urls)
    # print('dict: ', temp)
    # print()
    temp = txt_anal.analyse(temp)
    # print('analysed: ', temp)
    # print()
    create_json(temp, 'test')
#-------------------------


if __name__ == "__main__":
    sentence = 'the quick brown fox jumped over the lazy dog'
    main(sentence)
