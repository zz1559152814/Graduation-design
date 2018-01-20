# -*- coding: utf-8 -*-
import os,sys,re
sys.path.append('/home/dreamer/documents/code/Tools')
import Tools

def content_paras(filename):
	fopen	   = open(filename, 'r')
	content	 = fopen.read()
	lines	   = content.split('\n\n')
	fopen.close()
	return lines

f = "/home/dreamer/documents/code/database/analysis/1982_1984/wordIncluded/地域社会.txt"
paras = content_paras(f)
key = f.split('/')[-1][:-4]
print key
for p in paras:
	content = p.split('::')[-1]
	iparas = content.split('\n')
	for ip in iparas:
		if re.search(key,ip) and re.search('高齢',ip):
			print ip
			print "the next "
