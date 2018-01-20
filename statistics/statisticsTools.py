# -*- coding: utf-8 -*-
import sys
sys.path.append('../Mecab')
import mecab
import os
from collections import *
import re

class Statistics(object):

	def __init__(self,fileLists):
		self.counter	= 0
		self.fileLists	= fileLists
		self.wordBox 	= dict()

	def setBoxFile(self,wordBox):
		self.counter	= 0
		self.wordBox 	= wordBox

	def wordFre(self, keyword):
		count 		= 0
		if len(self.fileLists) is 0:
			return count
		for file in self.fileLists:
			fopen 		= open(file,'r')
			content	= fopen.read()
			try:
				count 		+= len(re.findall(keyword,content))
			except:
				print "there is something during dealing with keyword:",keyword
			fopen.close()
		return count

	def getWordBox(self):
		runCounter  	= 0
		for file in self.fileLists:
			runCounter += 1
			if runCounter%200 == 0:
				os.system('clear')
				print "This is the",runCounter,"th lines"
			fopen 		= open(file,'r')
			content		= fopen.read()
			paras  		= content.split('>>>')
			for para in paras:
				nounInCon	= mecab.MeCabClass(para.split('::')[-1]).GetNoun2()
				self.counter += len(nounInCon)
				for noun in nounInCon:
					if noun not in self.wordBox:
						self.wordBox[noun] = 1
					else:
						self.wordBox[noun] += 1
		return self.wordBox

	def setCounter(self,n):
		self.counter 	= n


	def wordCounter(self):
		if self.counter != 0:
			return self.counter
		else:
			for file in self.fileLists:
				fopen 		= open(file,'r')
				content		= fopen.read()
				nounInCon	= mecab.MeCabClass(content).GetNoun2()
				self.counter += len(nounInCon)
			return self.counter

	def LFfilter(self,threshold):
		for key in self.wordBox.keys():
			if self.wordBox[key] <= threshold:
				del self.wordBox[key]
