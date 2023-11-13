from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from Ui.ui_medianDialog import Ui_medianDialog

class MedianDialog(QDialog):
    def __init__(self):
        super(MedianDialog, self).__init__()
        self.ui = Ui_medianDialog()
        self.ui.setupUi(self)

    def get_mask(self):
        return self.ui.comboBox.currentText()
    
    def get_checked_opcja_brzegowa(self):
        if self.ui.radioButton.isChecked():
                return self.ui.radioButton.text()
        elif self.ui.radioButton_2.isChecked():
                return self.ui.radioButton_2.text()
        elif self.ui.radioButton_3.isChecked():
                return self.ui.radioButton_3.text()
