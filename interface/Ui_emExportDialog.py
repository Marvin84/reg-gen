# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Ui_emExportDialog.ui'
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

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(1171, 691)
        self.verticalLayout = QtGui.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setContentsMargins(-1, 0, -1, -1)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.label = QtGui.QLabel(Dialog)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedStates))
        self.label.setAlignment(QtCore.Qt.AlignBottom|QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout.addWidget(self.label)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.emExport = QtGui.QTableWidget(Dialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(2)
        sizePolicy.setHeightForWidth(self.emExport.sizePolicy().hasHeightForWidth())
        self.emExport.setSizePolicy(sizePolicy)
        self.emExport.setVerticalScrollMode(QtGui.QAbstractItemView.ScrollPerPixel)
        self.emExport.setHorizontalScrollMode(QtGui.QAbstractItemView.ScrollPerPixel)
        self.emExport.setObjectName(_fromUtf8("emExport"))
        self.emExport.setColumnCount(0)
        self.emExport.setRowCount(0)
        self.verticalLayout.addWidget(self.emExport)
        spacerItem1 = QtGui.QSpacerItem(20, 10, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        self.verticalLayout.addItem(spacerItem1)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setContentsMargins(-1, 0, -1, -1)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.groupBox_3 = QtGui.QGroupBox(Dialog)
        self.groupBox_3.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedStates))
        self.groupBox_3.setObjectName(_fromUtf8("groupBox_3"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.groupBox_3)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.formLayout = QtGui.QFormLayout()
        self.formLayout.setContentsMargins(-1, 0, -1, -1)
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.label_4 = QtGui.QLabel(self.groupBox_3)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.label_4)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.WhereLineplot = QtGui.QLineEdit(self.groupBox_3)
        self.WhereLineplot.setObjectName(_fromUtf8("WhereLineplot"))
        self.horizontalLayout_3.addWidget(self.WhereLineplot)
        self.WhereBrowserLineplot = QtGui.QToolButton(self.groupBox_3)
        self.WhereBrowserLineplot.setToolButtonStyle(QtCore.Qt.ToolButtonIconOnly)
        self.WhereBrowserLineplot.setArrowType(QtCore.Qt.NoArrow)
        self.WhereBrowserLineplot.setObjectName(_fromUtf8("WhereBrowserLineplot"))
        self.horizontalLayout_3.addWidget(self.WhereBrowserLineplot)
        self.formLayout.setLayout(0, QtGui.QFormLayout.FieldRole, self.horizontalLayout_3)
        self.label_5 = QtGui.QLabel(self.groupBox_3)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.label_5)
        self.normalization = QtGui.QComboBox(self.groupBox_3)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.normalization.sizePolicy().hasHeightForWidth())
        self.normalization.setSizePolicy(sizePolicy)
        self.normalization.setObjectName(_fromUtf8("normalization"))
        self.normalization.addItem(_fromUtf8(""))
        self.normalization.addItem(_fromUtf8(""))
        self.normalization.addItem(_fromUtf8(""))
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.normalization)
        self.label_6 = QtGui.QLabel(self.groupBox_3)
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.LabelRole, self.label_6)
        self.column = QtGui.QComboBox(self.groupBox_3)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.column.sizePolicy().hasHeightForWidth())
        self.column.setSizePolicy(sizePolicy)
        self.column.setObjectName(_fromUtf8("column"))
        self.column.addItem(_fromUtf8(""))
        self.column.addItem(_fromUtf8(""))
        self.column.addItem(_fromUtf8(""))
        self.formLayout.setWidget(2, QtGui.QFormLayout.FieldRole, self.column)
        self.label_7 = QtGui.QLabel(self.groupBox_3)
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.formLayout.setWidget(3, QtGui.QFormLayout.LabelRole, self.label_7)
        self.row = QtGui.QComboBox(self.groupBox_3)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.row.sizePolicy().hasHeightForWidth())
        self.row.setSizePolicy(sizePolicy)
        self.row.setObjectName(_fromUtf8("row"))
        self.row.addItem(_fromUtf8(""))
        self.row.addItem(_fromUtf8(""))
        self.row.addItem(_fromUtf8(""))
        self.formLayout.setWidget(3, QtGui.QFormLayout.FieldRole, self.row)
        self.label_8 = QtGui.QLabel(self.groupBox_3)
        self.label_8.setObjectName(_fromUtf8("label_8"))
        self.formLayout.setWidget(4, QtGui.QFormLayout.LabelRole, self.label_8)
        self.color = QtGui.QComboBox(self.groupBox_3)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.color.sizePolicy().hasHeightForWidth())
        self.color.setSizePolicy(sizePolicy)
        self.color.setObjectName(_fromUtf8("color"))
        self.color.addItem(_fromUtf8(""))
        self.color.addItem(_fromUtf8(""))
        self.color.addItem(_fromUtf8(""))
        self.formLayout.setWidget(4, QtGui.QFormLayout.FieldRole, self.color)
        self.verticalLayout_2.addLayout(self.formLayout)
        spacerItem2 = QtGui.QSpacerItem(20, 2, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem2)
        self.horizontalLayout_4 = QtGui.QHBoxLayout()
        self.horizontalLayout_4.setContentsMargins(-1, 0, -1, -1)
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        self.runLineplot = QtGui.QPushButton(self.groupBox_3)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.runLineplot.sizePolicy().hasHeightForWidth())
        self.runLineplot.setSizePolicy(sizePolicy)
        self.runLineplot.setMinimumSize(QtCore.QSize(200, 40))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.runLineplot.setFont(font)
        self.runLineplot.setObjectName(_fromUtf8("runLineplot"))
        self.horizontalLayout_4.addWidget(self.runLineplot)
        self.verticalLayout_2.addLayout(self.horizontalLayout_4)
        self.horizontalLayout_2.addWidget(self.groupBox_3)
        spacerItem3 = QtGui.QSpacerItem(20, 20, QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem3)
        self.line = QtGui.QFrame(Dialog)
        self.line.setFrameShape(QtGui.QFrame.VLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName(_fromUtf8("line"))
        self.horizontalLayout_2.addWidget(self.line)
        spacerItem4 = QtGui.QSpacerItem(20, 20, QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem4)
        self.groupBox_2 = QtGui.QGroupBox(Dialog)
        self.groupBox_2.setObjectName(_fromUtf8("groupBox_2"))
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.groupBox_2)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.formLayout_2 = QtGui.QFormLayout()
        self.formLayout_2.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout_2.setContentsMargins(-1, 0, -1, -1)
        self.formLayout_2.setObjectName(_fromUtf8("formLayout_2"))
        self.label_10 = QtGui.QLabel(self.groupBox_2)
        self.label_10.setObjectName(_fromUtf8("label_10"))
        self.formLayout_2.setWidget(0, QtGui.QFormLayout.LabelRole, self.label_10)
        self.horizontalLayout_6 = QtGui.QHBoxLayout()
        self.horizontalLayout_6.setObjectName(_fromUtf8("horizontalLayout_6"))
        self.WhereTests = QtGui.QLineEdit(self.groupBox_2)
        self.WhereTests.setObjectName(_fromUtf8("WhereTests"))
        self.horizontalLayout_6.addWidget(self.WhereTests)
        self.WhereBrowserTests = QtGui.QToolButton(self.groupBox_2)
        self.WhereBrowserTests.setToolButtonStyle(QtCore.Qt.ToolButtonIconOnly)
        self.WhereBrowserTests.setArrowType(QtCore.Qt.NoArrow)
        self.WhereBrowserTests.setObjectName(_fromUtf8("WhereBrowserTests"))
        self.horizontalLayout_6.addWidget(self.WhereBrowserTests)
        self.formLayout_2.setLayout(0, QtGui.QFormLayout.FieldRole, self.horizontalLayout_6)
        self.label_15 = QtGui.QLabel(self.groupBox_2)
        self.label_15.setObjectName(_fromUtf8("label_15"))
        self.formLayout_2.setWidget(1, QtGui.QFormLayout.LabelRole, self.label_15)
        self.horizontalLayout_7 = QtGui.QHBoxLayout()
        self.horizontalLayout_7.setObjectName(_fromUtf8("horizontalLayout_7"))
        self.input = QtGui.QLineEdit(self.groupBox_2)
        self.input.setObjectName(_fromUtf8("input"))
        self.horizontalLayout_7.addWidget(self.input)
        self.inputBrowser = QtGui.QToolButton(self.groupBox_2)
        self.inputBrowser.setToolButtonStyle(QtCore.Qt.ToolButtonIconOnly)
        self.inputBrowser.setArrowType(QtCore.Qt.NoArrow)
        self.inputBrowser.setObjectName(_fromUtf8("inputBrowser"))
        self.horizontalLayout_7.addWidget(self.inputBrowser)
        self.formLayout_2.setLayout(1, QtGui.QFormLayout.FieldRole, self.horizontalLayout_7)
        self.label_16 = QtGui.QLabel(self.groupBox_2)
        self.label_16.setObjectName(_fromUtf8("label_16"))
        self.formLayout_2.setWidget(2, QtGui.QFormLayout.LabelRole, self.label_16)
        self.inputType = QtGui.QComboBox(self.groupBox_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.inputType.sizePolicy().hasHeightForWidth())
        self.inputType.setSizePolicy(sizePolicy)
        self.inputType.setObjectName(_fromUtf8("inputType"))
        self.inputType.addItem(_fromUtf8(""))
        self.inputType.addItem(_fromUtf8(""))
        self.formLayout_2.setWidget(2, QtGui.QFormLayout.FieldRole, self.inputType)
        self.label_11 = QtGui.QLabel(self.groupBox_2)
        self.label_11.setObjectName(_fromUtf8("label_11"))
        self.formLayout_2.setWidget(3, QtGui.QFormLayout.LabelRole, self.label_11)
        self.testType = QtGui.QComboBox(self.groupBox_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.testType.sizePolicy().hasHeightForWidth())
        self.testType.setSizePolicy(sizePolicy)
        self.testType.setObjectName(_fromUtf8("testType"))
        self.testType.addItem(_fromUtf8(""))
        self.testType.addItem(_fromUtf8(""))
        self.testType.addItem(_fromUtf8(""))
        self.formLayout_2.setWidget(3, QtGui.QFormLayout.FieldRole, self.testType)
        self.label_12 = QtGui.QLabel(self.groupBox_2)
        self.label_12.setObjectName(_fromUtf8("label_12"))
        self.formLayout_2.setWidget(4, QtGui.QFormLayout.LabelRole, self.label_12)
        self.groupBy = QtGui.QComboBox(self.groupBox_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBy.sizePolicy().hasHeightForWidth())
        self.groupBy.setSizePolicy(sizePolicy)
        self.groupBy.setObjectName(_fromUtf8("groupBy"))
        self.groupBy.addItem(_fromUtf8(""))
        self.groupBy.addItem(_fromUtf8(""))
        self.groupBy.addItem(_fromUtf8(""))
        self.formLayout_2.setWidget(4, QtGui.QFormLayout.FieldRole, self.groupBy)
        self.label_13 = QtGui.QLabel(self.groupBox_2)
        self.label_13.setObjectName(_fromUtf8("label_13"))
        self.formLayout_2.setWidget(5, QtGui.QFormLayout.LabelRole, self.label_13)
        self.randomization = QtGui.QSpinBox(self.groupBox_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.randomization.sizePolicy().hasHeightForWidth())
        self.randomization.setSizePolicy(sizePolicy)
        self.randomization.setMaximum(999999)
        self.randomization.setProperty("value", 500)
        self.randomization.setObjectName(_fromUtf8("randomization"))
        self.formLayout_2.setWidget(5, QtGui.QFormLayout.FieldRole, self.randomization)
        self.verticalLayout_3.addLayout(self.formLayout_2)
        spacerItem5 = QtGui.QSpacerItem(20, 10, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_3.addItem(spacerItem5)
        self.horizontalLayout_5 = QtGui.QHBoxLayout()
        self.horizontalLayout_5.setContentsMargins(-1, 0, -1, -1)
        self.horizontalLayout_5.setObjectName(_fromUtf8("horizontalLayout_5"))
        self.runTests = QtGui.QPushButton(self.groupBox_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.runTests.sizePolicy().hasHeightForWidth())
        self.runTests.setSizePolicy(sizePolicy)
        self.runTests.setMinimumSize(QtCore.QSize(200, 40))
        self.runTests.setObjectName(_fromUtf8("runTests"))
        self.horizontalLayout_5.addWidget(self.runTests)
        self.verticalLayout_3.addLayout(self.horizontalLayout_5)
        self.horizontalLayout_2.addWidget(self.groupBox_2)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.line_2 = QtGui.QFrame(Dialog)
        self.line_2.setFrameShape(QtGui.QFrame.HLine)
        self.line_2.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_2.setObjectName(_fromUtf8("line_2"))
        self.verticalLayout.addWidget(self.line_2)
        self.horizontalLayout_8 = QtGui.QHBoxLayout()
        self.horizontalLayout_8.setObjectName(_fromUtf8("horizontalLayout_8"))
        spacerItem6 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_8.addItem(spacerItem6)
        self.exportButton = QtGui.QPushButton(Dialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.exportButton.sizePolicy().hasHeightForWidth())
        self.exportButton.setSizePolicy(sizePolicy)
        self.exportButton.setObjectName(_fromUtf8("exportButton"))
        self.horizontalLayout_8.addWidget(self.exportButton)
        self.buttonBox = QtGui.QDialogButtonBox(Dialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.buttonBox.sizePolicy().hasHeightForWidth())
        self.buttonBox.setSizePolicy(sizePolicy)
        self.buttonBox.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedStates))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Close)
        self.buttonBox.setCenterButtons(False)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.horizontalLayout_8.addWidget(self.buttonBox)
        self.verticalLayout.addLayout(self.horizontalLayout_8)

        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), Dialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Experimental Matrix Export", None))
        self.label.setText(_translate("Dialog", "Experimental Matrix", None))
        self.groupBox_3.setTitle(_translate("Dialog", "Lineplot", None))
        self.label_4.setText(_translate("Dialog", "Output Folder:", None))
        self.WhereBrowserLineplot.setText(_translate("Dialog", "...", None))
        self.label_5.setText(_translate("Dialog", "Normalization:", None))
        self.normalization.setItemText(0, _translate("Dialog", "None", None))
        self.normalization.setItemText(1, _translate("Dialog", "Rows", None))
        self.normalization.setItemText(2, _translate("Dialog", "Columns", None))
        self.label_6.setText(_translate("Dialog", "Column:", None))
        self.column.setItemText(0, _translate("Dialog", "None", None))
        self.column.setItemText(1, _translate("Dialog", "Reads", None))
        self.column.setItemText(2, _translate("Dialog", "Regions", None))
        self.label_7.setText(_translate("Dialog", "Row:", None))
        self.row.setItemText(0, _translate("Dialog", "None", None))
        self.row.setItemText(1, _translate("Dialog", "Reads", None))
        self.row.setItemText(2, _translate("Dialog", "Regions", None))
        self.label_8.setText(_translate("Dialog", "Color:", None))
        self.color.setItemText(0, _translate("Dialog", "None", None))
        self.color.setItemText(1, _translate("Dialog", "Reads", None))
        self.color.setItemText(2, _translate("Dialog", "Regions", None))
        self.runLineplot.setText(_translate("Dialog", "Run Lineplot", None))
        self.groupBox_2.setTitle(_translate("Dialog", "Association Tests", None))
        self.label_10.setText(_translate("Dialog", "Output Folder:", None))
        self.WhereBrowserTests.setText(_translate("Dialog", "...", None))
        self.label_15.setText(_translate("Dialog", "Input Matrix:", None))
        self.inputBrowser.setText(_translate("Dialog", "...", None))
        self.label_16.setText(_translate("Dialog", "Input Type:", None))
        self.inputType.setItemText(0, _translate("Dialog", "Reference", None))
        self.inputType.setItemText(1, _translate("Dialog", "Query", None))
        self.label_11.setText(_translate("Dialog", "Test Type:", None))
        self.testType.setItemText(0, _translate("Dialog", "Projection", None))
        self.testType.setItemText(1, _translate("Dialog", "Jacquard", None))
        self.testType.setItemText(2, _translate("Dialog", "Intersection", None))
        self.label_12.setText(_translate("Dialog", "Group By:", None))
        self.groupBy.setItemText(0, _translate("Dialog", "None", None))
        self.groupBy.setItemText(1, _translate("Dialog", "Regions", None))
        self.groupBy.setItemText(2, _translate("Dialog", "Reads", None))
        self.label_13.setText(_translate("Dialog", "Randomization:", None))
        self.runTests.setText(_translate("Dialog", "Run Association Test", None))
        self.exportButton.setText(_translate("Dialog", "Save Matrix as...", None))

