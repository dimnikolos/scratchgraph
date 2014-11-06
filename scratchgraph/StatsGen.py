#-*- coding: utf-8 -*-
import collections
from CommUnit import *
from JSONinfo import *
from Sprites  import *
from ScratchCommands import *


class StatsGen():
	"""
	class StatsGen
	a class that is used to write the csv file
	of the command appearances in the project
	"""
	def __init__(self,JSONinfo,spriteList,numofFloatingScripts):
		self.JI = JSONinfo
		self.sc = ScratchCommands()
		self.scriptIDcount = 0
		self.CUs = []
		self.floatingScripts = numofFloatingScripts
		self.sprites = spriteList
		self.catCounter = collections.Counter()
		self.commandCounter = collections.Counter()
		self.numofLocalVars = 0
		self.numofGlobalVars = 0
		self.numofVars = 0
		self.countVars()
		self.countCommands()
		#the delimeter is used for the csv file
		self.delimeter = ";"

	def countGlobalVars(self):
		globalVars = 0
		for aVar in self.JI.getGlobalVarNames():
			globalVars+=1
		self.numofGlobalVars = globalVars

	def countLocalVars(self):
		localVars = 0
		for aVar in self.JI.getLocalVarNames():
			localVars += 1
		self.numofLocalVars = localVars

	def countVars(self):
		self.countGlobalVars()
		self.countLocalVars()
		self.numofVars = self.numofLocalVars + self.numofGlobalVars

	def countCommands(self):
		CUList = []
		for sprite in self.sprites:
			for script in sprite.scripts:
				for expr in script:
					if (expr in self.sc.allCommands):
						self.commandCounter[expr] += 1
						#search category of command
						notinCat = True
						for cat in self.sc.catNames:
							if expr in self.sc.catCommands[cat]:
								self.catCounter[cat] += 1
								notinCat = False
						if (notinCat):
							print("%s command not in any category!") % (expr)

	def getVarCount(self):
		return(self.numofVars)

	def getLocalVarCount(self):
		return(self.numofLocalVars)

	def getGlobalVarCount(self):
		return(self.numofGlobalVars)

	def getCommandStats(self):
		return(self.commandCounter)

	def getCategoryStats(self):
		return(self.catCounter)

	def setCSVDelimeter(self,delimeter):
		self.delimeter = delimeter

	def writeStatstoCSV(self,filename):
		csvname = filename + ".csv"
		with open(csvname, 'wb') as f:
			line = "%s%s%s\n" %("Command Name or Category",self.delimeter,"Number of appearances")
			f.write(line)
			f.write("-" * 30 + "\n")
			for cat in self.sc.catNames:
				line = "%s%s%s\n" % (cat,self.delimeter,self.catCounter[cat])
				f.write(line)				
			for cat in self.sc.catNames:
				f.write("-" * 30 + "\n")
				for command in self.sc.catCommands[cat]:
					line = "%s%s%s\n" % (command,self.delimeter,self.commandCounter[command])
					f.write(line)
				f.write("-" * 30 + "\n")
			f.write("Number of floating scripts %s %d" % (self.delimeter,self.floatingScripts))
			

	def showStatsonScreen(self):
		for cat in sorted(self.catCounter.keys()):
			print("%s:%s") % (cat,self.catCounter[cat])
		print "-" * 30
		for command in sorted(self.commandCounter.keys()):
			print("%s:%s") % (command,self.commandCounter[command])
		print "-" * 30
		print("Number of floating scripts %s %d" % (self.delimeter,self.floatingScripts))





