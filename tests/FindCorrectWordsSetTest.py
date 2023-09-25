import sys
sys.path.insert(0, '../src')
from PhraseCleaner import PhraseCleaner

class FindCorrectWordsSetTest():
	"""
	This file run the test for evaluate each algorithm which find the correct posible set of words.
	"""
	def __init__(self, pathOfObjectDirectory='../bin/similarWords/'):
		self.__phraseCleaner = PhraseCleaner()
		self.__MAX_CARDINALITY_SET = 7

	def runTest(self, path='noiseTextWords/'):
		#Load targets
		textFile = open(path + "cleanWords.txt","r")
		cleanWords = []
		for word in textFile.readlines():
			cleanWords.append(word)
		textFile.close()

		generalCounts = {} #Dcitionary for storage results
		for randomLettersRate in np.arange(0.1,1.1,0.1): #Iterate every letter rates
			randomLettersRate = round(randomLettersRate,1)
			for maxRandoms in range(1,8): #Iterate every letter randoms
				textFile = open(path + "noiseWords{}_{}.txt".format(randomLettersRate, maxRandoms),"r")
				print('Testing FindCorrectWordsSet {}_{}'.format(randomLettersRate, maxRandoms))
				count = 0
				for indexWord, word in enumerate(textFile.readlines()): #Iterate every noise word in the file loaded
					wordsSet = self.__phraseCleaner.findCorrectWord(word, self.__MAX_CARDINALITY_SET)
					for indexList, possibleWord in enumerate(wordsSet): #Iterate elements of the set found
						if cleanWords[indexWord] == possibleWord[0]:
							for i in range(indexList, self.__MAX_CARDINALITY_SET-1):
								"""
								The method return the biggest set posible, so it is not necesary compute
								with every possible cardinality
								"""
								generalCounts['{}_{}_{}'.format(randomLettersRate, maxRandoms,i+1)] += 1
							break
					# print('x={} wordsSet{}'.format(x, wordsSet))

					count += 1                
					if count % 100 == 0:
						print('{} de {}'.format(count, len(cleanWords)))
						break
				textFile.close()

				for cardinality in range(1,self.__MAX_CARDINALITY_SET):
					file1 = open(path+"generalCountsText.txt", "a")  # append mode
					tmpCount = generalCounts['{}_{}_{}'.format(randomLettersRate, maxRandoms,cardinality)]
					tmp = 'TotalCounts {}_{}_{}={}\n'.format(randomLettersRate, maxRandoms,cardinality,tmpCount)
					# print(tmp)
					file1.write(tmp)
					file1.close()
					print('Accuracy {}_{}_{}={}'.format(randomLettersRate, maxRandoms,cardinality,tmpCount/len(cleanWords)))
					break
				break
			break


test = FindCorrectWordsSetTest()
test.runTest()