import scrapy
import re
from scrapy.contrib.spiders import CrawlSpider
from httplib2 import Response, has_timeout
from conference.items import ConferenceItem
import json
import chardet
import os
class ConferenceSpider(CrawlSpider):
	name = 'conference'
	# from 63
	# start_urls = ['http://kokkai.ndl.go.jp/SENTAKU/syugiin/main.html']
	start_urls = ['http://kokkai.ndl.go.jp/SENTAKU/syugiin/mainb1.html']
				# ['http://kokkai.ndl.go.jp/SENTAKU/sangiin/mainb1.html']
				# "http://kokkai.ndl.go.jp/SENTAKU/ryoin/main.html"
				# ['http://kokkai.ndl.go.jp/SENTAKU/syugiin/mainb1.html']
				# 'http://kokkai.ndl.go.jp/SENTAKU/ryoin/mainb1.html']
	def __init__(self):
		self.root = "http://kokkai.ndl.go.jp/SENTAKU/syugiin/"
		self.time = []
		self.department = []
		self.speaker =[]

	def parse(self,response):#http://kokkai.ndl.go.jp/SENTAKU/syugiin/mainb.html
		sel = scrapy.Selector()
		house = response.xpath('//img[@height="20"]/@alt').extract()[0]
		url_lists 	= response.xpath('//a[@target="_top"]/@href').extract()
		times 		= response.xpath('//a[@target="_top"]/text()').extract()

		print house.encode('utf8')
		for n in range(len(url_lists)):
			url_list = self.root+url_lists[n][2:]
			url_list = url_list[:-5] +'b'+ url_list[-5:]
			# print url_list
			if int(times[n][:3]) >= 63:
					yield scrapy.FormRequest(url_list,meta={'time':times[n][:3],'house':house},callback = self.secondparse)

	def secondparse(self,response):#http://kokkai.ndl.go.jp/SENTAKU/syugiin/154/mainb.html
		urls 		= response.xpath('//a[@target="_top"]/@href').extract()
		department 	= response.xpath('//a[@target="_top"]/text()').extract()
		# print response.meta['house'].encode('utf8'),response.meta['time'].encode('utf8')
		for n in range(len(urls)):
			url = self.root + response.meta['time'] + urls[n][1:]
			url = url[:-5] +'b'+ url[-5:]
			yield scrapy.FormRequest(url,meta={'time':response.meta['time'],'department':department[n],'url':url,'house':response.meta['house']},callback = self.thirdparse)

	def thirdparse(self,response):#http://kokkai.ndl.go.jp/SENTAKU/syugiin/159/0071/mainb.html
		# print response.xpath()
		file_urls  = response.xpath('//a[@target="MAIN"]/@href').extract()
		file_names = response.xpath('//a[@target="MAIN"]/text()').extract()
		for n in range(len(file_urls)):
			if (n%2) == 0:
				file_url = response.meta['url'][:-10] + file_urls[n][2:]
				file_url = file_url[:-6] + 'b' + file_url[-5:]
				file_name = file_names[n].encode('utf8')+'_'+response.meta['house'].encode('utf8')
				file_name = file_name + '_' + response.meta['department'].encode('utf8')+'.txt'
				if os.path.exists(file_name):
					print file_name+' already eixsted'
				else:
					print file_name+" don't already eixsted"
					# print file_url
					yield scrapy.FormRequest(file_url,meta={'time':response.meta['time'],'department':response.meta['department'],'house':response.meta['house'],'file_name':file_name},callback = self.fourthparse)
				# continue

	def fourthparse(self,response):#http://kokkai.ndl.go.jp/SENTAKU/syugiin/179/0253/17911170253002b.html
		Years	= re.search(u'\u5e73\u6210\d{1,2}',response.xpath('//td/text()').extract()[0])
		if Years is None:
			Years	= re.search(u'\u662d\u548c\d{1,2}',response.xpath('//td/text()').extract()[0])
		Years	= Years.group()
		file_url = response.url[:-6] + 'c' + response.url[-5:]
		# print file_url
		yield scrapy.FormRequest(file_url,meta={'time':response.meta['time'],'department':response.meta['department'],'house':response.meta['house'],'year':Years,'file_name':response.meta['file_name']},callback = self.lastparse)

	def lastparse(self,response):#http://kokkai.ndl.go.jp/SENTAKU/syugiin/164/0158/16405240158003c.html
		conferenceItem = ConferenceItem()
		conferenceItem['Times'] 		= response.meta['time'].encode('utf8')
		conferenceItem['Department'] 	= response.meta['department'].encode('utf8')
		conferenceItem['Contents']		= response.xpath('//body').extract()
		conferenceItem['Years']			= response.meta['year'].encode('utf8')
		conferenceItem['Houses']		= response.meta['house'].encode('utf8')
		# print conferenceItem['Years'],conferenceItem['Times'],conferenceItem['Department'],conferenceItem['Houses']
		# print conferenceItem['Houses']
		file = open('/home/dreamer/documents/code/database/conference/syugiin_1970_1999/'+response.meta['file_name'],'wb')
		for content in conferenceItem['Contents']:
			file.write(conferenceItem['Times']+'\n')
			file.write(conferenceItem['Department']+'\n')
			file.write(conferenceItem['Years']+'\n')
			file.write(conferenceItem['Houses']+'\n')
			file.write(content.encode('utf8'))
		return conferenceItem
