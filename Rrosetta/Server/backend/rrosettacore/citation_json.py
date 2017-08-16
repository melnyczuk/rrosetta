#PY3#HPM#
# This creates a JSON file containing all the images and text paragraphs
#   from each site used as a citation reference for the relevant wikipedia page
#   for any given noun

#=========================

import json
import random

import requests
from bs4 import BeautifulSoup

import img_anal
import txt_anal

#=========================


def citation_set(_noun):
    """
    Takes a String
    Returns a Set 
    --
    Set contains all external citation links
    from a wikipedia page 
    most relavent to any given noun
    """
    # take the passed noun fron the sentiment analysis and make it into a wikipedia url
    wiki = "https://en.wikipedia.org/wiki/{}".format(
        _noun)
    # pull that wikipedia page
    soup = pull(wiki)
    # THE LOOP BELOW WILL CHECK IF THIS IS A GOOD PAGE TO USE FOR EXTERNAL CONTENT
    x = 0
    # Start a While loop to keep trying stuff
    while True:
        # make list of all links on the page, if the links have a title and no colon
        links = [link['href'] for link in soup.find_all('a') if link.has_attr('title') and str(link).find(
            ':') == -1]
        # for all <span> tags in the soup:
        for i in soup.find_all('span'):
            # if a <span> tag has an 'id' attribute, and that 'id' attribute is 'Reference', and the page has external links, then HOORAY!
            if i.has_attr('id') and i.attrs['id'] == 'References' and "external text" not in soup:
                # break the loop and return a set of external links taken from the references section
                return set(t.attrs['href'] for t in soup.find_all('a', class_='external text'))
            # if this is not yet the last <span> tag, but we've yet to find a winner:
            elif i != soup.find_all('span')[-1]:
                # go back to the start
                pass
            # if none of the above because we have no external links
            elif "external text" not in soup:
                # increment x
                x += 1
                # try pulling the next page in the link list
                soup = pull("https://en.m.wikipedia.org{}".format(links[x]))
                # go back to the start
                pass
            # if none of the above,
            else:
                links = [link['href'] for link in soup.find_all('a') if link.has_attr(
                    'title') and str(link).find(':') == -1]   # make a fresh list to try again
                # pull the first link from the list
                soup = pull("https://en.m.wikipedia.org{}".format(links[x]))
                # go back to the start
                pass
#-------------------------


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
    for img in imgs:
        key = 'img_' + str(int(random.random() * 10**10))
        img_dict[key] = {
            'origin': _url,
            'src': img['src'],
            'alt': img['alt'],
            'title': img['title'],
            'dimensions': [img['width'], img['height']]
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
        try:
            print(link)
            soup = pull(link)
            c_dict['img'].update(sort_img(soup, link))
            c_dict['txt'].update(sort_txt(soup, link))
        except:
            pass
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


def main(_noun, _folder=""):
    """
    takes a String (, String)
    Saves a JSON file
    --
    JSON contains 
    dictionaries containing
    all the text and all the images
    for all pages marked as a 'Reference'
    on a wikipedia page
    following analysis
    """
    c_set = citation_set(_noun)
    name = "./{folder}/{noun}".format(folder=_folder, noun=_noun)
    temp = create_dict(c_set)
    create_json(temp, name)
    img_anal.analyse(_noun)
    txt_anal.analyse(_noun)
#-------------------------


#=========================
if __name__ == "__main__":
    import sys
    noun = sys.argv[1]
    main(noun, "citation_jsons")
