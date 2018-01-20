#-*-encoding:utf-8-*-
import chardet
import os,sys
import re
import linecache
sys.path.append('../Mecab')
import mecab
import random

class Item:
	def __init__(self):
		self.time		= ''
		self.date		= ''
		self.house		= ''
		self.department	= ''
		self.speaker	= ''
		self.content 	= ''

class Record:
	def __init__(self):

		self.length = 0
		self.bool	= 0

def deleteOver(filepath):
	files	= os.listdir(filepath)
	for file in files:
		if re.search("over",file):
			newname = re.sub('over','',file)
			os.rename(filepath+"/"+file,filepath+"/"+newname)

def eachFile(filepath):
	global recordlist
	global useCount
	global uselessCount
	useCount		= 0
	uselessCount	= 0
	recordlist = []
	files	= os.listdir(filepath)
	filelists	= []

	recordfile1 = open("./mailListFile.txt",'r')
	recordfile = open("./mailListFile.txt",'a')
	recordfileContent = recordfile1.read()
	speakings  = recordfileContent.split('>')
	for speaking in speakings:
		try:
			a = speaking.split(':')[0][-1]
			if int(speaking.split(':')[0][-1]) == 0:
				uselessCount += 1
			elif int(speaking.split(':')[0][-1]) == 1:
				useCount += 1
		except:
			continue
	recordfile1.close()

	for file in files:
		filelists.append(file)

	fileTested = set()
	for n in range(len(filelists)):
		x = random.randint(0,len(filelists))
		while x in fileTested:
			x = random.randint(0,len(filelists))
		if re.search("over",file):
			x = random.randint(0,len(filelists))
		file = filelists[x]

		print "start to test next file: ",filelists[x],"\n"
		sign = chooseUse(filepath+"/"+file,recordlist,recordfile)
		os.rename(filepath+"/"+file,filepath+"/"+file[:-4]+"over"+file[-4:])
		filelists[x] = file[:-4]+"over"+file[-4:]

		if sign == 1:
			recordfile.close()
			fileTested.add(x)
			break
		fileTested.add(x)
	recordfile.close()
def chooseUse(filename,recordlist,recordfile):
	global useCount
	global uselessCount
	item = Item()
	record	= Record()
	fopen	= open(filename,'r')
	content = fopen.read()[:-9]
	paras 	= content.split("<b>○")
	fopen.close()

	for n in range(len(paras)-1):
		para_split	= paras[n+1].split("</b>")
		#para_split[0]:speaker
		#para_split[1]:speaking
		item.speaker	= para_split[0]
		item.content 	= re.sub('<br>','',para_split[1])
		exit = ''
		if len(item.content) <300:
			thisMecab	= mecab.MeCabClass(item.content)
			print item.content+"	  "+str(len(item.content))
			print "Useful:",str(useCount),"Useless:",str(uselessCount),"all is",str(useCount+uselessCount),'\n'
			input = raw_input("y/n/e:");
			while(input != "y" or input != "n"):
				if input == "y":
					record.length 	= len(item.content)
					record.bool  	= 1
					recordlist.append([record.length,record.bool])
					recordfile.write(str(record.bool))
					recordfile.write(":")
					recordfile.write(item.content)
					recordfile.write(">\n")
					useCount += 1
					break
				elif input == "n":
					record.length 	= len(item.content)
					record.bool   	= 0
					recordfile.write(str(record.bool))
					recordfile.write(":")
					recordfile.write(item.content)
					recordfile.write(">\n")
					uselessCount = uselessCount+1
					break
				elif input == 'e':
					print "you really want to exit it?:(y/n)"
					exit = raw_input("y/n:")
					if exit == "y":
						return 1
				else:
					print "Please input again:(y/n/e):"
					input = raw_input("y/n:")
			print "\n\n\n"

def inspect(filename,recordlist,recordfile):
	global num
	global record
	item = Item()
	record	= Record()
	fopen	= open(filename,'r')
	content = fopen.read()[:-9]
	paras 	= content.split("<b>○")
	fopen.close()

	for n in range(len(paras)-1):
		para_split	= paras[n+1].split("</b>")
		#para_split[0]:speaker
		#para_split[1]:speaking
		item.speaker	= para_split[0]
		item.content 	= re.sub('<br>','',para_split[1])
		exit = ''
		if len(item.content) <300:
			print item.content+"	  "+str(len(item.content))
			# print "This is the "+str(num)+" sentences,is't useful?"
			input = raw_input("y/n/e:");

eachFile("../datatest/orgin")
# deleteOver("../datatest/orgin")
