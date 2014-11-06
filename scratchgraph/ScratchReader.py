#-*- coding: utf-8 -*-
import zipfile
import json

class ScratchReader():
    def __init__(self,thefile):
        self.thefile = thefile
        self.projectJSON = [];
        self.projectString = "";
  
    def readfile(self):
        try:
            zfile = zipfile.ZipFile(self.thefile,"r")
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
                

    
    def parseJSON(self):
		self.projectString = self.readfile()
		try:
		    return(json.loads(self.projectString.replace('\t', '').replace('\n','').replace('\r','')))
		except:
	#            print("Not A JSON file?")
		    return(None)
        
    

