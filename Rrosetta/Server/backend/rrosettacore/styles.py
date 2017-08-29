from random import randint
import math
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.lib.pagesizes import (
    A5, 
    A6, 
    landscape
)
from reportlab.platypus import (
    Paragraph,
    Spacer,
    Image
)  

class Fonts:
    from reportlab.pdfbase.ttfonts import TTFont
    fonts = [  
        TTFont('VT', 'Grouch Regular.ttf'),
        TTFont('VT-I', 'Hans-Grotesque-Italic.ttf'),
    ]

class Stylesheet:
    stylesheet = {'default': ParagraphStyle(
        'default',
        fontName='VT',
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
        wordWrap=1,
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
        fontSize=8,
        autoLeading='min',
        splitLongWords=0
    )
    stylesheet['title'] = ParagraphStyle(
        'title',
        parent=stylesheet['default'],
        fontName='VT-I',
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
        fontSize=12,
        autoLeading='max',
        splitLongWords=0
    )

class Framer:
    def __init__(self):
        from reportlab.platypus import Frame
        self.frame = Frame(0, 0, A5[0], A5[1], leftPadding=(A5[0] - A6[0]) / 2, bottomPadding=(
            A5[1] - A6[1]) / 2, rightPadding=(A5[0] - A6[0]) / 2, topPadding=(A5[1] - A6[1]) / 2)

class Storey:
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
        flow = randint(0,1)
        if flow == 1:
            flow = randint(1,2)
        if flow == 2:
            flow = randint(2,3)

        photo = self.photos[randint(0, len(self.photos)-1)]
        quote = self.quotes[randint(0, len(self.quotes)-1)]
        tainr = self.containers[randint(0, len(self.containers)-1)]

        q_sheet = randint(0, 5)
        c_sheet = randint(0, 1)


        if flow == 0:
            try:
                img = Image(self.dict['img'][photo]['src'])
                img.wrap(A6[0], A6[1])
                img.hAlign = ['CENTER', 'LEFT', 'RIGHT'][randint(0,3)]
                return img
            except:
                return Spacer(randint(0, 100), randint(0, 100))
        if flow == 3:
            return  Spacer(randint(0, 100), randint(0, 100))
        if flow == 1:
            #return Paragraph(quote, Stylesheet.stylesheet['quote'][q_sheet])
            return Paragraph(quote, Stylesheet.stylesheet['default'])
        if flow == 2:
            #return Paragraph(self.dict['txt'][tainr]['text'], Stylesheet.stylesheet['quote'][q_sheet])
            return Paragraph(self.dict['txt'][tainr]['text'], Stylesheet.stylesheet['default'])


    def try_pull(self, _key):
        try:
            img = Image(self.dict['img'][_key]['src'], A6[0], A6[1])
            img.wrap(A6[0], A6[1])
            img.hAlign = 'CENTER'
            return img
        except:
            self.photos.remove(_key)