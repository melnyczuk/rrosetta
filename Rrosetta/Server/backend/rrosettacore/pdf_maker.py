# https://docs.djangoproject.com/en/1.8/howto/outputting-pdf/
# https://www.davidfischer.name/2015/08/generating-pdfs-with-and-without-python/

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, A5
from reportlab.platypus import SimpleDocTemplate 
import json

PAGE_WIDTH, PAGE_HEIGHT = A5
PRINT_WIDTH, PRINT_HEIGHT = A4

def pull_json(_filepath):
    """
	Takes a String
	Returns a Dictionary
	"""
    with open(_filepath, 'r', encoding='utf-8') as infile:
        return json.load(infile)
#-------------------------

def gen_page(_doc):
    return
#-------------------------

def front_page():
    return
#-------------------------

def credit_page():
    return
#-------------------------

def back_page():
    return
#-------------------------

def make(_name):
    # Create the HttpResponse object with the appropriate PDF headers.
    path = "./{}.json".format(_name)
    d = pull_json(path)

    # Create the PDF object, using the response object as its "file."
    pdffilename = "{}.pdf".format(_name)
    zine = SimpleDocTemplate(pdffilename)


    p = canvas.Canvas(pdffilename, pagesize=A5)
   


    # Draw things on the PDF. Here's where the PDF generation happens.
    # See the ReportLab documentation for the full list of functionality.
    

    # Close the PDF object cleanly, and we're done.
    p.showPage()
    p.save()
#-------------------------


def write_pdf(_buf):
    with open('test.pdf', 'w') as fd:
        fd.write(_buf.getvalue())
#-------------------------