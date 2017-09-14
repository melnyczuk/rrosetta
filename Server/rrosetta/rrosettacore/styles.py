## THIS ZINE CONTAINS FUNCTIONS FOR FORMATTING AND STYLING THE ZINES

import math
import re
from random import randint

from bs4 import BeautifulSoup as bs
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A5, A6, landscape
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import Image, Paragraph, Spacer


class Fonts:
    """
    Loads Fonts
    
    These must have been preinstalled on computer system
    """
    from reportlab.pdfbase.ttfonts import TTFont
    fonts = [  
        TTFont('Reg', 'Hans-Grotesque.ttf'),
        TTFont('Bold', 'ArchivoBlack-Regular.ttf'),
        #TTFont('Bold', 'Berthold Akzidenz Grotesk Bold.otf'),
        TTFont('Ital', 'Hans-Grotesque-Italic.ttf'),
    ]

class Stylesheet:
    """
    A selection of stylesheets
    for various purposes
    """
    stylesheet = {'default': ParagraphStyle(
        'default',
        fontName='Reg',
        fontSize=12,
        leading=12,
        leftIndent=0,
        rightIndent=0,
        firstLineIndent=0,
        alignment=TA_LEFT,
        spaceBefore=0,
        spaceAfter=0,
        bulletFontName='Times-Roman',
        bulletFontSize=10,
        bulletIndent=0,
        textColor=[0.0, 0.0, 0.0],
        backColor=None,
        wordWrap=None,
        borderWidth=0,
        borderPadding=0,
        borderColor=None,
        borderRadius=None,
        allowWidows=1,
        allowOrphans=0,
        textTransform=None,  # 'uppercase' | 'lowercase' | None
        endDots=None,
        splitLongWords=1,
    )}
    stylesheet['credits'] = ParagraphStyle(
        'credits',
        parent=stylesheet['default'],
        fontName='Reg',
        fontSize=8,
        autoLeading='min',
        splitLongWords=0
    )
    stylesheet['title'] = ParagraphStyle(
        'title',
        parent=stylesheet['default'],
        fontName='Ital',
        fontSize=14,
        leftIndent=10,
        firstLineIndent=-10,
        autoLeading='min',
        spaceAfter=15,
        splitLongWords=0,
    )
    stylesheet['rrosetta'] = ParagraphStyle(
        'rrosetta',
        parent=stylesheet['default'],
        fontName='Reg',
        fontSize=12,
        autoLeading='max',
        splitLongWords=0
    )

class Framer:
    """
    Determines size of page frame
    """
    def __init__(self):
        from reportlab.platypus import Frame
        border = (A5[0] - A6[0]) / 2
        self.frame = Frame(0, 0, A5[0], A5[1], leftPadding=border, bottomPadding=border, rightPadding=border, topPadding=border,)
        self.frame.split

class Storey:
    """
    Fills page frame with content
    """
    def __init__(self, _dict):  
        self.dict = _dict
        self.photos = [k for k in _dict['img']
                       if _dict['img'][k]['photo'] == True]
        self.quotes = [quote for k in _dict['txt'] if _dict['txt']
                       [k]['quotes'] != False for quote in _dict['txt'][k]['quotes']]
        self.containers = [k for k in _dict['txt']
                           if _dict['txt'][k]['contains'] != False]
        self.story = self.gen_story()

    def gen_story(self):
        story = []
        for i in range(randint(1, 9)):
            story.append(self.gen_flowable())
        return story

    def gen_flowable(self):
        """
        Picks content from pool of content
        """
        flow = randint(0,randint(1,2))          ## Weighted random numbers to balance text to image ratio
        if flow == 0:
            try:
                photo = self.photos[randint(0, len(self.photos)-1)]
                img = Image(self.dict['img'][photo]['src'], self.dict['img'][photo]['dimensions'][0], self.dict['img'][photo]['dimensions'][1])
                img.wrap(A6[0],A6[1])
                img.hAlign = ['CENTER', 'LEFT', 'RIGHT'][randint(0,3)]
                return img
            except:
                return Spacer(randint(0, 100), randint(0, 100))
        elif flow == 1:
            try:
                quote = self.quotes[randint(0, len(self.quotes)-1)]
                q_sheet = randint(0, 5)
                #return Paragraph(quote, Stylesheet.stylesheet['quote'][q_sheet])
                return Paragraph(cleanhtml(quote), Stylesheet.stylesheet['title'])
            except:
                return Spacer(randint(0, 100), randint(0, 100))
        elif flow == 2:
            try:
                tainr = self.containers[randint(0, (len(self.containers)-1))]
                c_sheet = randint(0, 1)
                #return Paragraph(self.dict['txt'][tainr]['text'], Stylesheet.stylesheet['quote'][q_sheet])
                return Paragraph(cleanhtml(self.dict['txt'][tainr]['text']), Stylesheet.stylesheet['default'])
            except:
                return Spacer(randint(0, 100), randint(0, 100))
        else:
            return Spacer(randint(0, 100), randint(0, 100))

#https://stackoverflow.com/questions/9662346/python-code-to-remove-html-tags-from-a-string
def cleanhtml(raw_html):
  cleanr = re.compile('<.*?>')
  cleantext = re.sub(cleanr, '', raw_html)
  return cleantext
