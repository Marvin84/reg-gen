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

def rowDoubleClicked(index):
    QMessageBox.information(None,"Hello!","You Double Clicked: \n"+index.data().toString())

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
        rows = projectModel.rowCount()

        projectView = self.ui.dataTable
        projectView.setModel(projectModel)
        for i in range(1, columns-1):
            projectView.resizeColumnToContents(i)
        projectView.show()


        # on any change of the filter inputs, just update the data sql model
        # TODO: maybe be more efficient to let the table perform the sorting instead of the database?
        def onFilterInputChange(content):
          projectModel.setQuery(dbLayer.getDataSql()+dbLayer.buildSqlWhere(self.ui),db)


        # bind sql query for genome selector
        genomeModel = QSqlQueryModel()
        genomeModel.setQuery(dbLayer.getGenomeSql(),db)
        self.ui.comboBoxGenome.setModel(genomeModel)

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
        QtCore.QObject.connect(self.ui.dataTable, QtCore.SIGNAL(_fromUtf8("doubleClicked(QModelIndex)")), rowDoubleClicked)


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    Form = Gui()
    Form.show()
    sys.exit(app.exec_())

