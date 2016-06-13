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
        Form.resize(775, 455)
        self.buttonDownload = QtGui.QPushButton(Form)
        self.buttonDownload.setGeometry(QtCore.QRect(570, 400, 88, 27))
        self.buttonDownload.setObjectName(_fromUtf8("buttonDownload"))
        self.dataTable = QtGui.QTableView(Form)
        self.dataTable.setGeometry(QtCore.QRect(40, 170, 611, 192))
        self.dataTable.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.dataTable.setHorizontalScrollMode(QtGui.QAbstractItemView.ScrollPerPixel)
        self.dataTable.setSortingEnabled(True)
        self.dataTable.setObjectName(_fromUtf8("dataTable"))
        self.dataTable.verticalHeader().setVisible(True)
        self.dataTable.verticalHeader().setHighlightSections(False)
        self.lineEditName = QtGui.QLineEdit(Form)
        self.lineEditName.setGeometry(QtCore.QRect(40, 60, 111, 27))
        self.lineEditName.setObjectName(_fromUtf8("lineEditName"))
        self.comboBoxGenome = QtGui.QComboBox(Form)
        self.comboBoxGenome.setGeometry(QtCore.QRect(40, 20, 111, 27))
        self.comboBoxGenome.setObjectName(_fromUtf8("comboBoxGenome"))
        self.lineEditDescription = QtGui.QLineEdit(Form)
        self.lineEditDescription.setGeometry(QtCore.QRect(40, 100, 111, 27))
        self.lineEditDescription.setObjectName(_fromUtf8("lineEditDescription"))
        self.lineEditEpigenetic = QtGui.QLineEdit(Form)
        self.lineEditEpigenetic.setGeometry(QtCore.QRect(190, 20, 111, 27))
        self.lineEditEpigenetic.setObjectName(_fromUtf8("lineEditEpigenetic"))
        self.lineEditTechnique = QtGui.QLineEdit(Form)
        self.lineEditTechnique.setGeometry(QtCore.QRect(190, 100, 111, 27))
        self.lineEditTechnique.setObjectName(_fromUtf8("lineEditTechnique"))
        self.lineEditBiosource = QtGui.QLineEdit(Form)
        self.lineEditBiosource.setGeometry(QtCore.QRect(190, 60, 111, 27))
        self.lineEditBiosource.setObjectName(_fromUtf8("lineEditBiosource"))
        self.lineEditDataType = QtGui.QLineEdit(Form)
        self.lineEditDataType.setGeometry(QtCore.QRect(340, 60, 111, 27))
        self.lineEditDataType.setObjectName(_fromUtf8("lineEditDataType"))
        self.lineEditProject = QtGui.QLineEdit(Form)
        self.lineEditProject.setGeometry(QtCore.QRect(340, 20, 111, 27))
        self.lineEditProject.setObjectName(_fromUtf8("lineEditProject"))
        self.lineEditType = QtGui.QLineEdit(Form)
        self.lineEditType.setGeometry(QtCore.QRect(340, 100, 111, 27))
        self.lineEditType.setObjectName(_fromUtf8("lineEditType"))

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("Form", "Form", None))
        self.buttonDownload.setText(_translate("Form", "Download", None))

