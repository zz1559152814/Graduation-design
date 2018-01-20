import chardet
import os
import re

def eachFile(filepath):
	global FilePath
	files	= os.listdir(filepath)
	FilePath = filepath
	for file in files:
		if re.search('txt$',file) is not None:
			printContent(filepath+"/"+file)

def printContent(filename):
	resource 	= open(filename,'r')
	resource_data = resource.read()
	aimFilename	= filename[:-3]+'txt2'
	aim		 	= open(aimFilename,'wb')
	aim.write("{\n")
	items		= re.split('>>>',resource_data)
	for n in range(len(items)-1):
		print 1111111
		elements = re.split('::',items[n])
		line7	= "\t\t\t\"content\":"+" \""+re.sub('\s*','',elements[5])+'\"\n'
		aim.write(line7)
	aim.write("}")
	resource.close()
	aim.close()
eachFile("/home/dream/documents/papers/code/datatest/afterselect")