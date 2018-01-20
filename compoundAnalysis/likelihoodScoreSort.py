import os

def sort(filename):
	fopen	   = open(filename,'r')
	content	 = fopen.read()
	fopen.close()
	lines	   = content.split('\n')
	# print lines
	scoreList   = {}
	for line in lines:
		scoreStr = line.split(':')[-1]
		# scoreStr = line.split(':')[-1].split(' ')[-1]
		try:
			score   = float(scoreStr)
			scoreList[line] = score
		except:
			print scoreStr
			continue
	sortedScoreList 	= sorted(scoreList.items(), key=lambda d: d[1])

	newfilename	 = filename[:-4]+"_sorted.txt"
	# newFile	 = open('../database/afterCompoundScore/SortedTwoScoreRecord.txt','wb')
	newFile	 = open(newfilename,'wb')
	for element in sortedScoreList:
		# print element
		# word = element[0].split(':')[0]
		# wordscore = element[0].split(":")[-1]
		newFile.write(element[0]+'\n')
	newFile.close()

# filename = "/home/dreamer/documents/code/partOfSpeech/afterSpeech/TwoUseful_DuplicateRemoval.txt"
# filename = "/home/dreamer/documents/code/database/5afterCompoundScore/TwoScore.txt"
# filename = "/home/dreamer/documents/code/database/1afterAllwordSta/TwoAndThree.txt"
filename = "/home/dreamer/documents/code/database/5afterCompoundScore/TwoScore.txt"
sort(filename)
