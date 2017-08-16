
import sys
import requests
import csv
from bs4 import BeautifulSoup

## PULLS ALL THE HTML ##
def get_soup(url):                                                              # pass url;
    page = requests.get(url).content                                            # make http request;
    soup = BeautifulSoup(page, 'html.parser')                                   # parse html;
    return soup                                                                 # return soup;

def find_imgs(url):                                                      
    soup = get_soup(url)
    srcDict = {}
    try:
        for i, img in enumerate(soup.find_all('img')):
            src = img.attrs['src']
            if img.has_attrs(True):
                #nom = str(i) + img.attrs(['id', 'alt', 'name'])
                print(img.attrs(True))
                #srcDict[nom] = src
            else: srcDict[i] = src
    except Exception as e: 
        print('oops: ' + str(e))
        pass
    finally: return srcDict                            
     
def save_srcs(url, srcDict):
    with open('{}.csv'.format(name_gen(url)), 'w', newline='', encoding='UTF-8') as csvfile: 
        writer = csv.writer(csvfile)
        for i, [ids, src] in enumerate(srcDict.items()):
            writer.writerow([i, ids, src])


def name_gen(url):
    URLlist = url.split('/')
    return URLlist[2]# + '_' + URLlist[len(URLlist)-1]           

def main():
    siteURL = sys.argv[1] 
    save_srcs(siteURL, find_imgs(siteURL))

if __name__ == "__main__":
    main()