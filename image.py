import cv2
from os import path
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import numpy as np
import math
import matplotlib.pyplot as plt
from Ui.Ui_image import Ui_Image
from dialogs.error import ErrorMessage

class imageWindow(QWidget):
    last_active_window = None
    pressPos = None
    clicked = pyqtSignal()

    def __init__(self, image_path):
        super().__init__()

        self.setWindowFlag(Qt.FramelessWindowHint)

        self.ui = Ui_Image()
        self.ui.setupUi(self)

        self.image_path = image_path

        self.ui.closeBtn.clicked.connect(self.close_window)

        #load image
        self.image_cv = cv2.imread(image_path)

        #convert image to pixmap
        self.image = cv2.cvtColor(self.image_cv, cv2.COLOR_BGR2RGB)
        height, width, _ = self.image.shape
        bytesPerLine = 3 * width
        self.q_image = QImage(self.image.data, width, height, bytesPerLine, QImage.Format_RGB888)

        self.pixmap = QPixmap.fromImage(self.q_image)

        self.ui.imageLabel.setPixmap(self.pixmap)

        # set image title
        _, tail = path.split(image_path)
        image_name = tail.split('.')
        self.ui.imageTitle.setText(image_name[0])
        self.setGeometry(100, 100, self.pixmap.width(), self.pixmap.height()) 

        self._active = False
        

    def close_window(self):
        self.close()

    def get_image(self):
        return self.image

    def mousePressEvent(self, event):
        self.oldPosition = event.globalPos()
        if event.button() == Qt.LeftButton:
            self.pressPos = event.pos()

    def mouseMoveEvent(self, event):
        delta = QPoint(event.globalPos() - self.oldPosition)
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.oldPosition = event.globalPos()

    def mouseReleaseEvent(self, event):
        if (self.pressPos is not None and
            event.button() == Qt.LeftButton and
            event.pos() in self.rect()):
            self.clicked.emit()
            imageWindow.last_active_window = self
        self.pressPos = None

    def update_image(self, image):
        self.image = image
        qformat = QImage.Format_Indexed8

        if len(image.shape) == 3:
            if(image.shape[2]) == 4:
                qformat = QImage.Format_RGBA8888
            else:
                qformat = QImage.Format_RGB888
        img = QImage(image, image.shape[1], image.shape[0], image.strides[0], qformat)
        self.ui.imageLabel.setPixmap(QPixmap.fromImage(img))


    #image processing methods
    def set_to_grayscale(self):
        if len(self.image.shape) != 2:
            image = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
            self.update_image(image)  
        else:
            msg = ErrorMessage("Obraz jest już szaroodcieniowy")
            msg.exec_()

    def calculate_histogram(self):
        my_hist = np.zeros(256  )
        for h in range(self.image.shape[0]):
            for w in range(self.image.shape[1]):
                current_pixel = self.image[h,w]
                my_hist[current_pixel] += 1
        return my_hist

    def show_histogram(self):
        hist = self.calculate_histogram()
        plt.hist(self.image.ravel(),256,[0,256])
        plt.show()
        
    def red_channel_grayscale(self):
        red_channel = self.image_cv[:,:,2].astype(np.uint8)
        self.update_image(red_channel)

    def green_channel_grayscale(self):
        green_channel = self.image[:,:,1].astype(np.uint8)
        self.update_image(green_channel)

    def blue_channel_grayscale(self):
        blue_channel = self.image[:,:,0].astype(np.uint8)
        self.update_image(blue_channel)

    def convert_to_hsv(self):
        hsv_img = cv2.cvtColor(self.image_cv, cv2.COLOR_BGR2HSV)
        self.update_image(hsv_img)

    def convert_to_lab(self):
        lab = cv2.cvtColor(self.image, cv2.COLOR_RGB2LAB)
        for (name, chan) in zip(("L*", "a*", "b*"), cv2.split(lab)):
            cv2.imshow(name, chan)

    def normalizacja(self):
        im_min = np.min(self.image)
        im_max = np.max(self.image)

        new_max = 255
        new_min = 0

        img_stretch =np.zeros_like(self.image)
        for h in range(self.image.shape[0]):
            for w in range(self.image.shape[1]):
                current_pixel = self.image[h,w]
                img_stretch[h,w] = ((current_pixel-im_min)*new_max)/(im_max-im_min)
        self.update_image(img_stretch)

    def cumsum(self,a):
        a = iter(a)
        b = [next(a)]
        for i in a:
            b.append(b[-1] + i)
        return np.array(b)

    def equalizacja(self):
        hist = self.calculate_histogram()
        cs = self.cumsum(hist)
        cs_m = np.ma.masked_equal(cs,0)
        cs_min = cs_m.min()
        cs_max = cs_m.max()
        cs = ((cs - cs_min) * 255 )/ (cs_max - cs_min)
        cs = cs.astype('uint8')
        img_eq = cs[self.image]
        self.update_image(img_eq)

    def negacja(self):
        if len(self.image.shape) == 2:
            img_inv = (255-self.image)
            self.update_image(img_inv)
        else:
            msg = ErrorMessage("Obraz musi być szaroodcieniowy")
            msg.exec_()

    def posteryzacja(self):
        if len(self.image.shape) == 2:
            myPosterizeBinsNum = 8
            myBins = np.arange(0,255,np.round(255/myPosterizeBinsNum))

            img_pstrz = np.zeros_like(self.image)

            for h in range(self.image.shape[0]):
                for w in range(self.image.shape[1]):
                    current_pixel = self.image[h,w]

                    for bin in range(myPosterizeBinsNum):
                        if (current_pixel>myBins[bin]): img_pstrz[h,w]=myBins[bin]

                    if (current_pixel>myBins[-1]): img_pstrz[h,w]=255

            self.update_image(img_pstrz)
        else:
            msg = ErrorMessage("Obraz musi być szaroodcieniowy")
            msg.exec_()

    def get_opcja_brzegowa(self, opcja):
        if opcja == "Isolated":
            return cv2.BORDER_ISOLATED
        elif opcja == "Reflect":
            return cv2.BORDER_REFLECT
        elif opcja == "Replicate":
            return cv2.BORDER_REPLICATE

    def neighborhood_operation(self, operacja, opcja_brzegowa):
        match operacja:
            case "Blur":
                self.blur(opcja_brzegowa)
            case "Sobel":
                self.sobel(opcja_brzegowa)
            case "Laplacian":
                self.laplacian(opcja_brzegowa)
            case "Canny":
                self.canny(opcja_brzegowa)
            case "Wyostrzanie 1":
                mask = np.array([[ 0,-1, 0],[-1, 5,-1],[ 0,-1, 0]])
                self.wyostrzanie(mask, opcja_brzegowa)
            case "Wyostrzanie 2":
                mask = np.array([[-1,-1,-1],[-1, 9,-1],[-1,-1,-1]])
                self.wyostrzanie(mask, opcja_brzegowa)
            case "Wyostrzanie 3":
                mask = np.array([[ 1,-2, 1],[-2, 5,-2],[ 1,-2, 1]])
                self.wyostrzanie(mask, opcja_brzegowa)
            case "PrewittN":
                mask = np.array([[1,1, 1],[0, 0,0],[-1,-1, -1]])
                self.universal_mask(mask, opcja_brzegowa)
            case "PrewittS":
                mask = np.array([[ -1,-1, -1],[0, 0,0],[1,1, 1]])
                self.universal_mask(mask, opcja_brzegowa)
            case "PrewittE":
                mask = np.array([[ -1,0, 1],[-1, 0,1],[-1,0, 1]])
                self.universal_mask(mask, opcja_brzegowa)
            case "PrewittW":
                mask = np.array([[1,0, -1],[1, 0,-1],[1,0, -1]])
                self.universal_mask(mask, opcja_brzegowa)
            case "PrewittNE":
                mask = np.array([[ 0,1, 1],[-1, 0,1],[-1,-1, 0]])
                self.universal_mask(mask, opcja_brzegowa)
            case "PrewittNW":
                mask = np.array([[ 1,1, 0],[1, 0,-1],[0,-1, -1]])
                self.universal_mask(mask, opcja_brzegowa)
            case "PrewittSE":
                mask = np.array([[ -1,-1, 0],[-1, 0,1],[0,1, 1]])
                self.universal_mask(mask, opcja_brzegowa)
            case "PrewitSW":
                mask = np.array([[ 0,-1, -1],[1, 0,-1],[1,1, 0]])
                self.universal_mask(mask, opcja_brzegowa)

    def blur(self, opcja_brzegowa):
        new_img = cv2.blur(self.image, (3,3), borderType=self.get_opcja_brzegowa(opcja_brzegowa))
        self.update_image(new_img)

    def sobel(self, opcja_brzegowa):
        sobelx = cv2.Sobel(self.image,cv2.CV_64F,1,0,ksize=3, borderType=self.get_opcja_brzegowa(opcja_brzegowa))
        sobely = cv2.Sobel(self.image,cv2.CV_64F,0,1,ksize=3, borderType=self.get_opcja_brzegowa(opcja_brzegowa))
        frame_sobel = cv2.hconcat((sobelx, sobely))
        frame_sobel = cv2.convertScaleAbs(frame_sobel)
        self.update_image(frame_sobel)


    def laplacian(self, opcja_brzegowa):
        ddepth = cv2.CV_64F
        ksize = 3
        new_img = cv2.Laplacian(self.image, ddepth, ksize, borderType = self.get_opcja_brzegowa(opcja_brzegowa))
        new_img = cv2.convertScaleAbs(new_img)
        self.update_image(new_img)

    def canny(self, opcja_brzegowa):
        if opcja_brzegowa == "Isolated":
            new_img = cv2.Canny(self.image, 100, 200)
        elif opcja_brzegowa == "Reflect":
            new_img = cv2.Canny(self.image, 100, 200)
        elif opcja_brzegowa == "Replicate":
            new_img = cv2.Canny(self.image, 100, 200)
        self.update_image(new_img)


    def universal_mask(self, mask, opcja_brzegowa):
        new_img = cv2.filter2D(self.image, cv2.CV_64F, mask, borderType = self.get_opcja_brzegowa(opcja_brzegowa))
        new_img = cv2.convertScaleAbs(new_img)
        self.update_image(new_img)

    def filtr_medianowy(self, mask, opcja_brzegowa):
        rozmiar_maski = list(mask)[0]
        match(opcja_brzegowa):
            case "Isolated":
                new_img = cv2.medianBlur(self.image, int(rozmiar_maski))
            case "Reflect":
                new_img = cv2.medianBlur(self.image, int(rozmiar_maski))
            case "Replicate":
                new_img = cv2.medianBlur(self.image, int(rozmiar_maski))
        self.update_image(new_img)

    def wyostrzanie(self, mask, opcja_brzegowa):
        new_img = cv2.filter2D(self.image, cv2.CV_64F, mask, borderType = self.get_opcja_brzegowa(opcja_brzegowa))
        new_img = cv2.convertScaleAbs(new_img)
        self.update_image(new_img)
    
    def romb(self, rozmiar):
        r = int(rozmiar)
        return np.uint8(np.add.outer(*[np.r_[:r,r:-1:-1]]*2)>=r)
    
    def chosen_strel(self, element, rozmiar):
        if element == "Romb":
            return self.romb(rozmiar)
        elif element == "Kwadrat":
            return cv2.getStructuringElement(cv2.MORPH_RECT,(int(rozmiar), int(rozmiar)))
        
    def chosen_operation(self, operacja):
        match(operacja):
            case "Erozja":
                return cv2.MORPH_ERODE   
            case "Dylatacja":
                return cv2.MORPH_DILATE
            case "Zamkniecie":
                return cv2.MORPH_CLOSE
            case "Otwarcie":
                return cv2.MORPH_OPEN

    def operacja_morfologiczna(self, operacja, wybrany_element,  wybrana_opcja_brzegowa, rozmiar):
        chosen_operation = self.chosen_operation(operacja)
        element = self.chosen_strel(wybrany_element, rozmiar)
        opcja_brzegowa = self.get_opcja_brzegowa(wybrana_opcja_brzegowa)

        new_img =  cv2.morphologyEx(self.image, chosen_operation, element, borderType = opcja_brzegowa)
        self.update_image(new_img)

    def skeletonize(self):
        thinned = cv2.ximgproc.thinning(cv2.cvtColor(self.image, cv2.COLOR_RGB2GRAY))
        self.update_image(thinned)

    def threshold(self, prog):
        ret, new_img = cv2.threshold(self.image,prog,255,cv2.THRESH_BINARY)
        self.update_image(new_img)

    def adaptive_threshold(self, chosen_size):
        if len(self.image.shape) == 2:
            max_value = 255
            adaptive_method = cv2.ADAPTIVE_THRESH_MEAN_C
            threshold_type = cv2.THRESH_BINARY
            block_size = chosen_size
            new_img = cv2.adaptiveThreshold(self.image, max_value, adaptive_method, threshold_type, block_size, 5)
            self.update_image(new_img)
        else:
            msg = ErrorMessage("Obraz musi być szaroodcieniowy")
            msg.exec_()

    def otsu(self):
        if len(self.image.shape) == 2:
            blur = cv2.GaussianBlur(self.image,(5,5),0)
            ret3,th3 = cv2.threshold(blur,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
            self.update_image(th3)
        else:
            msg = ErrorMessage("Obraz musi być szaroodcieniowy")
            msg.exec_()
        
    def watershed(self):
        if len(self.image.shape) != 2:
            img_gray = cv2.cvtColor(self.image,cv2.COLOR_BGR2GRAY)
            ret2,thresh = cv2.threshold(img_gray,0,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
            kernel = np.ones((3,3),np.uint8)
            opening = cv2.morphologyEx(thresh,cv2.MORPH_OPEN,kernel, iterations = 1)

            sure_bg = cv2.dilate(opening,kernel,iterations=1)
            dist_transform = cv2.distanceTransform(opening,cv2.DIST_L2,5)

            ret, sure_fg = cv2.threshold(dist_transform,0.5*dist_transform.max(),255,0)
            sure_fg = np.uint8(sure_fg)

            unknown = cv2.subtract(sure_bg,sure_fg)
            ret, markers = cv2.connectedComponents(sure_fg)

            markers = markers+1
            markers[unknown==255] = 0

            markers2 = cv2.watershed(self.image, markers)

            img_gray[markers2 == -1] = 255
            self.image[markers2 == -1] = [255,0,0]

            print("Znaleziono "+ str(np.max(markers2)) + " obiektów.")
            new_img = cv2.applyColorMap(np.uint8(markers2*10), cv2.COLORMAP_JET)
            self.update_image(new_img)
        else:
            msg = ErrorMessage("Obraz nie może byc szaroodcieniowy")
            msg.exec_()
  
    def hough(self):
        dst = cv2.Canny(self.image, 50, 200, None, 3)
        cdst = cv2.cvtColor(dst, cv2.COLOR_GRAY2BGR)
        cdstP = np.copy(cdst)
        lines = cv2.HoughLines(dst, 1, np.pi / 180, 150, None, 0, 0)
        if lines is not None:
            for i in range(0, len(lines)):
                rho = lines[i][0][0]
                theta = lines[i][0][1]
                a = math.cos(theta)
                b = math.sin(theta)
                x0 = a * rho
                y0 = b * rho
                pt1 = (int(x0 + 1000*(-b)), int(y0 + 1000*(a)))
                pt2 = (int(x0 - 1000*(-b)), int(y0 - 1000*(a)))
                cv2.line(cdst, pt1, pt2, (0,0,255), 3, cv2.LINE_AA)

        linesP = cv2.HoughLinesP(dst, 1, np.pi / 180, 50, None, 50, 10)
        if linesP is not None:
            for i in range(0, len(linesP)):
                l = linesP[i][0]
                cv2.line(cdstP, (l[0], l[1]), (l[2], l[3]), (0,0,255), 3, cv2.LINE_AA)

        self.update_image(cdst)

    def get_image(self):
        return self.image