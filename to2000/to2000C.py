#-*-encoding:utf-8-*-
import chardet
import os,sys
import re
import linecache

class Item:
	def __init__(self):
		self.time		= ''
		self.date		= ''
		self.house		= ''
		self.department	= ''
		self.speaker	= ''
		self.content 	= ''

global FilePath

def printItem(item):
	return item.time+'::'+item.department+'::'+str(item.date)+'::'+item.house+'::'+item.speaker+'::'+item.content+'>>>'+'\n'

def eachFile(filepath):
	global FilePath
	fromFilenames	= []
	toFilenames		= []
	n				= 1
	files	= os.listdir(filepath)
	FilePath = filepath
	for file in files:
		fromFilenames.append(file)
	global isFileOpen
	global RemainStatus
	global wordCount
	global isLast
	isLast 			= 0
	wordCount 		= 0
	isFileOpen 		= 0
	RemainStatus	= 0
	times 			= 0
	contentLists 	= []
	remain 			= []
	while(1):
		if len(fromFilenames)==0 and RemainStatus == 0:
			break
		#read
		if RemainStatus != 1:
			if len(fromFilenames) == 0:
				isLast = 1
			else:
				fromFilename 	= fromFilenames.pop()
				print fromFilename
				fromFile 		= open(filepath + fromFilename)
				isFileOpen		= 1
		read2000(fromFile,contentLists,remain)
		if isFileOpen:
			fromFile.close()
			isFileOpen	= 0
		if RemainStatus == -1:
			continue
		#write
		# toFile	= open(filepath[:-9]+"to2000/"+str(times)+'.txt','wb')
		toFile	= open(filepath[:-2]+"to2000/"+str(times)+'.txt','wb')
		while len(contentLists) != 0:
			toFile.write(contentLists.pop())
		toFile.close()
		# print times
		times 	= times + 1

def read2000(fromFile,contentLists,remain):
	global isFileOpen
	global RemainStatus
	global wordCount
	global isLast

	perFileCount = 1766
	wordCount2 	= 0
	wordCount3 	= 0
	if RemainStatus != 1 :
		allcontent	= fromFile.read()
		allparas	= allcontent.split('>>>')
		for para in allparas[:-1]:
			try:
				speaking	= para.split('::')[5]
				speakingInSentences 	= speaking.split('。')
				for sentence in speakingInSentences:
					remain.append(sentence+'。')
					wordCount = wordCount + len(sentence)
			except:
				print para
	if wordCount <= perFileCount:
		RemainStatus = -1
		return

	while(wordCount2 < perFileCount):
		wordCount3 = len(remain[-1])
		wordCount2 = wordCount2 + wordCount3
		contentLists.append(remain.pop())

	wordCount = wordCount - wordCount2
	isFileOpen	= 0

	if wordCount == 0:
		RemainStatus = 0
	elif wordCount >= perFileCount:
		RemainStatus = 1
	elif wordCount < perFileCount:
		RemainStatus = -1
	print wordCount,RemainStatus
	return

# eachFile("../datatest/pretreat/")
eachFile("/home/dreamer/documents/code/database/afterselect/1/")
