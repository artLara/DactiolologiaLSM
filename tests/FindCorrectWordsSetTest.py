import sys
sys.path.insert(0, '../src')
from PhraseCleaner import PhraseCleaner
import numpy as np
class FindCorrectWordsSetTest():
	"""
	This file run the test for evaluate each algorithm which find the correct posible set of words.
	"""
	def __init__(self):
		self.__phraseCleaner = PhraseCleaner()
		self.__MAX_CARDINALITY_SET = 7

	def writeInFile(self, path, file_name, text):
		textFile = open(path + file_name + ".txt", "a")  # append mode
		textFile.write(text)
		textFile.close()

	def runTest(self, startLoop, endLoop, path2save='noiseTextWordsResult/', path='noiseTextWords/'):
		#Load targets
		textFile = open(path + "cleanWords.txt","r")
		cleanWords = []
		for word in textFile.readlines():
			cleanWords.append(word)
		textFile.close()

		generalCounts = {} #Dcitionary for storage results
		for randomLettersRate in np.arange(0.1,1.1,0.1):
			randomLettersRate = round(randomLettersRate,1)
			for maxRandoms in range(1,8):
				for cardinality in range(1,self.__MAX_CARDINALITY_SET):
					generalCounts['{}_{}_{}'.format(randomLettersRate, maxRandoms,cardinality)] = 0

		generalCountsSym = {} #Dcitionary for storage results
		for randomLettersRate in np.arange(0.1,1.1,0.1):
			randomLettersRate = round(randomLettersRate,1)
			for maxRandoms in range(1,8):
				generalCountsSym['{}_{}'.format(randomLettersRate, maxRandoms)] = 0

		generalCountsUnion = {} #Dcitionary for storage results
		for randomLettersRate in np.arange(0.1,1.1,0.1):
			randomLettersRate = round(randomLettersRate,1)
			for maxRandoms in range(1,8):
				for cardinality in range(1,self.__MAX_CARDINALITY_SET):
					generalCountsUnion['{}_{}_{}'.format(randomLettersRate, maxRandoms,cardinality)] = 0


		for randomLettersRate in np.arange(startLoop, endLoop, 0.1): #Iterate every letter rates
			randomLettersRate = round(randomLettersRate, 1)
			for maxRandoms in range(1, 8): #Iterate every letter randoms
				textFile = open(path + "noiseWords{}_{}.txt".format(randomLettersRate, maxRandoms),"r")
				print('Testing FindCorrectWordsSet {}_{}'.format(randomLettersRate, maxRandoms))
				count = 0
				for indexWord, word in enumerate(textFile.readlines()): #Iterate every noise word in the file loaded
					target = cleanWords[indexWord].strip()
					#Find correct algorithm
					wordsSet1 = self.__phraseCleaner.findCorrectWord(word, self.__MAX_CARDINALITY_SET)
					for indexList, possibleWord in enumerate(wordsSet1): #Iterate elements of the set found
						if target == possibleWord[0]:
							for i in range(indexList, self.__MAX_CARDINALITY_SET-1):
								"""
								The method return the biggest set posible, so it is not necesary compute
								with every possible cardinality
								"""
								generalCounts['{}_{}_{}'.format(randomLettersRate, maxRandoms,i+1)] += 1
							break

					#SymSpell algorithm
					wordsSet2 = self.__phraseCleaner.symSpell(word)
					for indexList, possibleWord in enumerate(wordsSet2): #Iterate elements of the set found
						if target == possibleWord[0]:
							"""
							The method return the Leivintah-- distance equals to 2, so de cardinality does not has sense
							"""
							generalCountsSym['{}_{}'.format(randomLettersRate, maxRandoms)] += 1
							break

					#Union of sets
					for indexList, possibleWord in enumerate(wordsSet1): #Iterate elements of the set found
						if target == possibleWord[0] or target in wordsSet2:
							for i in range(indexList, self.__MAX_CARDINALITY_SET-1):
								"""
								The method return the biggest set posible, so it is not necesary compute
								with every possible cardinality
								"""
								generalCountsUnion['{}_{}_{}'.format(randomLettersRate, maxRandoms,i+1)] += 1
							break

					# print('x={} wordsSet{}'.format(x, wordsSet))

					count += 1
					if count % 10000 == 0:
						print('{} de {}===={}%'.format(count, len(cleanWords), count/len(cleanWords)*100))
						# break
				textFile.close()

				#Write in files
				tmpCount = generalCountsSym['{}_{}'.format(randomLettersRate, maxRandoms)]
				tmp = 'Accuracy {}_{}={}\n'.format(randomLettersRate, maxRandoms,tmpCount)
				self.writeInFile(path2save, "accuracySym", tmp)
				for cardinality in range(1,self.__MAX_CARDINALITY_SET):
					tmpCount = generalCounts['{}_{}_{}'.format(randomLettersRate, maxRandoms,cardinality)]
					tmp = 'Accuracy {}_{}_{}={}\n'.format(randomLettersRate, maxRandoms,cardinality,tmpCount)
					self.writeInFile(path2save, "accuracyFindAlg", tmp)

					tmpCount = generalCountsUnion['{}_{}_{}'.format(randomLettersRate, maxRandoms,cardinality)]
					tmp = 'Accuracy {}_{}_{}={}\n'.format(randomLettersRate, maxRandoms,cardinality,tmpCount)
					self.writeInFile(path2save, "accuracyUnion", tmp)

					# print('Accuracy {}_{}_{}={}'.format(randomLettersRate, maxRandoms,cardinality,tmpCount/len(cleanWords)))
					# break
				# break
			# break

path2save = sys.argv[1]
startLoop = float(sys.argv[2])
endLoop = float(sys.argv[3])

test = FindCorrectWordsSetTest()
test.runTest(startLoop=startLoop, endLoop=endLoop, path2save=path2save)
