# https://docs.djangoproject.com/en/1.8/howto/outputting-pdf/
# https://www.davidfischer.name/2015/08/generating-pdfs-with-and-without-python/

#=========================

import json
import time
from random import randint

from reportlab.graphics.shapes import Image
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.pdfgen.canvas import Canvas

from reportlab.lib.pagesizes import (
    A4, 
    A5, 
    A6, 
    landscape
)

from reportlab.platypus import (
    Paragraph,
    SimpleDocTemplate,
    Frame,
    Table,
    Spacer,
    Image as Im,
)

from styles import Fonts
from styles import Stylesheet
from styles import Framer
from styles import Storey

#=========================

for font in Fonts.fonts:
    pdfmetrics.registerFont(font)

#=========================


class Zine:
    def __init__(self, _dict):
        self.dict = _dict
        self.filename = "{}.pdf".format(_dict['user'])

        self.canvas = Canvas(self.filename, A5, bottomup=1)
        self.doc = self.setup_doc()

        self.font = Fonts.fonts[0].fontName
        self.canvas.setFont(self.font, 0)

        self.style = Stylesheet.stylesheet

    #=========================

    def setup_doc(self):
        return SimpleDocTemplate(
            self.filename,
            pagesize=A5,
            showBoundary=0,
            leftMargin=20,
            rightMargin=20,
            topMargin=20,
            bottomMargin=20,
            allowSplitting=0,
            title=None,
            author=None,
            _pageBreakQuick=1,
            encrypt=None
        )
    #-------------------------

    def cover(self):    # Make Greyscale? 
        Framer().frame.addFromList(
            [self.cover_img()], self.canvas)
        self.canvas.setFillColorRGB(1.0, 1.0, 1.0)
        self.canvas.rect(0, 0.48 * A5[1], A5[0],
                         0.06 * A5[1], stroke=0, fill=1)
        self.canvas.setFillColorRGB(0.0, 0.0, 0.0)
        self.canvas.setFontSize(20)
        self.canvas.drawCentredString(
            A5[0] / 2, A5[1] / 2, str(self.dict['user']).encode('utf-8'))
        self.canvas.showPage()
    #-------------------------

    def gen_pages(self, _n):
        for n in range(_n):
            s = Storey(self.dict)
            Framer().frame.addFromList(s.story, self.canvas)
            s = Storey(self.dict)
            Framer().frame.addFromList(s.story, self.canvas)
            self.canvas.showPage()
    #-------------------------

    def credits(self):
        paragraphs = [Paragraph(url, self.style['credits'])
                      for url in self.dict['urls']]
        Framer().frame.addFromList(paragraphs, self.canvas)
        self.canvas.showPage()
    #-------------------------

    def back(self):
        story = []
        story.append(Spacer(A5[0], A5[1] / 20))
        for i in [Paragraph(sentence.title(), self.style['title']) for sentence in self.dict['sentences']]:
            story.append(i)
        story.append(Spacer(A5[0], A5[1] / 4))
        story.append(Paragraph("printed by Free Wifi Press at {time} on {date}".format(time=time.strftime(
            "%H:%M"), date=time.strftime("%d-%m-%Y")), self.style['rrosetta']))

        story.append(Spacer(A5[0], A6[1] / 100))
        story.append(Paragraph("--", self.style['rrosetta']))
        story.append(Spacer(A5[0], A6[1] / 100))
        story.append(Paragraph("Rrosetta by Howard Melnyczuk", self.style['rrosetta']))
        story.append(Spacer(A5[0], A6[1] / 100))
        story.append(
            Paragraph("h.melnyczuk@gmail.com", self.style['rrosetta']))
        story.append(Paragraph("http://melnycz.uk", self.style['rrosetta']))
        
        Framer().frame.addFromList(story, self.canvas)
        self.canvas.showPage()
    #-------------------------

    def cover_img(self):
        x = ''
        a = 0
        photos = Storey(self.dict).photos
        if len(photos) < 1:
            return
        # Find biggest image.
        for k in photos:
            if self.dict['img'][k]['dimensions'][1] / self.dict['img'][k]['dimensions'][0] > 1 and self.dict['img'][k]['dimensions'][0] > a:
                a = self.dict['img'][k]['dimensions'][0] * self.dict['img'][k]['dimensions'][1]
                x = k
        # If the image can't be pulled, remove it form the dictionary and try again with the next biggest
        try:
            img = Im(self.dict['img'][x]['src'], A6[0], A6[1])
            img.wrap(A6[0], A6[1])
            img.hAlign = 'CENTER'
            return img
        except:
            photos.remove(x)
            return self.cover_img()              
#-------------------------
#=========================


def make(_dict):
    zine = Zine(_dict)
    zine.cover()
    zine.gen_pages(5)
    zine.credits()
    zine.back()
    zine.canvas.save()
#-------------------------

#=========================


def pull_json(_filepath):
    """
        Takes a String
        Returns a Dictionary
        """
    with open(_filepath, 'r', encoding='utf-8') as infile:
        return json.load(infile)
#-------------------------

#=========================


if __name__ == "__main__":
    import sys
    d = pull_json(sys.argv[1])
    make(d)
