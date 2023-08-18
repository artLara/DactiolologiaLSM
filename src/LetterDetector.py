from HandsDetectorMP import HandsDetector
class LetterDetector():
    def __init__(self,parent=None):
        self.__handDetector = HandsDetector()

    def detect(self, image):
        handDetected = self.__handDetector.detect(image)
        # If a image contains a hand and it's detected by MP
        if handDetected != None:
            #Propagation thruoght neural network
            print('Hand detected!')
            return handDetected

        #Return None when MP didn't detect a hand
        print('Hand did not detect :(')
        return None
