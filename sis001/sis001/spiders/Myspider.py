# coding=utf-8
import scrapy
from sis001.items import Sis001Item


class MySpider(scrapy.Spider):
    name = 'sis001'
    allowed_domains = ['sis001.com']
    start_urls = ['http://sis001.com/forum/forumdisplay.php?fid=143']
    items = Sis001Item

    def parse(self, response):
        i = 0
        for p in response.xpath("//table[@id='forum_143'][4]/tbody/tr/th[@class='new']/span/a/@href").extract():
            self.items['site'] = 'sis001.com/forum/' + p
            self.items['name'] = response.xpath("//table[@id='forum_143'][4]/tbody/tr/th[@class='new']/span/a/text()").extract()[i]
            self.items['size'] = response.xpath("//form/table[@id='forum_143'][4]/tbody/tr/td[@class='nums'][2]/text()").extract()[i].spilt('/')[0]
            self.items['fileattr'] = response.xpath("//form/table[@id='forum_143'][4]/tbody/tr/td[@class='nums'][2]/text()").extract()[i].spilt('/')[1]
            self.items['type'] = response.xpath("//form/table[@id='forum_143'][4]/tbody/tr/th[@class='new']/em/a/text()").extract()[i]
            i += 1
            yield scrapy.Request(self.items['site'], callback=self.parseItem)

    def parseItem(self, response):
        self.logger.info('a response from %s has arrived', response.url)
        self.items['seedurl'] = response.xpath("//div[@class='box postattachlist']/dl[@class='t_attachlist']/dt/a[2]/@href").extract()
        self.items['likes'] = response.xpath("//span[@class='postratings']/a[@id='ajax_thanks']/text()").extract()
        tmp = response.xpath( "//td[@class='postcontent']/div[@class='postmessage defaultpost']/div/font/text()").extract().replace('】','')
        self.items['filetime'] = tmp.split('【')[3]
        yield self.items
