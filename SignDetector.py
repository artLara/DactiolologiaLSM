import tensorflow as tf
from tensorflow.keras import models
class SignDetector():
    def __init__(self):
        self.model = tf.keras.models.load_model('saved_model/alf_gray')
        self.dictOneHot = {0: 'A',
                         1: 'B',
                         2: 'C',
                         3: 'D',
                         4: 'E',
                         5: 'F',
                         6: 'G',
                         7: 'H',
                         8: 'I',
                         9: 'L',
                         10: 'M',
                         11: 'N',
                         12: 'O',
                         13: 'P',
                         14: 'Q',
                         15: 'R',
                         16: 'S',
                         17: 'T',
                         18: 'U',
                         19: 'V',
                         20: 'W',
                         21: 'X',
                         22: 'Y',
                         23: 'Z'}

    def detection(self, img):
        res = self.model.predict(img)
        # print(res)
        y_p, index_dict, sm_value = self.getClass(res, self.dictOneHot)
        return y_p, sm_value

    def getClass(self, x, dictOneHot):
        index, sm_value = self.getClassIndex(x)
        # print(ord(dictOneHot[index]) - ord('A'))
        return dictOneHot[index], index, sm_value

    def getClassIndex(self, x):
        for vector in x:
            maxValue = max(vector)
            output = []
            for index, val in enumerate(vector):
                if maxValue == val:
                    return index, maxValue

# s = SignDetector()
# print('FIn')
