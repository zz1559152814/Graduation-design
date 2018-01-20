import os

def sort(oldFile,newFile):
	fopen3	   = open(oldFile,'r')
	content3	 = fopen3.read()
	fopen3.close()

	lines3	   = content3.split('\n')
	lines		= lines3
	scoreList   = {}
	for line in lines:
		scoreStr = line.split(':')[-1]
		try:
			score   = float(scoreStr)
			scoreList[line] = score
		except:
			print scoreStr
			continue
	sortedScoreList 	= sorted(scoreList.items(), key=lambda d: d[1], reverse=True)
	
	new	 = open(newFile,'wb')
	for element in sortedScoreList:
		# print element
		# word = element[0].split(':')[0]
		# wordscore = element[0].split(":")[-1]
		new.write(element[0]+'\n')
	new.close()

oldFile = "/home/dreamer/documents/code/database/3afterFiliter/TwoAndThree_afterEntroy.txt"
newFile = "/home/dreamer/documents/code/database/3afterFiliter/TwoAndThree_afterEntroy_afterSorted.txt"
sort(oldFile,newFile)
