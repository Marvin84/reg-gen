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


selectAllText = "-- all --"
def buildSql(ui):
  where = []
  qry = """SELECT name, description, genome, epigenetic_mark, technique, project, data_type, biosource_name
        FROM experiments e 
        JOIN (SELECT sample_id,value AS biosource_name FROM sample_info WHERE key='biosource_name') bs ON (bs.sample_id = e.sample_id)"""

  # genome selection
  if ui.comboBoxGenome.currentIndex() > 0:
    where.append(('genome',str(ui.comboBoxGenome.currentText())))

  # build sql where clause from filter inputs
  filterInputs = [
    ("name", ui.lineEditName),
    ("description", ui.lineEditDescription),
    ("epigenetic_mark", ui.lineEditEpigenetic),
    ("technique", ui.lineEditTechnique),
    ("biosource_name", ui.lineEditBiosource),
    ("data_type", ui.lineEditDataType),
    ("project", ui.lineEditProject)]
  for (field,fIn) in filterInputs:
    content = fIn.text()
    if not content.isEmpty():
      where.append((field,str(content).strip()))

  if len(where) > 0:
    qry += " WHERE " + " AND ".join(map(lambda (field,text): "`"+field+"` LIKE '%"+text+"%'",where))

  return qry


class Gui(QtGui.QWidget):
    def __init__(self, parent = None):
        super(Gui, self).__init__(parent)
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        ui = self.ui


        db = connectDB()

        # bind data query to table
        projectModel = QSqlQueryModel()
        projectModel.setQuery(buildSql(self.ui),db)
        columns = projectModel.columnCount()
        rows = projectModel.rowCount()

        projectView = self.ui.dataTable
        projectView.setModel(projectModel)
        for i in range(1, columns-1):
            projectView.resizeColumnToContents(i)
        projectView.show()

        def onFilterInputChange(content):
          projectModel.setQuery(buildSql(ui),db)

        # bind sql query for genome selector
        genomeModel = QSqlQueryModel()
        genomeModel.setQuery("SELECT '"+selectAllText+"' AS genome UNION SELECT DISTINCT genome FROM experiments ORDER BY genome ASC",db)
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


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    Form = Gui()
    Form.show()
    sys.exit(app.exec_())

