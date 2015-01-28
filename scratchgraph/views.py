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

class FileForm(forms.Form):
   your_file = forms.FileField()

def index(request):
    problem = False
    c = {}
    c.update(csrf(request))
    if request.method == 'POST':
        form1 = NameForm(request.POST, prefix = 'url')
        form2 = FileForm(request.POST, prefix = 'file')
        if 'URLSubmit' in request.POST:
            project_url = request.POST['url-project_url']
            project_url = project_url.lstrip() #leading spaces (useful for mobile pastes)
            if project_url.startswith('http://scratch.mit.edu/projects/'):
               if project_url.endswith('#editor'):
                  project_url = project_url[:-7]
               if project_url.endswith('/'):
                  project_url = project_url[:-1]
               project_id = project_url[32:]
               projectName = project_id
               scratchJSONURL = "http://projects.scratch.mit.edu/internalapi/project/" + project_id + "/get/"
               rawJSON = urllib2.urlopen(scratchJSONURL).read()
               if (rawJSON):
                 scratchJSON = ScratchReader(rawJSON).parseJSON()
               else:
                 problem = True
            else:
              problem = True
        elif 'FileSubmit' in request.POST:
            project_file = request.FILES['file-your_file']
            projectName = project_file.name
            scratchJSON = ScratchReader(project_file,isFile=True).parseJSON()
        else:
            problem = True
        if problem:
          projectName = "Problem with file"
          cul = ""
          cug = ""
          graphJSstring = ""
        else:	
          scratchInfo = JSONinfo(scratchJSON)
          (floatingScripts,sprites) = jsontoSprites(scratchJSON)
          cul = CompCUs(scratchInfo,sprites).parseCUs()
          cug = CUGraph(cul,sprites)
          graphJSstring = str(cug)
        return render(request, 'main.html',{'filename':projectName,'table':str(cul),'graph':graphJSstring})
    else:
        form1 = NameForm(prefix = 'url')
        form2 = FileForm(prefix = 'file')
    return render(request, 'home.html',{'form1':form1,'form2':form2}, context_instance = RequestContext(request))

def about(request):
       return render(request, 'about.html')
    

