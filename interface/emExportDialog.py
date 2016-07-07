from PyQt4 import QtGui
from PyQt4.QtSql import QSqlQueryModel
from Ui_emExportDialog import Ui_Dialog
from rgtCommandDialog import rgtCommandDialog
import dbLayer
import re
import os
from functools import partial
import tempfile

class emExportDialog(QtGui.QDialog, Ui_Dialog):
  def __init__(self, parent = None):
    QtGui.QDialog.__init__(self, parent)
    self.setupUi(self)

    # which columns to export to the matrx
    # needs to coincide with dictionary keys returned by getExperimentExport
    # NOTE: epigenetic_mark corresponds to "factor" in RGT terminology
    self.headerLabels = ["name","type","file","factor","biosource_name","genome","technique","project"]
    self.selectableLabels = [                 "factor","biosource_name","genome","technique","project"]

    # defines which parts of the table contents are replaced by _
    self.escapeExpr = r'[\s,\+\\\/]'

    # initialize rgt run dialog
    self.rgtCommandDialog = rgtCommandDialog(self)

    # initialize combo boxes
    self.groupBy.addItems(self.selectableLabels)
    self.column.addItems(self.selectableLabels)
    self.row.addItems(self.selectableLabels)
    self.color.addItems(self.selectableLabels)

    # bind signal handlers
    self.exportButton.clicked.connect(self.exportButtonHandler)    

    self.WhereBrowserLineplot.clicked.connect(partial(self.fileDialog, lineEdit=self.WhereLineplot, title='Select Result Directory', directory=True))
    self.WhereBrowserTests.clicked.connect(partial(self.fileDialog, lineEdit=self.WhereTests, title='Select Result Directory', directory=True))
    self.inputBrowser.clicked.connect(partial(self.fileDialog, lineEdit=self.input, title='Select Experimental Matrix', directory=False, open=True))

    self.runTests.clicked.connect(self.startTests)
    self.runLineplot.clicked.connect(self.startLineplot)

  
  # initializes the table with the selected experiments from main window
  def initTable(self):

    # builds experiment dictionary from data
    def getExperimentExport(record):
      biosource_name  = re.sub(self.escapeExpr, '_', str(record.value("bs.biosource_name").toString()))
      epigenetic_mark = re.sub(self.escapeExpr, '_', str(record.value("e.epigenetic_mark").toString()))
      project         = re.sub(self.escapeExpr, '_', str(record.value("e.project").toString()))
      genome          = re.sub(self.escapeExpr, '_', str(record.value("e.genome").toString()))
      technique       = re.sub(self.escapeExpr, '_', str(record.value("e.technique").toString()))
      tpe             = "regions" if str(record.value("e.data_type").toString())=="peaks" else "reads"

      name = biosource_name+"__"+epigenetic_mark+"__"+tpe

      # build file url depending on experiment project
      if project == 'ENCODE':
        fname = str(record.value("encode_url").toString())
      elif project == 'BLUEPRINT_Epigenome':
        fname = "ftp://ftp.ebi.ac.uk/pub/databases/" + str(record.value("blueprint_url").toString())
      elif project == 'Roadmap_Epigenomics':
        fname = str(record.value("roadmap_url").toString())
      else:
        fname = "[UNKNOWN PROJECT]"

      # return dictionary indexed by header labels (see above)
      return { 
          "name": name
        , "type": tpe
        , "file": fname
        , "factor": epigenetic_mark
        , "biosource_name": biosource_name
        , "genome": genome
        , "technique": technique
        , "project": project
      }

    # load experimental data from database
    self.exportModel = QSqlQueryModel()
    self.exportModel.setQuery(dbLayer.getSelectedExpForExportSql(self.selExpIds)+dbLayer.sortSql(self.mainApp.ui.dataTableSelected.horizontalHeader()), self.mainApp.db)
    exportRows = self.exportModel.rowCount()

    # prepare table
    self.emExport.clear()
    self.emExport.setColumnCount(len(self.headerLabels))
    self.emExport.setRowCount(exportRows)
    self.emExport.setHorizontalHeaderLabels(self.headerLabels)

    # insert experiments into table
    exps = [getExperimentExport(self.exportModel.record(i)) for i in range(0, exportRows)]
    for i, exp in enumerate(exps):
      withSameName = 1

      # check following experiments for ones with same name
      for j in range(i+1,len(exps)):
        if exp["name"] == exps[j]["name"]:
          # rename replicate
          withSameName += 1
          exps[j]["name"] += "_"+str(withSameName)

      # there is another one with same name -> rename first one
      if withSameName > 1:
        exp["name"] += "_1"

      # insert current experiment into table
      for j, key in enumerate(self.headerLabels): 
        newitem = QtGui.QTableWidgetItem(exp[key])
        self.emExport.setItem(i, j, newitem)

    # finalize table
    self.emExport.resizeColumnsToContents()
    self.emExport.resizeRowsToContents()
    self.emExport.show()


  # browse file or directory location
  def fileDialog(self, lineEdit=None, title='', open=False, directory=False):
    # open or save? directoy or file?
    if not directory:
      dialogFunc = QtGui.QFileDialog.getSaveFileName if not open else QtGui.QFileDialog.getOpenFileName
    else:
      dialogFunc = QtGui.QFileDialog.getExistingDirectory

    # default title
    if title == '':
      title = 'Save as...' if not open else 'Open...'

    # already path given in lineEdit?
    if lineEdit != None:
      path = str(lineEdit.text())
    else:
      path = ''

    # open file dialog
    selectedPath = dialogFunc(self, title, path)

    # user actually selected something -> update lineEdit (if any) or return selected path
    if lineEdit != None:
      if selectedPath != '':
        lineEdit.setText(selectedPath)
    else:
      return selectedPath


  # handler for export button click
  def exportButtonHandler(self):
    fname = self.fileDialog(title='Save Experimental Matrix', open=False, directory=False)

    # no file selected (canceled)
    if len(fname) == 0:
      return

    self.saveEMTableToFile(fname)


  # write the current content of the experimental matrix table to given file name
  def saveEMTableToFile(self,fname):
    # write header to selected file
    expMatrix = open(fname, 'w')
    expMatrix.write("\t".join(self.headerLabels)+"\n")

    # export matrix entries
    for r in range(0, self.emExport.rowCount()):
      row = []
      for c in range(0, len(self.headerLabels)):
        row.append(str(self.emExport.item(r,c).text()))
      expMatrix.write("\t".join(row)+"\n")

    expMatrix.close()

  def startLineplot(self):
    # save experimental matrix to temporary file
    temp_file = os.path.join(tempfile.mkdtemp(), "export.em")
    self.saveEMTableToFile(temp_file)

    cmdDict = {
        "mainCmd":   "lineplot"
      , "em":        temp_file
      , "title":     "Lineplot"
      , "output":    str(self.WhereLineplot.text())
      , "normalize": None if str(self.normalization.currentText()) == "None" else str(self.normalization.currentText()).lower()
      , "row":       None if str(self.row.currentText()) == "None" else str(self.row.currentText()).lower()
      , "column":    None if str(self.column.currentText()) == "None" else str(self.column.currentText()).lower()
      , "color":     None if str(self.color.currentText()) == "None" else str(self.color.currentText()).lower()
    }

    self.rgtCommandDialog.show()
    self.rgtCommandDialog.start(cmdDict)


  def startTests(self):
    # save experimental matrix to temporary file
    temp_file = os.path.join(tempfile.mkdtemp(), "export.em")
    self.saveEMTableToFile(temp_file)

    cmdDict = {
        "mainCmd":       str(self.testType.currentText()).lower()
      , "title":         str(self.testType.currentText())
      , "output":        str(self.WhereTests.text())
      , "groupBy":       str(self.groupBy.currentText()).lower()
      , "randomization": self.randomization.value()
    }

    # which matrix is which?
    inputType = str(self.inputType.currentText()).lower()
    if inputType == "reference":
      cmdDict["reference"] = str(self.input.text())
      cmdDict["query"] = temp_file
    else:
      cmdDict["reference"] = temp_file
      cmdDict["query"] = str(self.input.text())

    self.rgtCommandDialog.show()
    self.rgtCommandDialog.start(cmdDict)


  def setMainApp(self, mainApp):
    self.mainApp = mainApp

  def setSelectedExperiments(self, expIds):
    self.selExpIds = expIds