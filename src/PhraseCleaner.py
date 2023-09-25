from spellchecker import SpellChecker
from WordsSelector import WordsSelector
from symspellpy import SymSpell, Verbosity

class PhraseCleaner():
    def __init__(self, maxOptWords=5):
        self.__maxOptWords = maxOptWords
        self.__maxFrecuency = None
        self.__spell = SpellChecker(language='es')
        self.__vocabByLen = self.loadVocabulary()
        self.__wordsSelector = WordsSelector()
        self.__symSpell = SymSpell()
        self.__symSpell.load_dictionary('../bin/dictionaries/es-100l.txt', 0, 1)

    def loadVocabulary(self):
        vocabByLen = []
        for i in range(100):
            vocabByLen.append([])

        for word in self.__spell:
            vocabByLen[len(word)].append(word)
            if self.__spell[word] > self.__maxFrecuency:
               self.__maxFrecuency = self.__spell[word]  

        return vocabByLen

    def findCorrectWord(self, word2clean, maxOptWords=None):
        if maxOptWords == None:
            maxOptWords = self.__maxOptWords

        validwords = set()#Array of clean words
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
                            # metric += self.__spell[validWord]/maxNumWords*0.3 #MOdificado aquiiiiiii
                            metric += self.__spell[validWord]/self.__maxFrecuency*0.3 #MOdificado aquiiiiiii

                            validwords.add((validWord, metric))
                            break
                    indexWord2Clean += 1

            if len(validwords) >= maxOptWords: #Modificar para un largo definido y mateices rectangulares
                break

        return validwords
        # if len(validwords) < maxOptWords: #For return square matrices
        #     for _ in range(len(validwords),maxOptWords):
        #         validwords.append(('-', -1))

        # return sorted(validwords, key= lambda x: x[1] , reverse=True)[:maxOptWords]
        # return max(validwords, key= lambda x: x[1] + self.__spell[x[0]]/maxNumWords*0.3)[0]

    def symSpell(self, word2clean, maxOptWords=None):
        validwords = set()
        suggestions = sym_spell.lookup(word2clean, Verbosity.CLOSEST,
                               max_edit_distance=2, include_unknown=True)

        for suggestion in suggestions:
            validWord = suggestion.term
            metric = len(validWord)/len(word2clean) #+ self.__spell[validWord]/maxNumWords
            metric += self.__spell[validWord]/self.__maxFrecuency*0.3 #MOdificado aquiiiiiii
            validwords.add((validWord, metric))

        return validwords

    def cleanSentence(self, phrase):
        if maxOptWords == None:
            maxOptWords = self.__maxOptWords
            
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
        # print('Word sets:')
        for word in words:
            set1 = self.findCorrectWord(word)
            set2 = self.symSpell(word)
            validwords = list(set1 | set2)
            for _ in range(len(validwords), self.__maxOptWords): #For square matrix
                validwords.append(('-', -1))
        
            validwords = sorted(validwords, key= lambda x: x[1] , reverse=True)[:self.__maxOptWords]
            # print(tmp)
            cleanWordsSet.append(validwords)

        words = self.__wordsSelector.getPhrase(cleanWordsSet, selector='contextGraph')
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
