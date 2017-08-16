## PY3 ## HPM ## THIS CREATES A CSV CATALOG OF ALL HYPERLINKS ON ANY URL (NUMBER//TEXT//URL//TYPE)
import sys
import requests
import csv
from bs4 import BeautifulSoup

## PULLS ALL THE HTML ##
def get_soup(url):                                                              # pass url;
    page = requests.get(url).content                                            # make http request;
    soup = BeautifulSoup(page, 'html.parser')                                   # parse html;
    return soup                                                                 # return soup;

## MAKES A DICTIONARY OF ALL LINKS BY TEXT ##
def create_dict(url):
    soup = get_soup(url)
    linkList = split_url(url)
    linkDict = {}
    try:
        for anchor in soup.find_all('a'):
            if(anchor.has_attr('href')):
                text = anchor.text
                link = anchor.attrs['href']
                if (link[0] == '/'): link = linkList[0] + '//' + linkList[2] + link
                linkDict[text] = link
            else: pass
    except Exception as e:
        print('oops: ' + str(e))
        pass
    finally:
        return linkDict

## SAVES A CSV FROM A DICTIONARY ##
def save_csv(url, dictionary):
    originalDomain = split_url(url)
    csvName = name_gen(originalDomain)
    with open('{}.csv'.format(csvName), 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)                                            # make csv writer;
        for i, [text, link] in enumerate(dictionary.items()):                   # loop through the dictionary of dictionaries;
            linkDomain = split_url(link)                                        # split up href url;
            #--
            if linkDomain[0][:5] == '#cite': linkType = 'citation'              # determines if link is wikipedia citation;
            elif linkDomain[0][0] == '#': linkType = 'site redirect'            # determines if link is site redirect;
            elif linkDomain[0] != 'http:' and linkDomain[0] != 'https:': linkType = 'other' # determines if link is not standalone url;
            elif linkDomain[2] == originalDomain[2]: linkType = 'internal'      # determines if link goes internally;
            elif linkDomain[2] != originalDomain[2]: linkType = 'external'      # determines if link goes externally;
            else: linkType = 'weird'                                            # if non of the above
            #--
            writer.writerow([i, text, link, linkType])                          # writes row;

##  SPLITS A URL AT '/' ##
def split_url(url):
    return url.split('/')

## GENERATE NAME FROM URL ##    
def name_gen(URLlist):
    return (URLlist[2] + '_' + URLlist[len(URLlist)-1])                         

def main(siteURL):                                                   # pass in a url;                                                   #
    linkDict = create_dict(siteURL)                                             #
    save_csv(siteURL, linkDict)                                              # save csv

if __name__ == "__main__":
    main(sys.argv[1])