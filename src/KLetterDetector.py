
class KLetterDetector():
    def __init__(self, pHand=None, tolerance = 0.3, MAXKFRAMES=5):
        self.__pHand = pHand #P sign
        self.__tolerance = tolerance
        self.__MAXKFRAMES = MAXKFRAMES
        self.__counter = 0
        self.__moving = False


    # def setPHand(self, pHand):
    #     self.__pHand = pHand #P sign
    #     self.__moving = True

    # def setMoving(self, moving):
    #     self.__moving = moving

    def startDetection(self, pHand):
        self.__pHand = pHand #P sign
        self.__moving = True
        # print('K detetection started')

    def stopDetection(self):
        self.__counter = 0
        self.__moving = False

    def detect(self, k):
        if not self.__moving and k.getLetter() == 'P':
            self.startDetection(k)
            return False

        if not self.__moving:
            return False

        if self.__moving and self.__counter > self.__MAXKFRAMES:
            self.stopDetection()
            return False

        p1 = (self.__pHand.getLandmarks()[8], self.__pHand.getLandmarks()[29])
        p2 = (self.__pHand.getLandmarks()[12], self.__pHand.getLandmarks()[33])
        k1 = (k.getLandmarks()[8], k.getLandmarks()[29])
        k2 = (k.getLandmarks()[12], k.getLandmarks()[33])
        t = self.__tolerance
        self.__counter += 1

        if p2[1]-p2[1]*t > k1[1] > p2[1]+p2[1]*t:#k1 ~ k2
            return False

        if k2[1]-k2[1]*t > abs(p2[1]-p1[1]) + p2[1] > k2[1]+k2[1]*t: #d(k1,k2)+k2~ ck2
            return False

        if k1[0]-k1[0]*t > p1[0] > k1[0]+k1[0]*t: #Movement in X axis:
            return False

        if k2[0]-k2[0]*t > p2[0] > k2[0]+k2[0]*t: #Movement in X axis:
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
