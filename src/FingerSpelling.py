import sys
sys.path.append('../')
from HandsDetectorMP import HandsDetector
from LetterDetector import LetterDetector

class FingerSpelling():
    def __init__(self,parent=None):
        self.__phrase = ""
        self.__letterDetector = LetterDetector()
        self.__secondsCounter = None
        self.__doubleLettersDetector = None
        self.__phraseCleaner = None
        self.__secuenceHands = []

        ####Test mode####
        self.__countLettersDetected = 0
        self.__countLettersNotDetected = 0

    def newPhrase(self):
        self.__phrase = ""

        ####Test mode####
        self.__countLettersDetected = 0
        self.__countLettersNotDetected = 0

    def run(self, image, testMode):
        if testMode:
            testRun(testMode)
        hand = self.__letterDetector.detect(image)
        if hand != None:
            self.__phrase += hand.getLetter()

        #Check K letter
        #Check double letters
        #Post-processing

    ####################TEST MODE##############################
    def testRun(self, image):
        hand = self.__letterDetector.detect(image)
        if hand != None:
            self.__countLettersDetected += 1
            self.__phrase += hand.getLetter()
            return
        self.__countLettersNotDetected += 1

    def loadConfig(self):
        # Load configuration of test from JSON file
        pass

    def printTestResult(self, printConfig=False):
        if printConfig:
            # Print configuration used
            pass

        print('Total of frames:', self.__countLettersNotDetected + self.__countLettersDetected)
        print('Hands detect:', self.__countLettersDetected)
        print('Hands did not detect:', self.__countLettersNotDetected)
        print('Phrase:', self.__phrase)
