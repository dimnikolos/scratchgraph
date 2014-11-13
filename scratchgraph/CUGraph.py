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
	def strgraphEdges(self):
		"""
		strgraphEdges(self)
                returns the edges string for js lib
		"""
		
		returnstr = ""
                for cu in self.CUCollection.getCollection():
                    if (cu.cuType == "variable"):
                       for aWriter in cu.getWriters():
			   returnstr += 'g.addEdge("' + unidecode(aWriter) + '","' + unidecode("var\\n"+cu.getName()) + '",{directed:true});\n' 
                       for aReader in cu.getReaders():
			   returnstr += 'g.addEdge("' + unidecode("var\\n"+cu.getName()) + '","' + unidecode(aReader) + '",{directed:true});\n' 
                    elif (cu.cuType == "list"):
                       for aWriter in cu.getWriters():
			   returnstr += 'g.addEdge("' + unidecode(aWriter) + '","' + unidecode("list\\n"+cu.getName()) + '",{directed:true});\n' 
                       for aReader in cu.getReaders():
			   returnstr += 'g.addEdge("' + unidecode("list\\n"+cu.getName()) + '","' + unidecode(aReader) + '",{directed:true});\n' 
                    elif (cu.cuType == "scene"):
                       for aWriter in cu.getWriters():
			   returnstr += 'g.addEdge("' + unidecode(aWriter) + '","' + unidecode("THE SCENE") + '",{directed:true});\n' 
                       for aReader in cu.getReaders():
			   returnstr += 'g.addEdge("' + unidecode("THE SCENE") + '","' + unidecode(aReader) + '",{directed:true});\n' 
                    elif (cu.cuType == "message"):
                       for aWriter in cu.getWriters():
                           for aReader in cu.getReaders():
			       returnstr += 'g.addEdge("' + unidecode(aWriter) + '","' + unidecode(aReader) + '",{directed:true, label: "' + unidecode(cu.getName()) + '"});\n' 
                    else:
                      returnstr = "Problem"
                      break
		return returnstr
	
	def __str__(self):
                returnstr = "var g = new Graph();\n"
                returnstr += self.strgraphEdges()
                returnstr += """ 
                    var layouter = new Graph.Layout.Spring(g);\n
                    layouter.layout();\n
                    var renderer = new Graph.Renderer.Raphael('canvas', g, 800, 600);\n
                    renderer.draw();\n
                    """
                return returnstr
