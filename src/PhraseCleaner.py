from spellchecker import SpellChecker
from WordsSelector import WordsSelector
class PhraseCleaner():
    def __init__(self):
        self.__maxOptWords = 5
        self.__vocabByLen = self.loadVocabulary()
        self.__wordsSelector = WordsSelector()

    def loadVocabulary(self):
        self.__spell = SpellChecker(language='es')
        vocabByLen = []
        for i in range(100):
            vocabByLen.append([])

        for word in self.__spell:
            vocabByLen[len(word)].append(word)

        return vocabByLen

    def findCorrectWord(self, word2clean, maxOptWords=None):
        if maxOptWords == None:
            maxOptWords = self.__maxOptWords

        validwords = [] #Array of clean words
        maxNumWords = 0
        for index in range(min(len(word2clean),len(self.__vocabByLen)), 0, -1):#iterate vocabulary by len from the longest to smallest
            for validWord in self.__vocabByLen[index]: #Iterate words with the same longitud
                indexValidWord = 0
                indexWord2Clean = 0
                while(len(validWord)-indexValidWord<=len(word2clean)-indexWord2Clean): #Check every letter by positition
                    if validWord[indexValidWord] == word2clean[indexWord2Clean]:
                        indexValidWord += 1
                        if indexValidWord == len(validWord):
                            if self.__spell[validWord] > maxNumWords:
                                maxNumWords=self.__spell[validWord]
                            metric = len(validWord)/len(word2clean) #+ self.__spell[validWord]/maxNumWords
                            metric += self.__spell[validWord]/maxNumWords*0.3 #MOdificado aquiiiiiii
                            validwords.append((validWord, metric))
                            break
                    indexWord2Clean += 1

            if len(validwords) >= maxOptWords: #Modificar para un largo definido y mateices rectangulares
                break

        if len(validwords) < maxOptWords: #For return square matrices
            for _ in range(len(validwords),maxOptWords):
                validwords.append(('-', -1))

        return sorted(validwords, key= lambda x: x[1] , reverse=True)[:maxOptWords]
        # return max(validwords, key= lambda x: x[1] + self.__spell[x[0]]/maxNumWords*0.3)[0]

    def cleanSentence(self, phrase):
        words = []
        for word in phrase.split(' '):
            if word == ' ' or word == '':
                continue

            tmp = self.cleanRepetitiveLetters(word).strip()

            if tmp == ' ' or tmp == '':
                continue

            words.append(tmp)

        cleanWordsSet = []
        # print(words)
        for word in words:
            tmp = self.findCorrectWord(word)
            # print(tmp)
            cleanWordsSet.append(tmp)

        return ' '.join(words)

    def cleanRepetitiveLetters(self, word):
        curryLetter = word[0]
        cleanWord = curryLetter
        index = 0
        letter = word[index]

        while index < len(word)-1:
            index += 1
            letter = word[index]
            if index == 0:
                continue
            if curryLetter == letter:
                continue
            if letter == '/':
                index += 1
                cleanWord += word[index]
                cleanWord += word[index]
                curryLetter = word[index]
                index += 2
                continue

            curryLetter = letter
            cleanWord += curryLetter

        return cleanWord.lower()
