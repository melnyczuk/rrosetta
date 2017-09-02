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
    d = {}

    for k in _dict:
        # remove duds
        if 'dimensions' in _dict[k].keys() and _dict[k]['dimensions'][0] > 1 and _dict[k]['dimensions'][1] > 1:
            d[k] = _dict[k]

    for k in d:
        # find square images (probably icons)
        if d[k]['dimensions'][0] / d[k]['dimensions'][1] == 1:
            d[k]['square'] = True
        else:
            d[k]['square'] = False
        # find big images (probably photos/useful)
        if d[k]['dimensions'][0] > 100 and d[k]['dimensions'][1] > 100 and d[k]['format'] == 'JPEG':
            d[k]['photo'] = True
        else:
            d[k]['photo'] = False
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
    for k in _dict:
        img = get_pil(_dict[k]['src'])
        try:
            _dict[k]['dimensions'] = img.size
            _dict[k]['format'] = img.format
            _dict[k]['mode'] = img.mode
        except:
            pass
    return format_dict(_dict)
#-------------------------
