#PY3#HPM#
# This script analyses all the images catalogued in a JSON file

#=========================

import json
import urllib.request as urllib
import cv2
import numpy as np

#=========================


def pull_json(_filepath):
    """
	Takes a String
	Returns a Dictionary
	"""
    with open(_filepath, 'r', encoding='utf-8') as infile:
        return json.load(infile)
#-------------------------


def update_json(_filepath, _dict):
    """
	Takes a String and a Dictionary
	Saves a JSON file
	"""
    with open(_filepath, 'w', encoding='utf-8') as outfile:
        json.dump(_dict, outfile, skipkeys=False,
                  ensure_ascii=True, sort_keys=True)
#-------------------------


def get_img(_src):
    """
	Takes a String
    Returns a CV2 Image
	--
    Gets OpenCV image
	from a source url
    credit: (https://prateekvjoshi.com/2016/03/01/how-to-read-an-image-from-a-url-in-opencv-python/)
    """
    try:
        url_response = urllib.urlopen(_src)
        img_array = np.array(bytearray(url_response.read()), dtype=np.uint8)
        return cv2.imdecode(img_array, -1)
    except:
        pass
#-------------------------


def analyse(_dict):
    """
	Takes a String
	Saves a JSON
	--
	Perform analysis
	from JSON file,
	the updates JSON
	"""
    d = _dict
    for k in d['img']:
        src = d['img'][k]['src']
        img = get_img(src)
        try:
            d['img'][k]['dimensions'] = img.shape
        except:
            pass
        # if d['img'][k]['dimensions'][0] < 1 or d['img'][k]['dimensions'][1] < 1:
        #	d['img'][k] = False
    return d
#-------------------------


#=========================


if __name__ == '__main__':
    import sys
    analyse(sys.argv[1])
