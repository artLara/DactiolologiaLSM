import sys
sys.path.append('../')
import cv2
from os import remove
import numpy as np

class Hand():
    def __init__(self,id=None):
        # self.__img= np.zeros((500, 500, 3), dtype=np.uint8)
        self.__img= None
        self.__imgR=None
        self.__coordenadas=[]
        self.__minY=0
        self.__minX=0
        self.__maxX=0
        self.__maxY=0
        self.__alto=None
        self.__ancho=None
        self.__landmarks=None
        self.__landmarksRaw = None


    def getImg(self):
        return self.__img
    def getMinX(self):
        return self.__minX
    def getMaxX(self):
        return self.__maxX
    def getMinY(self):
        return self.__minY
    def getMaxY(self):
        return self.__maxY
    def getAlto(self):
        return self.__alto
    def getAncho(self):
        return self.__ancho
    def getCoordenadas(self):
        return self.__coordenadas
    def getLandmarks(self):
        return self.__landmarks
    def getLandmarksRaw(self):
        return self.__landmarksRaw

    ####### SETTERS
    def setImg(self,img):
        self.__img=img
    def setMinX(self, d):
        self.__minX = d
    def setMinY(self, d):
        self.__minY = d
    def setMaxX(self, d):
        self.__maxX = d
    def setMaxY(self, d):
        self.__maxY = d
    def setAlto(self,alto):
        self.__alto=alto
    def setAncho(self,ancho):
        self.__ancho=ancho
    def setCoordenadas(self,coordenadas):
        self.__coordenadas=coordenadas
    def setLandMarks(self, d):
        self.__landmarks = d
    def setLandMarksRaw(self, d):
        self.__landmarksRaw = d
