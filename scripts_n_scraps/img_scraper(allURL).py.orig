import sys
from io import BytesIO                                                  # for converting http response bytes into image;
from urllib.parse import urlparse                                       # for using url in filename;
from bs4 import BeautifulSoup                                           # for finding img tags;
from PIL import Image                                                   # for saving the Images;
import requests                                                         # for http requests;

## FIND ALL IMG TAGS ON ANY GIVEN URL ##
def findIMGs(url):                                                      # pass url and send request;
    webpage = requests.get(url).content
    soup = BeautifulSoup(webpage, "lxml")                               # translate into html and parse;
    imgs = [img['src'] for img in soup.find_all('img')]
    return imgs                                                         # store the src of all img tags in list;
        
## SAVE ALL THE IMAGES ##
def saveIMGs(url):
    imgURLs = []
    imgURLs = findIMGs(url)                                             # store all src's in new list; (need clean-up?)
    for i in imgURLs:                                                   # iterate over every src in list
        try:
            src = str(i)                                                # get src as string;
            resp = requests.get(src)                                    # get http response
            image = Image.open(BytesIO(resp.content))                   # open response bytes content as image file;
            name = urlparse(src)[1]                                     # use site url in image file naming;
            num = imgURLs.index(str(i))                                 # use position in src's list in image file naming;
            print('yep: ' + str(name) + str(num))                       # print image file name;
            image.save(str(name) + str(num) + '.' + str(image.format))  # save image;
        except Exception as e:                                          # if src url fails or is blocked etc:
            print('nope: ' + str(e))                                    # print exception;
            pass                                                        # move on to next img tag src url;

## INPUT URL ##
if __name__ == "__main__":
    saveIMGs(sys.argv[1])