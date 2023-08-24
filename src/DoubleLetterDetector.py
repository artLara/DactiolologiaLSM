
class DoubleLetterDetector():
    def __init__(self, m0_hand=None, tolerance = 0.3, MAXKFRAMES=5):
        self.__m0_hand = m0_hand #P sign
        self.__tolerance = tolerance
        self.__MAXKFRAMES = MAXKFRAMES
        self.__counter = 0
        self.__moving = False
        self.__leter = ''
        self.__listOfLetters = set(['A','B','C','D','E','F','G','H','I','L','M',
                                    'N','O','P','Q','R','S','T','U','V','W','Y'])

    def getLetter(self):
        return self.__leter

    def startDetection(self, m0_hand):
        self.__m0_hand = m0_hand #P sign
        self.__moving = True
        self.__leter = m0_hand.getLetter()

    def stopDetection(self):
        self.__counter = 0
        self.__moving = False
        self.__leter = ''

    def detect(self, m1_hand):
        if not self.__moving and m1_hand.getLetter() in self.__listOfLetters:
            self.startDetection(m1_hand)
            return False

        if not self.__moving:
            return False

        if self.__moving and self.__counter > self.__MAXKFRAMES:
            self.stopDetection()
            return False

        m0 = (self.__m0_hand.getLandmarks()[0], self.__m0_hand.getLandmarks()[21])
        wbb = self.__m0_hand.getWidthBoundingBox()

        m1 = (m1_hand.getLandmarks()[0], m1_hand.getLandmarks()[21])
        t = self.__tolerance
        self.__counter += 1

        #Horizontal movement (rule 1)
        if (m0[0] + wbb) + (m0[0] + wbb)*t > m1[0]:
            return False

        #Vertical movement (rule 2)
        if m1[1]-m1[1]*t > m0[1] and m0[1] > m1[1]+m1[1]*t:
            return False

        self.stopDetection()
        return True
