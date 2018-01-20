# -*- coding: utf-8 -*-
from __future__ import division
import math
import os,sys,time,re
sys.path.append('../Tools')
import Tools,traceback
import numpy as np
def generateFileLists(filepath):
	fileLists	 = []
	files		= os.listdir(filepath)
	for file in files:
		fileLists.append(filepath+file)
	return fileLists

def entropy(probabilityList):
	result	  = 0
	for one in probabilityList:
		if one == 0:
			continue
		result  += -one*math.log(one,2)
	return result

def var(wordFrelist):
	sumC = sum(wordFrelist)
	aver = sumC/len(wordFrelist)
	varrance = 0
	for i in wordFrelist:
		varrance += pow((i-aver),2)
	return varrance/sumC
def entropyAmongFiles(allwordTxt, nounFilePath,tofile):
	fopen	   = open(allwordTxt,'r')
	content	 = fopen.read()
	lines	   = content.split('\n')
	entropyAmFiles = open(tofile,'wb')
	wordProTuple = {}

	runCounter  = 0
	startTime		  = time.time()
	files   = generateFileLists(nounFilePath)
	for line in lines:
		if runCounter%10 == 0:
			os.system('clear')
			print "This is the",runCounter,"th lines"
			endTime		  = time.time()
			print "Run time is:",endTime-startTime
			startTime		  = time.time()
		runCounter	  += 1
		# thisFileWordCnt = 0
		try:
			word	= line.split(':')[0]
			try:
				wordCnt = int(line.split(':')[1].split(' ')[-1])
			except:
				print 1,line
			wordProList  = []
			allThisWordCnt = 0
			for file in files:
				thisFile	= open(file,'r')
				thisContent = thisFile.read()
				thisFile.close()
				thisFileWordCnt = len(re.findall('_'+word+'_',thisContent))
				thisFileWordCnt += len(re.findall('^'+word+'_',thisContent))
				# thisFileWordCnt = len(re.findall(word,thisContent))
				wordProList.append(thisFileWordCnt)
				allThisWordCnt += thisFileWordCnt
			# if allThisWordCnt == 0:
			# print word,allThisWordCnt
			for n in range(len(wordProList)):
				# wordProList[n] = math.log(wordCnt)*wordProList[n]/allThisWordCnt
				wordProList[n] = wordProList[n]/allThisWordCnt
			entropyAmFiles.write(word+'\t:'+str(entropy(wordProList))+'\n')
		except:
			traceback.print_exc()
			continue
	entropyAmFiles.close()

def entropyAmongWords(allwordTxt, afterSpeechFile,tofilename):
	afterSpeech	  = open(afterSpeechFile, 'r')
	lines			  = afterSpeech.read().split('\n')
	suffixWordsSet  = set()
	for line in lines:
		try:
			suffixWord	 = line.split(':')[-1].split(' ')[-2]
		except:
			print line
		if suffixWord not in suffixWordsSet:
			suffixWordsSet.add(suffixWord)
	afterSpeech.close()

	wordProVectorTuple  = {}
	suffixwordDict	  = {}
	allwordfile	  = open(allwordTxt,'r')
	allwords		  = allwordfile.read().split('\n')
	allwordfile.close()

	runCounter  = 0
	tofile = open(tofilename,'wb')
	for suffixWord in suffixWordsSet:
		runCounter += 1
		if runCounter%100 == 0:
			os.system('clear')
			print "This is the",runCounter,"th lines"
		suffixWordCnt		  = 0
		freVector			  = []
		proVector			  = []
		wordWhichSuffixIsThisword = []
		for wordline in allwords:
			try:
				wordlineAttr	  = wordline.split(':')[1].split(' ')
			except:
				print wordline
			if len(wordlineAttr) > 2 and wordlineAttr[-2] == suffixWord:
				wordWhichSuffixIsThisword.append(wordline.split(':')[0])
				freVector.append(int(wordlineAttr[-1]))
				suffixWordCnt += int(wordlineAttr[-1])
		for x in freVector:
			proVector.append(x/suffixWordCnt)
		wordProVectorTuple[suffixWord]  = entropy(proVector)
		suffixwordDict[suffixWord]	  = wordWhichSuffixIsThisword

	wordProVectorlist	= sorted(wordProVectorTuple.items(), key=lambda d: d[1])
	for ele in wordProVectorlist:
		tofile.write(ele[0]+':'+str(ele[1])+'\n')
		for word in suffixwordDict[ele[0]]:
			tofile.write(word+' ')
		tofile.write('\n')
	tofile.close()
	# for word in wordProVectorTuple.keys():
	#	 for
	#	 proVector	  =
