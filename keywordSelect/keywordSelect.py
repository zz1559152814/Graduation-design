# -*- coding: utf-8 -*-
import os
import re

def select(keyword):
	fopen	   = open('./平成11年1月19日 _参議院_本会議_Pretreated.txt','r')
	content	 = fopen.read()
	paras	   = content.split('>>>')
	newFile	 = open('./d.txt','wb')
	for para in paras:
		speaking = para.split('::')[-1]
		if re.search(keyword,speaking) is not None:
			newFile.write(para+'\n')

select('高齢')
