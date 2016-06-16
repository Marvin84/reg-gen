# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'design.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName(_fromUtf8("Form"))
        Form.resize(1192, 615)
        self.dataTable = QtGui.QTableView(Form)
        self.dataTable.setGeometry(QtCore.QRect(40, 170, 801, 192))
        self.dataTable.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.dataTable.setHorizontalScrollMode(QtGui.QAbstractItemView.ScrollPerPixel)
        self.dataTable.setSortingEnabled(True)
        self.dataTable.setObjectName(_fromUtf8("dataTable"))
        self.dataTable.verticalHeader().setVisible(True)
        self.dataTable.verticalHeader().setHighlightSections(False)
        self.lineEditName = QtGui.QLineEdit(Form)
        self.lineEditName.setGeometry(QtCore.QRect(40, 90, 111, 27))
        self.lineEditName.setObjectName(_fromUtf8("lineEditName"))
        self.lineEditDescription = QtGui.QLineEdit(Form)
        self.lineEditDescription.setGeometry(QtCore.QRect(40, 130, 111, 27))
        self.lineEditDescription.setObjectName(_fromUtf8("lineEditDescription"))
        self.lineEditEpigenetic = QtGui.QLineEdit(Form)
        self.lineEditEpigenetic.setGeometry(QtCore.QRect(340, 130, 111, 27))
        self.lineEditEpigenetic.setObjectName(_fromUtf8("lineEditEpigenetic"))
        self.lineEditTechnique = QtGui.QLineEdit(Form)
        self.lineEditTechnique.setGeometry(QtCore.QRect(190, 130, 111, 27))
        self.lineEditTechnique.setObjectName(_fromUtf8("lineEditTechnique"))
        self.lineEditBiosource = QtGui.QLineEdit(Form)
        self.lineEditBiosource.setGeometry(QtCore.QRect(190, 90, 111, 27))
        self.lineEditBiosource.setObjectName(_fromUtf8("lineEditBiosource"))
        self.lineEditDataType = QtGui.QLineEdit(Form)
        self.lineEditDataType.setGeometry(QtCore.QRect(340, 90, 111, 27))
        self.lineEditDataType.setObjectName(_fromUtf8("lineEditDataType"))
        self.lineEditGeneralSearch = QtGui.QLineEdit(Form)
        self.lineEditGeneralSearch.setGeometry(QtCore.QRect(40, 50, 411, 27))
        self.lineEditGeneralSearch.setObjectName(_fromUtf8("lineEditGeneralSearch"))
        self.dataTableSelected = QtGui.QTableView(Form)
        self.dataTableSelected.setGeometry(QtCore.QRect(40, 380, 801, 131))
        self.dataTableSelected.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.dataTableSelected.setHorizontalScrollMode(QtGui.QAbstractItemView.ScrollPerPixel)
        self.dataTableSelected.setSortingEnabled(True)
        self.dataTableSelected.setObjectName(_fromUtf8("dataTableSelected"))
        self.dataTableSelected.verticalHeader().setVisible(True)
        self.dataTableSelected.verticalHeader().setHighlightSections(False)
        self.tableViewMeta = QtGui.QTableView(Form)
        self.tableViewMeta.setGeometry(QtCore.QRect(860, 170, 321, 341))
        self.tableViewMeta.setAutoScroll(True)
        self.tableViewMeta.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.tableViewMeta.setHorizontalScrollMode(QtGui.QAbstractItemView.ScrollPerPixel)
        self.tableViewMeta.setSortingEnabled(False)
        self.tableViewMeta.setObjectName(_fromUtf8("tableViewMeta"))
        self.tableViewMeta.verticalHeader().setVisible(True)
        self.tableViewMeta.verticalHeader().setHighlightSections(False)
        self.splitter = QtGui.QSplitter(Form)
        self.splitter.setGeometry(QtCore.QRect(50, 10, 190, 27))
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName(_fromUtf8("splitter"))
        self.label = QtGui.QLabel(self.splitter)
        self.label.setObjectName(_fromUtf8("label"))
        self.comboBoxGenome = QtGui.QComboBox(self.splitter)
        self.comboBoxGenome.setObjectName(_fromUtf8("comboBoxGenome"))
        self.comboBoxGenome.addItem(_fromUtf8(""))
        self.comboBoxGenome.addItem(_fromUtf8(""))
        self.comboBoxGenome.addItem(_fromUtf8(""))
        self.comboBoxGenome.addItem(_fromUtf8(""))
        self.splitter_2 = QtGui.QSplitter(Form)
        self.splitter_2.setGeometry(QtCore.QRect(260, 10, 182, 27))
        self.splitter_2.setOrientation(QtCore.Qt.Horizontal)
        self.splitter_2.setObjectName(_fromUtf8("splitter_2"))
        self.label_2 = QtGui.QLabel(self.splitter_2)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.comboBoxProject = QtGui.QComboBox(self.splitter_2)
        self.comboBoxProject.setObjectName(_fromUtf8("comboBoxProject"))
        self.comboBoxProject.addItem(_fromUtf8(""))
        self.comboBoxProject.addItem(_fromUtf8(""))
        self.comboBoxProject.addItem(_fromUtf8(""))
        self.comboBoxProject.addItem(_fromUtf8(""))
        self.splitter_3 = QtGui.QSplitter(Form)
        self.splitter_3.setGeometry(QtCore.QRect(470, 60, 86, 54))
        self.splitter_3.setOrientation(QtCore.Qt.Vertical)
        self.splitter_3.setObjectName(_fromUtf8("splitter_3"))
        self.pushButtonClear = QtGui.QPushButton(self.splitter_3)
        self.pushButtonClear.setObjectName(_fromUtf8("pushButtonClear"))
        self.buttonDownload = QtGui.QPushButton(self.splitter_3)
        self.buttonDownload.setObjectName(_fromUtf8("buttonDownload"))

        self.retranslateUi(Form)
        QtCore.QObject.connect(self.pushButtonClear, QtCore.SIGNAL(_fromUtf8("clicked()")), self.lineEditDataType.clear)
        QtCore.QObject.connect(self.pushButtonClear, QtCore.SIGNAL(_fromUtf8("clicked()")), self.lineEditGeneralSearch.clear)
        QtCore.QObject.connect(self.pushButtonClear, QtCore.SIGNAL(_fromUtf8("clicked()")), self.lineEditEpigenetic.clear)
        QtCore.QObject.connect(self.pushButtonClear, QtCore.SIGNAL(_fromUtf8("clicked()")), self.lineEditBiosource.clear)
        QtCore.QObject.connect(self.pushButtonClear, QtCore.SIGNAL(_fromUtf8("clicked()")), self.lineEditTechnique.clear)
        QtCore.QObject.connect(self.pushButtonClear, QtCore.SIGNAL(_fromUtf8("clicked()")), self.lineEditName.clear)
        QtCore.QObject.connect(self.pushButtonClear, QtCore.SIGNAL(_fromUtf8("clicked()")), self.lineEditDescription.clear)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("Form", "Form", None))
        self.lineEditName.setPlaceholderText(_translate("Form", "Name", None))
        self.lineEditDescription.setPlaceholderText(_translate("Form", "Description", None))
        self.lineEditEpigenetic.setPlaceholderText(_translate("Form", "Epigen. Mark", None))
        self.lineEditTechnique.setPlaceholderText(_translate("Form", "Technique", None))
        self.lineEditBiosource.setPlaceholderText(_translate("Form", "Biosource", None))
        self.lineEditDataType.setPlaceholderText(_translate("Form", "Data Type", None))
        self.lineEditGeneralSearch.setPlaceholderText(_translate("Form", "General Search", None))
        self.label.setText(_translate("Form", "Genome:", None))
        self.comboBoxGenome.setItemText(0, _translate("Form", "Neues Element", None))
        self.comboBoxGenome.setItemText(1, _translate("Form", "bbbbbb", None))
        self.comboBoxGenome.setItemText(2, _translate("Form", "jjutr", None))
        self.comboBoxGenome.setItemText(3, _translate("Form", "sagege", None))
        self.label_2.setText(_translate("Form", "Project:", None))
        self.comboBoxProject.setItemText(0, _translate("Form", "Neues Element", None))
        self.comboBoxProject.setItemText(1, _translate("Form", "bbbbbb", None))
        self.comboBoxProject.setItemText(2, _translate("Form", "jjutr", None))
        self.comboBoxProject.setItemText(3, _translate("Form", "sagege", None))
        self.pushButtonClear.setText(_translate("Form", "Clear All", None))
        self.buttonDownload.setText(_translate("Form", "Download", None))

