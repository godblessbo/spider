# -*- coding: utf-8 -*-

import time
import scrapy
from house.items import HouseItem


class MySpider(scrapy.Spider):
    name = 'house'
    allowed_domains = ['cd.ganji.com']
    start_urls = ['http://cd.ganji.com/fang1/gaoxinxiqu/']

    def parse(self, response):
        for i in response.xpath(
                "//ul[@class='list-style1']//div[@class='info-title']/a[@class='list-info-title js-title']/@href").extract():
            siteurl = 'http://' + self.allowed_domains[0] + str(i)
            yield scrapy.Request(siteurl, callback=self.parseItem)


    def parseItem(self, response):
        houseitems = HouseItem()
        self.logger.info('A response from %s just arrived!', response.url)
        title = response.xpath(
            "//div[@class='leftBox']/div[@class='col-cont title-box']/h1[@class='title-name']/text()").extract()
        money = response.xpath("//li[@class='clearfix']/b[@class='basic-info-price fl']/text()").extract()
        village = response.xpath(
            "//li[@class='spc-item clearfix']/div[@class='spc-cont']/a/@title").extract()
        location = response.xpath(
            "//ul[@class='basic-info-ul']/li/span[@class='addr-area']/text()").extract()
        setting = response.xpath("//ul[@class='basic-info-ul']/li[@class='peizhi']/p/text()").extract()
        owner = response.xpath(
            "//div[@class='contact-person tel-number clearfix']/span[@class='contact-col']/i[2]/text()").extract()
        nowtime = time.strftime("%Y/%m/%d-%H:%M:%S", time.localtime())
        size = response.xpath(
            "//ul[@class='basic-info-ul']/li[2]/text()").extract()[0].split('-')[2]
        room = response.xpath(
            "//ul[@class='basic-info-ul']/li[2]/text()").extract()[0].split('-')[0].replace(' ', '')
        houseitems['website'] = response.url
        houseitems['title'] = title[0]
        houseitems['money'] = money[0]
        houseitems['village'] = village[0]
        houseitems['location'] = location[0]
        houseitems['size'] = size
        houseitems['room'] = room
        houseitems['setting'] = setting[0]
        houseitems['nowtime'] = nowtime
        houseitems['owner'] = owner[0]
        print owner[0]
        yield houseitems
