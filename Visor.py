
import cv2
import numpy as np
import time

from HandsDetectorMP import HandsDetector
from CamaraWeb import CamaraWeb
from Hand import Hand
from SignDetector import SignDetector

from PIL import Image
from time import time
class Visor():

    def __init__(self):
        self.__nombreVentana="Alphabet Detection"
        self.__ssd=HandsDetector()
        self.__signDetector=SignDetector()

        cv2.namedWindow(self.__nombreVentana,cv2.WINDOW_NORMAL)
        cv2.resizeWindow(self.__nombreVentana, 700, 1020)

        #cv2.namedWindow(self.__nombreVentana2,cv2.WINDOW_NORMAL)
        #cv2.resizeWindow(self.__nombreVentana2, 700, 1020)
        self.__camara=CamaraWeb()
        self.iniciar()


    def iniciar(self):
        countFrame = 0
        while(True):
            # try:
                # Se recupera en frame desde la camara
            img=self.__camara.getFrame()

            hand, b, imageLandmarks =self.__ssd.handDetection(img)
            if b:
                handImage = hand.getImg()
                img = imageLandmarks
                cv2.rectangle(img,(hand.getMinX(),hand.getMinY()),(hand.getMaxX(),hand.getMaxY()),(0,255,0),2)
                letter = self.__signDetector.detection(handImage)

                # print('Letter=',letter)
                cv2.putText(img=img, text='Letra: '+letter, org=(10, 50), fontFace=cv2.FONT_HERSHEY_TRIPLEX, fontScale=1, color=(0, 255, 0),thickness=1)

            else:
                cv2.putText(img=img, text='Sin deteccion', org=(10, 50), fontFace=cv2.FONT_HERSHEY_TRIPLEX, fontScale=1, color=(0, 255, 0),thickness=1)

            cv2.imwrite('videoLandMarks/frame'+str(countFrame)+'.jpg', img)
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

vi = Visor()
vi.iniciar()
