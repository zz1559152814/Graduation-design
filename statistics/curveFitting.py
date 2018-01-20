# -*- coding: utf-8 -*-
from __future__ import division
import matplotlib
# matplotlib.use('Agg')
from pylab import *
from scipy import stats
sys.path.append('../Tools')
import Tools
from scipy import optimize
import os
import math
import re

def formatSize(bytes):
	try:
		bytes = float(bytes)
		kb = bytes / 1024
	except:
		print("传入的字节格式不对")
		return "Error"
	return kb

def a(x,y):
	return y*(int(x/y)+1)
def b(x,y):
	return int(x/y)*y
def normalFunction(x,a,b,c):
	return c*np.exp(-(x - a) ** 2 /(2* b **2))/(math.sqrt(2*math.pi)*b)
def pdfFitting(xdata,ydata):
	plt.figure(figsize=(20,10))
	guess = [180,100,1000]
	fita,fitb = optimize.curve_fit(normalFunction,xdata,ydata,guess)
	x = np.linspace(xdata.min(),xdata.max(),5000)
	y = fita[2]*stats.norm.pdf(x=x, loc=fita[0], scale=fita[1])

	plt.xlabel("the size if para",size=35)
	plt.ylabel("the count of n-size para",size=35)
	plt.plot(xdata,ydata,'o')
	plt.title('para\'s size - frequence',size=35)
	plt.plot(xdata,ydata,'g')
	plt.plot(x,y,'r')
	plt.savefig("/home/dreamer/documents/code/statistics/pdf"+'.png')
	plt.show()
	return fita
# def powerLaw(x,a,b):
#	 return b*a*exp(x*-a)
def reciprocalNp(x,a,b):
	c = np.arange(x.shape[0],dtype=np.float)
	for index in range(x.shape[0]):
		c[index]= a*((b*x[index])**-1)
	return c
def reciprocal(x,a,b):
	return a*((b*x)**-1)
	# return [a*x1**-1 for x1 in x]
def reciprocalFitting(xdata,ydata,title,filepath):
	plt.figure(figsize=(20,10))
	# guess = np.random.randn(2)*10
	fita,fitb = optimize.curve_fit(reciprocal,xdata,ydata)
	x = np.linspace(xdata.min(),xdata.max(),200)
	y = reciprocalNp(x,fita[0],fita[1])
	plt.title(title)
	plt.text(max(xdata)*0.8,max(ydata)*0.8,'y='+str(fita[0])+'*'+str(fita[1])+'*x^-1',color='blue',ha='center')
	plt.plot(xdata,ydata,'o',color='green')
	plt.plot(xdata,ydata,'g',label='data')
	plt.plot(x,y,'r',label='data',linewidth=2)
	if filepath != None:
		plt.savefig(filepath+title+'.png')
	# plt.show()
	print fita[0],fita[1]
	return fita

def powerLaw(x,a,b):
	# return b*a*exp(x*-a)
	# return b*x**-a
	return b*np.power(x,-a)
def powerNp(x,a):
	b = np.arange(x.shape[0],dtype=np.float)
	for index in range(x.shape[0]):
		b[index]= pow(x[index],a)
	return b
def powerLawFitting(xdata,ydata,title,filepath):
	plt.figure(figsize=(20,10))
	fita,fitb = optimize.curve_fit(powerLaw,xdata,ydata)
	x = np.linspace(xdata.min(),xdata.max(),5000)
	y = fita[1]*powerNp(x,-fita[0])
	plt.title(title)
	plt.text(max(xdata)*0.8,max(ydata)*0.8,'y='+str(fita[1])+'*x^-'+str(fita[0]),color='blue',ha='center')
	plt.plot(xdata,ydata,'o',color='green')
	plt.plot(xdata,ydata,'g',label='data')
	plt.plot(x,y,'r',label='data',linewidth=2)
	if filepath is not None:
		plt.savefig(filepath+title+'.png')
	# plt.show()
	print fita[0],fita[1]
	return fita

def powerLaw(x,a,b):
	# return b*a*exp(x*-a)
	# return b*x**-a
	return b*np.power(x,-a)
def powerNp(x,a):
	b = np.arange(x.shape[0],dtype=np.float)
	for index in range(x.shape[0]):
		b[index]= pow(x[index],a)
	return b
def powerLawFitting(xdata,ydata,title,filepath=None):
	plt.figure(figsize=(20,10))
	fita,fitb = optimize.curve_fit(powerLaw,xdata,ydata)
	x = np.linspace(xdata.min(),xdata.max(),5000)
	y = fita[1]*powerNp(x,-fita[0])
	plt.title(title)
	plt.text(max(xdata)*0.8,max(ydata)*0.8,'y='+str(fita[1])+'*x^-'+str(fita[0]),color='blue',ha='center')
	plt.plot(xdata,ydata,'.',color='red')
	plt.plot(xdata,ydata,'g',label='data',color='red')
	plt.plot(x,y,'r',label='data',linewidth=2,color='green')
	plt.show()
	# if filepath is not None:
	# 	plt.savefig(filepath+title+'.png')
	print fita[0],fita[1]
	return fita

