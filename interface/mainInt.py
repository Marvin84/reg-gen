import sys
from PyQt4 import QtCore, QtSql, QtGui
from PyQt4.QtSql import QSqlQueryModel,QSqlDatabase,QSqlQuery
from design import Ui_Form
import dbLayer
import re

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

def connectDB():
  db = QtSql.QSqlDatabase.addDatabase('QSQLITE')
  db.setDatabaseName('deepBlue.db')
  ok = db.open()
	
  if ok == False:
    QtGui.QMessageBox.critical(None, QtGui.qApp.tr("Cannot open database"),
    QtGui.qApp.tr("Unable to establish a database connection."),
    QtGui.QMessageBox.Cancel)		
    return False

  return db


selectedExperimentIds = []
class Gui(QtGui.QWidget):
  def __init__(self, parent = None):
    super(Gui, self).__init__(parent)
    self.ui = Ui_Form()
    self.ui.setupUi(self)
    ui = self.ui


    db = connectDB()

    # bind data query to table
    experimentsModel = QSqlQueryModel()
    experimentsModel.setQuery(dbLayer.getDataSql()+dbLayer.buildSqlWhere(self.ui),db)
    dataColumns = experimentsModel.columnCount()

    experimentsView = self.ui.dataTable
    experimentsView.setModel(experimentsModel)
    for i in range(2, dataColumns):
      experimentsView.resizeColumnToContents(i)

    experimentsView.setColumnHidden(0,True) # hide experiment id
    experimentsView.show()
    self.dataTableSelectionModel = experimentsView.selectionModel()


    # bind sql query for genome and project selectors
    genomeModel = QSqlQueryModel()
    genomeModel.setQuery(dbLayer.getGenomesSql(),db)
    self.ui.comboBoxGenome.setModel(genomeModel)

    projectsModel = QSqlQueryModel()
    projectsModel.setQuery(dbLayer.getProjectsSql(),db)
    self.ui.comboBoxProject.setModel(projectsModel)


    # bind sql model for extra data selector
    extraDataModel = QSqlQueryModel()
    self.ui.tableViewMeta.setModel(extraDataModel)


    # bind sql model for selected experiments
    selectedExpModel = QSqlQueryModel()
    selectedExpModel.setQuery(dbLayer.getSelectedExpSql(selectedExperimentIds), db)
    selectionColumns = selectedExpModel.columnCount()

    selectedExpView = self.ui.dataTableSelected
    selectedExpView.setModel(selectedExpModel)
    selectedExpView.setColumnHidden(0,True)

    for i in range(2, selectionColumns):
      columnWidth = experimentsView.columnWidth(i)
      selectedExpView.setColumnWidth(i, columnWidth)

    # sql model for exporting selected experiments
    exportModel = QSqlQueryModel()

    # on any change of the filter inputs, just update the data sql model
    # TODO: maybe be more efficient to let the table perform the sorting instead of the database?
    def onFilterInputChange(content):
      experimentsModel.setQuery(dbLayer.getDataSql()+dbLayer.buildSqlWhere(self.ui)+dbLayer.sortSql(self.ui),db)

    def onDataInputChangeSelected(content):
      selectedExpModel.setQuery(dbLayer.getSelectedExpSql(selectedExperimentIds)+dbLayer.sortSelectedSql(self.ui), db)

    def onExperimentSelect(selected, deselected):
      indexes = self.dataTableSelectionModel.selectedRows()
      if len(indexes) == 1:
        record = experimentsModel.record(indexes[0].row())
        experiment_id = record.value("experiment_id").toString()
        extraDataModel.setQuery(dbLayer.getAdditionalDataSql(experiment_id),db)
        self.ui.tableViewMeta.setColumnHidden(0,True)
      else:
        extraDataModel.clear()
        # TODO: table does not clear itself?   	

    def expDoubleClicked(index):
      #print("You Double Clicked: "+index.data().toString())
      #print("In row: \n"+str(index.row()))

      record = experimentsModel.record(index.row())
      experiment_id = record.value("experiment_id").toString()
      selectedExperimentIds.append(str(experiment_id))
      selectedExpModel.setQuery(dbLayer.getSelectedExpSql(selectedExperimentIds)+dbLayer.sortSelectedSql(self.ui), db)

    def selExpDoubleClicked(index):
      record = selectedExpModel.record(index.row())
      experiment_id = record.value("experiment_id").toString()
      selectedExperimentIds.remove(str(experiment_id))
      selectedExpModel.setQuery(dbLayer.getSelectedExpSql(selectedExperimentIds)+dbLayer.sortSelectedSql(self.ui), db)
    
    def addColumns():
      indexes = self.dataTableSelectionModel.selectedRows()
      if len(indexes) > 0:
	rows = sorted(set(index.row() for index in
                      self.ui.dataTable.selectedIndexes()))           	
	for i in range(0, len(rows)):
	  record = experimentsModel.record(indexes[i].row())
      	  experiment_id = record.value("experiment_id").toString()
	  selectedExperimentIds.append(str(experiment_id))
      	  selectedExpModel.setQuery(dbLayer.getSelectedExpSql(selectedExperimentIds)+dbLayer.sortSelectedSql(self.ui), db)
      else: 
	print("Select a dataset")


    def clearComboBoxes():
      self.ui.comboBoxGenome.setCurrentIndex(0)
      self.ui.comboBoxProject.setCurrentIndex(0)



    def exportMatrix():
      def getExportForExperimentRecord(record):
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

        return "\t".join([name, tpe, fname])

      # ask user which file to save the matrix to
      fname = QtGui.QFileDialog.getOpenFileName(self, 'Save file', '/home')

      # load experimental data from database
      exportModel.setQuery(dbLayer.getSelectedExpForExportSql(selectedExperimentIds)+dbLayer.sortSelectedSql(self.ui), db)
      exportRows = exportModel.rowCount()

      # write header and experiments to selected file
      expMatrix = open(fname, 'w')
      expMatrix.write("\t".join(['name','type','file'])+"\n")
      for i in range(0, exportRows):
        record = exportModel.record(i)
        expMatrix.write(getExportForExperimentRecord(record)+"\n")

      expMatrix.close()


    QtCore.QObject.connect(self.ui.pushButtonExport, QtCore.SIGNAL(_fromUtf8("clicked()")), self.ui.dataTable.update)
    QtCore.QObject.connect(self.ui.lineEditTechnique, QtCore.SIGNAL(_fromUtf8("textChanged(QString)")), self.ui.dataTable.update)

    # bind selectors
    QtCore.QObject.connect(self.ui.comboBoxGenome, QtCore.SIGNAL(_fromUtf8("currentIndexChanged(QString)")), onFilterInputChange)
    QtCore.QObject.connect(self.ui.comboBoxProject, QtCore.SIGNAL(_fromUtf8("currentIndexChanged(QString)")), onFilterInputChange)

    # bind filter input change handler to all inputs
    QtCore.QObject.connect(self.ui.lineEditName, QtCore.SIGNAL(_fromUtf8("textChanged(QString)")), onFilterInputChange)
    QtCore.QObject.connect(self.ui.lineEditDescription, QtCore.SIGNAL(_fromUtf8("textChanged(QString)")), onFilterInputChange)
    QtCore.QObject.connect(self.ui.lineEditEpigenetic, QtCore.SIGNAL(_fromUtf8("textChanged(QString)")), onFilterInputChange)
    QtCore.QObject.connect(self.ui.lineEditTechnique, QtCore.SIGNAL(_fromUtf8("textChanged(QString)")), onFilterInputChange)
    QtCore.QObject.connect(self.ui.lineEditBiosource, QtCore.SIGNAL(_fromUtf8("textChanged(QString)")), onFilterInputChange)
    QtCore.QObject.connect(self.ui.lineEditDataType, QtCore.SIGNAL(_fromUtf8("textChanged(QString)")), onFilterInputChange)
    QtCore.QObject.connect(self.ui.lineEditGeneralSearch, QtCore.SIGNAL(_fromUtf8("textChanged(QString)")), onFilterInputChange)

    # add double clicked row in data table to selection table
    QtCore.QObject.connect(self.ui.dataTable, QtCore.SIGNAL(_fromUtf8("doubleClicked(QModelIndex)")), expDoubleClicked)
    QtCore.QObject.connect(self.ui.dataTableSelected, QtCore.SIGNAL(_fromUtf8("doubleClicked(QModelIndex)")), selExpDoubleClicked)

    # bind experiment selection
    self.dataTableSelectionModel.selectionChanged.connect(onExperimentSelect)

    # clear
    QtCore.QObject.connect(self.ui.pushButtonClear, QtCore.SIGNAL(_fromUtf8("clicked()")), clearComboBoxes)

    # export
    QtCore.QObject.connect(self.ui.pushButtonExport, QtCore.SIGNAL(_fromUtf8("clicked()")), exportMatrix)

    # add
    QtCore.QObject.connect(self.ui.pushButtonAdd, QtCore.SIGNAL(_fromUtf8("clicked()")), addColumns)
	  
    self.connect(self.ui.dataTable.horizontalHeader(), QtCore.SIGNAL('sectionClicked (int)'), onFilterInputChange)
    self.connect(self.ui.dataTableSelected.horizontalHeader(), QtCore.SIGNAL('sectionClicked (int)'), onDataInputChangeSelected)


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    Form = Gui()
    Form.show()
    sys.exit(app.exec_())

