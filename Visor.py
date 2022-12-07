
import cv2
import numpy as np
import time

from HandsDetectorMP import HandsDetector
from CamaraWeb import CamaraWeb
from Hand import Hand
from SignDetector import SignDetector
from SimpleSecondsCounter import SecondCounter
from CleanSentence import getCleanSentence, cleanRepetitiveLetters, findCorrectWord

from PIL import Image
from time import time

from PyQt5.QtWidgets import QApplication,QMainWindow,QMessageBox
from PyQt5.uic import loadUi
from main import MainWindow

class Visor(QMainWindow):

    def __init__(self,parent=None):
        super(Visor,self).__init__(parent)
        loadUi("dactiolologia_ui.ui",self)
        self.delete_button.clicked.connect(self.deleteEditText)
        self.play_button.clicked.connect(self.playButton)

        self.__frase = ""
        self.__word = ""
        self.__count = SecondCounter()
        self.__inactiveCount = SecondCounter()

        self.__nombreVentana="Alphabet Detection"
        self.__ssd=HandsDetector()
        self.__signDetector=SignDetector()
        # self.__gui = MainWindow()
        # self.__gui.start_gui()

        cv2.namedWindow(self.__nombreVentana,cv2.WINDOW_NORMAL)
        cv2.resizeWindow(self.__nombreVentana, 920, 1020)

        #cv2.namedWindow(self.__nombreVentana2,cv2.WINDOW_NORMAL)
        #cv2.resizeWindow(self.__nombreVentana2, 700, 1020)
        self.__camara=CamaraWeb()

    def playButton(self):
        msg = self.textEdit.toPlainText()
        self.textEdit.setText("")

    def deleteEditText(self):
        self.translate.setText("")

    def iniciar(self):
        countFrame = 0
        while(True):
            # try:
                # Se recupera en frame desde la camara
            img=self.__camara.getFrame()
            img = cv2.flip(img, 1)
            # cv2.imwrite('video/frame'+str(countFrame)+'.jpg', img) #Para guardar
            hand, b, imageLandmarks =self.__ssd.handDetection(img)


            # if self.__inactiveCount.finishCount(2):
            #     if len(self.__word) > 0:
            #         self.__word = cleanRepetitiveLetters(self.__word)
            #         self.translate.setText(self.translate.toPlainText() + self.__word)
            #     self.__word = ""
            if self.__count.finished(2):
                if len(self.__word) > 0:
                    self.__word = cleanRepetitiveLetters(self.__word)
                    self.__word = findCorrectWord(self.__word)
                    self.translate.setText(self.translate.toPlainText() + self.__word+ " ")
                self.__word = ""

            if b:
                # handImage = hand.getImg()
                # if not self.__inactiveCount.isCounting():
                #     self.__inactiveCount.startCount()

                if self.__count.finishCount(2):
                    self.__frase += " "
                    # if len(self.__word) > 0:
                        # self.__word = cleanRepetitiveLetters(self.__word)
                        # self.translate.setText(self.translate.toPlainText() + self.__word)
                    # self.__word = ""
                    # if len(self.__word) > 0:
                    #     self.__word = cleanRepetitiveLetters(self.__word)
                    #     self.translate.setText(self.translate.toPlainText() + self.__word)
                    # self.__word = ""

                img = imageLandmarks
                cv2.rectangle(img,(hand.getMinX(),hand.getMinY()),(hand.getMaxX(),hand.getMaxY()),(0,255,0),2)
                # print('>>>>>>>>Landmarks', hand.getLandmarks())
                letter, sm_value = self.__signDetector.detection(hand.getLandmarks())
                sm_value = '%.4f'%(sm_value*100)
                # print('Letter=',letter)
                cv2.putText(img=img, text='Letra: '+letter+' '+sm_value+'%', org=(10, 50), fontFace=cv2.FONT_HERSHEY_TRIPLEX, fontScale=1, color=(0, 0, 255),thickness=1)
                self.__frase += letter
                self.__word += letter

                # self.translate.setText(self.__frase)
            else:
                # cv2.putText(img=img, text='Sin deteccion', org=(10, 50), fontFace=cv2.FONT_HERSHEY_TRIPLEX, fontScale=1, color=(0, 0, 255),thickness=1)
                if not self.__count.isCounting():
                    self.__count.startCount()

            # cv2.imwrite('videoLandMarks/frame'+str(countFrame)+'.jpg', img) #Para guardar
            countFrame += 1
            cv2.imshow(self.__nombreVentana,img)

            if cv2.waitKey(1) & 0xFF == ord('q'):#Metodo para salir, oprimir la letra Q del teclado
                break
            # except Exception as ex:
            #     print("ERROR GENERADO: {}".format(ex))
            #     continue


        self.finalizar()

    def finalizar(self):
        self.__camara.desconectar()
        cv2.destroyAllWindows()
        print(self.__frase.lower())
        print(getCleanSentence(self.__frase))

    def closeEvent(self,event):
        exit()

# vi = Visor()
# vi.iniciar()
