#-*-encoding:utf-8-*-
import sys
sys.path.append('../Mecab')
import mecab
import os
from collections import *
import re


def nounExtractFrom2000(fromFile,toFile):
	# aimFilePath		= "/home/dream/documents/papers/code/datatest/to2000Noun/"
	fopen			= open(fromFile,'r')
	newfile			= open(toFile,'wb')
	text			= fopen.read()
	textMecab		= mecab.MeCabClass(text)
	allWordLists	= textMecab.GetAll2()
	for n in range(len(allWordLists)):
		if textMecab.isNoun2(allWordLists[n][1]):
			newfile.write(allWordLists[n][0])
			if n != len(allWordLists) - 1:
				if textMecab.isNoun2(allWordLists[n+1][1]) == 0:
					newfile.write("_")
	fopen.close()
	newfile.close()

def nounExtractFromPretreat(filename,newfilename):
	fopen			= open(filename,'r')
	text			= fopen.read()
	contents  		= text.split('>>>')
	newfile  	= open(newfilename,'wb')
	for content in contents:
		speaking  		= content.split('::')[-1]
		paras  			= speaking.split('\n')
		for para in paras:
			textMecab		= mecab.MeCabClass(para)
			allWordLists	= textMecab.GetAll2()
			for n in range(len(allWordLists)):
				if textMecab.isNoun2(allWordLists[n][1]):
					newfile.write(allWordLists[n][0])
					if n != len(allWordLists) - 1:
							if textMecab.isNoun2(allWordLists[n+1][1]) == 0:
								newfile.write("_")
			newfile.write("\n")
	newfile.close()
	fopen.close()

def eachFile(filepath,toFilepath):
	files	= os.listdir(filepath)
	FilePath = filepath
	for file in files:
		# if re.search('noun',file) is None:
			# nounExtractFrom2000(filepath,file)
		newfilename = toFilepath+file[:-4]+'_noun.txt'
		nounExtractFromPretreat(FilePath+file,newfilename)
		# os.remove(filepath+file)

if __name__ == "__main__":
	pass
# eachFile("./testtxt/")
# newfile		= open("/home/dreamer/documents/code/database/afterselect/1/allcontentNoun.txt",'a')

# filepath  = "/home/dreamer/documents/code/database/0afterselect/1_speakSplit/"
# tofilepath  = "/home/dreamer/documents/code/database/0afterselect/1_speakSplit_noun/"
# eachFile(filepath,tofilepath)
# # newfile.close()
# 	eachFile()
# 	pass
