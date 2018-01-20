# -*- coding: utf-8 -*-
import sys
sys.path.append('../Mecab')
sys.path.append('../Tools')
import mecab,Tools
import re,os
import random
import traceback
def speech(filename,newfile,threshold):
	oneWordList  = Tools.content_wordList(filename,':')
	wordListFre = Tools.content_scoreList(filename,[':',' '])
	# print len(oneWordList),len(WordsFreList)
	allSpeech	  = set()
	allSpeechTuple = {}
	SpeechWordsFreTup = {}
	for n in range(len(oneWordList)):
		# try:
		# thisWord	= oneWord.split(':')[0]
		thisWord	= oneWordList[n]
		thisWordMec	= mecab.MeCabClass(thisWord)
		thisSpeechs = thisWordMec.GetAll3()
		try:
			thisSpeech  = thisSpeechs[0]
			for x in range(len(thisSpeechs)-1):
				thisSpeech += "+"+thisSpeechs[x+1]
				allSpeech.add(thisSpeech)
		except:
			pass
		# if thisWord not in allSpeechTuple[thisSpeech]:
		allSpeechTuple.setdefault(thisSpeech,[]).append(thisWord)
		# try:
		if thisSpeech in SpeechWordsFreTup.keys():
			SpeechWordsFreTup[thisSpeech] += wordListFre[n]
		else:
			SpeechWordsFreTup[thisSpeech] = wordListFre[n]

	newfile = open(newfile,'wb')
	for speech in allSpeechTuple.keys():
		if SpeechWordsFreTup[speech] > threshold:
			newfile.write(speech+':'+str(SpeechWordsFreTup[speech])+':\n')
			if SpeechWordsFreTup[speech] > 300:
				for n in range(300):
					try:
						x = random.randint(0, len(allSpeechTuple)-1)
						newfile.write(allSpeechTuple[speech][x]+' ')
					except:
						pass
						continue
			else:
				for word in allSpeechTuple[speech]:
					newfile.write(word+' ')
			newfile.write('\n\n')
	newfile.close()

	# newfile2 = open('allSpeechs2.txt','wb')
	# for a in allSpeech:
	#	 try:
	#		 newfile2.write(a+' '+str(len(allSpeechTuple[a]))+'\n')
	#	 except:
	#		 print a
	# newfile2.close()
	print len(allSpeech)

def usefulSpeech(filename,recordFile):
	fopen	   = open(filename, 'r')
	content	 = fopen.read()
	paras	   = content.split('\n\n')
	TwousefulSpeech = []
	ThreeusefulSpeech = []
	ThreeuselessSpeech = []
	for para in paras:
		attr	= para.split('\n')[0].split(':')
		try:
			if int(attr[-1]) == 1:
				if len(attr[0].split('+')) == 2:
					TwousefulSpeech.append(attr[0])
				elif len(attr[0].split('+')) == 3:
					ThreeusefulSpeech.append(attr[0])
			elif int(attr[-1]) == 2:
				if len(attr[0].split('+')) == 3:
					ThreeuselessSpeech.append(attr[0])
		except:
			continue
	record		 = open(recordFile,'wb')
	record.write("useful2:")
	for a in TwousefulSpeech:
		record.write(a+" ")
	record.write('\n')

	record.write("useful3:")
	for a in ThreeusefulSpeech:
		record.write(a+" ")
	record.write('\n')

	record.write("useless3:")
	for a in ThreeuselessSpeech:
		record.write(a+" ")
	record.write('\n')

	record.close()
	fopen.close()

def getusefulSpeechListFromFile(speechRecord):
	speechRecordFile		= open(speechRecord, 'r')

	TwousefulSpeechList	 = []
	speechRecordCont		= speechRecordFile.read()
	TwousefulSpeechs		= speechRecordCont.split('\n')[0].split(':')[-1].split(' ')
	for speech in TwousefulSpeechs:
		if speech != '':
			TwousefulSpeechList.append(speech)
	ThreeusefulSpeechList	 = []
	ThreeusefulSpeechs		= speechRecordCont.split('\n')[1].split(':')[-1].split(' ')
	for speech in ThreeusefulSpeechs:
		if speech != '':
			ThreeusefulSpeechList.append(speech)
	return TwousefulSpeechList,ThreeusefulSpeechList

