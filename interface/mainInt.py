import sys
from PyQt4 import QtCore, QtSql, QtGui
from PyQt4.QtSql import QSqlQueryModel,QSqlDatabase,QSqlQuery
from design import Ui_MainWindow
from emExportDialog import emExportDialog
import dbLayer

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

def connectDB():
  db = QtSql.QSqlDatabase.addDatabase('QSQLITE')
  db.setDatabaseName('db/deepBlue.db')
  ok = db.open()
  
  if ok == False:
    QtGui.QMessageBox.critical(None, QtGui.qApp.tr("Cannot open database"),
    QtGui.qApp.tr("Unable to establish a database connection."),
    QtGui.QMessageBox.Cancel)   
    return False

  return db


class Gui(QtGui.QMainWindow):
  def __init__(self, parent = None):
    super(Gui, self).__init__(parent)
    self.ui = Ui_MainWindow()
    self.ui.setupUi(self)

    # basic initialization
    self.selectedExperimentIds = set([])
    self.db = connectDB()

    # initialize dialogs
    self.emExportDialog = emExportDialog()
    self.emExportDialog.setMainApp(self)

    # bind sql query for genome and project selectors
    genomeModel = QSqlQueryModel()
    genomeModel.setQuery(dbLayer.getGenomesSql(), self.db)
    self.ui.comboBoxGenome.setModel(genomeModel)

    projectsModel = QSqlQueryModel()
    projectsModel.setQuery(dbLayer.getProjectsSql(), self.db)
    self.ui.comboBoxProject.setModel(projectsModel)

    # bind sql model for extra data selector
    self.extraDataModel = QSqlQueryModel()
    self.ui.tableViewMeta.setModel(self.extraDataModel)

    # bind main data query to search result table
    self.experimentsModel = QSqlQueryModel()
    self.ui.dataTable.setModel(self.experimentsModel)
    self.reloadExperiments()
    
    # selection model
    self.dataTableSelectionModel = self.ui.dataTable.selectionModel()

    # bind sql model for selected experiments
    self.selectedExpModel = QSqlQueryModel()
    self.selectedExpModel.setQuery(dbLayer.getSelectedExpSql(self.selectedExperimentIds), self.db)
    self.ui.dataTableSelected.setModel(self.selectedExpModel)

    # start state push buttons
    self.ui.pushButtonAdd.setEnabled(False)
    self.ui.pushButtonRemove.setEnabled(False)
    self.ui.pushButtonExport.setEnabled(False)

    # initialize TableViews
    experimentsView = self.ui.dataTable
    experimentsView.setColumnHidden(0,True) # hide experiment id
    experimentsView.resizeColumnsToContents()
    experimentsView.resizeRowsToContents()
    experimentsView.show()

    selectedExpView = self.ui.dataTableSelected
    selectedExpView.setColumnHidden(0,True) # hide experiment id
    selectedExpView.resizeColumnsToContents()
    selectedExpView.resizeRowsToContents()
    selectedExpView.show()

    # set all the signal handlers
    self.initializeSignalHandlers()

  def reloadExperiments(self):
    header = self.ui.dataTable.horizontalHeader()
    self.experimentsModel.setQuery(dbLayer.getDataSql()+dbLayer.buildSqlWhere(self.ui)+dbLayer.sortSql(header),self.db)
    self.ui.pushButtonAdd.setEnabled(False)

  def reloadSelectedExperiments(self):
    header = self.ui.dataTableSelected.horizontalHeader()
    self.selectedExpModel.setQuery(dbLayer.getSelectedExpSql(self.selectedExperimentIds)+dbLayer.sortSql(header), self.db)

    self.ui.dataTableSelected.resizeColumnsToContents()
    self.ui.dataTableSelected.resizeRowsToContents()

    self.ui.pushButtonRemove.setEnabled(False)
    self.ui.pushButtonExport.setEnabled(True)
    

  # handler for changes of filters and comboBoxes
  # on any change of the filter inputs, just update the data sql model
  def onFilterInputChange(self,content):
    # TODO: maybe be more efficient to let the table perform the sorting instead of the database?
    self.reloadExperiments()

  # handler for sorting table for selected experiments
  def onSelectedSortingChange(self,content):
    self.reloadSelectedExperiments()

  # handler for selection changes in main experiment table
  # updates metadata table
  def onExperimentSelect(self,selected, deselected):
    indexes = self.dataTableSelectionModel.selectedRows()
    if len(indexes) == 1:
      record = self.experimentsModel.record(indexes[0].row())
      experiment_id = record.value("experiment_id").toString()
      self.extraDataModel.setQuery(dbLayer.getAdditionalDataSql(experiment_id),self.db)
      self.ui.tableViewMeta.setColumnHidden(0,True)
    else:
      # TODO: table does not clear itself?
      #self.extraDataModel.clear()
      self.extraDataModel.setQuery("",self.db)


  # double-click handler for experiments table
  # adds experiment to experimental matrix
  def expDoubleClicked(self,index):
    record = self.experimentsModel.record(index.row())
    experiment_id = record.value("experiment_id").toString()
    self.selectedExperimentIds.add(str(experiment_id))
    self.reloadSelectedExperiments()
    self.ui.pushButtonExport.setEnabled(True)


  # double-click handler for selected experiments table
  # removes experiment from experimental matrix
  def selExpDoubleClicked(self,index):
    record = self.selectedExpModel.record(index.row())
    experiment_id = record.value("experiment_id").toString()
    self.selectedExperimentIds.discard(str(experiment_id))
    self.reloadSelectedExperiments()
    self.disablePushButtonRemoveAndExport()
  
  # add button handler
  # adds all selected experiments to experimental matrix
  def addRows(self):
    indices = self.dataTableSelectionModel.selectedRows()
    if len(indices) > 0:
      for index in indices:
        record = self.experimentsModel.record(index.row())
        experiment_id = record.value("experiment_id").toString()
        self.selectedExperimentIds.add(str(experiment_id))
      self.reloadSelectedExperiments()
      self.ui.pushButtonExport.setEnabled(True)

  # remove button handler
  # removes all selected experiments from experimental matrix
  def removeRows(self):
    model = self.ui.dataTableSelected.selectionModel()
    indices = model.selectedRows()
    if len(indices) > 0:           
      for index in indices:
        record = self.selectedExpModel.record(index.row())
        experiment_id = record.value("experiment_id").toString()
        self.selectedExperimentIds.discard(str(experiment_id))
      self.reloadSelectedExperiments()
      self.disablePushButtonRemoveAndExport()

  # enable push button add 
  def enablePushButtonAdd(self):
    if self.dataTableSelectionModel.hasSelection():
      self.ui.pushButtonAdd.setEnabled(True)
    else: 
      self.ui.pushButtonAdd.setEnabled(False)
  
  # enable push button remove
  def enablePushButtonRemove(self):
    if self.ui.dataTableSelected.selectionModel().hasSelection():
      self.ui.pushButtonRemove.setEnabled(True)
    else: 
      self.ui.pushButtonRemove.setEnabled(False)   

  # disable push button remove and export
  def disablePushButtonRemoveAndExport(self):
    self.ui.pushButtonRemove.setEnabled(False)
    numRows = self.ui.dataTableSelected.model().rowCount()
    if numRows == 0:
      self.ui.pushButtonExport.setEnabled(False) 

  # clear button click handler
  # resets comboBoxes
  def clearComboBoxes(self):
    self.ui.comboBoxGenome.setCurrentIndex(0)
    self.ui.comboBoxProject.setCurrentIndex(0)

  # export button click handler
  # opens export dialog
  def exportMatrix(self):
    #self.rgtCommand()
    if len(self.selectedExperimentIds) == 0:
      return

    # open dialog
    self.emExportDialog.setSelectedExperiments(self.selectedExperimentIds)
    self.emExportDialog.initTable()
    self.emExportDialog.show()

  # connects signal handlers to widget signals
  def initializeSignalHandlers(self):
    QtCore.QObject.connect(self.ui.pushButtonExport, QtCore.SIGNAL(_fromUtf8("clicked()")), self.ui.dataTable.update)
    QtCore.QObject.connect(self.ui.lineEditTechnique, QtCore.SIGNAL(_fromUtf8("textChanged(QString)")), self.ui.dataTable.update)

    # bind selectors
    QtCore.QObject.connect(self.ui.comboBoxGenome, QtCore.SIGNAL(_fromUtf8("currentIndexChanged(QString)")), self.onFilterInputChange)
    QtCore.QObject.connect(self.ui.comboBoxProject, QtCore.SIGNAL(_fromUtf8("currentIndexChanged(QString)")), self.onFilterInputChange)

    # bind filter input change handler to all inputs
    QtCore.QObject.connect(self.ui.lineEditName, QtCore.SIGNAL(_fromUtf8("textChanged(QString)")), self.onFilterInputChange)
    QtCore.QObject.connect(self.ui.lineEditDescription, QtCore.SIGNAL(_fromUtf8("textChanged(QString)")), self.onFilterInputChange)
    QtCore.QObject.connect(self.ui.lineEditEpigenetic, QtCore.SIGNAL(_fromUtf8("textChanged(QString)")), self.onFilterInputChange)
    QtCore.QObject.connect(self.ui.lineEditTechnique, QtCore.SIGNAL(_fromUtf8("textChanged(QString)")), self.onFilterInputChange)
    QtCore.QObject.connect(self.ui.lineEditBiosource, QtCore.SIGNAL(_fromUtf8("textChanged(QString)")), self.onFilterInputChange)
    QtCore.QObject.connect(self.ui.lineEditDataType, QtCore.SIGNAL(_fromUtf8("textChanged(QString)")), self.onFilterInputChange)
    QtCore.QObject.connect(self.ui.lineEditGeneralSearch, QtCore.SIGNAL(_fromUtf8("textChanged(QString)")), self.onFilterInputChange)

    # add double clicked row in data table to selection table
    QtCore.QObject.connect(self.ui.dataTable, QtCore.SIGNAL(_fromUtf8("doubleClicked(QModelIndex)")), self.expDoubleClicked)
    QtCore.QObject.connect(self.ui.dataTableSelected, QtCore.SIGNAL(_fromUtf8("doubleClicked(QModelIndex)")), self.selExpDoubleClicked)

    # bind experiment selection
    self.dataTableSelectionModel.selectionChanged.connect(self.onExperimentSelect)

    # clear
    QtCore.QObject.connect(self.ui.pushButtonClear, QtCore.SIGNAL(_fromUtf8("clicked()")), self.clearComboBoxes)

    # export
    QtCore.QObject.connect(self.ui.pushButtonExport, QtCore.SIGNAL(_fromUtf8("clicked()")), self.exportMatrix)

    # add
    QtCore.QObject.connect(self.ui.pushButtonAdd, QtCore.SIGNAL(_fromUtf8("clicked()")), self.addRows)

    # remove
    QtCore.QObject.connect(self.ui.pushButtonRemove, QtCore.SIGNAL(_fromUtf8("clicked()")), self.removeRows)
    
    self.connect(self.ui.dataTable.horizontalHeader(), QtCore.SIGNAL('sectionClicked (int)'), self.onFilterInputChange)
    self.connect(self.ui.dataTableSelected.horizontalHeader(), QtCore.SIGNAL('sectionClicked (int)'), self.onSelectedSortingChange)

    # enable/disable pushbuttons
    self.dataTableSelectionModel.selectionChanged.connect(self.enablePushButtonAdd)
    self.ui.dataTableSelected.selectionModel().selectionChanged.connect(self.enablePushButtonRemove)


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    Form = Gui()
    Form.showMaximized()
    sys.exit(app.exec_())
