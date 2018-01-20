import re
import chardet
import os

def eachFile(filepath):
	global FilePath
	files	= os.listdir(filepath)
	FilePath = filepath
	for file in files:
		if re.search('txt$',file) is not None:
			tojson(filepath+"/"+file)

def tojson(filename):
	resource 	= open(filename,'r')
	resource_data = resource.read()
	aimFilename	= filename[:-3]+'json'
	aim		 	= open(aimFilename,'wb')
	aim.write("{\n")
	items		= re.split('>>>',resource_data)
	for n in range(len(items)-1):
		elements = re.split('::',items[n])
		# print elements
		if items[n] != "" and items[n] != "\n\n" :
			line1 	= "\t\"item" + str(n+1) + "\":{\n"
			line2 	= "\t\t\t\"time\":"+" \""+re.search("\d{1,}",elements[0]).group()+'\",\n'
			line3	= "\t\t\t\"department\":"+" \""+elements[1]+'\",\n'
			line4	= "\t\t\t\"year\":"+" \""+elements[2]+'\",\n'
			line5	= "\t\t\t\"house\":"+" \""+elements[3]+'\",\n'
			line6	= "\t\t\t\"speaker\":"+" \""+elements[4]+'\",\n'
			line7	= "\t\t\t\"content\":"+" \""+re.sub('\s*','',elements[5])+'\"\n'
			if n != len(items)-1:
				line8	= "\t\t},\n\n"
			else:
				line8	= "\t\t}\n\n"
			aim.write(line1)
			aim.write(line2)
			aim.write(line3)
			aim.write(line4)
			aim.write(line5)
			aim.write(line6)
			aim.write(line7)
			aim.write(line8)
	aim.write("}")
	resource.close()
	aim.close()

# eachFile("/home/dream/codes/scrapy/conference/syugiinn11-29/Final")
# c/home/dream/codes/scrapy/conference/syugiinn11-29/Final")
eachFile("/home/dream/documents/papers/code/datatest/afterselect")	