def divideIntoUseAndUnuse(TwoWordsMecabList, ThreeWordsMecabList,topath):
	TwoWordsMecabListFile   = open(TwoWordsMecabList, 'r')
	ThreeWordsMecabListFile = open(ThreeWordsMecabList, 'r')
	# MultiWordsMecabListFile = open(MultiWordsMecabList, 'r')

	TwousefulSpeechList	 = Tools.content_wordList("/home/dreamer/documents/code/database/condition/SpeechUseful2.txt",'\t')
	ThreeusefulSpeechList   = Tools.content_wordList("/home/dreamer/documents/code/database/condition/SpeechUseful3.txt",' \t')

	TwoUsefulFileName   = topath+"TwoWordsAdjacency_afterSpeech.txt"
	ThreeUsefulFile	 = topath+"ThreeWordsAdjacency_afterSpeech.txt"

	TwoUsefulFile = open(TwoUsefulFileName, 'wb')
	ThreeUsefulFile = open(ThreeUsefulFile, 'wb')

	TwoWordsContent	 = TwoWordsMecabListFile.read()
	TwoWordSet		  = set()
	oneWordList = TwoWordsContent.split('\n')
	allSpeechTuple2 = {}
	for oneWord in oneWordList:
		if oneWord == '':
			continue
		thisWord	= oneWord.split(':')[0]
		TwoWordSet.add(thisWord)
		thisWordMec	= mecab.MeCabClass(thisWord)
		thisSpeechs = thisWordMec.GetAll3()
		try:
			thisSpeech  = thisSpeechs[0]
			for n in range(len(thisSpeechs)-1):
				thisSpeech += "+"+thisSpeechs[n+1]
			if thisSpeech in TwousefulSpeechList:
				TwoUsefulFile.write(oneWord+'\n')
		except:
			pass

	ThreeWordsContent	 = ThreeWordsMecabListFile.read()
	WordList3 = ThreeWordsContent.split('\n')
	allSpeechTuple3 = {}
	for oneWord in WordList3:
		if oneWord == '':
			continue
		thisWord	= oneWord.split(':')[0]
		thisWordMec	= mecab.MeCabClass(thisWord)
		thisSpeechs = thisWordMec.GetAll3()
		try:
			thisSpeech  = thisSpeechs[0]
			for n in range(len(thisSpeechs)-1):
				thisSpeech += "+"+thisSpeechs[n+1]
			if thisSpeech in ThreeusefulSpeechList:
				ThreeUsefulFile.write(oneWord+'\n')
			else:
				pass
		except:
			traceback.print_exc()
			continue


	TwoWordsMecabListFile.close()
	ThreeWordsMecabListFile.close()

	TwoUsefulFile.close()
	ThreeUsefulFile.close()

def DuplicateRemoval(filename):
	fopen	   = open(filename, 'r')
	content	 = fopen.read()
	oneWordList = content.split('\n')
	allSpeech	  = set()
	allSpeechTuple = {}
	wordTuple = {}
	for oneWord in oneWordList:
		# thisWord	= oneWord.split(':')[0]
		thisWord	= oneWord
		try:
			if thisWord in wordTuple.keys():
				wordTuple[thisWord] += int(oneWord.split(':')[1].split(' ')[-1])
			else:
				wordTuple[thisWord] = int(oneWord.split(':')[1].split(' ')[-1])
		except:
			traceback.print_exception()


	newfilename = filename[:-4]+"_DuplicateRemoval.txt"
	newfile = open(newfilename,'wb')
	wordList =  Tools.TupleSort(wordTuple)
	for word in wordList:
		# print word
		thisWordMec	= mecab.MeCabClass(word[0])
		thisSpeechs = thisWordMec.GetAll()
		newfile.write(word[0]+':')
		for subword in thisSpeechs:
			newfile.write(subword+' ')
		newfile.write(str(wordTuple[word[0]])+'\n')
	newfile.close()


# TwoallWord = "/home/dreamer/documents/code/partOfSpeech/allWord/TwoWordsMecabList.txt"
# newfile = "/home/dreamer/documents/code/partOfSpeech/allSpeech/speechAndWords2.txt"

# speech(TwoallWord, newfile,50)
# speech(TwoallWord, newfile,1000)

# usefulSpeech('./allSpeech/speechAndWords2.txt','./allSpeech/speechRecord.txt')
# TwoWordsMecabList = './allWord/TwoWordsMecabList.txt'
# ThreeWordsMecabList = './allWord/ThreeWordsMecabList.txt'
# speechRecord = './allSpeech/speechRecord.txt'
if __name__ == "__main__":
	TwoWordsMecabList = '/home/dreamer/documents/code/partOfSpeech/allWord/TwoWordsMecabList.txt'
	ThreeWordsMecabList = '/home/dreamer/documents/code/partOfSpeech/allWord/ThreeWordsMecabList.txt'
	speechRecord = "/home/dreamer/documents/code/partOfSpeech/allWord/"
	# divideIntoUseAndUnuse(TwoWordsMecabList, ThreeWordsMecabList, speechRecord)
	# DuplicateRemoval("/home/dreamer/documents/code/partOfSpeech/allWord/TwoWordsAdjacency_afterSpeech.txt")
	# DuplicateRemoval("/home/dreamer/documents/code/partOfSpeech/allWord/ThreeWordsAdjacency_afterSpeech.txt")
	# GetTwoUsefulSpeechWord(TwoWordsMecabList, ThreeWordsMecabList, speechRecord)

	# DuplicateRemoval("./afterSpeech/ThreeUsefulFile.txt")
	# DuplicateRemoval("/home/dreamer/documents/code/database/2afterSpeech/two_afterfiliter_TwoUseful.txt")
	# DuplicateRemoval("/home/dreamer/documents/code/database/2afterSpeech/three_afterfillter_ThreeUseful.txt")
	# DuplicateRemoval("/home/dreamer/documents/code/database/afterSpeech/afterSpeech_filiter.txt")
