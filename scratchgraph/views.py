from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django import forms
from django.template import RequestContext
from django.core.context_processors import csrf
from .models import Greeting
import urllib2


from ScratchReader import *
from JSONinfo import *
from Sprites import *
from CompCUs import *
from CUGraph import *

class NameForm(forms.Form):
   project_url = forms.CharField(max_length=200)

def index(request):
    c = {}
    c.update(csrf(request))
    if request.method == 'POST':
        form = NameForm(request.POST)
        if form.is_valid():
            project_url = request.POST['project_url']
            if project_url.startswith('http://scratch.mit.edu/projects/'):
               if project_url.endswith('#editor'):
                  project_url = project_url[:-7]
               if project_url.endswith('/'):
                  project_url = project_url[:-1]
               project_id = project_url[32:]
               projectName = project_id
               scratchJSONURL = "http://projects.scratch.mit.edu/internalapi/project/" + project_id + "/get/"
               rawJSON = urllib2.urlopen(scratchJSONURL).read()
               scratchJSON = ScratchReader(rawJSON).parseJSON()
               scratchInfo = JSONinfo(scratchJSON)
               (floatingScripts,sprites) = jsontoSprites(scratchJSON)
               cul = CompCUs(scratchInfo,sprites).parseCUs()
               cug = CUGraph(cul,sprites)
               graphJSstring = str(cug)
            else:
                 projectName = "Problem with file"
                 graphJSstring = "Problem with sb2 file"
                 cul =""
            return render(request, 'main.html',{'filename':projectName,'table':str(cul),'graph':graphJSstring})
    else:
        form = NameForm()
    return render(request, 'home.html',{'form':form}, context_instance = RequestContext(request))

def about(request):
       return render(request, 'about.html')
    

