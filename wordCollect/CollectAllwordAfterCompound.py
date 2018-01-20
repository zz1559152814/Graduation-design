# -*- coding: utf-8 -*-
import re,os,sys

# 将词频大于三且满足复合条件的词组全部写入到一个新的文件里面
def collect():
	# file1	   = open("/home/dreamer/documents/code/database/afterAllwordSta/OneWordsMecabList.txt",'r')
	file3	   = open("/home/dreamer/documents/code/database/afterAllwordSta/ThreeWordsMecabList.txt",'r')
	# newFilefor1	 = open("/home/dreamer/documents/code/database/afterCompoundScore/AllAfterCompound1.txt",'wb')
	newFilefor3	 = open("/home/dreamer/documents/code/database/afterCompoundScore/AllAfterCompound3.txt",'wb')
	dictornary  = open("/home/dreamer/documents/code/database/afterAllwordSta/allwordByMecab.txt",'r')

	# content1	= file1.read()
	content3	= file3.read()
	dictornaryContent = dictornary.read()
	# file1.close()
	file3.close()
	dictornary.close()
	# line1s	  = content1.split('\n')
	line3s	  = content3.split('\n')
	dictornaryLines = dictornaryContent.split('\n')


	for line in line3s:
		# try:
		try:
			if int(line.split(':')[-1].split(' ')[-1]) > 6:
				a	   = line.split(':')
				b	   = a[1].split(' ')
				for dictornaryLine in dictornaryLines:
					try:
						singleword = dictornaryLine.split('\t')[0]
						singlewordCnt =  dictornaryLine.split('\t')[1]
						# singlewordCnt = dictornaryLine.split('\t')[1]
					except:
						# print dictornaryLine.split('\t')
						continue
					if b[0] == singleword:
						b0Cnt = singlewordCnt
					elif b[1] == singleword:
						b1Cnt = singlewordCnt
					elif b[2] == singleword:
						b2Cnt = singlewordCnt
				prints  = a[0]+'\t:'+b[0]+' '+b0Cnt+'\t:'+b[1]+' '+b1Cnt+'\t:'+b[2]+' '+b2Cnt+'\t:'+b[-1]+'\t:'+str(-9999)
				newFilefor3.write(prints+'\n')
		except:
			print line
	newFilefor3.close()

	# for line in line1s:
	#	 try:
	#		 if int(line.split(':')[-1].split(' ')[-1]) > 3:
	#			 a	   = line.split(':')
	#			 prints  = a[0] + '\t:' + a[-1].split(' ')[0] + '\t:' + a[-1].split(' ')[1] + '\t:' + str(-9999)+'\n'
	#			 newFilefor1.write(prints)
	#	 except:
	#		 print line
	# newFilefor1.close()
collect()
