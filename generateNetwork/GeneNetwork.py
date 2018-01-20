#-*-encoding:utf-8-*-
import os,sys,re
sys.path.append('../Tools')
import Tools,time

def search(word, file):
	if re.search('_'+word+'_',file):
		return True
	if re.search('^'+word+'_',file):
		return True
	return False

def generateFileLists(filepath):
	fileLists 	= []
	files		= os.listdir(filepath)
	for file in files:
		fileLists.append(filepath+file)
	return fileLists

# @Tools.exeTime
def GenerNetwork(finalWordRec, txtFilename, recordFile):
	wordlist			= []
	finalWordlines	  = Tools.content_lines(finalWordRec)
	for line in finalWordlines:
		if line != '':
			wordlist.append(line.split('\t:')[0])

	filelists		   = generateFileLists(txtFilename)
	txtlist			 = []
	for file in filelists:
		txtFilelines		= Tools.content_lines(file)
		for para in txtFilelines:
			if para != '':
				txtlist.append(para)

	recordFile		  = open(recordFile, 'wb')
	runCounter 		= 0
	startTime  		= time.time()
	for word in wordlist:
		runCounter += 1
		if runCounter%20 == 0:
			# os.system('clear')
			# print "This is the",runCounter,"th lines"
			endTime  		= time.time()
			# print "Run time is:",endTime-startTime
			startTime  		= time.time()
		# cooccurSet		  = set() # 无权重，即无重复链接，一个与一个词汇之间只有一个链接
		cooccurList			= []  # 加权重，即允许重复链接
		for para in txtlist:
			if search(word, para) is True:
				for word2 in wordlist:
					if word2 != word:
						if search(word2,para) is True:
							cooccurList.append(word2)
		recordFile.write(word+':')
		# for cooccurWord in cooccurSet:
		for cooccurWord in cooccurList:
			recordFile.write(cooccurWord+' ')
		recordFile.write('\n')
	recordFile.close()

finalWordRec	= "/home/dreamer/documents/code/database/analysis/1973_1975/final/final.txt"
# txtFilepath	 = '../database/afterselect/1/allcontentNoun.txt'
txtFilepath	 = "/home/dreamer/documents/code/database/analysis/1973_1975/nounExtract_pre/"
# finalWordRec	= './test2.txt'
# txtFilepath	 = './test1.txt'
recordFile	  = "/home/dreamer/documents/code/database/analysis/1973_1975/net.txt"
# GenerNetwork(finalWordRec, txtFilepath, recordFile)
