#-*- coding: utf-8 -*-
from Sprites import *
from CommUnit import *
from JSONinfo import *
import os.path

class CompCUs():
	"""
	class CompCUs
	a class that is used to compute communication units statistics
	"""
	def __init__(self,JSONInfo,spriteList):
		self.CUCollection = CUCollection()
		self.sprites = spriteList
		self.JI = JSONInfo
		self.globalVarNames = self.JI.getGlobalVarNames()

	def getCUCollectionObject(self):
		return self.CUCollection

	def writeCUReporttoFile(self,filename):
		"""
		writeCUReporttoFile(self,filename)
		writes communication units statistics to a file
		with extension .cur
		Does not include scenes
		"""
		cuVarCount = 0
		cuListCount = 0
		cuMessCount = 0
		numofSprites = len(self.sprites)
		for cu in self.getCUCollectionObject().getCollection():
			if ((len(cu.readers)>0) and (len(cu.writers)>0)):
				#a message/variable must be sent and received to count as a
				#communication unit
				if (cu.readers != cu.writers):
					if (cu.cuType == "variable"):
						cuVarCount += 1
					elif (cu.cuType == "message"):
						cuMessCount += 1
					elif (cu.cuType == "list"):
						cuListCount += 1
		with open(filename + ".cur","a") as f:
			f.write("Number of sprites: %d\n" %(numofSprites))
			f.write("Number of variables: %d\n" % (cuVarCount))
			f.write("Variables as CUs per sprite: %.2f\n"  %(float(cuVarCount) / numofSprites))
			f.write("Number of messages: %d\n" %(cuMessCount))
			f.write("Messages as CUs per sprite: %.2f\n" %(float(cuMessCount) / numofSprites))
			f.write("Number of lists: %d\n" % (cuListCount))
			f.write("Lists as CUs per sprite %.2f\n" %(float(cuListCount) / numofSprites))
			cuCount = cuVarCount + cuMessCount + cuListCount
			f.write("Total CUs: %d\n" %(cuCount))
			f.write("CUs per sprite %.2f\n" %(float(cuCount)/numofSprites))

	def parseCUs(self):
		"""
		parseCUs(self)
		the basic function that computes the communication units
		"""
		for sprite in self.sprites:
			for script in sprite.scripts:
				for (i,expr) in enumerate(script):
					#script is flattened from the function jsontoSprites
					if ((expr == "setVar:to:") or (expr == "changeVar:to:")):
						try:
							#setVar or changevar must be followed by a global variable
							if (script[i+1] in self.globalVarNames):
								self.CUCollection.addWriter(script[i+1],sprite.name,"variable")
						except IndexError:#script[i+1] does not exist!
							pass
					elif (expr == "readVariable"):
						try:
							#readVariable must be followed by a global variable
							if (script[i+1] in self.globalVarNames):
								self.CUCollection.addReader(script[i+1],sprite.name,"variable")
						except IndexError:
							pass
					elif (expr == "broadcast:"):
						try:
							#script[i+1] is the message name and the communication unit name
							self.CUCollection.addWriter(script[i+1],sprite.name,"message")
						except IndexError:
							pass
					elif (expr == "doBroadcastAndWait"):
						try:
							#script[i+1] is the message name and the communication unit name
							self.CUCollection.addWriter(script[i+1],sprite.name,"message",True)
						except IndexError:
							pass
					elif (expr == "whenIReceive"):
						try:
							#script[i+1] is the message name and the communication unit name
							self.CUCollection.addReader(script[i+1],sprite.name,"message")
						except IndexError:
							pass
					elif ((expr == "append:toList:") or (expr == "deleteLine:ofList:") or 
						(expr == "setLine:ofList:to:")):
						try:
							#the structure of the commands is append[item]to[list] 
							#script[i+2] is the list name and the communiction unit name
							self.CUCollection.addWriter(script[i+2],sprite.name,"list")
						except IndexError:
							pass
					elif (expr == "insert:at:ofList:"):
						try:
							#the structure of the command is insert[item]at[pos]oflist[list]
							#script[i+3] is the list name and the communication unit name
							self.CUCollection.addWriter(script[i+3],sprite.name,"list")
						except IndexError:
							pass
					elif (expr == "getLine:ofList:"):
						try:
							#the structure of the command is getLine[linecount]ofList[list]
							#script[i+2] is the list name and the communiction unit name
							self.CUCollection.addReader(script[i+2],sprite.name,"list")
						except IndexError:
							pass
					elif ((expr == "lineCountOfList:") or (expr == "list:contains:")):
						try:
							#linecountoflist[list]
							#list[list]contains[item]
							#script[i+1] is the list name and the communiction unit name
							self.CUCollection.addReader(script[i+1],sprite.name,"list")
						except IndexError:
							pass
					elif ((expr == "startScene") or (expr == "startSceneAndWait")):
						self.CUCollection.addWriter("scene",sprite.name,"scene")
					elif (expr == "whenSceneStarts"):
						self.CUCollection.addReader("scene",sprite.name,"scene")



		return(self.CUCollection)

