import json
import urllib.request as urllib
import cv2
import numpy as np

def pull_json(_path):
    with open(_path, 'r', encoding='utf-8') as infile:
    	return json.load(infile)
    
def update_json(_path, _dict):
    with open(_path, 'w', encoding='utf-8') as outfile:
    	json.dump(_dict, outfile, skipkeys=False, ensure_ascii=True, sort_keys=True) 

def get_img(_src):
	"""
	Returns a cv2 image
	from a source url
	credit: (https://prateekvjoshi.com/2016/03/01/how-to-read-an-image-from-a-url-in-opencv-python/)
	"""
	try:
		url_response = urllib.urlopen(_src)
		img_array = np.array(bytearray(url_response.read()), dtype=np.uint8)
		return cv2.imdecode(img_array, -1)
	except:
		pass

def analyse(_json):
    path = "citation_jsons/{}.json".format(_json)
    d = pull_json(path)
    for k in d['img']:
       	src = d['img'][k]['src']
       	img = get_img(src)
       	try: d['img'][k]['dimensions'] = img.shape
       	except: d['img'][k]['dimensions'] = [0,0,0]; pass
        	# if d['img'][k]['dimensions'][0] < 1 or d['img'][k]['dimensions'][1] < 1 or d['img'][k]['dimensions'][2] < 1:
        	#     d['img'][k] = False
    update_json(path, d)

if __name__ == '__main__':
    import sys
    analyse(sys.argv[1])