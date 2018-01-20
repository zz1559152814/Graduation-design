# -*- coding: utf-8 -*-
import os,sys
sys.path.append('../Mecab')
sys.path.append('../Tools')
sys.path.append('../pretreatment')
sys.path.append('../nounExtract')
sys.path.append('../compoundAnalysis')
import pretreatment,mecab,Tools,nounExtract
import likelihood
import speech
# fromFilepath = "/home/dreamer/documents/code/database/conference/ryoin11-29/"
# fromFilepath = "/home/dreamer/documents/code/database/conference/sanngiinn11-29/"
fromFilepath = "/home/dreamer/documents/code/database/conference/syugiinn11-29.zip/"
toFilepath   = "./pretreatment/"

# pretreatment.eachFile(fromFilepath, toFilepath)
# fromFilepath = "/home/dreamer/documents/code/database/conference/sanngiinn11-29/"
# toFilepath   = "./includeKeyword/"
# nounExtractFilePath = './nounExtractFile/'
# nounExtract.eachFile(toFilepath,nounExtractFilePath)

toFilepath = './nounExtractFile/'
allWord = './allWord/allWord.txt'
# likelihood.generateAllWords(toFilepath,allWord)
# likelihood.generateMecabList('./allWord/','allWord.txt','./allWord/')
newfile		 = './speechAndWords3.txt'
speech.speech("./allWord/TwoAndThree.txt",newfile)
