# -*- coding: utf-8 -*-
import time,os,shutil
from pylab import *
from scipy import stats
from scipy import optimize
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
# matplotlib.use('Agg')

import traceback,re

def exeTime(func):
	def newFunc(*args, **args2):
		t0 = time.time()
		print "@%s, {%s} start" % (time.strftime("%X", time.localtime()), func.__name__)
		back = func(*args, **args2)
		print "@%s, {%s} end" % (time.strftime("%X", time.localtime()), func.__name__)
		print "@%.3fs taken for {%s}" % (time.time() - t0, func.__name__)
		return back
	return newFunc

def generateFileLists(filepath):
	fileLists 	= []
	files		= os.listdir(filepath)
	for file in files:
		if os.path.isdir(filepath+file):
			fileLists.append(filepath+file+'/')
		else:
			fileLists.append(filepath+file)
	return fileLists

@exeTime
def foo():
	for i in xrange(10000000):
		pass
def divideToTwoAndThree(from1):
	fromfile  		= open(from1,'r')
	lines  			= fromfile.read().split('\n')
	twofileName  	= from1[:-4]+'_two.txt'
	threefileName  	= from1[:-4]+'_three.txt'
	twoFile = open(twofileName,'wb')
	threeFile = open(threefileName,'wb')
	for line in lines:
		if len(line.split(':')[-1].split(' ')) == 3:
			twoFile.write(line+'\n')
		elif len(line.split(':')[-1].split(' ')) == 4:
			threeFile.write(line+'\n')
	twoFile.close()
	threeFile.close()
def sort(fromfile,threshold=-1):
	fopen3	   = open(fromfile,'r')
	content3	 = fopen3.read()
	fopen3.close()

	lines3	   = content3.split('\n')
	lines		= lines3
	scoreList   = {}
	for line in lines:
		scoreStr = line.split('\t:')[-1]
		try:
			score   = float(scoreStr)
			scoreList[line] = score
		except:
			print scoreStr
			continue
	sortedScoreList 	= sorted(scoreList.items(), key=lambda d: d[1],reverse=True)
	newFile	 = open(fromfile[:-4]+'_sorted.txt','wb')
	# newFile	 = open('/home/dreamer/documents/code/database/finalword/SortedFinalword.txt','wb')
	if threshold != -1:
		for element in range(threshold):
			newFile.write(sortedScoreList[-element][0]+'\n')
	else:
		for element in sortedScoreList:
			newFile.write(element[0]+'\n')
		newFile.close()
def TupleSort(Tuple):
	sortedList 	= sorted(Tuple.items(), key=lambda d: d[1], reverse=True)
	return sortedList
def merge(files,c):
	cf = open(c,'wb')
	for file in files:
		a = open(file,'r')
		cf.write(a.read()+'\n')
		a.close()
	cf.close()
#少子高齢:少子 高齢 1367 -> 取少子高齢
def content_wordList(filename, separator):
	fopen	   = open(filename, 'r')
	content	 = fopen.read()
	lines	   = content.split('\n')
	wordsList   = []
	for line in lines:
		wordsList.append(line.split(separator)[0])
	fopen.close()
	return wordsList[:-1]
#少子高齢:少子 高齢 1367 -> 取数字
def content_scoreList(filename, separators):
	fopen	   = open(filename, 'r')
	content	 = fopen.read()
	lines	   = content.split('\n')
	scoresList  = []
	for line in lines:
		try:
			scoresList.append(int(line.split(separators[-1])[-1].split(separators[1])[-1]))
		except:
			pass
	fopen.close()
	return scoresList
#高齢	86397 -> 取数字
def content_countList(filename, separators):
	fopen	   = open(filename, 'r')
	content	 = fopen.read()
	lines	   = content.split('\n')
	scoresList  = []
	for line in lines:
		try:
			scoresList.append(int(line.split(separators)[-1]))
		except:
			print line
	fopen.close()
	return scoresList
def content_lines(filename):
	fopen	   = open(filename, 'r')
	content	 = fopen.read()
	lines	   = content.split('\n')
	fopen.close()
	return lines
def content_paras(filename):
	fopen	   = open(filename, 'r')
	content	 = fopen.read()
	lines	   = content.split('>>>')
	fopen.close()
	return lines
