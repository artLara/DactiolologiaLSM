from FingerSpelling import FingerSpelling
from CamaraWeb import CamaraWeb
class Visor():
    def __init__(self, source=None):
        self.__fingerSpelling = FingerSpelling()
        self.__camara=CamaraWeb(source)

    def start(self, testMode=False):
        validated, img = self.__camara.getFrame()
        while(validated):
            img = cv2.flip(img, 1) #Changein case of left hand
            self.__fingerSpelling.run(img, testMode)
            validated, img = self.__camara.getFrame()

path = '../tests/phrasesLSM/'
visor = Visor(source=path+'phrase_de_nada.mp4')
visor.start()
