from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_AdaptiveThresholdDialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(221, 107)
        Dialog.setMaximumSize(221, 107)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(-10, 70, 201, 21))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.Hs_rozmiar = QtWidgets.QSlider(Dialog)
        self.Hs_rozmiar.setGeometry(QtCore.QRect(30, 30, 161, 21))
        self.Hs_rozmiar.setMinimum(3)
        self.Hs_rozmiar.setMaximum(17)
        self.Hs_rozmiar.setSingleStep(2)
        self.Hs_rozmiar.setPageStep(2)
        self.Hs_rozmiar.setProperty("value", 3)
        self.Hs_rozmiar.setOrientation(QtCore.Qt.Horizontal)
        self.Hs_rozmiar.setObjectName("Hs_rozmiar")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(30, 5, 68, 21))
        self.label.setObjectName("label")
        self.slider_value_label = QtWidgets.QLabel(Dialog)
        self.slider_value_label.setGeometry(QtCore.QRect(110, 5, 20, 21))
        self.slider_value_label.setObjectName("slider_value_label")

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept) # type: ignore
        self.buttonBox.rejected.connect(Dialog.reject) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Adaptive Threshold"))
        self.label.setText(_translate("Dialog", "Rozmiar okna:"))
        self.slider_value_label.setText(_translate("Dialog", "3"))
