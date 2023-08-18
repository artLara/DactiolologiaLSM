


from HandsDetectorMP import HandsDetector
from LetterDetector import LetterDetector

class FingerSpelling():
    def __init__(self,parent=None):
        self.__phrase = ""
        self.__letterDetector = LetterDetector()
        self.__secondsCounter = None
        self.__doubleLettersDetector = None
        self.__phraseCleaner = None

    def run(self, image):
        self.__letterDetector.detect(image)
