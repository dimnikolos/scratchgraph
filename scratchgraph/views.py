from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django import forms
from django.template import RequestContext
from django.core.context_processors import csrf
from .models import Greeting

from ScratchReader import *
from JSONinfo import *
from Sprites import *
from CompCUs import *
from CUGraph import *

class NameForm(forms.Form):
    your_file = forms.FileField()

def index(request):
    c={}
    c.update(csrf(request))
    if request.method == 'POST':
        form = NameForm(request.POST,request.FILES)
        if form.is_valid():
            scratchJSON = ScratchReader(request.FILES['your_file']).parseJSON()
            scratchInfo = JSONinfo(scratchJSON)
            (floatingScripts,sprites) = jsontoSprites(scratchJSON)
            cul = CompCUs(scratchInfo,sprites).parseCUs()
            cug = CUGraph(cul,sprites)
            graphJSstring = str(cug)
            return render(request, 'main.html',{'table':str(cul),'graph':graphJSstring})
    else:
        form = NameForm()
    return render(request, 'home.html',{'form':form}, context_instance = RequestContext(request))

def about(request):
       return render(request, 'about.html')
    
