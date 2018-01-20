from __future__ import division
import re
import os
import sys
from scipy import stats

def generateCompoundList():
	fopen 		= open("/home/dreamer/documents/code/database/5afterCompoundScore/TwoScore.txt",'r')
	newFile  	= open("/home/dreamer/documents/code/database/5afterCompoundScore/TwoScore_sorted.txt",'wb')
	content 	= fopen.read()
	lines 		= content.split('\n')
	for line in lines:
		try:
			if float(line.split(":")[-1]) < -3.94:
				# if float(line.split(":")[-2]) > 10:
				newFile.write(line+'\n')
		except:
			continue
		# if score < -3.94 :
		# 	compound 	= line.split(':')[0]
		# 	newFile.write(compound,counter)

generateCompoundList()
