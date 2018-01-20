# -*- coding: utf-8 -*-
from __future__ import division
import sys,traceback
sys.path.append('../Tools')
sys.path.append('../statistics')
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import Tools,curveFitting
from scipy import stats,optimize
import igraph
class nxClass(object):
	def __init__(self,filename,threshold = 0):
		edgeLines = Tools.content_lines(filename)
		# 构建加权网络以及根据阈值建立链接
		self._generate_weighted_graph_(edgeLines, threshold)
		# 构建无权网络
		self._generate_graph_(edgeLines, threshold)
		# 构建相似权加权网络
		self._generate_similarity_weighted_graph_()
		self.nodeCnt = nx.number_of_nodes(self.WG)
		self.edgeCnt = self.edgeC()
		print "the number of nodes in this network is:",self.nodeCnt
		print "the number of edges in this network is:",self.edgeCnt
		print "the number of edges in this network is:",nx.number_of_edges(self.G)
		# 计算平均距离
		# self.average_dis =  self._average_distance_()
	def _generate_weighted_graph_(self,edgeLines, threshold=0):
		self.WG=nx.MultiGraph()
		connTuple = {}
		for line in edgeLines:
			if line in connTuple.keys():
				connTuple[line] += 1
			else:
				connTuple[line] = 1
		for conn in connTuple.keys():
			if connTuple[conn] >threshold:
				vertexs = conn.split(' ')
				try:
					# print conn,connTuple[conn]
					self.WG.add_edge(vertexs[0],vertexs[1],weight=connTuple[conn])
				except:
					pass

		allnode1 = self.WG.node
		allnode2 = self.WG.node
	def _generate_graph_(self,edgeLines,threshold):
		self.G=nx.Graph()
		for line in edgeLines:
			vertexs = line.split(' ')
			edge_set = set()
			cnt =0
			try:
				if vertexs[0]+','+vertexs[1] not in edge_set:
					self.G.add_edge(vertexs[0],vertexs[1])
				edge_set.add(vertexs[0]+','+vertexs[1])
				edge_set.add(vertexs[1]+','+vertexs[0])
			except:
				# traceback.print_exc()
				print line
	def _generate_similarity_weighted_graph_(self):
		connectSet = set()
		self.SWG = nx.MultiGraph()
		allnode1 = self.WG.node
		allnode2 = self.WG.node
		connectSet  = set()
		for node1 in allnode1:
			for node2 in allnode2:
				if node2+' '+node1 not in connectSet:
					connectSet.add(node1+' '+node2)
					if self.WG.has_edge(node1, node2):
						Sweight = self.weightBwt(node1, node2, "WG")
						self.SWG.add_edge(node1, node2,weight=float(1)/float(Sweight))
						S2weight = self.weightBwt(node1, node2, "SWG")
	def average_distance(self):
		Total_dis = 0
		for node1 in self.SWG:
			for node2 in self.SWG:
				if self.SWG.has_edge(node1,node2):
					shortPathLength = nx.shortest_path_length(self.SWG,node1,node2,weight='weight')
					Total_dis += shortPathLength
		average_dis = Total_dis/(self.nodeCnt*(self.nodeCnt-1))
		return average_dis
	def all_neibor(self,node):
		return nx.all_neighbors(self.WG,node)
	def average_clustering(self):
		return nx.average_clustering(self.WG,weight='weight')
	def average_weight(self):
		edge_num1 =  self.edgeCnt
		edge_num2 =  nx.number_of_edges(self.G)
		return edge_num1/edge_num2
	def assortativity(self):
		return nx.degree_assortativity_coefficient(self.SWG,weight='weight')
	def betweenness_centrality(self):
				a = nx.betweenness_centrality(self.SWG,weight='weight')
				self.bcList = Tools.TupleSort(a)
	def betweenness(self, node):
					bcList = self.betweenness_centrality()
					for bc in self.bcList:
						if bc[0] == node:
							return bc[1]
	def betweenness_distribution(self):
		y = np.zeros(len(self.bcList))
		for n in range(len(self.bcList)):
			y[n] = self.bcList[n][1]
		x = np.arange(0,len(self.bcList),1)
		title = "betweenness_distribution"
		Tools.plot(x,y,title)
	def clustering_degree_correlation(self,filepath=None):
		x = np.linspace(1,self.nodeCnt,self.nodeCnt)
		degreeTuple = {}
		nodeList	= []
		degreeList  = []
		# 对于每个度值下对应的多个点，对其中每个点分析其与其邻居间存在的边数，记录在degreeTuple中
		# 并将度值记录在degreeList，再进行排序
		allnode = self.WG.node
		for node in allnode:
			degree_unweight = self.G.degree(node)
			# degree_unweight = self.weightOfNode(node)
			if degree_unweight in degreeTuple:
				degreeTuple[degree_unweight].append(nx.clustering(self.WG, node, weight="weight"))
			else:
				degreeTuple[degree_unweight] = []
				degreeTuple[degree_unweight].append(nx.clustering(self.WG, node, weight="weight"))
		for key in degreeTuple.keys():
			degreeTuple[key] = sum(degreeTuple[key])/len(degreeTuple[key])
		degree_clustering = [(d,degreeTuple[d]) for d in sorted(degreeTuple.keys())]
		degreeNp		= np.array([x[0] for x in degree_clustering][1:])
		correlationsNp  = np.array([x[1] for x in degree_clustering[1:]])
		title = "clustering_degree_correlation curve fitting"
		# return curveFitting.reciprocalFitting(degreeNp, correlationsNp, title,filepath)
		return curveFitting.powerLawFitting(degreeNp, correlationsNp, title,filepath)
		# Tools.plot(degreeNp, correlationsNp,title,filepath)
	def center(self):
		return nx.center(self.SWG)
	def degree(self):
		return self.WG.degree(weight="weight")
	def degree_node(self,node):
		return self.WG.degree(node,weight="weight")
	def degree_node_unweight(self,node):
		return len(self.WG.adj[node])
	def degree_distrubition(self):
		x = np.linspace(1,self.nodeCnt,self.nodeCnt)
		degreeTuple = {}
		for ele in self.WG.degree(weight='weight'):
			degreeTuple[ele[0]] = ele[1]
		degreeList = Tools.TupleSort(degreeTuple)
		degreeNp   = np.array([degreeList[n][1] for n in range(self.nodeCnt)])
		vertexIndex = np.array(x)
		title = "Degree distribution curve fitting"
		curveFitting.powerLawFitting(vertexIndex, degreeNp, title)
		Tools.plot(vertexIndex, degreeNp)
	def density(self):
		all_clustering = 0
		for ele in self.WG.degree(weight='weight'):
			all_clustering += ele[1]
			return all_clustering*2/(self.nodeCnt*(self.nodeCnt-1))
	def diameter(self):
		return nx.diameter(self.SWG)
	def distance_distribution(self,graph="SWG"):
		if graph=="WG":
			thisGraph = nx.MultiGraph()
			thisGraph = self.WG
		elif graph=="SWG":
			thisGraph = nx.MultiGraph()
			thisGraph = self.SWG
		elif graph=="G":
			thisGraph = nx.Graph()
			thisGraph = self.G
		shortPathLengthTuple = {}
		for node1 in thisGraph:
			for node2 in thisGraph:
				if thisGraph.has_edge(node1,node2):
					shortPathLength = nx.shortest_path_length(thisGraph,node1,node2,weight='weight')
					shortPathLength2 = curveFitting.b(shortPathLength,0.05)
					if shortPathLength2 in shortPathLengthTuple:
						shortPathLengthTuple[shortPathLength2] += 1
					else:
						shortPathLengthTuple[shortPathLength2] = 1
		shortPathLengthList = sorted(shortPathLengthTuple.items(),key=lambda d:d[0],reverse=True)
		x = np.zeros(len(shortPathLengthList))
		y = np.zeros(len(shortPathLengthList))
		for n in range(len(shortPathLengthList)):
			x[n] = shortPathLengthList[n][0]
			y[n] = shortPathLengthList[n][1]/2
		title = "distance_distribution"
		Tools.plot(x,y,title)
	def edgeC(self):
		dis = 0
		for n,nbrsdict in self.WG.adjacency():
			for nbr,keydict in nbrsdict.items():
				for key,eattr in keydict.items():
					if 'weight' in eattr:
						dis += eattr['weight']
		return int(dis/2)
	def nodeC(self):
		return self.nodeCnt
	def printAllEdges(self):
		for node1 in self.WG.node:
			for node2 in self.WG.node:
				if self.WG.has_edge(node1,node2):
					print node1, node2, self.weightBwt(node1, node2,"WG")
	def rich_club_coefficient(self):
		return nx.rich_club_coefficient(self.G)
	def returnGraph(self,graph = "WG"):
		if graph == "WG":
			return self.WG
		elif graph == "SWG":
			return self.SWG
		elif graph == "G":
			return self.SWG
	def subgraph(self,list):
		return self.WG.subgraph(list)
	def shortest_path(self, node1, node2, graph="WG"):
		if graph=="WG":
			return nx.all_shortest_paths(self.WG, node1, node2)
		elif graph=="SWG":
			return nx.all_shortest_paths(self.SWG, node1, node2)
		elif graph=="G":
			return nx.all_shortest_paths(self.G, node1, node2)
	def weightBwt(self, node1, node2, graph="WG"):
		try:
			dis = 0
			if graph == "WG":
				Thisgraph = self.WG
			elif graph == 'SWG':
				Thisgraph = self.SWG
			for n,nbrsdict in Thisgraph.adjacency():
				if n == node1:
					for nbr,keydict in nbrsdict.items():
						if nbr == node2:
							for key,eattr in keydict.items():
								if 'weight' in eattr:
									dis += eattr['weight']
			return dis
		except:
			traceback.print_exc()
			# print node1,node2
	def weightOfNode(self,node):
		wei = 0
		for n,nbrsdict in self.WG.adjacency():
			if n == node:
				for nbr,keydict in nbrsdict.items():
					for key,eattr in keydict.items():
						if 'weight' in eattr:
							wei += eattr['weight']
		return wei
	def weight_distribution(self,filepath):
		connectCntTuple = {}
		for n,nbrsdict in self.WG.adjacency():
			for nbr,keydict in nbrsdict.items():
				for key,eattr in keydict.items():
					if 'weight' in eattr:
						if n+' '+nbr in connectCntTuple.keys():
							connectCntTuple[n+' '+nbr] += eattr['weight']
						else:
							connectCntTuple[n+' '+nbr] = eattr['weight']
		connectCntList = Tools.TupleSort(connectCntTuple)
		x = np.arange(1,len(connectCntList)+1,1)
		y = np.zeros(len(connectCntList))
		for n in range(len(connectCntList)):
			y[n] = connectCntList[n][1]
			# print connectCntList[n][1]
		title = 'weight_distribution'
		# Tools.plot(x,y,title)
		return curveFitting.powerLawFitting(x,y,title,filepath)
	def draw(self):
		nx.draw(self.SWG,weight="weight")
		nx.draw(self.SWG,pos=nx.spring_layout(G1),weight="weight")
		plt.draw()
		plt.show()
	def test(self):
		allnode1 = self.WG.node
		allnode2 = self.WG.node
		for node1 in allnode1:
			for node2 in allnode2:
				if self.WG.has_edge(node1, node2):
					# if node1 =="連立政権" and node2=="社会保障":
					print node1, node2,self.weightBwt(node1, node2, graph="WG")/2

if __name__ == "__main__":
	pass
	G = nxClass("/home/dreamer/documents/code/database/analysis/1970_1972/networkFile/networkList.csv",threshold = 0)
	print G.average_weight()
	# G.test()
