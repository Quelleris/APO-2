from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from Ui.Ui_threshoding import Ui_thresholdingDialog

class ThresholdDialog(QDialog):
    def __init__(self):
        super(ThresholdDialog, self).__init__()
        self.ui = Ui_thresholdingDialog()
        self.ui.setupUi(self)
        self.ui.Hs_prog.valueChanged.connect(self.update_label)

    def update_label(self, value):
        self.ui.slider_value_label.setText(str(value))

    def get_prog(self):
        return self.ui.Hs_prog.value()
    
    

    # Tu dodać opcję podglądu obrazu z threshold