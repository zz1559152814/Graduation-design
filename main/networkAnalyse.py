# -*- coding: utf-8 -*-
from __future__ import division
import os,sys
sys.path.append('../Tools')
sys.path.append('../networkx')
sys.path.append('../generateNetwork')
import math,time,traceback,nxClass,graph
import numpy as np
import Tools,GeneNetwork,tocsv,re
from matplotlib.ticker import MultipleLocator, FormatStrFormatter

analysisPath = "/home/dreamer/documents/code/database/analysis/"
filepaths	= Tools.generateFileLists(analysisPath)
filepaths = sorted(filepaths)
# filepaths = ["/home/dreamer/documents/code/database/analysis/2000_2002/"]

# creat network file
print "creat network file begin"
for filepath in filepaths:
	print "\tprocess with ",filepath.split("/")[-2]
	Tools.mkdir(filepath+'networkFile/')
	finalWordRec = filepath+'final/final.txt'
	txtFilepath  = filepath+'nounExtract_pre/'
	recordFile   = filepath+'networkFile/networkList.txt'
	if os.path.exists(recordFile) is False:
		GeneNetwork.GenerNetwork(finalWordRec, txtFilepath, recordFile)
	# if os.path.exists(recordFile_csv) is False:
	recordFile_csv   = filepath+"networkFile/networkList.csv"
	tocsv.tocsv(recordFile,recordFile_csv)
print "creat network file end"

creat networkx
print "creat networkx begin"
for filepath in filepaths:
	print "\tprocess with ",filepath.split("/")[-2]
	recordFile_csv   = filepath+"networkFile/networkList.csv"
	recordFile_thres   = filepath+"networkFile/networkList_threshold_3.csv"
	Tools.mkdir(filepath+'networkx/')
	# get threshold
	G = nxClass.nxClass(recordFile_csv,threshold = 0)
	# threshold = int(round(G.average_weight()))
	# generate the file networkList_threshold_3.csv
	# tocsv.threshold(recordFile_csv,threshold)
	# generate the network with threshold
	# G = nxClass.nxClass(recordFile_thres,threshold = threshold)
	recordFilename = filepath+'networkx/recordFile.txt'
	if os.path.exists(recordFilename) is False:
		recordFile = open(recordFilename,"wb")
		# 平均聚集系数 -
		print "\taverage_clustering procession"
		recordFile.write("average_clustering:")
		recordFile.write(str(G.average_clustering())+'\n')
		# 平均权   - threshold
		print "\taverage_weight procession"
		recordFile.write("average_weight:")
		recordFile.write(str(G.average_weight())+'\n')
		# 层次性
		print "\tclustering_degree_correlation procession"
		recordFile.write("clustering_degree_correlation:")
		a = G.clustering_degree_correlation(filepath+'networkx/')
		recordFile.write(str(a[0])+'\n')
		# 平均距离 - 小世界
		print "\taverage_distance procession"
		recordFile.write("average_distance:")
		recordFile.write(str(G.average_distance())+'\n')
		# 权重分布 - 无标度
		print "\tweight_distribution procession"
		recordFile.write("weight_distribution:")
		a = G.weight_distribution(filepath+'networkx/')
		recordFile.write(str(a[0])+'\n')
		# 高龄 出现频数
		print "\tweight_distribution procession"
		recordFile.write("高龄_frequence:")
		lines = Tools.content_lines(filepath+'wordRecord/allwordByMecab.txt')
		for n in range(len(lines)):
			if re.search('高齢',lines[-n]):
				cnt = lines[-n].split('\t')[1]
				break
		recordFile.write(cnt+'\n')
		recordFile.close()
print "creat networkx end\n"

community divide
print "community divide begin"
for filepath in filepaths:
	print "\tprocess with ",filepath.split("/")[-2]
	if os.path.exists(filepath+'communityInfo/') is False:
		Tools.mkdir(filepath+'communityInfo/')
		netWorkFile = filepath+"networkFile/networkList.csv"
		# if Tools.generateFileLists(filepath+'communityInfo') == []:
		IG = graph.igraph(netWorkFile)
		community_1 = IG.community()
		community_2 = IG.community_2(community_1)
		# print len(community_1)
		AllStrength = IG.AllStrength()
		f1 = open(filepath+'communityInfo/'+'community'+'_level1.txt','wb')
		for n in range(len(community_1)):
			f = open(filepath+'communityInfo/'+'community'+str(n)+'.txt','wb')
			f.write(str(n)+':')
			f1.write(str(n)+':'+str(IG.importance(community_1[n])/AllStrength)+':')
			for vertexs in community_1[n].vs():
				f.write(vertexs['name']+' ')
				f1.write(vertexs['name']+' ')
			f1.write('\n\n')
			f.write('\n\n')
			# community level1
			for m in range(len(community_2[n])):
				f.write(str(m)+':'+str(IG.importance(community_2[n][m])/AllStrength)+':')
				for vertexs in community_2[n][m].vs():
					f.write(vertexs['name']+' ')
				f.write('\n\n')
			f.close()
print "community divide end\n"

# Longitudinal analyse
print "Longitudinal analyse begin"
x = np.linspace(1,16,16)
y_average_clustering = np.zeros(16)
y_average_weight	 = np.zeros(16)
y_clustering_degree_correlation = np.zeros(16)
y_average_distance 	 = np.zeros(16)
y_weight_distribution = np.zeros(16)
y_kourei_frequence = np.zeros(16)
cnt = 0
titles = ['average_clustering','average_weight','clustering_degree_correlation','average_distance','weight_distribution','kourei_frequence']
Tools.mkdir(analysisPath+'../Longitudinal_analyse/')
for filepath in filepaths:
	print "\tprocess with ",filepath.split("/")[-2]
	lines = Tools.content_lines(filepath+'networkx/recordFile.txt')
	y_average_clustering[cnt] = float(lines[0].split(':')[1])
	y_average_weight[cnt] = float(lines[1].split(':')[1])
	y_clustering_degree_correlation[cnt] = float(lines[2].split(':')[1])
	y_average_distance[cnt] = float(lines[3].split(':')[1])
	y_weight_distribution[cnt] = float(lines[4].split(':')[1])
	y_kourei_frequence[cnt] = float(lines[5].split(':')[1])
	# print '\t',cnt,y_average_clustering[cnt],y_average_weight[cnt]
	cnt += 1
Tools.plot(x,y_average_clustering,titles[0],xlabel="years",ylabel=titles[0],filepath=analysisPath+'../Longitudinal_analyse/',for_long=1)
Tools.plot(x,y_average_weight,titles[1],xlabel="years",ylabel=titles[1],filepath=analysisPath+'../Longitudinal_analyse/',for_long=1)
Tools.plot(x,y_clustering_degree_correlation,titles[2],xlabel="years",ylabel=titles[2],filepath=analysisPath+'../Longitudinal_analyse/',for_long=1)
Tools.plot(x,y_average_distance,titles[3],xlabel="years",ylabel=titles[3],filepath=analysisPath+'../Longitudinal_analyse/',for_long=1)
Tools.plot(x,y_weight_distribution,titles[4],xlabel="years",ylabel=titles[4],filepath=analysisPath+'../Longitudinal_analyse/',for_long=1)
Tools.plot(x,y_kourei_frequence,titles[5],xlabel="years",ylabel=titles[5],filepath=analysisPath+'../Longitudinal_analyse/',for_long=1)
# get threshold
print "Longitudinal analyse end\n"
