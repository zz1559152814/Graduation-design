#!/usr/bin/python
# -*- coding: utf-8 -*-
import MeCab
import re

def MeCabClassForText(text):
	wordlist = []
	t = MeCab.Tagger (" ")
	textNode = t.parseToNode(text)
	while textNode:
		wordlist.append(textNode.surface)
		print textNode.surface
		textNode	= textNode.next

class MeCabClass(object):

	def __init__(self, text):
		self.text	= text;
		try:
			self.t = MeCab.Tagger (" ")
			self.textNode = self.t.parseToNode(text)
			self.word_box	= []
			self.word_dict	= {}
		except RuntimeError as e:
			print("RuntimeError:", e);
	def WordCount(self):
		count = 0
		while self.textNode:
			if self.textNode.feature[0] != 'B':
				count = count + 1
			self.textNode	= self.textNode.next
		return count
	def PrintAll(self):
		counter = 0
		while self.textNode:
			if self.textNode.feature[0] != 'B':
				print self.textNode.surface, "\t", self.textNode.feature
				counter = counter + 1
			self.textNode	= self.textNode.next
		print "words counter:",counter
		return counter
	def PrintNoun(self): #语义上的名词,#形容動詞語幹,语义上的名词
		while self.textNode:
			featureList	= re.split(',',self.textNode.feature)
			if featureList[0] == "名詞":
				if featureList[1] != "数" and featureList[1] != "副詞可能"  and featureList[1] != "接尾" \
				and featureList[1] != "非自立" and featureList[1] != "代名詞" and featureList[2] != "人名" \
				and featureList[1] != "サ変接続":
					print self.textNode.surface, "\t\t", self.textNode.feature
			self.textNode	= self.textNode.next
	def PrintNoun2(self):#包含サ変接続语义上的名词
		while self.textNode:
			featureList	= re.split(',',self.textNode.feature)
			if featureList[0] == "名詞":
				if featureList[1] != "数" and featureList[1] != "副詞可能"  and featureList[1] != "接尾" \
				and featureList[1] != "非自立" and featureList[1] != "代名詞" and featureList[2] != "人名":
					print self.textNode.surface, "\t\t", self.textNode.feature
			self.textNode	= self.textNode.next
	def PrintNoun2AndMark(self):#包含サ変接続语义上的名词
		while self.textNode:
			featureList	= re.split(',',self.textNode.feature)
			if featureList[0] == "名詞":
				if featureList[1] != "数" and featureList[1] != "副詞可能"  and featureList[1] != "接尾" \
				and featureList[1] != "非自立" and featureList[1] != "代名詞" and featureList[2] != "人名":
					print self.textNode.surface, "\t\t", self.textNode.feature
			if featureList[0] == "記号":
				print self.textNode.surface, "\t\t", self.textNode.feature
			self.textNode	= self.textNode.next
	def PrintNounl(self): #语义上的名词,#形容動詞語幹,语义上的名词
		while self.textNode:
			featureList	= re.split(',',self.textNode.feature)
			if featureList[0] == "名詞":
				print self.textNode.surface, "\t\t", self.textNode.feature
			self.textNode	= self.textNode.next
	def PrintAdj(self):
		while self.textNode:
			featureList	= re.split(',',self.textNode.feature)
			if featureList[0] == "名詞" and featureList[1] == "形容動詞語幹" or featureList[0] == "形容詞":
				print self.textNode.surface, "\t\t", self.textNode.feature
			self.textNode	= self.textNode.next
	def PrintAdv(self):
		while self.textNode:
			featureList	= re.split(',',self.textNode.feature)
			if featureList[0] == "副詞":
				print self.textNode.surface, "\t\t", self.textNode.feature
			self.textNode	= self.textNode.next
	def PrintVerb(self):
		while self.textNode:
			featureList	= re.split(',',self.textNode.feature)
			if featureList[0] == "動詞" and featureList[1] != "接尾":
				if featureList[5] != "未然レル接続" and featureList[4] != "サ変・スル" :
					print self.textNode.surface, "\t\t", self.textNode.feature
			elif featureList[0] == "名詞" and featureList[1] == "サ変接続":
				print self.textNode.surface, "\t\t", self.textNode.feature
			self.textNode	= self.textNode.next
	def PrintAux(self):
		while self.textNode:
			featureList	= re.split(',',self.textNode.feature)
			if featureList[0] == "助詞":
				print self.textNode.surface, "\t\t", self.textNode.feature
			self.textNode	= self.textNode.next
	def PrintAuxV(self):
		while self.textNode:
			featureList	= re.split(',',self.textNode.feature)
			if featureList[0] == "助動詞":
				print self.textNode.surface, "\t\t", self.textNode.feature
			self.textNode	= self.textNode.next
	def isNoun2(self,wordDiscript):#包含サ変接続语义上的名词
		featureList	= re.split(',',wordDiscript)
		if featureList[0] == "名詞":
			if featureList[1] != "数" and featureList[1] != "副詞可能"  and featureList[1] != "接尾" \
			and featureList[1] != "非自立" and featureList[1] != "代名詞" and featureList[2] != "人名":
				return 1
		return 0
	def GetAll(self):
		VerbNodeList	= []
		while self.textNode:
			# wordDiscript	= [self.textNode.surface,self.textNode.feature]
			if self.textNode.feature[0] != 'B':
				VerbNodeList.append(self.textNode.surface)
			self.textNode = self.textNode.next
		return VerbNodeList
	def GetAll2(self): # surface and feature
		VerbNodeList	= []
		while self.textNode:
			# wordDiscript	= [self.textNode.surface,self.textNode.feature]
			if self.textNode.feature[0] != 'B':
				VerbNodeList.append([self.textNode.surface,self.textNode.feature])
			self.textNode = self.textNode.next
		return VerbNodeList
	def GetAll3(self): # feature[1] 即第二詞性
		VerbNodeList	= []
		while self.textNode:
			# wordDiscript	= [self.textNode.surface,self.textNode.feature]
			if self.textNode.feature[0] != 'B':
				VerbNodeList.append(self.textNode.feature.split(',')[1]+'_'+self.textNode.feature.split(',')[2])
			self.textNode = self.textNode.next
		return VerbNodeList
	def GetVerb(self):
		VerbNodeList	= []
		while self.textNode:
			# print self.textNode.surface, "\t", self.textNode.feature
			featureList	= re.split(',',self.textNode.feature)
			if featureList[0] == "動詞" and featureList[1] != "接尾":
				if featureList[5] != "未然レル接続" and featureList[4] != "サ変・スル" :
					VerbNodeList.append(self.textNode.surface)
			elif featureList[0] == "名詞" and featureList[1] == "サ変接続":
				VerbNodeList.append(self.textNode.surface)
			self.textNode = self.textNode.next
		return VerbNodeList
	def GetNoun(self):
		VerbNodeList	= []
		while self.textNode:
			# print self.textNode.surface, "\t", self.textNode.feature
			featureList	= re.split(',',self.textNode.feature)
			if featureList[0] == "名詞":
				if featureList[1] != "数" and featureList[1] != "副詞可能"  and featureList[1] != "接尾" \
				and featureList[1] != "非自立" and featureList[1] != "代名詞" and featureList[2] != "人名" \
				and featureList[1] != "サ変接続":
					VerbNodeList.append(self.textNode.surface)
			self.textNode = self.textNode.next
		return VerbNodeList
	#incldue サ変接続 : for classify
	def GetNoun2(self):
		VerbNodeList	= []
		while self.textNode:
			# print self.textNode.surface, "\t", self.textNode.feature
			featureList	= re.split(',',self.textNode.feature)
			if featureList[0] == "名詞":
				if featureList[1] != "数" and featureList[1] != "副詞可能"  and featureList[1] != "接尾" \
				and featureList[1] != "非自立" and featureList[1] != "代名詞" and featureList[2] != "人名" :
					VerbNodeList.append(self.textNode.surface)
			self.textNode = self.textNode.next
		return VerbNodeList
	def GetAdj(self):
		VerbNodeList	= []
		while self.textNode:
			# print self.textNode.surface, "\t", self.textNode.feature
			featureList	= re.split(',',self.textNode.feature)
			if featureList[0] == "名詞" and featureList[1] == "形容動詞語幹" or featureList[0] == "形容詞":
				VerbNodeList.append(self.textNode.surface)
			self.textNode = self.textNode.next
		return VerbNodeList
	def GetAdv(self):
		VerbNodeList	= []
		while self.textNode:
			# print self.textNode.surface, "\t", self.textNode.feature
			featureList	= re.split(',',self.textNode.feature)
			if featureList[0] == "副詞":
				VerbNodeList.append(self.textNode.surface)
			self.textNode = self.textNode.next
		return VerbNodeList
	def GetAux(self):
		VerbNodeList	= []
		while self.textNode:
			# print self.textNode.surface, "\t", self.textNode.feature
			featureList	= re.split(',',self.textNode.feature)
			if featureList[0] == "助詞":
				VerbNodeList.append(self.textNode.surface)
			self.textNode = self.textNode.next
		return VerbNodeList
	def GetAuxV(self):
		VerbNodeList	= []
		while self.textNode:
			# print self.textNode.surface, "\t", self.textNode.feature
			featureList	= re.split(',',self.textNode.feature)
			if featureList[0] == "助動詞":
				VerbNodeList.append(self.textNode.surface)
			self.textNode = self.textNode.next
		return VerbNodeList
	def Frequence(self,word):
		while self.textNode:
			self.word_box.append(self.textNode.surface)
			self.textNode	= self.textNode.next
		for item in self.word_box:
			if item not in self.word_dict:
				self.word_dict[item]	= 1
			else:
				self.word_dict[item]	+= 1
		return self.word_dict[word]

if __name__ == '__main__':
	pass
	# def GetVerb
	# def GetVerb
	# def GetVerb
