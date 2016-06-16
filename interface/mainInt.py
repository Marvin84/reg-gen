import sys
from PyQt4 import QtCore, QtSql, QtGui
from PyQt4.QtSql import QSqlQueryModel,QSqlDatabase,QSqlQuery
from design import Ui_Form
import dbLayer

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
    projectModel = QSqlQueryModel()
    projectModel.setQuery(dbLayer.getDataSql()+dbLayer.buildSqlWhere(self.ui),db)
    columns = projectModel.columnCount()

    projectView = self.ui.dataTable
    projectView.setModel(projectModel)
    for i in range(1, columns-1):
      projectView.resizeColumnToContents(i)

    projectView.setColumnHidden(0,True) # hide experiment id
    projectView.show()
    self.dataTableSelectionModel = projectView.selectionModel()


    # bind sql query for genome selector
    genomeModel = QSqlQueryModel()
    genomeModel.setQuery(dbLayer.getGenomeSql(),db)
    self.ui.comboBoxGenome.setModel(genomeModel)


    # bind sql model for extra data selector
    extraDataModel = QSqlQueryModel()
    self.ui.tableViewMeta.setModel(extraDataModel)


    # bind sql model for selected experiments
    selectedExpModel = QSqlQueryModel()
    selectedExpModel.setQuery(dbLayer.getSelectedExpSql(selectedExperimentIds), db)
    self.ui.dataTableSelected.setModel(selectedExpModel)


    # on any change of the filter inputs, just update the data sql model
    # TODO: maybe be more efficient to let the table perform the sorting instead of the database?
    def onFilterInputChange(content):
      projectModel.setQuery(dbLayer.getDataSql()+dbLayer.buildSqlWhere(self.ui),db)

    def onExperimentSelect(selected, deselected):
      indexes = self.dataTableSelectionModel.selectedRows()
      if len(indexes) == 1:
        record = projectModel.record(indexes[0].row())
        experiment_id = record.value("experiment_id").toString()
        extraDataModel.setQuery(dbLayer.getAdditionalDataSql(experiment_id),db)
      else:
        extraDataModel.clear()
        # TODO: table does not clear itself?

    def expDoubleClicked(index):
      print("You Double Clicked: "+index.data().toString())
      print("In row: \n"+str(index.row()))

      record = projectModel.record(index.row())
      experiment_id = record.value("experiment_id").toString()
      selectedExperimentIds.append(str(experiment_id))
      selectedExpModel.setQuery(dbLayer.getSelectedExpSql(selectedExperimentIds), db)

    def selExpDoubleClicked(index):
      print("You Double Clicked: "+index.data().toString())
      print("In row: \n"+str(index.row()))

      record = selectedExpModel.record(index.row())
      experiment_id = record.value("experiment_id").toString()
      selectedExperimentIds.remove(str(experiment_id))
      selectedExpModel.setQuery(dbLayer.getSelectedExpSql(selectedExperimentIds), db)


    QtCore.QObject.connect(self.ui.buttonDownload, QtCore.SIGNAL(_fromUtf8("clicked()")), self.ui.dataTable.update)
    QtCore.QObject.connect(self.ui.lineEditTechnique, QtCore.SIGNAL(_fromUtf8("textChanged(QString)")), self.ui.dataTable.update)

    # bind genome selector
    QtCore.QObject.connect(self.ui.comboBoxGenome, QtCore.SIGNAL(_fromUtf8("currentIndexChanged(QString)")), onFilterInputChange)

    # bind filter input change handler to all inputs
    QtCore.QObject.connect(self.ui.lineEditName, QtCore.SIGNAL(_fromUtf8("textChanged(QString)")), onFilterInputChange)
    QtCore.QObject.connect(self.ui.lineEditDescription, QtCore.SIGNAL(_fromUtf8("textChanged(QString)")), onFilterInputChange)
    QtCore.QObject.connect(self.ui.lineEditEpigenetic, QtCore.SIGNAL(_fromUtf8("textChanged(QString)")), onFilterInputChange)
    QtCore.QObject.connect(self.ui.lineEditTechnique, QtCore.SIGNAL(_fromUtf8("textChanged(QString)")), onFilterInputChange)
    QtCore.QObject.connect(self.ui.lineEditBiosource, QtCore.SIGNAL(_fromUtf8("textChanged(QString)")), onFilterInputChange)
    QtCore.QObject.connect(self.ui.lineEditDataType, QtCore.SIGNAL(_fromUtf8("textChanged(QString)")), onFilterInputChange)
    QtCore.QObject.connect(self.ui.lineEditProject, QtCore.SIGNAL(_fromUtf8("textChanged(QString)")), onFilterInputChange)
    QtCore.QObject.connect(self.ui.lineEditType, QtCore.SIGNAL(_fromUtf8("textChanged(QString)")), onFilterInputChange)

    # add double clicked row in data table to selection table
    QtCore.QObject.connect(self.ui.dataTable, QtCore.SIGNAL(_fromUtf8("doubleClicked(QModelIndex)")), expDoubleClicked)
    QtCore.QObject.connect(self.ui.dataTableSelected, QtCore.SIGNAL(_fromUtf8("doubleClicked(QModelIndex)")), selExpDoubleClicked)

    # bind experiment selection
    self.dataTableSelectionModel.selectionChanged.connect(onExperimentSelect)


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    Form = Gui()
    Form.show()
    sys.exit(app.exec_())

