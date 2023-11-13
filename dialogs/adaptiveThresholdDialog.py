from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from Ui.Ui_AdaptiveThresholdingDialog import Ui_AdaptiveThresholdDialog

class AdaptiveThresholdDialog(QDialog):
    def __init__(self):
        super(AdaptiveThresholdDialog, self).__init__()
        self.ui = Ui_AdaptiveThresholdDialog()
        self.ui.setupUi(self)
        self.ui.Hs_rozmiar.valueChanged.connect(self.update_label)

    def update_label(self, value):
        if self.ui.Hs_rozmiar.value() % 2 == 0:
            self.ui.Hs_rozmiar.setValue(self.get_slider_value() + 1)
        else: self.ui.slider_value_label.setText(str(value))

    def get_slider_value(self):
        return self.ui.Hs_rozmiar.value()
    
    