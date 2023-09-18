import sys
sys.path.insert(0, '../src')
from FingerSpelling import FingerSpelling
from CamaraWeb import CamaraWeb
import cv2
class TestSystem():
    def __init__(self, source=None):
        self.__fingerSpelling = FingerSpelling()
        self.__camara=CamaraWeb(source)

    def testPhrase(self):
        self.__fingerSpelling.newPhrase()
        validated, img = self.__camara.getFrame()
        while(validated):
            img = cv2.flip(img, 1) #Change it in case of left hand
            finished = self.__fingerSpelling.testRun(img)
            if finished:
                # self.__fingerSpelling.printTestResult()
                # self.__fingerSpelling.newPhrase()
                pass
            validated, img = self.__camara.getFrame()
        self.__fingerSpelling.printTestResult()

    def runTest(self):
        print('Start test')
        path = '../tests/phrasesLSM/'
        self.__camara.setSource(source=path+'phrase2_720.mp4')
        self.testPhrase()


path = '../tests/phrasesLSM/'
test = TestSystem(source=path+'phrase2_720.mp4')
test.runTest()
