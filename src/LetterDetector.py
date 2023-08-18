from HandsDetectorMP import HandsDetector
from SignClassification import SignClassification

class LetterDetector():
    def __init__(self,parent=None):
        self.__handDetector = HandsDetector()
        self.__signClassification = SignClassification()

    def detect(self, image):
        handDetected = self.__handDetector.detect(image)
        # If a image contains a hand and it's detected by MP
        if handDetected != None:
            #Propagation thruoght neural network
            letter, sm_confidense = self.__signClassification.classification(handDetected.getLandmarksNormalized())
            handDetected.setLetter(letter)
            handDetected.setConfidense(sm_confidense)
            return handDetected

        #Return None when MP didn't detect a hand
        # print('Hand did not detect :(')
        return None
