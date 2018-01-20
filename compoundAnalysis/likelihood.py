# -*- coding: utf-8 -*-
from __future__ import division
import re,os,sys
sys.path.append('../Mecab')
sys.path.append('../Tools')
sys.path.append('../statistics')
from scipy import stats
import mecab,statisticsTools,Tools
import math,time,traceback

#记录一个名词连体中含有单词数量超过n的单词数
global count
# 抽取出所有名词的文本的路径
global filePath

def binomial(k,n,x):
	return stats.binom.pmf(k,n,x)

def test(filename):
	global count
	fopen   = open(filename)
	content = fopen.read()

	words   = content.split('_')
	for word in words:
		mec	 = mecab.MeCabClass(word)
		allw	= mec.GetNoun2()
		if len(allw) > 3:
			count = count + 1

@Tools.exeTime
def getScoreOfTwo(allwordByMecab,WordsMecabListsFilepath,TwoWordsFile, threshold):
	global wordCount
	global ScoreRecord
	global filePath
	ScoreRecord  	= {}
	wordCount		= 0
	fileLists  		= generateFileLists(filePath)
	# 获取总次数 利用用Mecab处理得到的总词数
	allWordMecab  	= open(allwordByMecab,'r')
	content  		= allWordMecab.read()
	lines  			= content.split('\n')
	allWordBox  	= {}
	# 利用Mecab分词得到的分词文件列表，统计出一个wordbox
	for line in lines:
		try:
			wordCount = wordCount + int(line.split('\t')[1])
			word  	= line.split('\t')[0]
			wordfre = int(line.split('\t')[1])
			allWordBox[word] = wordfre
		except:
			continue
	print wordCount

	# 处理拥有两个子单位的相连共现词组
		# 因为在拥有三个以及多个的相连词汇共现词组里也拥有包含着一些二元词组，因此要在各个文件中都进行检测
	WordsMecabLists = [WordsMecabListsFilepath+'TwoWordsMecabList.txt',WordsMecabListsFilepath+'ThreeWordsMecabList.txt',WordsMecabListsFilepath+'MultiWordsMecabList.txt']
	TwoScoreRecord  = open("/home/dreamer/documents/code/database/5afterCompoundScore/TwoScore.txt",'wb')
	TwoWordsMecabList 		= open(TwoWordsFile,'r')
	TwoWordsMecabListcontent  	= TwoWordsMecabList.read()
	TwoWordsMecabListlines  	= TwoWordsMecabListcontent.split('\n')

	# 把词频数小于阈值的词从列表中删除
	runCounter 		= 0
	startTime  		= time.time()
	for line in TwoWordsMecabListlines[:-1]:
		runCounter += 1
		wordFre  		= 0
		if runCounter%200 == 0:
			os.system('clear')
			print "This is the",runCounter,"th lines"
			endTime  		= time.time()
			print "Run time is:",endTime-startTime
			startTime  		= time.time()
		TwoWordEle	  = line.split(':')
		wholeWord	   = TwoWordEle[0]
		try:
			subwords		= TwoWordEle[1].split(' ')[:-1]
			wordCountOfThisLine = int(TwoWordEle[1].split(' ')[-1])
		except:
			print subwords
			continue
		if wordCountOfThisLine > threshold:
			for wordMecabfile in WordsMecabLists:
				fopen  		= open(wordMecabfile,'r')
				content  	= fopen.read()
				lines  		= content.split('\n')
				for line1 in lines:
					if re.search(wholeWord,line1) is not None:
						# print "in"
						lineEle = line1.split(':')
						wordFreStr = lineEle[1].split(' ')[-1]
						try:
							wordFre = wordFre + int(wordFreStr)
						except:
							print lineEle[1]
							continue
				fopen.close()
			DoubleCompoundAnalysis(wholeWord,subwords[0],subwords[1],TwoScoreRecord,wordFre,allWordBox)
			wordFre = 0
	TwoWordsMecabList.close()
	TwoScoreRecord.close()

def DoubleCompoundAnalysis(wholeWord,subword1,subword2,TwoScoreRecord,wordFre,allWordBox):
	global filePath
	global wordCount
	global ScoreRecord
	# c1:subWord1的词频
	# c2:subWord2的词频
	# c12:subWord1,2合成词汇的词频
	# p:假设一中的概率{ P = P(W2|W1) = P(W2|!W1) = C2/N　｝
	# p1:假设二中的概率{ P1 = P(W2|W1) = Ｃ12/C1 }
	# p12:假设二中的概率{ P1 = P(W2|!W1) = (Ｃ2-C12)/(N-C1) }
	try:
		c1				= allWordBox[subword1]
		c2				= allWordBox[subword2]
	except:
		return
	c12				= wordFre
	p  				= c2/wordCount
	p1  			= c12/c1
	p2  			= (c2 - c12)/(wordCount - c1)
	try:
		score  			= math.log(binomial(c12,c1,p))  + math.log(binomial(c2-c12,wordCount-c1,p)) \
						- math.log(binomial(c12,c1,p1)) - math.log(binomial(c2-c12,wordCount-c1,p2))
		TwoScoreRecord.write(wholeWord+'\t:'+subword1+' '+str(c1)+'\t:'+subword2+' '+str(c2)+'\t:'+str(c12)+'\t:'+str(score)+'\n')
		ScoreRecord[wholeWord]  	= score
	except:
		TwoScoreRecord.write(wholeWord+'\t:'+subword1+' '+str(c1)+'\t:'+subword2+' '+str(c2)+'\t:'+str(c12)+'\t:'+str(-9999)+'\n')
		ScoreRecord[wholeWord]  	= -9999


count = 0
global filePath
filePath	= "../datatest/to2000Noun/"
# # AllWordFile = "../compoundAnalysis/wordsMecabList/AllWords.txt"
# # generateAllWords("/home/dreamer/documents/code/database/afterselect/to2000N/")
# # generateMecabList("/home/dreamer/documents/code/database/afterAllwordSta/","AllWordsBy_.txt")
# TwoWordsFile = "/home/dreamer/documents/code/database/5afterCompoundScore/buffer_DuplicateRemoval_two.txt"
# allwordByMecab   		= "/home/dreamer/documents/code/database/1afterAllwordSta/allwordByMecab.txt"
# WordsMecabListsFilepath = "/home/dreamer/documents/code/database/1afterAllwordSta/"
# getScoreOfTwo(allwordByMecab,WordsMecabListsFilepath,TwoWordsFile,18)
