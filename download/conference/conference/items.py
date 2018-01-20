# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ConferenceItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    Years		=	scrapy.Field()
    Department	=	scrapy.Field()
    Speaker		=	scrapy.Field()
    Contents	=	scrapy.Field()
    Times		= 	scrapy.Field()
    Houses		= 	scrapy.Field()
    pass
