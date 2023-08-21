import sys
sys.path.append('../')
from HandsDetectorMP import HandsDetector
from LetterDetector import LetterDetector
from SimpleSecondsCounter import SecondCounter
from KLetterDetector import KLetterDetector
from DoubleLetterDetector import DoubleLetterDetector

class FingerSpelling():
    def __init__(self,parent=None):
        self.__phrase = ""
        self.__letterDetector = LetterDetector()
        self.__secondsCounter = SecondCounter()
        self.__kLetterDetector = KLetterDetector()
        self.__doubleLettersDetector = DoubleLetterDetector()
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

        #Check double letters
        #Post-processing

    ####################TEST MODE##############################
    def testRun(self, image):
        hand = self.__letterDetector.detect(image)
        if hand == None:
            #Hand did not detect
            self.__countLettersNotDetected += 1
            #Start counter
            if not self.__secondsCounter.isCounting():
                self.__secondsCounter.startCount()

            #Separation between words
            if self.__secondsCounter.finished(2):
                self.__phrase += ' '

            #The phrase is complete
            if self.__secondsCounter.finished(4):
                return True

            return False

        self.__secondsCounter.finishCount()
        self.__countLettersDetected += 1
        if hand.getConfidense() < 0.73:
            return False
        self.__phrase += hand.getLetter()
        if self.__kLetterDetector.detect(hand):
            print('K is detected!!!!!!!!!!!')
            self.__phrase += 'K'

        if self.__doubleLettersDetector.detect(hand):
            print('Double  letter was detected!!!')
            self.__phrase += '/' + self.__doubleLettersDetector.getLetter() + '/'
        return False

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
