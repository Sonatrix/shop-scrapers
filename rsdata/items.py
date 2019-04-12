# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html
from scrapy.item import Item, Field
import re
import scrapy


class Item(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    name = scrapy.Field()
    city = scrapy.Field()
    area = scrapy.Field()
    phone = scrapy.Field()
    url = scrapy.Field()
    address = scrapy.Field()
    sender = scrapy.Field()
    type = scrapy.Field()
