import os
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from image import imageWindow
from Ui.ui_aboutDialog import Ui_aboutDialog
from dialogs.neighborhoodDialog import NeighborhoodDialog
from dialogs.medianDialog import MedianDialog
from Ui.Ui_mainWindow import Ui_MainWindow
from dialogs.morfologiaDialog import MorfologiaDialog
from dialogs.threshold import ThresholdDialog
from dialogs.adaptiveThresholdDialog import AdaptiveThresholdDialog
from dialogs.error import ErrorMessage
from PIL import Image


class MainWindow(QMainWindow):
    count = 0
    def __init__(self):
        super(MainWindow, self).__init__()

        #UI
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.show()

        self.windows = []

        #Connect functions to buttons
        self.ui.actionO_programie.triggered.connect(self.open_about_dialog)
        self.ui.actionOtworz.triggered.connect(self.open_file)
        self.ui.actionZapisz.triggered.connect(self.save_image)
        self.ui.actionKonwersja_do_obrazu_szaroodcieniowego.triggered.connect(self.convert_grayscale)
        self.ui.actionHistogram.triggered.connect(self.show_histogram)
        self.ui.action3_kanaly_szaroodcieniowe.triggered.connect(self.three_channels_grayscale)
        self.ui.actionDuplikuj.triggered.connect(self.duplicate)
        self.ui.actionKonwersja_RGB_do_HSV.triggered.connect(self.convert_to_hsv)
        self.ui.actionKonwersja_RGB_do_Lab.triggered.connect(self.convert_to_lab)
        self.ui.actionNormalizacja.triggered.connect(self.normalizacja)
        self.ui.actionEqualizacja.triggered.connect(self.equalizacja)
        self.ui.actionNegacja.triggered.connect(self.negacja)
        self.ui.actionPosteryzacja.triggered.connect(self.posteryzacja)
        self.ui.actionOperacje_sasiectwa.triggered.connect(self.open_neighborhood_dialog)
        self.ui.actionFiltr_Medianowy.triggered.connect(self.filtr_medianowy)
        self.ui.actionOperacje_morfologiczne.triggered.connect(self.open_morfologiaDialog)
        self.ui.actionSzkieletyzacja.triggered.connect(self.szkieletyzacja)
        self.ui.actionHough.triggered.connect(self.hough)
        self.ui.actionThresholding.triggered.connect(self.open_threshold_dialog)
        self.ui.actionAdaptive_Thresholding.triggered.connect(self.open_adaptive_threshold_dialog)
        self.ui.actionProgowanie_metod_Otsu.triggered.connect(self.otsu)
        self.ui.actionWatershed.triggered.connect(self.watershed)

    #Functions
    def open_file(self):
        file_filter = 'Image (*.bmp *.jpg *.png)'
        image_path = QFileDialog.getOpenFileName(
            parent=self,
            caption='Wybierz obraz',
            directory=os.getcwd(),
            filter=file_filter
        )
        if image_path[0]:
            self.open_window(image_path[0])

    def open_window(self, image_path):
        MainWindow.count = MainWindow.count + 1
        image = imageWindow(image_path)
        self.windows.append(image)
        imageWindow.last_active_window = image
        image.show()
        return image

    def get_selected_image(self):
        if self.windows:
            return self.windows[0].last_active_window
        else: return False
    
    def open_about_dialog(self):
        self.dialog = QDialog()
        self.ui = Ui_aboutDialog()
        self.ui.setupUi(self.dialog)
        self.dialog.exec_()

    def save_image(self):
        if self.get_selected_image():
            file_path, _ = QFileDialog.getSaveFileName(self, "Save Image", "",
                            "PNG(*.png);;JPEG(*.jpg *.jpeg);;")
        
            if file_path == "":
                return
            
            arr = self.get_selected_image().get_image()
            arr_to_image = Image.fromarray(arr)
            arr_to_image.save(file_path)

    def duplicate(self):
        if self.get_selected_image():
            image = self.get_selected_image().get_image()
            duplicate = self.open_window(self.get_selected_image().image_path)
            duplicate.update_image(image)


    def convert_grayscale(self):
        if self.get_selected_image():
            self.get_selected_image().set_to_grayscale()

    def show_histogram(self):
        if self.get_selected_image():
            self.get_selected_image().show_histogram() 

    def convert_to_hsv(self):
        if self.get_selected_image():
            image1 = self.open_window(self.get_selected_image().image_path)
            image2 = self.open_window(self.get_selected_image().image_path)
            image3 = self.open_window(self.get_selected_image().image_path)
            image1.convert_to_hsv()
            image2.convert_to_hsv()
            image3.convert_to_hsv()
            image1.red_channel_grayscale()
            image2.green_channel_grayscale()
            image3.blue_channel_grayscale()

    def convert_to_lab(self):
        if self.get_selected_image():
            self.get_selected_image().convert_to_lab()
        
    def three_channels_grayscale(self):
        if self.get_selected_image():
            image1 = self.open_window(self.get_selected_image().image_path)
            image2 = self.open_window(self.get_selected_image().image_path)
            image3 = self.open_window(self.get_selected_image().image_path)
            image1.red_channel_grayscale()
            image2.green_channel_grayscale()
            image3.blue_channel_grayscale()

    def normalizacja(self):
        if self.get_selected_image():
            self.get_selected_image().normalizacja()

    def equalizacja(self):
        if self.get_selected_image():
            self.get_selected_image().equalizacja()

    def negacja(self):
        if self.get_selected_image():
            self.get_selected_image().negacja()

    def posteryzacja(self):
        if self.get_selected_image():
            self.get_selected_image().posteryzacja()

    def open_neighborhood_dialog(self):
        if self.get_selected_image():
            dialog = NeighborhoodDialog()
            if dialog.exec_():
                if dialog.ui.comboBox.currentText() == "Uniwersalna maska":
                    mask = dialog.get_mask_values()  
                    if isinstance(mask, bool):
                        msg = ErrorMessage("nieprawidłowa maska")
                        msg.exec_()
                       
                    else:
                        self.get_selected_image().universal_mask(
                            dialog.get_mask_values(), 
                            dialog.get_checked_opcja_brzegowa()
                            )
                else:
                    operacja = dialog.get_comboBox_value()
                    opcja_brzegowa = dialog.get_checked_opcja_brzegowa()
                    self.get_selected_image().neighborhood_operation(
                        operacja, opcja_brzegowa
                        )      
            
    def filtr_medianowy(self):
        if self.get_selected_image():
            dialog = MedianDialog()
            if dialog.exec_():
                mask = dialog.get_mask()
                opcja_brzegowa = dialog.get_checked_opcja_brzegowa()
                self.get_selected_image().filtr_medianowy(mask, opcja_brzegowa)

    def open_morfologiaDialog(self):
        if self.get_selected_image():
            dialog = MorfologiaDialog()
            if dialog.exec_():
                self.get_selected_image().operacja_morfologiczna(
                    dialog.get_operacja(), 
                    dialog.get_element_strukturalny(),
                    dialog.get_opcja_brzegowa(),
                    dialog.get_rozmiar()
                )

    def szkieletyzacja(self):
        if self.get_selected_image():
            self.get_selected_image().skeletonize()

    def open_threshold_dialog(self):
        if self.get_selected_image():
            dialog = ThresholdDialog()
            if dialog.exec_():
                self.get_selected_image().threshold(dialog.get_prog())

    def open_adaptive_threshold_dialog(self):
        if self.get_selected_image():
            dialog = AdaptiveThresholdDialog()
            if dialog.exec_():
                self.get_selected_image().adaptive_threshold(dialog.get_slider_value())

    def otsu(self):
        if self.get_selected_image():
            self.get_selected_image().otsu()

    def watershed(self):
        if self.get_selected_image():
            self.get_selected_image().watershed()

    def hough(self):
        if self.get_selected_image():
            self.get_selected_image().hough()

    # zamknięcie wszystkich okien przed zamknięciem main window 
    def closeEvent(self, event):
        for window in self.windows:
            window.close()
        event.accept()