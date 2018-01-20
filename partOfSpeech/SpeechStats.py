# -*- coding: utf-8 -*-
from __future__ import division
import sys
sys.path.append('../Mecab')
sys.path.append('../Tools')
import mecab,Tools
import re,os
import random,math
import traceback
from scipy import stats

#从文本中提取出来的最初的那些相连词汇-二元相连词汇【所有】
global TwoCooccurFile
TwoCooccurFile   = "/home/dreamer/documents/code/partOfSpeech/allWord/TwoWordsMecabList.txt"
#从文本中提取出来的最初的那些相连词汇-三元相连词汇【所有】
global ThreeCooccurFile
ThreeCooccurFile = '/home/dreamer/documents/code/partOfSpeech/allWord/ThreeWordsMecabList.txt'
global AllWordFile
AllWordFile   = "/home/dreamer/documents/code/partOfSpeech/allWord/allwordByMecab.txt"

def speechStats1():
	global TwoCooccurFile
	global ThreeCooccurFile
	# TwoWordList	 = Tools.content_wordList(TwoCooccurFile,':')
	TwoWordList	 = Tools.content_wordList(ThreeCooccurFile,':')
	allSpeech	   = set()
	allSpeechTuple = {}
	for word in TwoWordList:
		thisWordMec	= mecab.MeCabClass(word)
		thisSpeechs = thisWordMec.GetAll3()
		try:
			thisSpeech  = thisSpeechs[0]
			for n in range(len(thisSpeechs)-1):
				thisSpeech += "+"+thisSpeechs[n+1]
				allSpeech.add(thisSpeech)
		except:
			pass
		allSpeechTuple.setdefault(thisSpeech,[]).append(word)

	SpeechCntTuple = {}
	for speech in allSpeechTuple.keys():
		SpeechCntTuple[speech] = len(allSpeechTuple[speech])

	sortedList		  = Tools.TupleSort(SpeechCntTuple)
	Speech	  = []
	SpeechCnt	  = []

	Cnt = 0
	for ele in sortedList:
		Cnt+= 1
		print Cnt,':',ele[0],':\t',ele[1]
		Speech.append(Cnt)
		SpeechCnt.append(ele[1])

	Tools.plot(Speech,SpeechCnt)

def speechStats2():
	global TwoCooccurFile
	global ThreeCooccurFile
	# lines	 = Tools.content_lines(TwoCooccurFile)
	wordListFre = Tools.content_scoreList(TwoCooccurFile,[':',' '])
	wordList = Tools.content_wordList(TwoCooccurFile,':')
	allSpeech	   = set()
	allSpeechTuple = {}
	allSpeechTuple2 = {}
	for n in range(len(wordList)-1):
		# print wordList[n],wordListFre[n]
		thisWordMec	= mecab.MeCabClass(wordList[n])
		thisSpeechs = thisWordMec.GetAll3()
		try:
			thisSpeech  = thisSpeechs[0]
		except:
			pass
		for x in range(len(thisSpeechs)-1):
			thisSpeech += "+"+thisSpeechs[x+1]
		try:
			if thisSpeech in allSpeechTuple.keys():
				allSpeechTuple2[thisSpeech] += wordListFre[n]
				allSpeechTuple[thisSpeech] += 1

			else:
				allSpeechTuple2[thisSpeech] = wordListFre[n]
				allSpeechTuple[thisSpeech] = 1
		except:
			print n,wordList[n]

	sortedList		  = Tools.TupleSort(allSpeechTuple2)
	Speech	  = []
	SpeechCnt	  = []

	Cnt = 0
	for ele in sortedList:
		Cnt+= 1
		# print Cnt,':',ele[0],' ',ele[1]
		# print ele[0],'\t',ele[1]
		Speech.append(Cnt)
		SpeechCnt.append(ele[1])

	title = "Part_of_speech-frequence distribution"
	Tools.plot(Speech,SpeechCnt,title,xlabel="Part of speech",ylabel="frequence")

def binomial(k,n,x):
	return stats.binom.pmf(k,n,x)

