from spellchecker import SpellChecker
spell = SpellChecker(language='es')
totalWords = 0
wordsByLen = []
for i in range(40):
    wordsByLen.append([])

for word in spell:
    #print(word)
    wordsByLen[len(word)].append(word)
    totalWords += spell[word]

def findCorrectWord(word2clean):
    validwords = []
    word_len = len(word2clean)
    #print(min(word_len,len(wordsByLen)))
    maxNumWords = 0
    for index in range(min(word_len,len(wordsByLen)), 0, -1):#recorre la lista de palabras
        for validWord in wordsByLen[index]:
            indexValidWord = 0
            indexWord2Clean = 0
            while(len(validWord)-indexValidWord<=len(word2clean)-indexWord2Clean):
                if validWord[indexValidWord] == word2clean[indexWord2Clean]:
                    indexValidWord += 1
                    if indexValidWord == len(validWord):
                        if spell[validWord] > maxNumWords:
                            maxNumWords=spell[validWord]
                        metric = len(validWord)/len(word2clean) #+ spell[validWord]/maxNumWords
                        validwords.append((validWord, metric))
                        break
                        #return validWord
                indexWord2Clean += 1

        if len(validwords) >= 5:
            break

    #for v in validwords:
        #print(v[0], v[1] + spell[v[0]]/maxNumWords*0.3)
    return max(validwords, key= lambda x: x[1] + spell[x[0]]/maxNumWords*0.3)[0]
def getCleanSentence(sentence):
    cleanSentence = ""
    words = sentence.split(" ")
    for word in words:
        if len(word) > 0:
            cleanWord = cleanRepetitiveLetters(word)
            # tmp = spell.correction(cleanWord)
            # if tmp != None:
            #     cleanSentence += tmp + " "
            # else:
            #     cleanSentence += cleanWord + " "
            cleanSentence += cleanWord + " "
    return cleanSentence

def cleanRepetitiveLetters(word):
    curryLetter = word[0]
    cleanWord = curryLetter

    for index, letter in enumerate(word):
        if index == 0:
            continue
        if curryLetter == letter:
            continue
        curryLetter = letter
        cleanWord += curryLetter

    return cleanWord.lower()
