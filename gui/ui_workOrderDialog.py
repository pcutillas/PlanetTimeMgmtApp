# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui/ui/workOrderDialog.ui',
# licensing of 'gui/ui/workOrderDialog.ui' applies.
#
# Created: Sun May 17 12:55:13 2020
#      by: pyside2-uic  running on PySide2 5.13.0
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(411, 425)
        Dialog.setMinimumSize(QtCore.QSize(411, 425))
        self.layoutWidget = QtWidgets.QWidget(Dialog)
        self.layoutWidget.setGeometry(QtCore.QRect(10, 385, 391, 30))
        self.layoutWidget.setObjectName("layoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.layoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.planetButton = QtWidgets.QPushButton(self.layoutWidget)
        self.planetButton.setObjectName("planetButton")
        self.horizontalLayout.addWidget(self.planetButton)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.buttonBox = QtWidgets.QDialogButtonBox(self.layoutWidget)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.horizontalLayout.addWidget(self.buttonBox)
        self.errorSection = QtWidgets.QLabel(Dialog)
        self.errorSection.setGeometry(QtCore.QRect(0, 325, 411, 50))
        self.errorSection.setMinimumSize(QtCore.QSize(0, 50))
        self.errorSection.setAlignment(QtCore.Qt.AlignCenter)
        self.errorSection.setObjectName("errorSection")
        self.layoutWidget1 = QtWidgets.QWidget(Dialog)
        self.layoutWidget1.setGeometry(QtCore.QRect(10, 24, 391, 291))
        self.layoutWidget1.setObjectName("layoutWidget1")
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout(self.layoutWidget1)
        self.horizontalLayout_7.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.label = QtWidgets.QLabel(self.layoutWidget1)
        self.label.setObjectName("label")
        self.horizontalLayout_2.addWidget(self.label)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem2)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem3)
        self.label_2 = QtWidgets.QLabel(self.layoutWidget1)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_3.addWidget(self.label_2)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        spacerItem4 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem4)
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        spacerItem5 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_8.addItem(spacerItem5)
        self.label_6 = QtWidgets.QLabel(self.layoutWidget1)
        self.label_6.setObjectName("label_6")
        self.horizontalLayout_8.addWidget(self.label_6)
        self.verticalLayout.addLayout(self.horizontalLayout_8)
        spacerItem6 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem6)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        spacerItem7 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem7)
        self.label_3 = QtWidgets.QLabel(self.layoutWidget1)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_4.addWidget(self.label_3)
        self.verticalLayout.addLayout(self.horizontalLayout_4)
        spacerItem8 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem8)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        spacerItem9 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem9)
        self.label_5 = QtWidgets.QLabel(self.layoutWidget1)
        self.label_5.setObjectName("label_5")
        self.horizontalLayout_5.addWidget(self.label_5)
        self.verticalLayout.addLayout(self.horizontalLayout_5)
        spacerItem10 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem10)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        spacerItem11 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_6.addItem(spacerItem11)
        self.label_4 = QtWidgets.QLabel(self.layoutWidget1)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_6.addWidget(self.label_4)
        self.verticalLayout.addLayout(self.horizontalLayout_6)
        self.horizontalLayout_7.addLayout(self.verticalLayout)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.woNumber = QtWidgets.QSpinBox(self.layoutWidget1)
        self.woNumber.setObjectName("woNumber")
        self.verticalLayout_2.addWidget(self.woNumber)
        spacerItem12 = QtWidgets.QSpacerItem(17, 25, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem12)
        self.numPieces = QtWidgets.QSpinBox(self.layoutWidget1)
        self.numPieces.setObjectName("numPieces")
        self.verticalLayout_2.addWidget(self.numPieces)
        spacerItem13 = QtWidgets.QSpacerItem(17, 25, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem13)
        self.yldBox = QtWidgets.QSpinBox(self.layoutWidget1)
        self.yldBox.setObjectName("yldBox")
        self.verticalLayout_2.addWidget(self.yldBox)
        spacerItem14 = QtWidgets.QSpacerItem(17, 25, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem14)
        self.side = QtWidgets.QComboBox(self.layoutWidget1)
        self.side.setCursor(QtCore.Qt.PointingHandCursor)
        self.side.setObjectName("side")
        self.side.addItem("")
        self.side.addItem("")
        self.verticalLayout_2.addWidget(self.side)
        spacerItem15 = QtWidgets.QSpacerItem(17, 25, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem15)
        self.machineNum = QtWidgets.QComboBox(self.layoutWidget1)
        self.machineNum.setCursor(QtCore.Qt.PointingHandCursor)
        self.machineNum.setObjectName("machineNum")
        self.verticalLayout_2.addWidget(self.machineNum)
        spacerItem16 = QtWidgets.QSpacerItem(17, 25, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem16)
        self.planetNum = QtWidgets.QComboBox(self.layoutWidget1)
        self.planetNum.setMinimumSize(QtCore.QSize(250, 0))
        self.planetNum.setCursor(QtCore.Qt.PointingHandCursor)
        self.planetNum.setObjectName("planetNum")
        self.verticalLayout_2.addWidget(self.planetNum)
        self.horizontalLayout_7.addLayout(self.verticalLayout_2)

        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), Dialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtWidgets.QApplication.translate("Dialog", "Dialog", None, -1))
        self.planetButton.setText(QtWidgets.QApplication.translate("Dialog", "Configure Planets...", None, -1))
        self.errorSection.setText(QtWidgets.QApplication.translate("Dialog", "TextLabel", None, -1))
        self.label.setText(QtWidgets.QApplication.translate("Dialog", "Work Order Number:", None, -1))
        self.label_2.setText(QtWidgets.QApplication.translate("Dialog", "Number of Pieces:", None, -1))
        self.label_6.setText(QtWidgets.QApplication.translate("Dialog", "Yield (Optional):", None, -1))
        self.label_3.setText(QtWidgets.QApplication.translate("Dialog", "Side:", None, -1))
        self.label_5.setText(QtWidgets.QApplication.translate("Dialog", "Machine:", None, -1))
        self.label_4.setText(QtWidgets.QApplication.translate("Dialog", "Planet:", None, -1))
        self.side.setItemText(0, QtWidgets.QApplication.translate("Dialog", "Side 1", None, -1))
        self.side.setItemText(1, QtWidgets.QApplication.translate("Dialog", "Side 2", None, -1))
