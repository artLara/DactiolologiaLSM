from FingerSpelling import FingerSpelling
from CamaraWeb import CamaraWeb
class Visor():
    def __init__(self, source=None):
        self.__fingerSpelling = FingerSpelling()
        self.__camara=CamaraWeb(source)

    def start(self):
        validated, img = self.__camara.getFrame()
        while(validated):
            img = cv2.flip(img, 1) #Changein case of left hand
            self.__fingerSpelling.run(img)
            validated, img = self.__camara.getFrame()

visor = Visor(source='pathVideos')
visor.start()
