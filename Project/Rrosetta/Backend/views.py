from django.shortcuts import render
from django.http import HttpResponse
from . import master_control as mc
from . import citation_json as cj

def index(request):
    context = {}
    return render(request, "../Frontend/Rrosetta_template.html", context)

def make_json(request, _noun):
    cj.main(_noun)
    index(request)