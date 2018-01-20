# -*- coding: utf-8 -*-
import os,re,sys
sys.path.append('../Tools')
sys.path.append('../partOfSpeech')
sys.path.append('../Mecab')
sys.path.append('../statistics')
import mecab,statisticsTools
import math,Tools,speech
import re

# to generate dictionary
def Detect10(line):
	eles = line.split('\t')
	list10 = ''
	wrongIndex = []
	for ele in eles:
		if ele != '':
			if re.search('\d-\d',ele):
				list10 = list10+str(0)
			if re.search('\d-\d',ele) is None:
				list10 = list10+str(1)
	result =  re.sub('10','22',list10)
	if re.findall("(?!2+)",result) == ['']:
		return -1
	else:
		# print result
		for i in range(len(result)):
			if result[i] != '2':
				wrongIndex.append(int(i))
		wrongIndex.append(result)
		return wrongIndex
# to generate dictionary
def troubleLineSplit(lines):
	wordList = []
	# if len(lines) == 2:
	#	 detect0 =  Detect10(lines[0])
	#	 detect1 =  Detect10(lines[1])
	#	 if detect0[0] != detect1[0]:
			# print lines[0]
			# print lines[1]
			# # wordList.append(str([detect0[1])[int(detect0[0])],str(detect1[1])[int(detect1[0])]])
			# print [detect0[-1][int(detect0[0])],detect1[-1][int(detect1[0])]]
			# print detect0,detect1
			# print '\n'
	# elif len(lines) == 3:
	#	 pass
	for line in lines:
		eleLine = line.split('\t')
		detect =  Detect10(line)
		for i in detect[:-1]:
			eleLine[i] = ','

		cnt = 0
		for j in range(len(eleLine)):
			if eleLine[j] == ',':
				cnt += 1
		for i in range(cnt):
			eleLine.remove(',')
		if len(eleLine)%2 != 0:
			for j in range(0,len(eleLine[1:]),2):
				wordList.append([eleLine[j],eleLine[j+1]])
		else:
			if len(eleLine) != 0:
				for j in range(0,len(eleLine),2):
					wordList.append([eleLine[j],eleLine[j+1]])
	return wordList
# to generate dictionary
def GenerDict(srcFile, dictFile):
	lines = Tools.content_lines(srcFile)
	troubleLines = []
	NotroubleLines = []
	troubleLine = []
	lastLineSign = 0
	thisLineSign = 0
	for line in lines:
		ele = line.split('\t')
		if line != '':
			if Detect10(line) == -1:
				lastLineSign = thisLineSign
				thisLineSign = 0
				NotroubleLines.append(line)
				if lastLineSign == 1:
					troubleLines.append(troubleLine)
					troubleLine = []
			else:
				lastLineSign = thisLineSign
				thisLineSign = 1
				troubleLine.append(line)

	dictF = open(dictFile,'wb')
	for i in range(len(NotroubleLines)):
		splitEle = NotroubleLines[i].split('\t')
		if len(splitEle) != 0:
			try:
				for j in range(0,len(splitEle),2):
					dictF.write(splitEle[j]+','+splitEle[j+1]+'\n')
			except:
				print splitEle[0]

	for i in troubleLines:
		if len(i) == 2:
			wordList = troubleLineSplit(i)
			for word in wordList:
				dictF.write(word[0]+','+word[1]+'\n')
				# dictF.write(word[0]+','+splitEle[1])
		elif len(i) == 3:
			wordList = troubleLineSplit(i)
			for word in wordList:
				dictF.write(word[0]+','+word[1]+'\n')
		if len(i)%2 == 0 and len(i)>2:
			wordList = troubleLineSplit(i)
			for word in wordList:
				dictF.write(word[0]+','+word[1]+'\n')
	dictF.close()

# level=1: 法案 ['1']
# level=2: 法案 ['1.3']
# level=3: 法案 ['1.30']
# level=4: 法案 ['1.3084']
# level=5: 法案 ['1.3084-12']
def inquiry(keywords,level=5):
	dictF = "/home/dreamer/documents/code/eliminate/dict/dict.txt"
	lines = Tools.content_lines(dictF)
	keywordTuple = {}
	cnt = 0
	for key in keywords:
		cnt += 1
		print key,cnt
		for line in lines:
			if re.search("・",line) is None:
				if re.search("^"+key+",",line) or re.search("^"+key+"\(.*\),",line):
					if level == 1:
						classification = line.split(',')[-1][0]
					elif level == 2:
						classification = line.split(',')[-1][0:2]
					elif level == 3:
						classification = line.split(',')[-1][0:4]
					elif level == 4:
						classification = line.split(',')[-1][0:6]
					elif level == 5:
						classification = line.split(',')[-1]
					if key in keywordTuple.keys():
						keywordTuple[key].append(classification)
					else:
						keywordTuple[key] = []
						keywordTuple[key].append(classification)
			else:
					words = line.split(',')[0].split('・')
					if re.search("\(",line) is None:
						if key in words:
							if level == 1:
								classification = line.split(',')[-1][0]
							elif level == 2:
								classification = line.split(',')[-1][0:2]
							elif level == 3:
								classification = line.split(',')[-1][0:4]
							elif level == 4:
								classification = line.split(',')[-1][0:6]
							elif level == 5:
								classification = line.split(',')[-1]
							if key in keywordTuple.keys():
								keywordTuple[key].append(classification)
							else:
								keywordTuple[key] = []
								keywordTuple[key].append(classification)
	return keywordTuple

