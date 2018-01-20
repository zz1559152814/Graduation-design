#-*-encoding:utf-8-*-
import chardet
import os,sys
import re
import linecache
sys.path.append('../Mecab')
import mecab
import random

def chooseUse(fromfile,tofile):
	fromFile	= open(fromfile,'r')
	toFile	  = open(tofile,'r+')

	toFileContent   = toFile.read()
	toFileLines	 = toFileContent.split('\n')
	toFileLineCount = len(toFileLines) - 1
	print toFileLineCount
	fromContent	 = fromFile.read()
	fromLines   = fromContent.split('\n')
	fromFileLineCount = 0
	for line in fromLines:
		if fromFileLineCount < toFileLineCount:
			fromFileLineCount += 1
			continue
		fromFileLineCount += 1
		print line
		# print "这个词汇是否可以作为一个节点？"
		input = raw_input("y/n/e:");
		while(input != "y" or input != "n"):
			if input == "y":
				toFile.write(line+'\t'+'1'+'\n')
				break
			elif input == "n":
				toFile.write(line+'\t'+'0'+'\n')
				break
			elif input == 'e':
				print "你确定要退出吗?:(y/n)"
				exit = raw_input("y/n:")
				if exit == "y":
					return 0
				break
			else:
				print "Please input again:(y/n/e):"
				input = raw_input("y/n:")
				break
		print "\n\n\n"
	print "恭喜你完成了这一艰巨而又伟大的任务！！！！！"

chooseUse("./useRecord.txt","./1.txt")
