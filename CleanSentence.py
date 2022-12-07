from spellchecker import SpellChecker
spell = SpellChecker(language='es')

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
