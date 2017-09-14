## PY3 ## HPM ## CREATES CSV OF EVERY LINK BY TAG, ID
import sys                                                                      # inc py install;
import requests                                                                 # pip install requests;
import csv                                                                      # inc py install;
from bs4 import BeautifulSoup                                                   # pip install beautifulsoup4;

## PULLS ALL THE HTML ##
def get_soup(url):                                                              # pass url;
    page = requests.get(url).content                                            # make http request;
    soup = BeautifulSoup(page, 'html.parser')                                   # parse html;
    return soup                                                                 # return soup;

## MAKES A DICTIONARY OF LINKS BY ID & NUMBER ##
def dict_links(soup, tag):                                                      # pass soup (html) & specific tag;
    tagname = str(tag)                                                          # make a string of tag;
    ids = []                                                                    # local list of all ids;
    src = []                                                                    # local list of all srcs links;
    try:
        for i, t in enumerate(soup.find_all(tagname)):                          # loop through all tags of type t in soup, and track of iteration;
            if t.has_attr('id'):                                                # look for id attribute;
                id = t.attrs['id']                                              # get value of id attribute;
                ids.append(str(i) + ' ' + str(id))                              # append iteration and id number to list of ids;
            elif t.has_attr('alt'):                                             # if no id attribute, find alt attribute;
                alt = t.attrs['alt']                                            # get value of alt attribute;
                ids.append(str(i) + ' ' + str(alt))                             # append iteration number and alt to list of ids;
            elif t.has_attr('name'):                                            # if not id or alt, find name attribute;
                name = t.attrs['name']                                          # get value of name attribute;
                ids.append(str(i) + ' ' + str(name))                            # append interation number & name to list of ids;
            else: ids.append(str(i))                                            # if no id, alt or name: just use iteration number;

            if t.has_attr('href'):                                              # look for href link attribute;
                h = t.attrs['href']                                             # get link url;
                src.append(str(h))                                              # append to srcs list;
            elif t.has_attr('src'):                                             # if no href find src links;
                h = t.attrs['src']                                              # get link url;
                src.append(str(h))                                              # append to srcs list;
            else: src.append('')                                                # if no link present, append blank (removed later but keeps dictionary order);

        dic = dict(zip(ids, src))                                               # zip ids and srcs into a single dictionary;
        return {k: v for k, v in dic.items() if v != ''}                        # remove entries with no links;
        
    except Exception as e:
        print('You might want to check that url:')                              # error message;
        print(e)                                                                # print exception msg;
        pass                                                                    # move on, life is short;

## MAKE A LIST OF ALL TAGS PRESENT IN HTML ##
def list_tags(soup):
    try:
        return [tag.name for tag in soup]                                       # gets name of tag from all tags in soup;
    except:
        pass                                                                    # if this fails, skip over;

## MAKE A SET OF ALL UNIQUE TAG TYPES ##
def set_tag_types(tags):
    tagTypes = set(tags)                                                        # converts list of tags into a set;
    tagTypes.discard(None)                                                      # removes any non real tags 
    return tagTypes                                                             # returns as set;

## MAKE AND SAVE CSV FILE FROM DICTIONARY ##   
def save_csv(csvName, dictionary):
    with open('{}.csv'.format(csvName), 'w', newline='') as csvfile:            # make and save a csv with name of site page;
        writer = csv.writer(csvfile)                                            # make csv writer;
        for tag in dictionary:                                                  # for all keys in dictionary of id/src dictionaries
            for k, v in dictionary[tag].items():                                # loop through the dictionary of dictionaries;
                t = str(tag)
                k = str(k)                                                      # make a csv entry with tag and id (aka outer and inner dictionary keys) combined
                v = str(v)                                                      # make a csv entry for the links
                writer.writerow([t, k, v])                                      # write these as a new row in the csv file and save it;

## RUN THIS BAD BOY: GIVE IT A URL IN CMD ##
def main(siteURL):                                                # pass in a url;
    wiki = siteURL.split('/')                                                   # parse url at /;
    wiki = wiki[2] + '_' + wiki[len(wiki)-1]                                                    # get final level domain name (aka page name);                             
    soup = get_soup(siteURL)                                                    # turn url into soup;

    tagsList = list_tags(soup.descendants)                                      # get list of all tags present in whole soup;
    tagTypes = set_tag_types(tagsList)                                          # turns this list into a set of tag types;
    tagTypes = [str(tag) for tag in tagTypes]                                   # formats this set into strings;

    srcList = []                                                                # empty list of srcs/links;
    for tag in tagTypes:                                                        # runs on every tag type present in html;
        srcList.append(dict_links(soup, tag))                                   # appends the id/src dictionary for every tag type;
    srcDict = dict(zip(tagTypes, srcList))                                      # zips together another dictionary with tag as key and the dictionary of id/src for that tag;
    srcDict = {k: v for k, v in srcDict.items() if v}                           # removes blank id/src dictionaries;

    save_csv(wiki, srcDict)                                         

if __name__ == "__main__":
    main(sys.argv[1])