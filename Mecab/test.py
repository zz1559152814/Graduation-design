#!/usr/bin/python
# -*- coding: utf-8 -*-

import mecab

text 	= "お隣中国"
# mecab.MeCabClassForText(text)
test	= mecab.MeCabClass(text)
# a = test.GetAll3()
# print b
# for b in a:

print test.PrintAll()
#	1. print
# print test.PrintNoun2AndMark()
# print test.PrintNoun2()
#	2. get (retur	n list)
# VerbNodeList	= test.GetAdj()
# mydict	= dict()
# for node in VerbNodeList:
# 	if node not in mydict:
# 		mydict[node]	= 1
# 	else:
# 		mydict[node]	+= 1
