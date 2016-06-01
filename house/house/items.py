# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class HouseItem(scrapy.Item):
    website = scrapy.Field()  # 信息来源网站
    title = scrapy.Field()  # 标题
    money = scrapy.Field()  # 房租
    location = scrapy.Field()  # 位置
    size = scrapy.Field()  # 平方数
    village = scrapy.Field()  # 小区
    room = scrapy.Field()  # 户型
    nowtime = scrapy.Field()  # 发布时间
    owner = scrapy.Field()  # 房东
    setting = scrapy.Field()  # 配置
    pass

