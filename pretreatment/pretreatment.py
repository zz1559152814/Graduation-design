#-*-encoding:utf-8-*-
import chardet
import os,sys
import re
import linecache

class Item:
	def __init__(self):
		self.time		= ''
		self.date		= ''
		self.house		= ''
		self.department	= ''
		self.speaker	= ''
		self.content 	= ''

global FilePath

def printItem(item):
	return item.time+'::'+item.department+'::'+str(item.date)+'::'+item.house+'::'+item.speaker+'::'+item.content+'>>>'+'\n'

def eachFile(filepath,toFilepath):
	global FilePath
	files	= os.listdir(filepath)
	FilePath = filepath
	runCounter = 0
	for file in files:
		runCounter += 1
		if runCounter%200 == 0:
			os.system('clear')
			print "This is the",runCounter,"th files"
		cutcontent(filepath,file,toFilepath)

def cutcontent(filepath,filename,toFilepath):
	finalfilename = filepath+filename
	if finalfilename == '../datatest/Final':
		return
	item   = Item()
	Maininfo 	= linecache.getlines(finalfilename)[:4]
	if len(Maininfo) == 0:
		if os.path.isdir(finalfilename) is False:
			os.remove(finalfilename)
		return
	elif len(linecache.getlines(finalfilename)[0]) > 6:
		os.remove(finalfilename)
		return
	item.time		= Maininfo[0][:-1]
	item.department	= Maininfo[1][:-1]
	item.house		= Maininfo[3][:-1]
	linecache.clearcache()
	strDateOb		= re.search('昭和.*日',finalfilename)
	if strDateOb is None:
		strDateOb	= re.search('平成.*日',finalfilename)

	strDate 		= strDateOb.group()
	# year			= re.sub('[\u4e00-\u9fa5]','-',strDate)
	listDate		= re.findall(r'[0-9]+',strDate)
	for n in range(len(listDate)):
		if len(listDate[n])==1:
			listDate[n] = '0'+listDate[n]

	if re.search('平成',finalfilename) is not None:
		listDate[0] 	= int(listDate[0])+1988
	elif re.search('昭和',finalfilename) is not None:
		listDate[0] 	= int(listDate[0])+1925

	item.date  			= int(str(listDate[0])+listDate[1]+listDate[2])
	fopen  	= open(finalfilename, 'r')
	content = fopen.read()[:-9]
	paras 	= content.split("<b>○")
	fopen.close()

	newFileName = toFilepath + filename[:-4]+'_Pretreated'+filename[-4:]
	newFile 	= open(newFileName,'wb')
	for n in range(len(paras)-1):
		para_split	= paras[n+1].split("</b>")
		#para_split[0]:speaker
		#para_split[1]:speaking
		item.speaker	= para_split[0]
		item.content 	= re.sub('<br>','',para_split[1])
		# if isSpamMail(item.content)
		newFile.write(printItem(item))
	newFile.close()
	select(newFileName,item.date)
	os.remove(newFileName)

def select(filename,date):
	global FilePath
	fileWithPre 	= open(filename,'r')
	content 		= fileWithPre.read()
	items			= re.split('>>>',content)
	keyword			= "高齢"
	# lastfile = open(FilePath+"/../afterselect/"+keyword+"_"+str(date)[:4]+'.txt','a')
	lastfile = open("/home/dreamer/documents/code/database/pretreatment/"+str(date)[:4]+'.txt','a')
	lastfile_without = open("/home/dreamer/documents/code/database/pretreatment/"+str(date)[:4]+'_without.txt','a')
	for item in items:
		if re.search(keyword,item) is not None:
			pass
			# lastfile.write(item)
			# lastfile.write(">>>\n")
		else:
			lastfile_without.write(item)
			lastfile_without.write(">>>\n")
	fileWithPre.close()
	lastfile.close()
	lastfile_without.close()

if __name__ == "__main__":
	# to final 2010.txt
	# toFilepath   = "/home/dreamer/documents/code/database/pretreatment/"
	# fromFilepath = "/home/dreamer/documents/code/database/conference/ryoin/"
	# eachFile(fromFilepath, toFilepath)
	# eachFile("../syugiinn11-29")
	# select("../datatest/text1.txt")
