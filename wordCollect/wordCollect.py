# -*- coding: utf-8 -*-
import sys,os
sys.path.append('../statistics')
sys.path.append('../Tools')
sys.path.append('../MeCab')
import statisticsTools,Tools,mecab
import time

def generateFileLists(filepath):
	fileLists 	= []
	files		= os.listdir(filepath)
	for file in files:
		fileLists.append(filepath+file)
	return fileLists

# filepath = "/home/dream/documents/papers/code/datatest/orgin/"
# filepath 	= "/home/dream/documents/papers/code/statistics/testtxt/"
@Tools.exeTime
def generateAllWordsByMecab(fromFilePath,toFilePath):
	# filepath	= "/home/dreamer/documents/code/datatest/to2000/"
	files		= os.listdir(fromFilePath)
	fileLists 	= []
	runCounter  = 0
	for file in files:
		fileLists.append(fromFilePath+file)

	newfile 	= open(toFilePath+"allwordByMecab.txt",'wb')
	analyise	= statisticsTools.Statistics(fileLists)
	wordBoxs 	= analyise.getWordBox()
	wordlist 	= sorted(wordBoxs.items(), key=lambda d: d[1])
	for wordItem in wordlist:
		newfile.write(wordItem[0]+'\t'+str(wordItem[1])+'\n')
@Tools.exeTime
def generateAllWords(filepath,topath):
	fileCounter = 0
	# AllWords	= open(filepath + '../../afterAllwordSta/AllWords.txt','wb')
	AllWords	= open(topath+'AllWord.txt','wb')
	WordSet	= {}
	filelists   = generateFileLists(filepath)
	# print filelists
	for file in filelists:
		if fileCounter%500 == 0:
			os.system("clear")
			print "This is",fileCounter,"th file"
		fileCounter = fileCounter + 1
		fopen   = open(file,'r')
		content = fopen.read()
		wordsList   = content.split('_')
		for word in wordsList:
			if word in WordSet:
				WordSet[word] += 1
			else:
				WordSet[word] = 1
		fopen.close()
	wordlist 	= sorted(WordSet.items(), key=lambda d: d[1])
	for wordItem in wordlist:
		AllWords.write(wordItem[0]+'\t'+str(wordItem[1])+'\n')
@Tools.exeTime
def generateMecabList(allWordFileName,topath):
	allWordFile 	= open(allWordFileName,'r')
	content  		= allWordFile.read()
	lines  			= content.split('\n')
	OneFile	 = open(topath + 'OneWordsAdjacency.txt','wb')
	TwoFile	 = open(topath + 'TwoWordsAdjacency.txt','wb')
	ThreeFile   = open(topath + 'ThreeWordsAdjacency.txt','wb')
	MultiFile   = open(topath + 'MultiWordsAdjacency.txt','wb')
	AllFile  	= open(topath + 'AllWordsAdjacency.txt','wb')
	runCounter  = 0
	for line in lines:
		runCounter += 1
		if runCounter%2000 == 0:
			os.system('clear')
			print "This is the",runCounter,"th lines"
		try:
			lineEle = line.split('\t')
		except:
			continue
		word  			= lineEle[0]
		try:
			wordFreStr  	= lineEle[1]
		except:
			continue
		wordFre			= int(wordFreStr)
		if wordFre > 0:
			mec   = mecab.MeCabClass(word)
			wordbox = mec.GetAll()
			if len(wordbox) == 1:
				OneFile.write(word)
				AllFile.write(word)
				OneFile.write(":")
				AllFile.write(":")
				OneFile.write(wordbox[0]+" "+wordFreStr+'\n')
				AllFile.write(wordbox[0]+" "+wordFreStr+'\n')
			elif len(wordbox) == 2:
				TwoFile.write(word)
				TwoFile.write(":")
				TwoFile.write(wordbox[0]+' '+wordbox[1]+" "+wordFreStr+'\n')
				AllFile.write(word)
				AllFile.write(":")
				AllFile.write(wordbox[0]+' '+wordbox[1]+" "+wordFreStr+'\n')
			elif len(wordbox) == 3:
				ThreeFile.write(word)
				ThreeFile.write(":")
				ThreeFile.write(wordbox[0]+' '+wordbox[1]+' '+wordbox[2]+" "+wordFreStr+'\n')
				AllFile.write(word)
				AllFile.write(":")
				AllFile.write(wordbox[0]+' '+wordbox[1]+' '+wordbox[2]+" "+wordFreStr+'\n')
			elif len(wordbox) > 3:
				MultiFile.write(word)
				MultiFile.write(":")
				AllFile.write(word)
				AllFile.write(":")
				for index in range(len(wordbox)-1):
					MultiFile.write(wordbox[index]+' ')
					AllFile.write(wordbox[index]+' ')
				MultiFile.write(wordbox[-1]+" "+wordFreStr)
				MultiFile.write('\n')
				AllFile.write(wordbox[-1]+" "+wordFreStr)
				AllFile.write('\n')
	OneFile.close()
	TwoFile.close()
	ThreeFile.close()
	MultiFile.close()
	AllFile.close()

if __name__ == "__main__":
	pass
# fromFilePath = "/home/dreamer/documents/code/partOfSpeech/includeKeyword/"
# toFilePath   = "/home/dreamer/documents/code/partOfSpeech/allWord/"
# generateAllWordsByMecab(fromFilePath,toFilePath)
