from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_thresholdingDialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(215, 112)
        Dialog.setMaximumSize(215, 112)
        self.verticalLayout = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout.setSpacing(15)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.slider_value_label = QtWidgets.QLabel(Dialog)
        self.slider_value_label.setText("60")
        self.slider_value_label.setObjectName("slider_value_label")
        self.horizontalLayout.addWidget(self.slider_value_label)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.Hs_prog = QtWidgets.QSlider(Dialog)
        self.Hs_prog.setMaximum(255)
        self.Hs_prog.setProperty("value", 60)
        self.Hs_prog.setOrientation(QtCore.Qt.Horizontal)
        self.Hs_prog.setObjectName("Hs_prog")
        self.verticalLayout.addWidget(self.Hs_prog)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setCenterButtons(True)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept) # type: ignore
        self.buttonBox.rejected.connect(Dialog.reject) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Threshold"))
        self.label.setText(_translate("Dialog", "Wartość progu:"))