def plot(x,y,title,xlabel=None,ylabel=None,filepath = None,for_long = 0,show=0):
	plt.figure(figsize=(20,10))
	plt.title(title,size=35)
	plt.plot(x,y,'o')
	plt.xlabel(xlabel,size=35)
	plt.ylabel(ylabel,size=35)
	# plt.axis([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16])
	if for_long == 1:
		subfileroot = []
		for i in range(1970,2017,3):
			subfileroot.append(str(i)+'-'+str(i+2))
		xticks([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16],subfileroot)
	plt.plot(x,y,'g',label='data',linewidth=1,color = 'green')
	# plt.plot(x,y,'r')
	if filepath is not None:
		plt.savefig(filepath+title+'.png')
	if show==1:
		plt.show()
def search(word, file):
	if re.search('_'+word+'_',file):
		return True
	if re.search('^'+word+'_',file):
		return True
	return False
# 最后一步，截取多少行
def ConvertCut(filename, newfilename, rows):
	lines	   = content_lines(filename)
	newfile	 = open(newfilename,'wb')
	for n in range(rows+1):
		newfile.write(lines[n]+'\n')
	newfile.close()
def mkdir(filePathname):
	if os.path.exists(filePathname) == False:
		os.mkdir(filePathname)
def exists(filePathname):
	return os.path.exists(filePathname)
def mergeDirectory(path1,path2,path3):
	if os.path.exists(path3) == False:
		Tools.mkdir(path3)
	path1fileList = generateFileLists(path1)
	path2fileList = generateFileLists(path2)
	for file in path1fileList:
		shutil.copy(file[:-1], path3+file.split('/')[-1])
	for file in path2fileList:
		shutil.copy(file[:-1], path3+file.split('/')[-1])
def getdirsize(dir):
   size = 0L
   for root, dirs, files in os.walk(dir):
	  size += sum([os.path.getsize(os.path.join(root, name)) for name in files])
   return size
def eliminate(source_file,aim_file,eliminate_wordlist):
	wordlist = content_lines(source_file)
	e_wordlist = content_lines(eliminate_wordlist)
	aim = open(aim_file,'wb')
	w = 1
	eliminate_list = ["^十分","^大変","大臣\t","委員\t","長官\t"]
	for line in wordlist:
		for word in e_wordlist:
			if word != '':
				if len(re.findall(word,line)) > 0:
					w = 0
		for x in eliminate_list:
			if len(re.findall(x,line)) > 0:
				w = 0
		if w == 1:
			aim.write(line+'\n')
		w = 1
	aim.close()
def select(word,path,aimPath):
	files = generateFileLists(path)
	newFile = open(aimPath+word+'.txt','wb')
	for file in files:
		paras = content_paras(file)
		for para in paras:
			content = para.split('::')[-1]
			iparas = content.split('\n')
			for ip in iparas:
				if re.search(word,ip) and re.search('高齢',ip):
					newFile.write(ip)
					newFile.write("\n")
	newFile.close()
if __name__ == "__main__":
	pass
	# path1 = "/home/dreamer/documents/code/database/conference/syugiin_1970_1999/"
	# path2 = "/home/dreamer/documents/code/database/conference/syugiin_2000_2017/"
	# path3 = "/home/dreamer/documents/code/database/conference/syugiin/"
	# mergeDirectory(path1,path2,path3)
	# a = "/home/dreamer/documents/code/database/2afterSpeech/TwoWordsMecabList.txt"
	# b= "/home/dreamer/documents/code/database/2afterSpeech/ThreeWordsMecabList.txt"
	# c = "/home/dreamer/documents/code/database/2afterSpeech/allWordsMecabList.txt"
	# merge(a,b,c)
	# divideToTwoAndThree("/home/dreamer/documents/code/database/3afterFiliter/allWordsMecabList.txt")
	# # sort("/home/dreamer/documents/code/database/6afterEntroyAmongFiles/entropyAmongFiles2.txt",500)
	# filename = "/home/dreamer/documents/code/database/6afterEntroyAmongFiles/allWordsMecabList.txt"
	# newfilename = "/home/dreamer/documents/code/database/6afterEntroyAmongFiles/allWordsMecabList_afterCut.txt"
	# ConvertCut(filename, newfilename, 500)
	# sort("/home/dreamer/documents/code/distributionEntropy/elimiate_wordList.txt")
	# aim_file = "/home/dreamer/documents/code/database/2000-2002/7finalword/SortedFinalword3.txt"
	# source_file = "/home/dreamer/documents/code/database/2000-2002/7finalword/SortedFinalword.txt"
	# eliminate_wordlist = "/home/dreamer/documents/code/database/condition/eliminate_wordlist.txt"
	# eliminate(source_file,aim_file,eliminate_wordlist)
