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
        extraDataModel.setQuery(dbLayer.getAdditionalDataSql('e54478'),db)
        self.ui.tableViewMeta.setModel(extraDataModel)


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

        # bind experiment selection
        self.dataTableSelectionModel.selectionChanged.connect(onExperimentSelect)


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    Form = Gui()
    Form.show()
    sys.exit(app.exec_())

