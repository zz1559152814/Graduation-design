import os,sys
sys.path.append('../Tools')
import Tools

def tocsv(networkFile, tofile):
	fopen	   = open(networkFile, 'r')
	content	 = fopen.read()
	oneWordList = content.split('\n')
	newfile	 = open(tofile,'wb')
	connectSet  = set()
	for oneWord in oneWordList:
		try:
			thisWord	= oneWord.split(':')[0]
			occurWord   = oneWord.split(':')[1].split(' ')[:-1]
			for word in occurWord:
				if word+' '+thisWord not in connectSet:
					newfile.write(thisWord+' '+word+'\n')
					connectSet.add(thisWord+' '+word)
		except:
			print oneWord
	newfile.close()
	fopen.close()

def toNum(networkFile1,networkFile2, tofile):
	fopen	   = open(networkFile1, 'r')
	content	 = fopen.read()
	fopen.close()
	WordsList   = content.split('\n')
	wordsIndex  = {}
	for n in range(len(WordsList)):
		try:
			thisWord	= WordsList[n].split(':')[0]
			wordsIndex[thisWord] = n+1
			# print thisWord,wordsIndex[thisWord]
		except:
			print oneWord

	fopen2	  = open(networkFile2, 'r')
	content2	= fopen2.read()
	connectList = content2.split('\n')
	newfile	 = open(tofile,'wb')
	newfile.write("*Vertices"+" "+str(len(wordsIndex.keys())-1)+'\n')

	for x in range(len(wordsIndex)):
		wordIndexList = Tools.TupleSort(wordsIndex)
		if wordIndexList[x][0] != '':
			newfile.write(str(wordIndexList[x][1])+" \""+wordIndexList[x][0]+"\""+'\n')
	newfile.write("*Edges"+'\n')
	for connect in connectList:
		try:
			connectSide1 = connect.split(' ')[0]
			connectSide2 = connect.split(' ')[1]
			if wordsIndex[connectSide1] < wordsIndex[connectSide2]:
				newfile.write(str(wordsIndex[connectSide1])+' '+str(wordsIndex[connectSide2])+'\n')
		except:
			print connect
	newfile.close()

def NoWeight(NumNet, NoWeightf):
	lines = Tools.content_lines(NumNet)
	lineSet = set()
	NoWeightFile = open(NoWeightf,'wb')
	for line in lines:
		if line not in lineSet:
			lineSet.add(line)
			NoWeightFile.write(line+'\n')
	NoWeightFile.close()

def threshold(networkFile,thres):
	connTuple = {}
	edgeLines = Tools.content_lines(networkFile)
	newfile = open(networkFile[:-4]+"_threshold_3.csv",'wb')
	for line in edgeLines:
		if line in connTuple.keys():
			connTuple[line] += 1
		else:
			connTuple[line] = 1
	for conn in connTuple.keys():
		if connTuple[conn] >thres:
			vertexs = conn.split(' ')
			# try:
			i = connTuple[conn]
			# print i
			while(i):
				newfile.write(vertexs[0]+' '+vertexs[1]+'\n')
				i -= 1
			# except:

# networkFile  = "/home/dreamer/documents/code/generateNetwork/networkList.txt"
# tofile	   = "/home/dreamer/documents/code/generateNetwork/networkList.csv"
# # tocsv(networkFile,tofile)
# # threshold(tofile)
# fromFile1	= "/home/dreamer/documents/code/generateNetwork/networkList.txt"
# fromFile2	= "/home/dreamer/documents/code/generateNetwork/networkList_threshold_3.sif"
# NumNetword   = "/home/dreamer/documents/code/generateNetwork/networkSetNum_threshold_3.csv"
# # toNum(fromFile1, fromFile2, NumNetword)
# #
# NumNet = "/home/dreamer/documents/code/generateNetwork/networkSetNum.net"
# NoWeightf = "/home/dreamer/documents/code/generateNetwork/networkSetNumNoWeight.net"
# NoWeight(NumNet, NoWeightf)
