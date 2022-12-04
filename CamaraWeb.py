import cv2

class CamaraWeb():
    def __init__(self):
        self.__cap = cv2.VideoCapture(2)

    def getFrame(self):
        validated, img = self.__cap.read()
        # return cv2.flip(img, 1)
        return img

    def desconectar(self):
        self.__cap.release()
