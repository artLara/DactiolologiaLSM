import sys
sys.path.insert(0, '../src')
import pandas as pd
from PhraseCleaner import PhraseCleaner
class PhraseCleanerTest():
    def __init__(self):
        self.__phraseCleaner = PhraseCleaner()

    def metric(self):
        pass

    def runTest(self):
        print('=================Testing PhraseCleaner=======================')
        df = pd.read_csv('noisePhrases/dataset.csv')
        for index in df.index:
            target = df['target'][index]
            noisePhrase = open("noisePhrases/"+df['file_name'][index], "r")
            cleanPhrase = self.__phraseCleaner.cleanSentence(noisePhrase.read())
            print(cleanPhrase)



test = PhraseCleanerTest()
test.runTest()