def GetConnPro():
	global TwoCooccurFile
	global ThreeCooccurFile
	TwoWordList	 = Tools.content_wordList(TwoCooccurFile,':')
	TwoWordCntlist	  = Tools.content_scoreList(TwoCooccurFile,[':',' '])
	# print len(AllWordList),len(AllWordCntlist),len(TwoWordList),len(TwoWordCntlist)
	# print AllWordList[-1],AllWordCntlist[-1],TwoWordList[-1],TwoWordCntlist[-1]
	TwoWordCnt = 0
	for Cnt in TwoWordCntlist:
		TwoWordCnt += Cnt

	OneWordSpeechTuple	  = {}
	TwoWordSpeechTuple	  = {}

	# print key
	for n in range(len(TwoWordList)):
		thisWordMec	= mecab.MeCabClass(TwoWordList[n])
		thisSpeechs = thisWordMec.GetAll3()
		thisSpeech  = thisSpeechs[0] + "+" + thisSpeechs[1]

		if thisSpeechs[0] in OneWordSpeechTuple:
			OneWordSpeechTuple[thisSpeechs[0]] += TwoWordCntlist[n]
		else:
			OneWordSpeechTuple[thisSpeechs[0]] = TwoWordCntlist[n]

		if thisSpeechs[1] in OneWordSpeechTuple:
			OneWordSpeechTuple[thisSpeechs[1]] += TwoWordCntlist[n]
		else:
			OneWordSpeechTuple[thisSpeechs[1]] = TwoWordCntlist[n]

		if thisSpeech in TwoWordSpeechTuple:
			TwoWordSpeechTuple[thisSpeech] += TwoWordCntlist[n]
		else:
			TwoWordSpeechTuple[thisSpeech] = TwoWordCntlist[n]

	# for key in TwoWordSpeechTuple.keys():
	#	 # TwoWordSpeechTuple[key] = float(TwoWordSpeechTuple[key])/float(TwoWordCnt)
	#	 print key,TwoWordSpeechTuple[key]
	# for key in OneWordSpeechTuple.keys():
	#	 # OneWordSpeechTuple[key] = float(OneWordSpeechTuple[key])/float(TwoWordCnt*2)
	#	 print key,OneWordSpeechTuple[key]

	TwoWordConnTuple = {}
	for key in TwoWordSpeechTuple.keys():
		try:
			a = key.split('+')[0]
			b = key.split('+')[1]
		except:
			print key
		try:
			c1				= OneWordSpeechTuple[a]
			c2				= OneWordSpeechTuple[b]
		except:
			return
		c12				= TwoWordSpeechTuple[key]
		p  				= float(c2)/float(TwoWordCnt*2)
		p1  			= float(c12)/float(c1)
		p2  			= float((c2 - c12))/float((TwoWordCnt*2 - c1))
		try:
			score  			= math.log(binomial(c12,c1,p))  + math.log(binomial(c2-c12,TwoWordCnt*2-c1,p)) \
							- math.log(binomial(c12,c1,p1)) - math.log(binomial(c2-c12,TwoWordCnt*2-c1,p2))
			# TwoWordConnTuple[key].write(wholeWord+'\t:'+subword1+' '+str(c1)+'\t:'+subword2+' '+str(c2)+'\t:'+str(c12)+'\t:'+str(score)+'\n')
			TwoWordConnTuple[key]  	= score
		except:
			# traceback.print_exc()
			# TwoScoreRecord.write(wholeWord+'\t:'+subword1+' '+str(c1)+'\t:'+subword2+' '+str(c2)+'\t:'+str(c12)+'\t:'+str(-9999)+'\n')
			TwoWordConnTuple[key]  	= -9999


	TwoWordConnList = Tools.TupleSort(TwoWordConnTuple)
	Speech	  = []
	SpeechCnt	  = []
	Cnt = 0
	for ele in TwoWordConnList:
		Cnt+= 1
		print Cnt,':',ele[0],ele[1],TwoWordSpeechTuple[ele[0]]
		Speech.append(Cnt)
		SpeechCnt.append(ele[1])

	Tools.plot(Speech,SpeechCnt)


# GetConnPro()
speechStats2()
