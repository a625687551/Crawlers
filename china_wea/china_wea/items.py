# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class WeaItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    city = scrapy.Field()
    date = scrapy.Field()
    clim = scrapy.Field()
    temph = scrapy.Field()
    templ = scrapy.Field()
    AQI = scrapy.Field()
    LNG = scrapy.Field()
    LAT = scrapy.Field()

