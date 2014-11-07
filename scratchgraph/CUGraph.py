#-*- coding: utf-8 -*-
from unidecode import unidecode
from Sprites import *


class CUGraph():
	"""
	class CUGraph is a class
	that is used to create
	graph of communication units
	"""
	def __init__(self,CUCollection,spriteList):
		self.CUCollection = CUCollection
		#nameList is a list of the names of the sprites
		#it is used to get a consistent index of a sprite
		self.nameList = [sp.name for sp in spriteList]
		self.spritesNumber = len(spriteList)
		self.nameList.extend([cu.getName() for cu in self.CUCollection.getCollection()])

	def graphEdges(self,cuType,cuAsNode = False):
		"""
		graphEdges(self,cuType)
		returns list of tuples
		to be used for graphs
		"""
		
		edges = []
		if (cuAsNode):
			
			for cu in self.CUCollection.getCollection():
				#cuType filters the communication units
				#according to type
				if (cu.getCUType() == cuType):
					for aWriter in cu.getWriters():
						edges.append((unidecode(aWriter),unidecode(cu.getName())))
					for aReader in cu.getReaders():
						edges.append((unidecode(cu.getName()),unidecode(aReader)))
		else:
			for cu in self.CUCollection.getCollection():
				#cuType filters the communication units
				#according to the type
				if (cu.getCUType() == cuType):
					for aReader in cu.getReaders():
						for aWriter in cu.getWriters():
							#do not remove duplicates
							#if ((self.nameList.index(aReader),self.nameList.index(aWriter)) not in edges):
								edges.append((unidecode(aWriter),unidecode(aReader)))
		return edges
	
	def __str__(self):
            #allEdges is consists of edges from variables/messages/lists
	    allEdges = self.graphEdges("variable",True)
	    #REMOVE DUPLICATES
            #allEdges.extend([edge for edge in self.graphEdges("list") if edge not in allEdges])
            #allEdges.extend([edge for edge in self.graphEdges("message") if edge not in allEdges])
            #allEdges.extend([edge for edge in self.graphEdges("scene",True) if edge not in allEdges])
            #ALLOW DUPLICATES
            allEdges.extend([edge for edge in self.graphEdges("list",True)])
            allEdges.extend([edge for edge in self.graphEdges("message",False)])
            allEdges.extend([edge for edge in self.graphEdges("scene",True)])
            if (len(allEdges)>0):
                returnstr = "var g = new Graph();\n"
                for anEdge in allEdges:
                    returnstr += 'g.addEdge("' + str(anEdge[0])+ '","' + str(anEdge[1]) + '",{directed:true});\n'
                returnstr += """ 
                    var layouter = new Graph.Layout.Spring(g);\n
                    layouter.layout();\n
                    var renderer = new Graph.Renderer.Raphael('canvas', g, 800, 600);\n
                    renderer.draw();\n
                    """
            else:
                returnstr = 'document.write("No communications");\n'
            return returnstr
