# -*- coding: utf-8 -*-
from igraph import *
import sys
sys.path.append('/home/dreamer/documents/code/Tools')
import Tools

# def subGraphCommunity(file,vertexList):
# 	lines = Tools.content_lines()
# 	g = Graph()
# 	g.es["weight"] = 1.0
# 	edgeTuple = {}
# 	for l in lines:
# 		word1 = l.split(',')[0]
# 		word2 = l.split(',')[1]
# 		if word1 in vertexList and word2 in vertexList:
# 			if word1+","+word2 in edgeTuple.keys():
# 				edgeTuple[word1+","+word2] = 1
# 			else:
# 				edgeTuple[word1+","+word2] += 1
# 	for e in edgeTuple.keys():
# 		w1 = e.split(',')[0]
# 		w2 = e.split(',')[1]
# 		g[w1,w2] = edgeTuple[e]
# 	communities = g.community_multilevel(weights='weight',return_levels=False)
# 	return communities
class igraph(object):
	def __init__(self,file):
		lines = Tools.content_lines(file)
		edgeTuple = {}
		verticlesTuple = {}
		for l in lines[:-1]:
			if l in edgeTuple.keys():
				edgeTuple[l] += 1
			else:
				edgeTuple[l] = 1
			word1 = l.split(' ')[0]
			word2 = l.split(' ')[1]
			if word1 in verticlesTuple.keys():
				verticlesTuple[word1] += 1
			else:
				verticlesTuple[word1] = 1
			if word2 in verticlesTuple.keys():
				verticlesTuple[word2] += 1
			else:
				verticlesTuple[word2] = 1
		self.g =Graph()
		self.g.es["weight"] = 1.0
		for key in verticlesTuple.keys():
			verticlesTuple[key] /= 2
			self.g.add_vertices([key])
		for key in edgeTuple.keys():
			self.g[key.split(' ')[0],key.split(' ')[1]] = edgeTuple[key]

	def community(self):
		communities = self.g.community_multilevel(weights='weight',return_levels=False)
		commCnt = communities.__len__()
		communitiesList = []
		for n in range(commCnt):
			g	= Graph()
			g	= communities.subgraph(n)
			communitiesList.append(g)
		return communitiesList

	def community_2(self,communitiesList):
		subCommList  	 = []
		subCommListInOne = []
		for comm in communitiesList:
			subComm = comm.community_multilevel(weights='weight',return_levels=False)
			commCnt = subComm.__len__()
			for n in range(commCnt):
				g	= Graph()
				g	= subComm.subgraph(n)
				subCommListInOne.append(g)
			subCommList.append(subCommListInOne)
			subCommListInOne = []
		return subCommList

	def importance(self,community):
		vs = []
		for v in community.vs():
			vs.append(v)
		return sum(self.g.strength(vs,weights='weight'))

	def AllStrength(self):
		return sum(self.g.strength(self.g.vs(),weights='weight'))
if __name__ == "__main__":
	file = "/home/dreamer/documents/code/generateNetwork/networkList_threshold_3.csv"
	IG = igraph(file)

	for g in IG.community():
		print g
