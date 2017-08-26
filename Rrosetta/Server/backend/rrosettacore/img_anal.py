#PY3#HPM#
# This script analyses all the images catalogued in a JSON file
#=========================

import json
import urllib.request as urllib
from io import BytesIO

import numpy as np
from PIL import Image
import requests

import cv2

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


def get_cv(_src):
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
        img = cv2.imread()
        return img
    except:
        pass
#-------------------------


def get_pil(_src):
    try:
        resp = requests.get(_src)
        image = Image.open(BytesIO(resp.content))
        return image
    except:
        pass
#-------------------------


def format_dict(_dict):
    x = 0
    d = {}
    d['txt'] = _dict['txt']
    d['urls'] = _dict['urls']
    d['img'] = {}
    print(len(_dict['img'].keys()))
    for k in _dict['img']:
        if 'dimensions' in _dict['img'][k].keys() and _dict['img'][k]['dimensions'][0] > 1 and _dict['img'][k]['dimensions'][1] > 1:
            d['img'][k] = _dict['img'][k]
    print(len(d['img'].keys()))
    for k in d['img']:
        if d['img'][k]['dimensions'][0] / d['img'][k]['dimensions'][1] == 1:
            d['img'][k]['square'] = True
        else: d['img'][k]['square'] = False
        if d['img'][k]['dimensions'][0] > 100 and d['img'][k]['dimensions'][1] > 100 and d['img'][k]['format'] == 'JPEG':
            d['img'][k]['photo'] = True
            x += 1
            print(x)
        else: d['img'][k]['photo'] = False
    return d
#-------------------------


def analyse(_dict):
    """
	Takes a Dictionary
    Returns a dictionary
	--
	Perform analysis
    on a dictionary
	"""
    d = _dict
    for k in d['img']:
        src = d['img'][k]['src']
        img = get_pil(src)
        try:
            d['img'][k]['dimensions'] = img.size
            d['img'][k]['format'] = img.format
            d['img'][k]['mode'] = img.mode
        except:
            pass
    d = format_dict(d)
    return d
#-------------------------

#=========================


if __name__ == '__main__':
    d = pull_json("../../test.json")
    d = analyse(d)
    update_json("./test.json", d)