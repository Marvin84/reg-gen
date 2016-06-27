from PyQt4 import QtCore, QtGui
from PyQt4.QtSql import QSqlQueryModel
from Ui_emExportDialog import Ui_Dialog
import dbLayer
import re

class emExportDialog(QtGui.QDialog, Ui_Dialog):
  def __init__(self, parent = None):
    QtGui.QDialog.__init__(self, parent)
    self.setupUi(self)
    self.headerLabels = ["name","type","file"]
      
  def setMainApp(self, mainApp):
    self.mainApp = mainApp

  def setSelectedExperiments(self, expIds):
    self.selExpIds = expIds

  def initTable(self):
    def addExperimentToTable(record):
      # build experiment name from cell name, epigenetic mark and data type (regions/reads)
      name = re.sub(r'[\s,\+\\\/]', '_', str(record.value("bs.biosource_name").toString()))
      name += "__"+re.sub(r'[\s,\+\\\/]', '_', str(record.value("e.epigenetic_mark").toString()))
      tpe = "regions" if str(record.value("e.data_type").toString())=="peaks" else "reads"
      name += "__"+tpe

      # build file url depending on experiment project
      project = str(record.value("e.project").toString())
      if project == 'ENCODE':
        fname = str(record.value("encode_url").toString())
      elif project == 'BLUEPRINT Epigenome':
        fname = "ftp://ftp.ebi.ac.uk/pub/databases/" + str(record.value("blueprint_url").toString())
      elif project == 'Roadmap Epigenomics':
        fname = str(record.value("roadmap_url").toString())
      else:
        fname = "[UNKNOWN PROJECT]"

      return (name,tpe,fname)

    # load experimental data from database
    self.exportModel = QSqlQueryModel()
    self.exportModel.setQuery(dbLayer.getSelectedExpForExportSql(self.selExpIds)+dbLayer.sortSelectedSql(self.mainApp.ui), self.mainApp.db)
    exportRows = self.exportModel.rowCount()

    # insert into table
    self.emExport.clear()
  
    self.emExport.setColumnCount(len(self.headerLabels))
    self.emExport.setRowCount(exportRows)

    self.emExport.setHorizontalHeaderLabels(self.headerLabels)
    for i in range(0, exportRows):
      res = addExperimentToTable(self.exportModel.record(i))

      for j, content in enumerate(res): 
        newitem = QtGui.QTableWidgetItem(content)
        self.emExport.setItem(i, j, newitem)

    self.emExport.resizeColumnsToContents()
    self.emExport.resizeRowsToContents()
    self.emExport.show()


  def accept(self):
    # ask user which file to save the matrix to
    fname = QtGui.QFileDialog.getOpenFileName(self, 'Save Experimental Matrix', '/home')

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

    QtGui.QDialog.accept(self)