# -*- coding: utf-8 -*-
from __future__ import division
import re
import os
import sys
sys.path.append('../Mecab')
import mecab
import math


def loadDataTest():
	global mailLists
	global mailIndex
	mailLists		= []
	mailIndex		= []
	mailListFile	= open("./mailListFile.txt")
	mailContents	= mailListFile.read()
	mailConOrg		= re.split('>',mailContents)
	for mail in mailConOrg:
		mailList 	= re.split(':',mail)
		mailLists.append(mailList[1])
		if re.search("\w",mailList[0]).group() == "0":
			mailIndex.append(0)
		elif re.search("\w",mailList[0]).group() == "1":
			mailIndex.append(1)
		else:
			print "error"
			return

def addWordToDict(word,dict):
	if word not in dict:
		dict[word]	= 1
	else:
		dict[word]	= dict[word] + 1

def createVocabList():
	global mailLists
	global mailIndex
	global spamPro
	global ordPro
	global spamNum
	global ordNum
	spamPro		= 0
	ordPro	 	= 0
	spamDict	= {}
	ordDict		= {}
	spamNum 	= 0
	ordNum		= 0
	for n in range(len(mailLists)):
		wordInMail	= mecab.MeCabClass(mailLists[n])
		NounWords	= wordInMail.GetNoun2()
		AdjWords	= wordInMail.GetAdj()
		if mailIndex[n] == 1:
			for noun in NounWords:
				ordNum		= ordNum + 1
				addWordToDict(noun,ordDict)
			for adj in AdjWords:
				ordNum		= ordNum + 1
				addWordToDict(adj,ordDict)
		if mailIndex[n] == 0:
			for noun in NounWords:
				spamNum		= spamNum + 1
				addWordToDict(noun,spamDict)
			for adj in AdjWords:
				spamNum		= spamNum + 1
				addWordToDict(adj,spamDict)

	spamPro 	= float(spamNum/(spamNum + ordNum))
	ordPro		= float(ordNum/(spamNum + ordNum))
	return spamDict,ordDict

def isSpamMail(mail,spamDict,ordDict):
	global spamPro
	global ordPro
	global spamNum
	global ordNum
	wordBox		= {}
	wordsNum	= 0
	wordInMail	= mecab.MeCabClass(mail)
	NounWords	= wordInMail.GetNoun2()
	AdjWords	= wordInMail.GetAdj()
	for noun in NounWords:
		addWordToDict(noun,wordBox)
		wordsNum = wordsNum + 1
	for adj in AdjWords:
		addWordToDict(adj,wordBox)
		wordsNum = wordsNum + 1

	spam 		= 1
	ordinary 	= 1
	#begin to get probility of per features
	print len(wordBox)
	for key in wordBox:
		if key not in spamDict:
			spam 		= spam 	* (0.5/spamNum)**(10/len(wordBox))
		else:
			spam 		= spam 	* (spamDict[key]/spamNum)**(10/len(wordBox))

		if key not in ordDict:
			ordinary	= ordinary 	* (0.5/ordNum) **(10/len(wordBox))
		else:
			ordinary	= ordinary 	* (ordDict[key] /ordNum) **(10/len(wordBox))

	spam 	= spamPro*spam
	ordinary 	= ordPro*ordinary
	print "spam: ",spam
	print "ordinary: ",ordinary
	if spam > ordinary:
		return True
	else:
		return False

global mailLists
global mailIndex
loadDataTest()
spamDict,ordDict 		= createVocabList()
content 				= "それから、もう一つ申します。これは、時間の都合でもう一つ申します。今、積立金というのは、積み立てておくということがなぜ必要なのかということをはっきりさせていただくことだと思う。なぜかというと、今、積立金は積もりに積もって残高百四十兆になっております。百四十兆。ただごとでない額なんですが、これは毎年給付額の大体五倍弱になっているんじゃないでしょうか。そうすると、この積み立ての中身というのが実は問題なんです。"
if isSpamMail(content,spamDict,ordDict):
	print "is spam"
else:
	print "is ordinary"
