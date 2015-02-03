#-*- coding: utf-8 -*-
import zipfile
import json

class ScratchReader():
  def __init__(self,JSONOrFileName,isFile = False):
    if (isFile):
      self.thejson = self.readfile(JSONOrFileName)
    else:
      self.thejson = JSONOrFileName

  def parseJSON(self):
    try:
      return(json.loads(self.thejson.replace('\t', '').replace('\n','').replace('\r','')))
    except:
      return(None)


  def readfile(self,fileName):
    try:
      zfile = zipfile.ZipFile(fileName,"r")
    except:
      return None
    try:
      zfile.extract("project.json",path = "/tmp/")
    except:
      return None
    try:
      f = open('/tmp/project.json')
      return(f.read().decode('utf-8'))
    except:
      return None
