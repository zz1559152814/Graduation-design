# -*- coding: utf-8 -*-
import os,sys,re
sys.path.append('../Mecab')
import mecab

def main(filename):
	fopen = open(filename,'r')
	lines = fopen.read().split('\n')

	highEntroy = open("/home/dreamer/documents/code/database/4afterEntroyAmongWords/highEntroy.txt")
	throwfile = open("/home/dreamer/documents/code/database/4afterEntroyAmongWords/throw.txt")

	highEntroyContent = highEntroy.read()
	throwfileContent = throwfile.read()
	highEntroySet = set()
	throwfileSet = set()
	for highEntroy in highEntroyContent.split('\n'):
		if highEntroy != '':
			highEntroySet.add(highEntroy)
			# print highEntroy,','
	for throw in throwfileContent.split('\n'):
		if throw != '':
			throwfileSet.add(throw)
	# print throwfileSet
			# print throw
	# print len(highEntroySet)
	# print len(throwfileSet)
	goodWordSet = set()
	simplySet = set()
	twowordSet = set()
	for line in lines:
		ele = line.split(':')[-1].split(' ')
		if len(ele) == 4:
			if ele[-2] not in highEntroySet:
				if ele[-2] not in throwfileSet:
					goodWordSet.add(line)
					# print line
			elif ele[-2] in highEntroySet:
				newline = re.sub(ele[-2],'',line)
				newline = re.sub('  ',' ',newline)
				simplySet.add(newline)
				print line
			elif ele[-2] in throwfileSet:
				# print line
				pass
		elif len(ele) == 3:
			if ele[-2] not in throwfileSet:
				twowordSet.add(line)
				# print ele[-2]

	newfile = open('/home/dreamer/documents/code/database/4afterEntroyAmongWords/buffer.txt',"wb")
	for x in simplySet:
		newfile.write(x+'\n')
		# print x
	for x in goodWordSet:
		newfile.write(x+'\n')
	for x in twowordSet:
		newfile.write(x+'\n')


def DuplicateRemoval(filename):
	fopen	   = open(filename, 'r')
	content	 = fopen.read()
	oneWordList = content.split('\n')
	allSpeech	  = set()
	allSpeechTuple = {}
	wordTuple = {}
	for oneWord in oneWordList:
		thisWord	= oneWord.split(':')[0]
		try:
			if thisWord in wordTuple.keys():
				wordTuple[thisWord] += int(oneWord.split(':')[1].split(' ')[-1])
			else:
				wordTuple[thisWord] = int(oneWord.split(':')[1].split(' ')[-1])
		except:
			print oneWord


	newfilename = filename[:-4]+"_DuplicateRemoval.txt"
	newfile = open(newfilename,'wb')
	for word in wordTuple:
		# print word
		thisWordMec	= mecab.MeCabClass(word)
		thisSpeechs = thisWordMec.GetAll()
		newfile.write(word+':')
		for subword in thisSpeechs:
			newfile.write(subword+' ')
		newfile.write(str(wordTuple[word])+'\n')
	newfile.close()


# main("/home/dreamer/documents/code/database/3afterFiliter/all_3.txt")
DuplicateRemoval("/home/dreamer/documents/code/database/4afterEntroyAmongWords/buffer.txt")
