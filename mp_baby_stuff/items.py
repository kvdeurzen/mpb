# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field

class MPBabyStuffItem(Item):
  _id = Field()
  title = Field()
  url = Field()
  seller = Field()
  seller_url = Field()
  date_posted = Field()
  condition = Field()
  type = Field()
  description = Field()
  brand = Field()
  characteristics = Field()
  category = Field()
  asking_price = Field()
  town = Field()
  province = Field()
