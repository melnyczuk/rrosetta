# https://docs.djangoproject.com/en/1.8/howto/outputting-pdf/
# https://www.davidfischer.name/2015/08/generating-pdfs-with-and-without-python/

from reportlab.pdfgen import canvas
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.pagesizes import A4, A5, landscape
from reportlab.lib.utils import ImageReader
from reportlab.graphics.shapes import Image
from reportlab.platypus import SimpleDocTemplate, Flowable, ImageAndFlowables
from img_anal import get_pil
import json

PAGE_W, PAGE_H = A5
PRINT_H, PRINT_W = A4


def pull_json(_filepath):
    """
        Takes a String
        Returns a Dictionary
        """
    with open(_filepath, 'r', encoding='utf-8') as infile:
        return json.load(infile)
#-------------------------


def gen_page(_canvas):
    _canvas.showPage()
#-------------------------


def front_page(_canvas):
    _canvas.showPage()
#-------------------------


def credit_page(_canvas):
    _canvas.showPage()
#-------------------------


def back_page(_canvas):
    _canvas.showPage()
#-------------------------


def pull_photos(_dict):
    photos = {}
    for k in _dict['img']:
         if _dict['img'][k]['photo'] == True:
             photos = _dict['img']
    return photos
#-------------------------

def get_big_img(_photos):
    x = ''
    w = 0
    h = 0
    for k in _photos:
        if _photos[k]['dimensions'][1] > h:
            h = _photos[k]['dimensions'][1]
            x = k
        elif _photos[k]['dimensions'][0] > w:
            w = _photos[k]['dimensions'][0]  
            x = k 
    try: 
        return ImageReader(_photos[x]['src'])
    except:
        _photos.pop(x)
        return get_big_img(_photos)
    # If the image can't be pulled, remove it form the dictionary and try again with the next biggest


def make(_name):
    path = "./{}.json".format(_name)
    d = pull_json(path)
    photos = pull_photos(d)
    pdffilename = "{}.pdf".format(_name)
    zine = SimpleDocTemplate(pdffilename)
    c = Canvas(pdffilename, pagesize=landscape(A4))
    
    img = get_big_img(photos)
    img_w, img_h = img.getSize()

    c.drawImage(img, (A4[1]-A5[0])/2, 0, width=A5[0], height=A5[1], mask=None, preserveAspectRatio=True)
    c.setFillColorRGB(1.0, 1.0, 1.0)
    c.setFont('Helvetica', img_w/40, leading = None)
    c.drawCentredString(PRINT_W/2, PRINT_H/2, str(d['user']).upper())
    c.showPage()
    c.save()
#-------------------------


def write_buf_pdf(_buf):
    with open('test.pdf', 'w') as fd:
        fd.write(_buf.getvalue())
#-------------------------

if __name__ == "__main__":
    import sys
    make("h.melnyczuk@gmail.com")