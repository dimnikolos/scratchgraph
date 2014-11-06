#-*- coding: utf-8 -*-
from ScratchCommands import *

def flattenScripts(myscript):	
	"""
	flattenScripts(myscript)
	a recursive function that flattens a script 
	which is represented by a list of lists of lists
	to a single list
	"""
	script = myscript
	flat = False
	while (flat==False):
		flattenedScript = []
		flat = True
		if (type(script)==list):
			for aScript in script:
				if (type(aScript) == list):
					flat=False
					for aaScript in aScript:
						flattenedScript.append(aaScript)
				else:
					flattenedScript.append(aScript)
		else:
		 	print("Script is not list!")
		 	return(None)
		script = flattenedScript
	return(flattenedScript)



class Sprite():
	"""
	class Sprite
	sprite consists of name and scripts
	"""
	def __init__(self,name):
		self.scripts=[]
		self.name = name
		

	def appendScript(self,script):
		self.scripts.append(script)

	def __str__(self):
		returnString =  self.name + "\n"
		for script in self.scripts:
			returnString += str(script) + "\n"
		return(returnString)


def jsontoSprites(JSONStruct):
	"""
	jsontoSprites(JSONStruct) returns (floatingScripts,spriteList)
	takes the json and returns a list of Sprite objects
	it also returns the number of floatingScripts
	"""

	spriteList = []
	floatingScripts = 0
	if ("scripts" in JSONStruct.keys()):#scripts in the first
										#level of JSON means that
										#the stage has scripts
		spriteList.append(Sprite("stage"))
		for aScript in JSONStruct["scripts"]:
			spriteList[0].appendScript(flattenScripts(aScript[2]))
	
	if ("children" in JSONStruct.keys()):
			for child in JSONStruct["children"]:
				if ("scripts" in child.keys()):
					spriteList.append(Sprite(child["objName"]))
					for aScript in child["scripts"]:
						flatScript = flattenScripts(aScript[2])
						if (flatScript[0] in ScratchCommands().getHatCommands()):
							spriteList[-1].appendScript(flattenScripts(aScript[2]))
						else:
							floatingScripts += 1


	return(floatingScripts,spriteList)