# to find the rule which the word what i don't need have
def main(tofile):
	to = open(tofile,'wb')
	fileList = ['/home/dreamer/documents/code/eliminate/test/test.txt']
	analyise	= statisticsTools.Statistics(fileList)
	wordBoxs 	= analyise.getWordBox()
	wordlist	= wordBoxs.keys()
	# for word in wordlist:
	#	 print word
	print len(wordlist)
	dictTuple   = inquiry(wordlist,level=4)
	dictList = Tools.TupleSort(dictTuple)
	lines	   = Tools.content_lines("/home/dreamer/documents/code/eliminate/test/test.txt")
	for a in dictList:
		for line in lines:
			if a[0] in line:
				to.write(line+','+a[0]+','+str(a[1])+'\n')
				break
def main1(tofile):
	lines	   = Tools.content_lines("/home/dreamer/documents/code/eliminate/test/test_dict_for_singleWord.txt")
	wordDictTuple = {}
	for l in lines:
		if l != '':
			spl = l.split(',')
			wordDictTuple[spl[1]] = spl[2][2:-2]
	lines	   = Tools.content_lines("/home/dreamer/documents/code/eliminate/test/test.txt")
	to = open(tofile,'wb')
	for line in lines[:-1]:
		try:
			a = mecab.MeCabClass(line).GetAll()
			to.write(a[0]+','+a[1]+',')
			if a[0] not in wordDictTuple.keys() and a[1] not in wordDictTuple.keys():
				to.write('\n')
			elif a[0] not in wordDictTuple.keys():
				to.write(','+str(wordDictTuple[a[1]])+'\n')
			elif a[1] not in wordDictTuple.keys():
				to.write(str(wordDictTuple[a[0]])+','+'\n')
			else:
				to.write(str(wordDictTuple[a[0]])+','+str(wordDictTuple[a[1]])+'\n')
		except:
			print line
	to.close()
def main2(tofile):
	compoundLines = Tools.content_lines("/home/dreamer/documents/code/eliminate/test/test_dict_for_commpound.txt")
	classTuple = {}
	for cline in compoundLines:
		if cline != '':
			csp = cline.split(',')
			class1 = csp[2]
			class2 = csp[3]
			# classM = max(class1,class2)
			# classS = min(class1,class2)
			print class1,class2,csp[0],csp[1]
			# classOfWord = str(classM)+'+'+str(classS)
			classOfWord = class1+"+"+class2
			if classOfWord in classTuple.keys():
				classTuple[classOfWord].append(csp[0]+csp[1])
			else:
				classTuple[classOfWord] = []
				classTuple[classOfWord].append(csp[0]+csp[1])
	to = open(tofile,'wb')
	# classlist = classTuple.sorted()
	for aClass in classTuple.keys():
		to.write(aClass+':')
		for word in classTuple[aClass]:
			to.write(word+' ')
		to.write("\n")
	to.close()
if __name__ == '__main__':
	# tofile1 = "/home/dreamer/documents/code/eliminate/test/test_dict_for_singleWord_level4.txt"
	# main(tofile1)
	# tofile2 = "/home/dreamer/documents/code/eliminate/test/test_dict_for_commpound.txt"
	# main1(tofile2)
	tofile3 = "/home/dreamer/documents/code/eliminate/test/test_classification.txt"
	main2(tofile3)

	# a = "/home/dreamer/documents/code/database/2000-2002/5afterCompoundScore/TwoScore.txt"
	# words = Tools.content_wordList(a,'\t:')
	# for word in words:
	#	 print word
	# for b in a.keys():
	#	 print b,a[b]
	# words = Tools.content_lines("/home/dreamer/documents/code/database/condition/eliminate_wordlist.txt")
	# # print words
	# T  = inquiry(words)
	# for w in T.keys():
	# 	print w,T[w]
	a = '\\xc2\\x81w\\xc2\\x95\\xc2\\xaa\\xc2\\x97\\xc3\\x9e\\xc2\\x8c\\xc3\\xaa\\xc2\\x9cb\\xc2\\x95'.decode('utf8')
	print a

# srcFile = "/home/dreamer/documents/code/eliminate/a.txt"
# dictFile = "/home/dreamer/documents/code/eliminate/dict.txt"
# GenerDict(srcFile,dictFile)
