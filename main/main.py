# -*- coding: utf-8 -*-
from __future__ import division
import os,sys,shutil
sys.path.append('../Tools')
sys.path.append('../statistics')
sys.path.append('../nounExtract')
sys.path.append('../pretreatment')
sys.path.append('../wordCollect')
sys.path.append('../partOfSpeech')
sys.path.append('../distributionEntropy')
import statisticsTools,Tools,nounExtract,wordCollect
import speakingSplit,speech,wordFreStats,entropy
import traceback,curveFitting
from scipy import stats

fileRoot	= "/home/dreamer/documents/code/database/analysis/"
subfileroot  = []
prefileRoot = "/home/dreamer/documents/code/database/pretreatment/"
prefilenames = []
subPrefilenames = []

for i in range(1970,2017,3):
# for i in range(2000,2002,3):
	for j in range(3):
		subPrefilenames.append(prefileRoot+str(i+j)+'.txt')
	subfileroot.append(fileRoot+str(i)+'_'+str(i+2)+'/')
	prefilenames.append(subPrefilenames)
	subPrefilenames = []

# creat filepath
for sub in subfileroot:
	if os.path.exists(sub) == False:
		os.mkdir(sub)

# copy prefilenames to 2000_2002
for n in range(len(prefilenames)):
	threeYearFilePath = subfileroot[n]
	subPrefilenames   = prefilenames[n]
	subPretreatmentPath = threeYearFilePath+'pretreatment/'
	if os.path.exists(subPretreatmentPath) == False:
		os.mkdir(threeYearFilePath+'pretreatment')
	for file in subPrefilenames:
		if os.path.exists(subPretreatmentPath+file[-8:])== False:
			shutil.copy(file, subPretreatmentPath+file[-8:])

analysisPath = "/home/dreamer/documents/code/database/analysis/"
filepaths	= Tools.generateFileLists(analysisPath)

filepaths = sorted(filepaths)
# speakSplit
print "speakSplit start"
for filepath in filepaths:
	print "\tprocess with ",filepath.split("/")[-2]
	print filepath
	Tools.mkdir(filepath+'speakSplit/')
	if Tools.generateFileLists(filepath+'speakSplit/') == []:
		speakingSplit.speakSplit(filepath+'pretreatment/',filepath+'speakSplit/')
print "speakSplit end"

# noun extract
print "noun extract begin"
for filepath in filepaths:
	print "\tprocess with ",filepath.split("/")[-2]
	Tools.mkdir(filepath+'nounExtract/')
	if Tools.generateFileLists(filepath+'nounExtract/') == []:
		nounExtract.eachFile(filepath+'speakSplit/',filepath+'nounExtract/')
print "noun extract end"

# noun extract with pretreatment
print "noun extract with pretreatment begin"
for filepath in filepaths:
	print "\tprocess with ",filepath.split("/")[-2]
	Tools.mkdir(filepath+'nounExtract_pre/')
	if Tools.generateFileLists(filepath+'nounExtract_pre/') == []:
		nounExtract.eachFile(filepath+'pretreatment/',filepath+'nounExtract_pre/')
print "noun extract with pretreatment end"

# word extract
print "word extract begin"
for filepath in filepaths:
	print "\tprocess with ",filepath.split("/")[-2]
	Tools.mkdir(filepath+'wordRecord/')
	# print Tools.generateFileLists(filepath+'nounExtract/')
	if os.path.exists(filepath+'wordRecord/allwordByMecab.txt') == False:
		wordCollect.generateAllWordsByMecab(filepath+'pretreatment/',filepath+'wordRecord/')
	if os.path.exists(filepath+'wordRecord/AllWord.txt') == False:
		wordCollect.generateAllWords(filepath+'nounExtract/',filepath+'wordRecord/')
	if os.path.exists(filepath+'wordRecord/AllWordsAdjacency.txt') == False:
		wordCollect.generateMecabList(filepath+'wordRecord/AllWord.txt',filepath+'wordRecord/')
print "word extract end"

