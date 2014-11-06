#-*- coding: utf-8 -*-
class JSONinfo():
	"""
	class JSONinfo
	reads the info section of the project.json and
	returns info
	"""
	def __init__(self,JSONstruct):
		self.JSONstruct = JSONstruct

	def getProjectID(self):
		if ("projectID" in self.JSONstruct["info"].keys()):
			return(self.JSONstruct["info"]["projectID"])
		else:
			return(None)

	def getSpriteCount(self):
		if ("scripts" in self.JSONstruct.keys()):
			return(self.JSONstruct["info"]["spriteCount"]+1)
		else:
			return(self.JSONstruct["info"]["spriteCount"])


	def getScriptCount(self):
		return(self.JSONstruct["info"]["scriptCount"])

	def getGlobalVarCount(self):
		if ("variables" in self.JSONstruct.keys()):
			return(len(self.JSONstruct["variables"]))
		else:
			return(0)

	def getListCount(self):
		if ("lists" in self.JSONstruct.keys()):
			return(len(self.JSONstruct["lists"]))
		else:
			return(0)

	def getLocalVarCount(self):
		localVarCount = 0
		for child in self.JSONstruct["children"]:
			if ("variables" in child.keys()):
				localVarCount += len(child["variables"])
		return(localVarCount)

	def getVarCount(self):
		return(self.getLocalVarCount() + self.getGlobalVarCount())

	def getLocalVarNames(self):
		localVarNames = []
		for child in self.JSONstruct["children"]:
			if ("variables" in child.keys()):
				for aVar in child["variables"]:
					#local var name is SpriteName + [space] + VarName e.g. "Sprite1 position"
					localVarNames.append(child["objName"] + " " + aVar["name"])
		return(localVarNames)

	def getGlobalVarNames(self):
		globalVarNames = []
		if ("variables" in self.JSONstruct.keys()):
			for aVar in self.JSONstruct["variables"]:
				globalVarNames.append(aVar["name"])
		return(globalVarNames)

	def getVarNames(self):
		return(self.getGlobalVarNames.append(self.getLocalVarNames()))








