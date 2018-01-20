# -*- coding: utf-8 -*-
import sys,os



file = "/home/dreamer/a.txt"
f = open(file,'r')
content = f.read()
paras = content.split('\n\n')
print len(paras)
# words = content.split(' ')
# wordTuple = {}
# for w in words:
# 	if w not in wordTuple.keys():
# 		wordTuple[w] = 1
# 	else:
# 		wordTuple[w] += 1
#
# wordList = sorted(wordTuple.items(), key=lambda d: d[1], reverse=True)
#
# for w in wordList:
# 	print w[0],w[1]
