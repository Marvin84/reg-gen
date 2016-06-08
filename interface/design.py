# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'table.ui'
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
        self.buttonDownload.setGeometry(QtCore.QRect(620, 350, 88, 27))
        self.buttonDownload.setObjectName(_fromUtf8("buttonDownload"))
        self.dataTable = QtGui.QTableView(Form)
        self.dataTable.setGeometry(QtCore.QRect(90, 120, 611, 192))
        self.dataTable.setSortingEnabled(True)
        self.dataTable.setObjectName(_fromUtf8("dataTable"))
        self.dataTable.verticalHeader().setVisible(False)
        self.dataTable.verticalHeader().setHighlightSections(False)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("Form", "Form", None))
        self.buttonDownload.setText(_translate("Form", "Download", None))

"""
if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    Form = QtGui.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
"""
