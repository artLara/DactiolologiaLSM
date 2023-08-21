
class DoubleLetterDetector():
    def __init__(self, m0_hand=None, tolerance = 0.3, MAXKFRAMES=5):
        self.__m0_hand = m0_hand #P sign
        self.__tolerance = tolerance
        self.__MAXKFRAMES = MAXKFRAMES
        self.__counter = 0
        self.__moving = False
        self.__leter = ''
        a,b,c,d,e,f,g,h,i,l,m,n,o,p,r,s,t,u,v,w,y.
        self.__listOfLetters = set('A','B','C','D','E','F','G','H','I','L','M',
                                    'N','O','P','Q','R','S','T','U','V','W','Y')

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

        m1 = (self.__m1_hand.getLandmarks()[0], self.__m1_hand.getLandmarks()[21])
        p2 = (self.__m0_hand.getLandmarks()[12], self.__m0_hand.getLandmarks()[33])
        t = self.__tolerance
        self.__counter += 1

        if (m0[0] + wbb) - (m0[0] + wbb)*t > m1[0] > (m0[0] + wbb) + (m0[0] + wbb)*t:
            return False

        if m1[1]-m1[1]*t > m0[1] > m1[1]+m1[1]*t:
            return False

        self.stopDetection()
        return True
        #
        # if k2[1]-k2[1]*t <= ck1[1] <= k2[1]+k2[1]*t:#k1 ~ k2
        #     # print('Pasa 1')
        #     if ck2[1]-ck2[1]*t <= abs(k2[1]-k1[1]) + k2[1] <= ck2[1]+ck2[1]*t: #d(k1,k2)+k2~ ck2
        #         # print('Pasa 2')
        #
        #         if ck1[0]-ck1[0]*t <= k1[0] <= ck1[0]+ck1[0]*t and ck2[0]-ck2[0]*t <= k2[0] <= ck2[0]+ck2[0]*t: #Movimiento en #x:
        #             # print('Pasa 3')
        #             return True
        #
        # return False
