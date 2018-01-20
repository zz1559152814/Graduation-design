# -*- coding: utf-8 -*-
import scrapy 
import re
import chardet
import sys,os
from scrapy.contrib.spiders import CrawlSpider
from httplib2 import Response, has_timeout
from literature.items import LiteratureItem
reload(sys)   
sys.setdefaultencoding('utf8')

class LiteratureSpider(CrawlSpider):

	name		= "literature"
	start_urls	= ["http://www.aozora.gr.jp"]

	def __init__(self):
		self.root		= 'http://www.aozora.gr.jp/'

	def parse(self,response): #http://www.aozora.gr.jp/
		subsites_all	= response.xpath('//td[@bgcolor="#f0f8ff"]//a/@href').extract()
		for subsite in subsites_all:
			if re.search('sakuhin',subsite):
				url_f 	= self.root + subsite
				for n in range(5):
					url = url_f[:-6] + str(n+1) + url_f[-5:]
					yield scrapy.FormRequest(url,callback = self.secondparse)

	def secondparse(self,response): #http://www.aozora.gr.jp/index_pages/sakuhin_a1.html
		urls 	= response.xpath('//td[@align="left"]//a/@href').extract()
		for url in urls:
			url = self.root + url[3:]
			yield scrapy.FormRequest(url,callback = self.thirdparse)

	def thirdparse(self,response): #http://www.aozora.gr.jp/cards/000020/card2569.html
		paras	= re.split('/',response.url)
		root	= paras[0]+'//'+paras[2]+'/'+paras[3]+'/'+paras[4]+'/'
		# print root
		urls 	= response.xpath('//a[contains(text(),"html")]/@href').extract()
		if len(urls) > 0:
			url = urls[0]
			url 	= root + url[2:]
			yield scrapy.FormRequest(url,callback = self.lastparse)		

	def lastparse(self,response): #http://www.aozora.gr.jp/cards/000908/files/52154_41460.html
		item 			= LiteratureItem()
		item['name'] 	= response.xpath('//h1/text()').extract()[0]
		item['author']	= response.xpath('//h2/text()').extract()[0]
		contents 		= response.xpath('//div[@class="main_text"]/text() | //div[@class="main_text"]/ruby/rb/text()').extract()
		filename		= "/home/dream/documents/papers/code/database/literature/"+item['name']+"_"+item['author']
		fopen			= open(filename+".txt",'wb')
		for content in contents:
			fopen.write(content)
		fopen.close()








