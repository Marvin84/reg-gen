from PyQt4 import QtGui, QtCore
from Ui_rgtDialog import Ui_Dialog
import webbrowser, os

class rgtCommandDialog(QtGui.QDialog, Ui_Dialog):
  def __init__(self, parent = None):
    QtGui.QDialog.__init__(self, parent)
    self.setupUi(self)

    self.doc = self.plainTextEdit.document()

  def start(self, commandDict):
    # construct command
    self.cmdDict = commandDict
    cmdline = self.constructCommand(commandDict)
    self.doc.setPlainText("$ "+cmdline+"\n")

    # start the process and make sure its output is written to text input
    self.process = QtCore.QProcess(self)
    self.process.readyReadStandardOutput.connect(self.handleOutput)
    self.process.readyReadStandardError.connect(self.handleError)
    self.process.finished.connect(self.processFinished)
    self.process.start(cmdline)

  def handleOutput(self):
    scrollBar = self.plainTextEdit.verticalScrollBar()
    autoScroll = scrollBar.value() == scrollBar.maximum()
    
    processOutput = self.process.readAllStandardOutput()
    self.plainTextEdit.textCursor().insertText(str(processOutput))

    if autoScroll:
      scrollBar.setValue(scrollBar.maximum())

  def handleError(self):
    scrollBar = self.plainTextEdit.verticalScrollBar()
    autoScroll = scrollBar.value() == scrollBar.maximum()

    processOutput = self.process.readAllStandardError()
    self.plainTextEdit.textCursor().insertText(str(processOutput))

    if autoScroll:
      scrollBar.setValue(scrollBar.maximum())

  def processFinished(self):
    resultIndex = os.path.join(self.cmdDict["output"], self.cmdDict["title"], "index.html")
    if os.path.exists(resultIndex):
      webbrowser.open(resultIndex)

  def constructCommand(self, cmdDict):
    key2param = {
        "output":    "-o"
      , "color":     "-c"
      , "column":    "-col"
      , "row":       "-row"
      , "title":     "-t"

      , "groupBy":   "-g"
      , "reference": "-r"
      , "query":     "-q"
    }
    params = []

    # add parameters from cmdDict to params
    for k in cmdDict:
      v = cmdDict[k]

      if k in key2param and v != None:
        params.append(key2param[k]+" "+v)

      elif k == "normalize" and v in ["rows","columns"]:
        params.append("-srow" if v == "rows" else "-scol")

      elif k == "randomization":
        if   cmdDict["mainCmd"] == "jaccard":      params.append("-rt "+str(v))
        elif cmdDict["mainCmd"] == "intersection": params.append("-stest "+str(v))

    # build final command line
    cmd = ""
    if   cmdDict["mainCmd"] == "lineplot":
      cmd = "rgt-viz lineplot "+cmdDict["em"]+" "+" ".join(params)
    elif cmdDict["mainCmd"] == "jaccard" or cmdDict["mainCmd"] == "projection":
      cmd = "rgt-viz "+cmdDict["mainCmd"]+" "+" ".join(params)
    elif cmdDict["mainCmd"] == "intersection":
      cmd = "rgt-viz intersect "+" ".join(params)


    return cmd

  def accept(self):
    self.process.terminate()
    QtGui.QDialog.accept(self)

  def reject(self):
    self.process.terminate()
    QtGui.QDialog.reject(self)