# speech process
print "speech process begin"
for filepath in filepaths:
	print "\tprocess with ",filepath.split("/")[-2]
	Tools.mkdir(filepath+'afterSpeech/')
	if Tools.generateFileLists(filepath+'afterSpeech/') == []:
		speech.divideIntoUseAndUnuse(filepath+'wordRecord/TwoWordsAdjacency.txt',filepath+'wordRecord/ThreeWordsAdjacency.txt',filepath+'afterSpeech/')
	# if os.path.exists(filepath+'afterSpeech/TwoWordsAdjacency_afterSpeech.txt') == False:
	wordFreStats.filiter(filepath+'afterSpeech/TwoWordsAdjacency_afterSpeech.txt',2)
	wordFreStats.filiter(filepath+'afterSpeech/ThreeWordsAdjacency_afterSpeech.txt',2)
	if os.path.exists(filepath+'afterSpeech/TwoWordsAdjacency_afterSpeech_filiter_DuplicateRemoval.txt') == False:
		speech.DuplicateRemoval(filepath+'afterSpeech/TwoWordsAdjacency_afterSpeech_filiter.txt')
		speech.DuplicateRemoval(filepath+'afterSpeech/ThreeWordsAdjacency_afterSpeech_filiter.txt')
print "speech process end"

# Entroy Among Files 正态分布
print "compute entroy among files begin"
for filepath in filepaths:
	print "\tprocess with ",filepath.split("/")[-2]
	Tools.mkdir(filepath+'afterEntroyAmongFiles/')
	a = filepath+'afterSpeech/TwoWordsAdjacency_afterSpeech_filiter_DuplicateRemoval.txt'
	b = filepath+'afterSpeech/ThreeWordsAdjacency_afterSpeech_filiter_DuplicateRemoval.txt'
	allwordTxt = filepath+'afterEntroyAmongFiles/WordsAdjacency_afterSpeech.txt'
	if Tools.generateFileLists(filepath+'afterEntroyAmongFiles/') == []:
		c = [a,b]
		Tools.merge(c,allwordTxt)

	tofile = filepath+'afterEntroyAmongFiles/EntroyAmongFilesScore.txt'
	if os.path.exists(tofile) is False:
		speakSplitFilePath = filepath+'nounExtract/'
		# speakSplitFilePath = "/home/dreamer/documents/code/database/2000-2002/0afterselect/1_speakSplit_noun/"
		entropy.entropyAmongFiles(allwordTxt, speakSplitFilePath,tofile)
	tofile_sort = filepath+'afterEntroyAmongFiles/EntroyAmongFilesScore_sorted.txt'
	if os.path.exists(tofile_sort) is False:
		Tools.sort(tofile,-1)
	# print Tools.generateFileLists(filepath+'nounExtract/')
print "compute entroy among files end"

# eliminate conference-related words
print "eliminate conference-related words begin"
for filepath in filepaths:
	print "\tprocess with ",filepath.split("/")[-2]
	Tools.mkdir(filepath+'eliminate/')
	# print Tools.generateFileLists(filepath+'nounExtract/')
	aim_file = filepath+'eliminate/eliminate.txt'
	source_file = filepath+'afterEntroyAmongFiles/EntroyAmongFilesScore_sorted.txt'
	eliminate_wordlist = "/home/dreamer/documents/code/database/condition/eliminate_wordlist.txt"
	if os.path.exists(aim_file) is False:
		Tools.eliminate(source_file,aim_file,eliminate_wordlist)
print "eliminate conference-related words end"

# extract 500 word
print "extract 500 word begin"
for filepath in filepaths:
	print "\tprocess with ",filepath.split("/")[-2]
	Tools.mkdir(filepath+'final/')
	# print Tools.generateFileLists(filepath+'nounExtract/')
	aim_file = filepath+'final/final.txt'
	allWordFile = filepath+'eliminate/eliminate.txt'
	if os.path.exists(filepath+'final/final.txt') is False:
		Tools.ConvertCut(allWordFile,aim_file,500)
print "extract 500 word end"

# 500 word files
print "500 word files begin"
for filepath in filepaths:
	print "\tprocess with ",filepath.split("/")[-2]
	Tools.mkdir(filepath+'wordIncluded/')
	# print Tools.generateFileLists(filepath+'nounExtract/')
	sourceFile = filepath+'final/final.txt'
	sourcePath = filepath+'pretreatment/'
	aimPath = filepath+'wordIncluded/'
	if Tools.generateFileLists(aimPath) == []:
		wordList = Tools.content_wordList(sourceFile,'\t:')
		for w in wordList:
			Tools.select(w,sourcePath,aimPath)
print "extract 500 word end"

# # 500 word files
# print "500 word files begin"
# aimfilePath = "/home/dreamer/documents/code/database/Longitudinal_analyse/"
# curveFitting.JaccardPlot(aimfilePath)	# Jaccard.append(len(sets[n]&set[n+1])/len(sets[n]|set[n+1]))
# # print Jaccard
# print "extract 500 word end"