def linear(x,a,b):
	# return b*a*exp(x*-a)
	# return b*x**-a
	return a*x+b
def linearNp(x,a,b):
	c = np.arange(x.shape[0],dtype=np.float)
	c=a*x+b
	return c
def linearFitting(xdata,ydata,title,filepath=None):
	plt.figure(figsize=(20,10))
	fita,fitb = optimize.curve_fit(linear,xdata,ydata)
	x = np.linspace(xdata.min(),xdata.max(),5000)
	y = linearNp(x,fita[0],fita[1])
	plt.title(title,size=35)
	xlabel = "years"
	ylabel = "Jaccard"
	plt.xlabel(xlabel,size=35)
	plt.ylabel(ylabel,size=35)
	subfileroot = []
	for i in range(1970,2017,3):
		subfileroot.append(str(i)+'-'+str(i+2))
	xticks([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16],subfileroot)
	plt.text(max(xdata)*0.8,max(ydata)*0.8,'y='+str(fita[0])+'*x+'+str(fita[1]),color='blue',ha='center')
	plt.plot(xdata,ydata,'.',color='red')
	plt.plot(xdata,ydata,'g',label='data',color='red')
	plt.plot(x,y,'r',label='data',linewidth=2,color='green')
	if filepath is not None:
		plt.savefig(filepath+title+'.png')
	plt.show()
	print fita[0],fita[1]
	return fita

def FileSizeFit(filepath):
	files			  = os.listdir(filepath)
	fileSizeRecord	= {}
	for file in files:
		size	= os.path.getsize(filepath+file)
		sizeKb  = int(formatSize(size))
		sizeKbDivide = a(sizeKb,15)
		# sizeKbDivide = sizeKbDivide*10
		if sizeKbDivide in fileSizeRecord.keys():
			if sizeKbDivide >= 50:
				fileSizeRecord[sizeKbDivide] += 1
		else:
			if sizeKbDivide >= 50:
				fileSizeRecord[sizeKbDivide] = 1
	fileSizeList = fileSizeRecord.items()
	fileSizeList.sort()
	size	  = np.array([x[0] for x in fileSizeList])
	sizeCount = np.array([x[1] for x in fileSizeList])
	print pdfFitting(size,sizeCount)
def wordCountFit(filename):
	scoreRecord	= {}
	fopen		   = open(filename,'r')
	content		 = fopen.read()
	paras		   = content.split('\n')
	wordcount	   = 0
	scoreList	   = []
	for para in paras:
		try:
			score   = int(para.split("\t")[-1])
			# score   = int(para.split(":")[-1].split(" ")[-1])
			scoreList.append(score)
		except:
			continue

	scoreList.sort(reverse=True)
	# score1	 = np.array([d for d in range(len(scoreList))])
	allWordCnt = 0
	for n in scoreList:
		allWordCnt += n
	# rank_log = np.array([float(d+1) for d in range(len(scoreList))])
	rank_log = np.array([float(d+1) for d in range(8000)])
	# fre_log  = np.array([float(x) for x in scoreList])
	fre_log  = np.array([float(scoreList[x]) for x in range(8000)])
	rank	 = np.array([float(d+1) for d in range(len(scoreList))])
	fre	  = np.array([float(x) for x in scoreList])
	title = 'Zipf\'s laws'
	# Tools.plot(rank_log,fre_log,title, xlabel="log(rank)",ylabel="log(frequence)")
	# Tools.plot(rank,fre,title)
	print powerLawFitting(rank_log,fre_log,title)
	# print " Total number of word is:",allWordCnt
	# for x in range(len(scoreList)):
	# 	if x>scoreList[x]:
	# 		print "The h-point of all word is:",x
	# 		return x

def rank_frequence(filename):
	scoreRecord	= {}
	fopen		   = open(filename,'r')
	content		 = fopen.read()
	paras		   = content.split('\n')
	wordcount	   = 0
	scoreList	   = []
	for para in paras:
		try:
			score   = int(para.split("\t")[-1])
			# score   = int(para.split(":")[-1].split(" ")[-1])
			scoreList.append(score)
		except:
			continue

	scoreList.sort(reverse=True)
	# score1	 = np.array([d for d in range(len(scoreList))])
	allWordCnt = 0
	for n in scoreList:
		allWordCnt += n
	rank_log = np.array([math.log(float(d+1)) for d in range(len(scoreList))])
	fre_log  = np.array([math.log(float(x)) for x in scoreList])
	rank	 = np.array([float(d+1) for d in range(len(scoreList))])
	fre	  = np.array([float(x) for x in scoreList])
	title = 'Zipf\'s laws'
	Tools.plot(rank_log,fre_log,title, xlabel="log(rank)",ylabel="log(frequence)",filepath="/home/dreamer/documents/code/statistics/")
	# print powerLawFitting(rank,fre,title)
	print " Total number of word is:",allWordCnt
	# for x in range(len(scoreList)):
	# 	if x>scoreList[x]:
	# 		print "The h-point of all word is:",x
	# 		return x
	# return rank,fre
