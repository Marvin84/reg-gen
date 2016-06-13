import sys
from PyQt4 import QtCore, QtSql, QtGui
from PyQt4.QtSql import QSqlQueryModel,QSqlDatabase,QSqlQuery
from design import Ui_Form

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

        db = connectDB()

        projectModel = QSqlQueryModel()
        projectModel.setQuery("SELECT name, description, genome, epigenetic_mark, sample_id, technique, project, data_type, type FROM experiments",db)
        columns = projectModel.columnCount()
        rows = projectModel.rowCount()

        projectView = self.ui.dataTable
        projectView.setModel(projectModel)
        for i in range(1, columns-1):
            projectView.resizeColumnToContents(i)
        projectView.show()

        QtCore.QObject.connect(self.ui.buttonDownload, QtCore.SIGNAL(_fromUtf8("clicked()")), self.ui.dataTable.update)
        QtCore.QObject.connect(self.ui.lineEditTechnique, QtCore.SIGNAL(_fromUtf8("textChanged(QString)")), self.ui.dataTable.update)
        QtCore.QObject.connect(self.ui.comboBoxGenome, QtCore.SIGNAL(_fromUtf8("currentIndexChanged(QString)")), self.ui.dataTable.update)


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    Form = Gui()
    Form.show()
    sys.exit(app.exec_())