# entropy([1/3,1/3,1/3,0,0])

def entropyAmongClasses(allwordTxt, classesPath,tofile):
	fopen	   = open(allwordTxt,'r')
	content	 = fopen.read()
	lines	   = content.split('\n')
	entropyAmFiles = open(tofile,'wb')
	wordProTuple = {}

	runCounter  = 0
	startTime		  = time.time()
	files   = generateFileLists(classesPath)
	for line in lines:
		if runCounter%10 == 0:
			os.system('clear')
			print "This is the",runCounter,"th lines"
			endTime		  = time.time()
			print "Run time is:",endTime-startTime
			startTime		  = time.time()
		runCounter	  += 1
		# thisFileWordCnt = 0
		try:
			word	= line.split('\t:')[0]
			wordProList  = []
			allThisWordCnt = 0
			for file in files:
				thisFile	= open(file,'r')
				thisContent = thisFile.read()
				thisFile.close()
				thisFileWordCnt = len(re.findall(word,thisContent))
				cntInClass = thisFileWordCnt
				allThisWordCnt += thisFileWordCnt
				wordProList.append(cntInClass)
			wordFreList = wordProList
			for n in range(len(wordProList)):
				# wordProList[n] = math.log(wordCnt)*wordProList[n]/allThisWordCnt
				wordProList[n] = wordProList[n]/allThisWordCnt
			entropyAmFiles.write(word+'\t:'+str(entropy(wordProList))+'\t:'+str(var(wordFreList))+'\n')
		except:
			# traceback.print_exc()
			print 'wrong:',word,allThisWordCnt
			continue
	entropyAmFiles.close()
# 类间分布熵
def relativeWordFrequency_entropyAmongClass():
	x = np.linspace(0,1,200)
	# x1 = np.linspace(0,1,200)
	y = np.zeros(200)
	entroyList = []
	for n in range(len(x)):
		proList = []
		proList.append(x[n])
		for i in range(17):
			proList.append((1-x[n])/17)
		entroyList.append(entropy(proList))
	maxE = max(entroyList)
	for n in range(len(x)):
		entroyList = []
		entroyList.append(x[n])
		for i in range(17):
			entroyList.append((1-x[n])/17)
		y[n] = 1-entropy(entroyList)/(maxE + 0.0001)
	title = "relativeWordFrequency_entropyAmongClass"
	Tools.plot(x,y,title)
# 类内分布熵，用一个很小的值代替概率向量中为零的部分，看分布
def relativeWordFrequency_entropyAmongFile():
	x = np.linspace(1,101,100)
	y = np.zeros(100)
	allPro	  = 1
	entroyList = []
	for n in range(len(x)):
		proList = []
		for j in range(n):
			proList.append(allPro/n)
		for i in range(100-n):
			proList.append(0)
		entroyList.append(entropy(proList))
	for n in range(len(x)):
		y[n] = entroyList[n]
	title = "distribution entropy function graph"
	xlabel = " Uniform distribution in x documents"
	ylabel = " entropy of Q"
	filepath = "/home/dreamer/documents/code/distributionEntropy/"
	Tools.plot(x,y,title,xlabel=xlabel,ylabel=ylabel,filepath=filepath,show=1)
def compare_freEquelentropy_entropy(tofile,tofile2):
	word1s = Tools.content_lines(tofile)
	word2s = Tools.content_lines(tofile2)
	wordSet1 = set()
	wordSet2 = set()
	for n in range(500):
		wordSet1.add(word1s[n].split('\t:')[0])
		# print word1s[n].split('\t:')[0]
		wordSet2.add(word2s[n].split('\t:')[0])
	a = wordSet1  &  wordSet2
	for key in wordSet2-wordSet1:
		print key

# def random_split(pre,pre_w):
#	 split -b ....k pre_w
#	 ....k = filesize of pre
if __name__ == "__main__":
	relativeWordFrequency_entropyAmongFile()
	pass
	# allwordTxt = "/home/dreamer/documents/code/database/2000-2002/7finalword/SortedFinalword2.txt"
	# classesPath = "/home/dreamer/documents/code/distributionEntropy/classes/"
	# tofile = "/home/dreamer/documents/code/distributionEntropy/elimiate_wordList.txt"
	# entropyAmongClasses(allwordTxt, classesPath,tofile)
