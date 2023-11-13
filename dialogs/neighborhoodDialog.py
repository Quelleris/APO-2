from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from Ui.Ui_Operacjesasiedzctwa import Ui_Dialog
import numpy as np
from dialogs.error import ErrorMessage

class NeighborhoodDialog(QDialog):
    def __init__(self):
        super(NeighborhoodDialog, self).__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.change_textField_state(True)
        self.ui.comboBox.currentTextChanged.connect(self.on_comboBox_changed)

    def change_textField_state(self, state):
            textFields = (self.ui.gridLayout.itemAt(i).widget() for i in range(self.ui.gridLayout.count())) 
            for field in textFields:
                field.setReadOnly(state)

    def on_comboBox_changed(self, value):  
        if(value == "Uniwersalna maska"):
            self.change_textField_state(False)
        else: 
            self.change_textField_state(True)

    def get_comboBox_value(self):
        return self.ui.comboBox.currentText()
    
    def get_checked_opcja_brzegowa(self):
        if self.ui.opcja_brzegowa.isChecked():
                return self.ui.opcja_brzegowa.text()
        elif self.ui.opcja_brzegowa_2.isChecked():
                return self.ui.opcja_brzegowa_2.text()
        elif self.ui.opcja_brzegowa_3.isChecked():
                return self.ui.opcja_brzegowa_3.text()
        
    def validate_mask(self):
        grid = self.ui.gridLayout
        for i in range(9):
            try:
                int(grid.itemAt(i).widget().text())
            except ValueError:
                return False
        return True
    
    def get_mask_values(self):
        grid = self.ui.gridLayout
        mask = np.zeros((3,3))
        k = 0
        if self.validate_mask():
            for i in range(3):
                for j in range(3):
                    mask[i, j] = int(grid.itemAt(k).widget().text())
                    k += 1
            return mask
        else:
            return False
    

        
