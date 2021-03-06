import sys
import JSONinfo

class Writer:
  """
  a Writer is a sprite that writes to the communication unit
  it either broadcasts a message or writes on a variable/list
  the class is used to distinct the simple broadcast from
  broadcast and wait
  """
  def __init__(self,writerName,wait=False):
    self.writerName = writerName
    self.wait = wait

  def __unicode__(self):
    if (self.wait):
      return(self.writerName + u"*")
    else:
      return(self.writerName)

class CommUnit:
  """CommUnit is a communication unit it is a variable, a message or a list
  with readers and writers
  """
  def __init__(self,cuName,cuType):
    if (cuType=="variable" or cuType == "list" or cuType == "message" or cuType == "scene"):
      self.cuName = cuName
      self.cuType = cuType
      self.writers = []
      self.readers = []
    else:
      return(None)
  def getCUType(self):
    return(self.cuType)
  def getName(self):
    return(self.cuName)
  def addWriter(self,writerObj):
    """
    addWriter(self,writerObj)
    adds a writer to the CU
    must be an instance of class Writer
    """
    #if not already in list put writerObj in list of writers
    if (writerObj.writerName not in [awriter.writerName for awriter
      in self.writers]):
      self.writers.append(writerObj)
  def addReader(self,objName):
    """
    addReader(self,objName)
    adds a reader to the CU
    readers are strings
    """
    if (objName not in self.readers):
      self.readers.append(objName)
  def getNumofWriters(self):
    return(len(self.writers))
  def getNumofWriterswithWait(self):
    """
    getNumofWriterswithWait(self)
    get the number of sprites that broadcast
    the message with broadcastandwait
    """
    returnNum = 0
    for writer in self.writers:
      if (writer.wait):
        returnNum += 1
    return(returnNum)

  def getNumofWriterswithoutWait(self):
    """
    getNumofWriterswithoutWait(self)
    get the number of sprites that
    broadcast the message with
    simple broadcast
    """
    return(self.getNumofWriters()-self.getNumofWriterswithWait())
  def getNumofReaders(self):
    return(len(self.readers))
  def getReaders(self):
    return(self.readers)
  def getWriters(self):
    return([w.writerName for w in self.writers])
  def __unicode__(self):
    """
    __unicode__(self)
    a string report of a cu
    it produces the following
    cuName
    ------------------
    readers: sprite1,sprite2
    writers: sprite3,sprite4*
    * means that a sprite used broadcastandwait and it
    is only used in messages
    """
    returnString = ""
    if (self.cuType == "message"):
      returnString = u"<tr><td><b>" + self.cuType + ": " + self.cuName + u"</b><br/>" + u"Receivers: "
    else:
      returnString = u"<tr><td><b>" + self.cuType + ": " + self.cuName + u"</b><br/>" + u"Readers: "
    returnString += ','.join(self.readers)
    if (self.cuType == "message"):
      returnString += u"<br/>Senders: "
    else:
      returnString += u"<br/>Writers: "
    returnString += ','.join([unicode(writer) for writer in self.writers])
    returnString += "</td></tr>"
    return(returnString)
class CUCollection():
  """
  CUCollection is the collection of CUs in the project
  """
  def __init__(self):
    self.collection = []
  def getCollection(self):
    return(self.collection)
  def addCU(self,CU):
    self.collection.append(CU)
  def getCUID(self,CUName,CUType):
    """
    getCUID(self,CUName,CUType):
    get index of CUCollection using CUType and CUName
    both name and type are used because a variable can have
    the same name with a message or a list
    """
    for (i,CU) in enumerate(self.collection):
      if ((CU.cuName == CUName) and (CU.cuType == CUType)):
        return(i)
    return(None)
  def addWriter(self,CUName,spriteName,CUType,wait=False):
    """
    addWriter(self,CUName,spriteName,CUType,wait=False)
    adds a writer directly to the CUCollection
    writer must be of class Writer
    """
    CUID = self.getCUID(CUName,CUType)
    #if it is it may be already in the list
    if (CUID is not None): #if it is add a writer
      self.collection[CUID].addWriter(Writer(spriteName))
    else:
      #if it is not create a new communication unit
      #add writer and add the new communication unit
      #to the collection
      newCU = CommUnit(CUName,CUType)
      newCU.addWriter(Writer(spriteName,wait))
      self.addCU(newCU)

  def addReader(self,CUName,spriteName,CUType):
    """
    addReader(self,CUName,spriteName,CUType)
    adds a reader directly to the CU in the
    CUCollection
    """
    CUID = self.getCUID(CUName,CUType)
    #if it is it may be already in the list
    if (CUID is not None): #if it is add a reader
      self.collection[CUID].addReader(spriteName)
    else: #if it is not create a new communication unit
      newCU = CommUnit(CUName,CUType)
      newCU.addReader(spriteName)
      self.addCU(newCU)
  def __unicode__(self):
    """
    __unicode__(self)
    a report of all communication units in the collection
    """
    returnString = "<table width='70%' border='1'>"
    for cu in self.collection:
      returnString += unicode(cu)
    returnString += "</table>"
    return(returnString)

  def __str__(self):
    """
    __str__(self)
    encodes the report to utf8
    """
    return unicode(self).encode('utf8')

  def writeCUStoFile(self,baseName):
    """
    writeCUStoFile(self,baseName)
    writes the detailed report of communication units
    to a file with .cus extension
    """
    with open(baseName+".cur",'w') as f:
      f.write(str(self))
