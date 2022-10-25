import tensorflow as tf
from tensorflow.keras import models
class SignDetector():
    def __init__(self):
        self.model = tf.keras.models.load_model('saved_model_alf/alf_gray')
        self.dictOneHot = {0: 'A',
                         1: 'B',
                         2: 'C',
                         3: 'D',
                         4: 'E',
                         5: 'F',
                         6: 'G',
                         7: 'H',
                         8: 'I',
                         9: 'J',
                         10: 'K',
                         11: 'L',
                         12: 'M',
                         13: 'N',
                         14: 'O',
                         15: 'P',
                         16: 'Q',
                         17: 'R',
                         18: 'S',
                         19: 'T',
                         20: 'U',
                         21: 'V',
                         22: 'W',
                         23: 'X',
                         24: 'Y',
                         25: 'Z'}

    def detection(self, img):
        res = self.model.predict(img)
        # print(res)
        y_p, index_dict = self.getClass(res, self.dictOneHot)
        return y_p

    def getClass(self, x, dictOneHot):
        index = self.getClassIndex(x)
        # print(ord(dictOneHot[index]) - ord('A'))
        return dictOneHot[index], index

    def getClassIndex(self, x):
        for vector in x:
            maxValue = max(vector)
            output = []
            for index, val in enumerate(vector):
                if maxValue == val:
                    return index

# s = SignDetector()
# print('FIn')
