from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Image(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(498, 322)
        Dialog.setFocusPolicy(QtCore.Qt.ClickFocus)
        Dialog.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
        self.verticalLayout = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(2)
        self.verticalLayout.setObjectName("verticalLayout")
        self.frame = QtWidgets.QFrame(Dialog)
        self.frame.setMinimumSize(QtCore.QSize(0, 30))
        self.frame.setMaximumSize(QtCore.QSize(16777215, 30))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.frame)
        self.horizontalLayout.setContentsMargins(6, 2, 6, 2)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.imageTitle = QtWidgets.QLabel(self.frame)
        self.imageTitle.setText("")
        self.imageTitle.setObjectName("imageTitle")
        self.horizontalLayout.addWidget(self.imageTitle)
        self.closeBtn = QtWidgets.QPushButton(self.frame)
        self.closeBtn.setMinimumSize(QtCore.QSize(20, 0))
        self.closeBtn.setMaximumSize(QtCore.QSize(20, 16777215))
        self.closeBtn.setObjectName("closeBtn")
        self.horizontalLayout.addWidget(self.closeBtn)
        self.verticalLayout.addWidget(self.frame)
        self.imageLabel = QtWidgets.QLabel(Dialog)
        self.imageLabel.setText("")
        self.imageLabel.setObjectName("imageLabel")
        self.verticalLayout.addWidget(self.imageLabel)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.closeBtn.setText(_translate("Dialog", "X"))
