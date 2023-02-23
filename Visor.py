
import cv2
import numpy as np
import time
from time import sleep
import asyncio
from threading import Thread

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
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QTimer, QEventLoop
from main import MainWindow

class Visor(QMainWindow):

    def __init__(self,parent=None):
        super(Visor,self).__init__(parent)
        loadUi("dactiolologia_ui.ui",self)
        self.delete_button.clicked.connect(self.deleteEditText)
        # self.play_button.clicked.connect(self.playButton)
        self.thread = None

        self.__frase = ""
        self.__word = ""
        self.__count = SecondCounter()
        self.__inactiveCount = SecondCounter()

        self.__nombreVentana="Alphabet Detection"
        self.__ssd=HandsDetector()
        self.__signDetector=SignDetector()
        self.__MAXKFRAMES = 5
        # self.__gui = MainWindow()
        # self.__gui.start_gui()

        cv2.namedWindow(self.__nombreVentana,cv2.WINDOW_NORMAL)
        cv2.resizeWindow(self.__nombreVentana, 920, 1020)

        #cv2.namedWindow(self.__nombreVentana2,cv2.WINDOW_NORMAL)
        #cv2.resizeWindow(self.__nombreVentana2, 700, 1020)
        self.__camara=CamaraWeb()

    # def spanish2lsm(self, sentence):
    #     for word in sentence.split(" "):
    #         for letter in word:
    #             counterAux = SecondCounter()
    #             counterAux.startCount()
    #             self.pixmap = QPixmap('ImagenesAbecedario/'+letter+'.jpg')
    #             # adding image to label
    #             self.image_sign.setPixmap(self.pixmap)
    #
    #             sleep(1)
    #             # await asyncio.sleep(1)
    #             # loop = QEventLoop()
    #             # QTimer.singleShot(2000, loop.quit)
    #             # loop.exec_()
    #
    # def playButton(self):
    #     msg = self.textEdit.toPlainText()
    #     # self.thread = Thread(target=self.spanish2lsm, args=msg)
    #     # self.thread.start()
    #     # self.thread.join()
    #     # self.spanish2lsm(msg)
    #     self.textEdit.setText("")

    def deleteEditText(self):
        self.translate.setText("")

    def iniciar(self):
        countFrame = 0
        p_moving = False
        k1 = (0,0)
        k2 = (0,0)

        k_counter = self.__MAXKFRAMES
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

            if b:#Se detecta una mano
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
                # print(hand.getLandmarks())
                if letter == 'P' and not p_moving:
                    k1 = (hand.getLandmarksRaw()[0][8], hand.getLandmarksRaw()[0][29])
                    k2 = (hand.getLandmarksRaw()[0][12], hand.getLandmarksRaw()[0][33])
                    # print(k1,k2)
                    # print('Buscando K')
                    p_moving = True

                if p_moving and k_counter > 0:
                    c_k1 = (hand.getLandmarksRaw()[0][8], hand.getLandmarksRaw()[0][29])
                    c_k2 = (hand.getLandmarksRaw()[0][12], hand.getLandmarksRaw()[0][33])

                    if self.detectK(k1,k2,c_k1,c_k2):
                        self.__word = 'K'
                        print('K IS DETECTED!!!!!!!!!!!!!!!!!!!!!!!!')
                        p_moving = False
                        k_counter = self.__MAXKFRAMES
                    else:
                        k_counter -= 1
                else:
                    p_moving = False
                    k_counter = self.__MAXKFRAMES

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

    def detectK(self,k1,k2,ck1,ck2):
        t = 0.3 #Tolerancia de error
        # print('k1=',k1,'k2=',k2)
        # print('ck1=',ck1,'ck2=',ck2)

        if k2[1]-k2[1]*t <= ck1[1] <= k2[1]+k2[1]*t:#k1 ~ k2
            # print('Pasa 1')
            if ck2[1]-ck2[1]*t <= abs(k2[1]-k1[1]) + k2[1] <= ck2[1]+ck2[1]*t: #d(k1,k2)+k2~ ck2
                # print('Pasa 2')

                if ck1[0]-ck1[0]*t <= k1[0] <= ck1[0]+ck1[0]*t and ck2[0]-ck2[0]*t <= k2[0] <= ck2[0]+ck2[0]*t: #Movimiento en #x:
                    # print('Pasa 3')
                    return True

        return False
    def finalizar(self):
        self.__camara.desconectar()
        cv2.destroyAllWindows()
        print(self.__frase.lower())
        print(getCleanSentence(self.__frase))

    def closeEvent(self,event):
        exit()

# vi = Visor()
# vi.iniciar()
