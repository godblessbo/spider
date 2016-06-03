# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Sis001Item(scrapy.Item):
    title = scrapy.Field()  # 片名
    site = scrapy.Field()  # 网页
    seedurl = scrapy.Field()  # 种子链接
    likes = scrapy.Field()  # 赞
    fileattr = scrapy.Field()  # 格式
    type = scrapy.Field()  # 分类
    size = scrapy.Field()  # 大小
    filetime = scrapy.Field()  # 时长
