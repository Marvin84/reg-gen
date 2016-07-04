from PyQt4 import QtGui
from PyQt4.QtSql import QSqlQueryModel
from Ui_emExportDialog import Ui_Dialog
import dbLayer
import re

class emExportDialog(QtGui.QDialog, Ui_Dialog):
  def __init__(self, parent = None):
    QtGui.QDialog.__init__(self, parent)
    self.setupUi(self)

    # which columns to export to the matrx
    # needs to coincide with dictionary keys returned by getExperimentExport
    self.headerLabels = ["name","type","file","biosource_name","epigenetic_mark","genome","technique","project"]

    # defines which parts of the table contents are replaced by _
    self.escapeExpr = r'[\s,\+\\\/]'
  
  # initializes the table with the selected experiments
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
        , "epigenetic_mark": epigenetic_mark
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


  # handler for accept button click
  def accept(self):
    # ask user which file to save the matrix to
    fname = QtGui.QFileDialog.getSaveFileName(self, 'Save Experimental Matrix')

    # no file selected (canceled)
    if len(fname) == 0:
      return

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

    # close dialog
    QtGui.QDialog.accept(self)


  def setMainApp(self, mainApp):
    self.mainApp = mainApp

  def setSelectedExperiments(self, expIds):
    self.selExpIds = expIds