from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django import forms
from django.template import RequestContext
from django.core.context_processors import csrf
from django.utils.safestring import mark_safe
from .models import Greeting
import urllib2


from ScratchReader import *
from JSONinfo import *
from Sprites import *
from CompCUs import *
from CUGraph import *

class NameForm(forms.Form):
  project_url = forms.CharField(max_length=220,
                label=mark_safe("Project url:<br/>"))
  your_file = forms.FileField(label=mark_safe("<br/><br/>OR<br/><br/>"
                "Upload Scratch 2.0 project (.sb2 file)<br/>"))
def index(request):
  urlproblem = False
  fileproblem = False
  c = {}
  c.update(csrf(request))
  if request.method == 'POST':
    form = NameForm(request.POST,label_suffix='')
    if 'project_url' in request.POST.keys():
        project_url = request.POST['project_url']
		#leading spaces (useful for mobile pastes)
        project_url = project_url.lstrip()
        if project_url.startswith('http://scratch.mit.edu/projects/'):
          if project_url.endswith('#editor'):
            project_url = project_url[:-7]
          if project_url.endswith('/'):
            project_url = project_url[:-1]
          project_id = project_url[32:]
          projectName = project_id
          scratchJSONURL = ("http://projects.scratch.mit.edu/"
		                   "internalapi/project/") + project_id + "/get/"
          rawJSON = urllib2.urlopen(scratchJSONURL).read()
          if (rawJSON):
            scratchJSON = ScratchReader(rawJSON).parseJSON()
          else:
            urlproblem = True
        else:
            urlproblem = True
    else:
        urlproblem = True
    if urlproblem:
            if 'your_file' in request.FILES.keys():
                project_file = request.FILES['your_file']
                projectName = project_file.name
                scratchJSON = ScratchReader(project_file,isFile=True).\
                              parseJSON()
            else:
                fileproblem = True
            if fileproblem:
              projectName = "Problem with file"
              cul = ""
              cug = ""
              graphJSstring = ""
    if (not (fileproblem and urlproblem)):
      scratchInfo = JSONinfo(scratchJSON)
      (floatingScripts,sprites) = jsontoSprites(scratchJSON)
      cul = CompCUs(scratchInfo,sprites).parseCUs()
      cug = CUGraph(cul,sprites)
      graphJSstring = str(cug)
    return render(request, 'main.html',{'filename':projectName,'table':str(cul),
                  'graph':graphJSstring})
  else:
    form = NameForm(label_suffix='')
    return render(request, 'home.html',{'form':form},
	              context_instance = RequestContext(request))

def about(request):
       return render(request, 'about.html')
