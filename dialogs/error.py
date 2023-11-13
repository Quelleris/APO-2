from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

class ErrorMessage(QMessageBox):
    def __init__(self, message):
        super(ErrorMessage, self).__init__()
        self.setIcon(QMessageBox.Information)
        self.setText(message)
        self.setWindowTitle("Ups!")