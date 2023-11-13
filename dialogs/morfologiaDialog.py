from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from Ui.Ui_morfologiaDialog import Ui_MorfologiaDialog

class MorfologiaDialog(QDialog):
    def __init__(self):
        super(MorfologiaDialog, self).__init__()
        self.ui = Ui_MorfologiaDialog()
        self.ui.setupUi(self)

    def get_operacja(self):
        return self.ui.Cb_operation.currentText()
    
    def get_element_strukturalny(self):
        if self.ui.Rbtn_elem1.isChecked():
                return self.ui.Rbtn_elem1.text()
        elif self.ui.Rbtn_elem2.isChecked():
                return self.ui.Rbtn_elem2.text()
        
    def get_opcja_brzegowa(self):
            if self.ui.Rbtn_option1.isChecked():
                return self.ui.Rbtn_option1.text()
            elif self.ui.Rbtn_option2.isChecked():
                return self.ui.Rbtn_option2.text()
            elif self.ui.Rbtn_option3.isChecked():
                return self.ui.Rbtn_option3.text()
            
    def get_rozmiar(self):
        rozmiar = self.ui.Cb_size.currentText()
        return list(rozmiar)[0]