def ParaSizeFit(filepath):
	files		= Tools.generateFileLists(filepath)
	paraSizeRecord = {}
	for file in files:
		paras		   = Tools.content_paras(file)
		for para in paras:
			length1	 = len(para.split('::')[-1])
			length	  = a(length1,60)
			if length1 == 0 or length1 > 20000:
				continue
			if length in paraSizeRecord:
				paraSizeRecord[length] += 1
			else:
				paraSizeRecord[length] = 1
	paraSizeList		= paraSizeRecord.items()
	paraSizeList.sort()
	length			  = np.array([x[0] for x in paraSizeList])
	lengthCount		 = np.array([x[1] for x in paraSizeList])
	print pdfFitting(length,lengthCount)
	# plt.figure(figsize=(20,10))
	# plt.plot(length,lengthCount,'o')
	# plt.show()
def getHpoint(filename):
	scoreRecord	= {}

	fopen		   = open(filename,'r')
	content		 = fopen.read()
	paras		   = content.split('\n')
	wordcount	   = 0
	for para in paras:
		try:
			# score   = int(para.split("\t")[-1])
			score   = int(para.split(":")[-1].split(" ")[-1])
			# scoreb  = b(score,0.25)
			scoreb  = a(score,1)
			# if scoreb<2000:
			if scoreb in scoreRecord:
				scoreRecord[scoreb] += 1
			else:
				scoreRecord[scoreb] = 1
			# print scoreb
		except:
			continue

	scoreList = scoreRecord.items()
	scoreList.sort()
	# print scoreList
	for x in scoreList:
		print x[0],x[1]
	score1	  = np.array([x[0] for x in scoreList])
	scoreCount = np.array([x[1] for x in scoreList])
	title = 's'
	Tools.plot(score1,scoreCount,title)

	# a = 1.57507979e+00
	# b = 8.31522290e+04
	# x=1
	# while(x<powerLaw(x,a,b)):
	#	 x+= 1
	# print x
	# print powerLawFitting(score1,scoreCount,title)
def JaccardPlot(aimfilePath):
	# f = open("/home/dreamer/documents/code/database/Longitudinal_analyse/top10.txt",'wb')
	sets = []
	root = "/home/dreamer/documents/code/database/analysis/"
	filepaths	= Tools.generateFileLists(root)
	filepaths = sorted(filepaths)
	for filepath in filepaths:
		print filepath
		# print Tools.generateFileLists(filepath+'nounExtract/')
		wordS = set()
		sourceFile = filepath+'final/final.txt'
		lines = Tools.content_lines(sourceFile)
		# f.write(filepath.split("/")[-2]+',')
		for l in lines:
			wordS.add(l.split("\t:")[0])
			# f.write(l.split(":")[0]+',')
		sets.append(wordS)
		# f.write('\n')
	Jaccard = []
	for n in range(15):
		Jaccard.append(len(sets[n]&sets[15])/len(sets[n]|sets[15]))
		# Jaccard.append(len(sets[n]&sets[n+1])/len(sets[n]|sets[n+1]))
	rank	 = np.array([float(d+1) for d in range(len(Jaccard))])
	fre	  = np.array([float(x) for x in Jaccard])
	title = 'Jaccard_Index'
	# Tools.plot(rank,fre,title, xlabel="years",ylabel="Jaccard",show=1)
	Tools.plot(rank,fre,title,xlabel="years",ylabel="Jaccard",filepath="/home/dreamer/")
	print linearFitting(rank,fre,title,aimfilePath)


if __name__ == "__main__":
	pass

	# ParaSizeFit("/home/dreamer/documents/code/database/analysis/2000_2002/pretreatment/")
	aimfilePath = "/home/dreamer/documents/code/database/Longitudinal_analyse/"
	JaccardPlot(aimfilePath)
# filelist = ["/home/dreamer/documents/code/database/1afterAllwordSta/AllWords.txt","/home/dreamer/documents/code/database/1afterAllwordSta/allwordByMecab.txt"]
# rank_frequence("/home/dreamer/documents/code/database/1afterAllwordSta/AllWords.txt")
# rank_frequence(filelist[0])
# rank_frequence(filelist[1])
	# rank_frequence("/home/dreamer/documents/code/database/2000-2002/1afterAllwordSta/AllWords.txt")
# getHpoint("/home/dreamer/documents/code/database/1afterAllwordSta/TwoAndThree_sorted.txt")
