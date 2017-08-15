# PY3 ## HPM ## THIS CREATES A JSON CATALOG OF TEXT PARAGRAPHS AND IMAGES
import requests
import json
import random
from bs4 import BeautifulSoup

# MAKE A SET OF ALL CITATIONS ON A WIKI PAGE IN ORDER TO FIND ZINE CONTENT #


def citation_set(_noun):
    """
    Returns a Set 
    containing all external citation links
    from a wikipedia page 
    most relavent to any given noun
    """
    wiki = "https://en.wikipedia.org/wiki/{}".format(
        _noun)                                                                     # take the passed noun fron the sentiment analysis and make it into a wikipedia url
    # pull that wikipedia page
    soup = pull(wiki)
    # THE LOOP BELOW WILL CHECK IF THIS IS A GOOD PAGE TO USE FOR EXTERNAL CONTENT
    x = 0
    # Start a While loop to keep trying stuff
    while True:
        links = [link['href'] for link in soup.find_all('a') if link.has_attr('title') and str(link).find(
            ':') == -1]           # make list of all links on the page, if the links have a title and no colon
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


def pull(_url):
    """
    Returns the BeautifulSoup for URL
    """
    page = requests.get(_url).content
    soup = BeautifulSoup(page, 'html.parser')
    return soup


def catalog_url(_url):
    """
    Returns a dictionary 
    containing all text and images grouped as such.
    """
    soup = pull(_url)
    # Seperates images and text into internal nested dictionaries of each
    content = {'img': {}, 'txt': {}}
    # Updates nested dictionary of images
    content['img'].update(sort_img(soup, _url))
    # Updates nested dictionary of text
    content['txt'].update(sort_all_txt(soup, _url))
    return content


def sort_txt(_soup, _url):
    """
    Returns a dictionary 
    containing the text (if any) from every <p> tag in a page
    """
    p_dict = {}
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


def sort_all_txt(_soup, _url):
    """
    Returns a dictionary 
    containing all the text on a page
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


def sort_img(_soup, _url):
    """
    Returns a dictionary 
    containing all the image source urls on a page
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


def create_dict(_set):
    """
    Returns a dictionary 
    combing all the text and all the image dictionaries 
    for all pages marked as a 'Reference'
    on a wikipedia page
    """
    c_dict = {'img': {}, 'txt': {}}
    for l in _set:
        try:
            print(l)
            soup = pull(l)
            c_dict['img'].update(sort_img(soup, l))
            c_dict['txt'].update(sort_txt(soup, l))
        except:
            pass
    return c_dict


def create_json(_dict, _name):
    """
    Saves a JSON file from dictionary _dict with name _name
    containing all the text and all the image dictionaries 
    for all pages marked as a 'Reference'
    on a wikipedia page
    """
    with open("{}.json".format(_name), 'w', encoding='utf-8') as outfile:
        json.dump(_dict, outfile, skipkeys=False,
                  ensure_ascii=True, sort_keys=True)


def main(_noun, _folder=""):
    """
    Saves a JSON file for any passed in NOUN
    containing all the text and all the image dictionaries 
    for all pages marked as a 'Reference'
    on a wikipedia page
    """
    c_set = citation_set(_noun)
    name = "./{folder}/{noun}".format(folder=_folder, noun=_noun)
    temp = create_dict(c_set)
    create_json(temp, name)


#=========================
if __name__ == "__main__":
    import sys
    import img_anal
    import txt_anal
    noun = sys.argv[1]
    main(noun, "citation_jsons")
    img_anal.analyse(noun)
    txt_anal.analyse(noun)
