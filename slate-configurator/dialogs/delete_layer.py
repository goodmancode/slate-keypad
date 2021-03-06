# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'delete_layer.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_deleteLayerDialog(object):
    def setupUi(self, deleteLayerDialog):
        deleteLayerDialog.setObjectName("deleteLayerDialog")
        deleteLayerDialog.resize(230, 100)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(deleteLayerDialog.sizePolicy().hasHeightForWidth())
        deleteLayerDialog.setSizePolicy(sizePolicy)
        deleteLayerDialog.setMinimumSize(QtCore.QSize(230, 100))
        deleteLayerDialog.setMaximumSize(QtCore.QSize(230, 100))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("images/slate_windowicon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        deleteLayerDialog.setWindowIcon(icon)
        self.verticalLayoutWidget = QtWidgets.QWidget(deleteLayerDialog)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(0, 0, 231, 101))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.widget = QtWidgets.QWidget(self.verticalLayoutWidget)
        self.widget.setObjectName("widget")
        self.buttonBox = QtWidgets.QDialogButtonBox(self.widget)
        self.buttonBox.setGeometry(QtCore.QRect(30, 51, 161, 51))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.label = QtWidgets.QLabel(self.widget)
        self.label.setGeometry(QtCore.QRect(70, 20, 91, 31))
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.widget)

        self.retranslateUi(deleteLayerDialog)
        self.buttonBox.accepted.connect(deleteLayerDialog.accept) # type: ignore
        self.buttonBox.rejected.connect(deleteLayerDialog.reject) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(deleteLayerDialog)

    def retranslateUi(self, deleteLayerDialog):
        _translate = QtCore.QCoreApplication.translate
        deleteLayerDialog.setWindowTitle(_translate("deleteLayerDialog", "Delete Layer"))
        self.label.setText(_translate("deleteLayerDialog", "Delete layer?"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    deleteLayerDialog = QtWidgets.QDialog()
    ui = Ui_deleteLayerDialog()
    ui.setupUi(deleteLayerDialog)
    deleteLayerDialog.show()
    sys.exit(app.exec_())
