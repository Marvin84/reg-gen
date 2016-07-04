from PyQt4 import QtGui, QtCore
from Ui_rgtDialog import Ui_Dialog

class rgtCommandDialog(QtGui.QDialog, Ui_Dialog):
  def __init__(self, parent = None):
    QtGui.QDialog.__init__(self, parent)
    self.setupUi(self) 

    self.doc = self.plainTextEdit.document()

  def setMainApp(self, mainApp):
    self.mainApp = mainApp

  def start(self):
    # construct command
    cmdline = self.constructCommand()
    self.doc.setPlainText("$ "+cmdline+"\n")

    # start the process and make sure its output is written to text input
    self.process = QtCore.QProcess(self)
    self.process.readyReadStandardOutput.connect(self.handleOutput)
    self.process.readyReadStandardError.connect(self.handleError)
    self.process.start(cmdline)

  def handleOutput(self):
    processOutput = self.process.readAllStandardOutput()
    self.doc.setPlainText(str(self.doc.toPlainText()) + str(processOutput))

  def handleError(self):
    processOutput = self.process.readAllStandardError()
    self.doc.setPlainText(str(self.doc.toPlainText()) + str(processOutput))


  def constructCommand(self):
    return "ping google.com"