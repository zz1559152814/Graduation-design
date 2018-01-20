#-*-encoding:utf-8-*-
import os,sys,re
sys.path.append('../Tools')
import Tools,time

def speakSplit(filepath,tofilePath):
	global FilePath
	files	= os.listdir(filepath)
	FilePath = filepath
	runCounter = 0
	for file in files:
		fileSpeaks = Tools.content_paras(filepath+file)
		# print filepath+file,len(fileSpeaks)
		for speak in fileSpeaks:
			runCounter += 1
			speaking = speak.split('::')[-1]
			newfile = open(tofilePath+str(runCounter)+".txt","wb")
			newfile.write(speaking)
			newfile.close()

# speakSplit("/home/dreamer/documents/code/database/0afterselect/1/")
if __name__ == "__main__":
	pass
