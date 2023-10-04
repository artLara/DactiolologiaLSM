import numpy as np
import pickle as pkl
class SpellingCorrectionTrajectory():
    def __init__(self,coordenatesOrd=None, sizeTable=20):
        self.__sizeTable = sizeTable
        self.__confidenceIoU = 0.5
        if coordenatesOrd == None:
            #Load from file
            with open('../bin/spellingCorrectionTrajectory/coordenatesOrd.pkl', 'rb') as handle:
                coordenatesOrd = pkl.load(handle)

        self.__coordenatesOrd = coordenatesOrd

    def findCorrectWord(self, word2clean):
        pass

    def compareWords(self, word1, word2):
        table1 = self.makeTableTrajectories(word1)
        table2 = self.makeTableTrajectories(word2)
        intersection = np.logical_and(table1, table2).sum()
        union = np.logical_or(table1, table2).sum()
        iou = intersection/union
        print('IoU=',iou)
        return iou

    def __linealFunction(self, m, p, x):
        return int(m*x - m*p[0] + p[1])

    def calculateTrajectory(self, c1, c2):
        p1 = None
        p2 = None
        if c1[0] < c2[0]:
            p1 = c1
            p2 = c2
        else:
            p1 = c2
            p2 = c1

        m = (p1[1]-p2[1]) / (p1[0]-p2[0])
        trajectory = []
        for x in range(p1[0], max(p2[0], p2[1])+1):
            y = self.__linealFunction(m, p1, x)
            trajectory.append((x, y))
            if (x, y) == p2:
                break

        return trajectory

    def drawTrayectory(self, table, coordenates, start, end, verbose=False):
        trajectory = self.calculateTrajectory(coordenates[start], coordenates[end])
        if verbose:
            print('Trajectory:',start,'->', end)
            print(trajectory)
        for i,j in trajectory:
            table[i][j] = start

    def makeTableTrajectories(self, word):
        table = [[0 for _ in range(self.__sizeTable)] for _ in range(self.__sizeTable)]
        tableN = np.asarray(table)
        tokens = self.tokenizer(word)
        # print(tokens)
        index = 0
        while(index < len(tokens)-1):
            self.drawTrayectory(table, self.__coordenatesOrd, tokens[index], tokens[index+1])
            index += 1

        return table

    def replaceAccents(self, c):
        if c == 'á':
            c = 'a'

        if c == 'é':
            c = 'e'

        if c == 'í':
            c = 'i'

        if c == 'ó':
            c = 'o'

        if c == 'ú':
            c = 'u'

        if c == 'ü':
            c = 'u'

        return c

    def tokenizer(self, word):
        tokens = []
        index = 0
        while index < len(word):
            if index < len(word)-1 and word[index] == word[index+1]:
                tmp = ord(self.replaceAccents(word[index])) + ord(self.replaceAccents(word[index]))
                tokens.append(tmp)
                index += 2
                continue
            tmp = ord(self.replaceAccents(word[index]))
            tokens.append(self.replaceAccents(tmp))
            index += 1

        return tokens

    def printTable(self, table):
        for i in range(len(table)):
            for j in range(len(table)):
                print('{}\t'.format(table[i][j]), end=' ')
            print('')

st = SpellingCorrectionTrajectory()
# st.printTable(st.makeTableTrajectories('perro'))
# st.printTable(st.makeTableTrajectories('cerro'))
st.compareWords('perro', 'cerro')
st.compareWords('perro', 'erro')
st.compareWords('que', 'hue')
