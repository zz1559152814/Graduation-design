# -*- coding: utf-8 -*-
from pylab import *
from scipy import stats
from scipy import optimize
import os
import math
import re

def percentFrom(start,end,filename):
	# fopen	   = open('./wordsMecabList/TwoWordsMecabList.txt','r')
	fopen	   = open(filename,'r')
	content	 = fopen.read()
	lines	   = content.split('\n')
	countRecord = {}
	allwordCount = 0 # 总词汇量
	allwordCount2 = 0 # 总词汇类型数目
	for line in lines:
		try:
			# countStr   = line.split(':')[1].split(' ')[-1]
			countStr   = line.split('\t')[-1]
			# countStr   = line.split(':')[-1].split(' ')[-1]
			count	  = int(countStr)
			print
		except:
			continue
		# if count < 500:
		allwordCount += count
		allwordCount2 += 1
		if count in countRecord:
			countRecord[count] += 1
		else:
			countRecord[count] = 1

	# for a in countRecord.keys():
	#	 print a, countRecord[a]
	print allwordCount,allwordCount2
	ns  = np.linspace(start, end, end-start+1)
	x  = 0
	unuseWordCount = 0
	for n in ns:
		if n not in countRecord.keys():
			continue
		d = int(n)
		x += n*countRecord[d]
		unuseWordCount += countRecord[d]
		print int(n),':',x/allwordCount,':',unuseWordCount,float(unuseWordCount)/float(allwordCount2)/(x/allwordCount)
	print "词频为",end,"个以下的词汇所含有信息是：",x
	print "词频为",end,"个以下的词汇所含有信息的百分比是：",x/allwordCount
	print "词频为",end,"个以上的词汇所占词汇总量是：",float(allwordCount2)-float(unuseWordCount)
	print "词频为",end,"个以下的词汇所占词汇总量的百分比：",float(unuseWordCount)/float(allwordCount2)

def filiter(filename, threshold):
	newfilename = filename[:-4]+"_filiter.txt"
	fopen = open(filename,'r')
	newfile = open(newfilename, 'wb')
	content = fopen.read()
	fopen.close()
	lines = content.split('\n')
	for line in lines:
		try:
			if int(line.split(':')[1].split(' ')[-1]) > threshold:
				newfile.write(line+'\n')
		except:
			pass
	newfile.close()

# percentFrom(1,5,"/home/dreamer/documents/code/database/afterAllwordSta/TwoWordsMecabList.txt")
# percentFrom(1,5,"/home/dreamer/documents/code/database/afterAllwordSta/AllWords.txt")
# filename = '/home/dreamer/documents/code/database/1afterAllwordSta/TwoAndThree.txt'
# filename = "/home/dreamer/documents/code/database/2afterSpeech/allWordsMecabList.txt"
# filename = "/home/dreamer/documents/code/partOfSpeech/allSpeech/speechFreRecord3.txt"
# filename = "/home/dreamer/documents/code/partOfSpeech/allSpeech/speechFreRecord2.txt"
# percentFrom(1,50,filename)
# percentFrom(1,1000,filename)
# filiter(filename,18)
# percentFrom(1,10,'./wordsMecabList/TwoWordsMecabList.txt')
