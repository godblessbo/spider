# coding=utf-8

import scrapy

from sis001.items import Sis001Item

class MySpider(scrapy.Spider):
    name = 'sis001'
    allowed_domains = ['sis001.com']

    start_urls=['http://sis001.com/forum/forum-143-1.html']

    def parse(self, response):
        i = 0
        siteitems={}
        nextpage = response.xpath("//div[@class='pages_btns'][2]/div[@class='pages']/a[@class='next']/@href").extract()[0]
        print 'fuckckckckc'+response.url
        if response.url == self.start_urls[0]:
            pagexpath ="//table[@id='forum_143'][4]/tbody/tr/th[@class='new']/span/a/@href"
            title = "//table[@id='forum_143'][4]/tbody/tr/th[@class='new']/span/a/text()"
            sizeandattr = "//table[@id='forum_143'][4]/tbody/tr/td[@class='nums'][2]/text()"
        else:
            pagexpath ="//tbody/tr/th/span[1]/a/@href"
            title = "//tbody/tr/th/span[1]/a/text()"
            sizeandattr = "//table[@id='forum_143']/tbody/tr/td[@class='nums'][2]/text()"
        for p in response.xpath(pagexpath).extract():
            siteitems['title'] = response.xpath(title).extract()[i]
            if len(response.xpath(sizeandattr).extract())>=i:
                siteitems['size'] = response.xpath(sizeandattr).extract()[i].split('/')[0]
                siteitems['fileattr'] = response.xpath(sizeandattr).extract()[i].split('/')[1]
            else :
                siteitems['size'] = ''
                siteitems['fileattr'] =''
            i += 1
            yield scrapy.Request('http://sis001.com/forum/' + p, meta=siteitems, callback=self.parseItem)
        if nextpage:
            yield scrapy.Request('http://sis001.com/forum/' + nextpage, callback=self.parse)


    def parseItem(self, response):
        Sisitems = Sis001Item()
        tmpitem = response.meta
        Sisitems['fileattr'] = tmpitem['fileattr']
        Sisitems['size'] = tmpitem['size']
        Sisitems['title'] = tmpitem['title']
        Sisitems['type'] = response.xpath("//*[@id='wrapper']/div/form/div/h1/a/text()").extract()[0]
        self.logger.info('a response from %s has arrived', response.url)
        Sisitems['site'] = response.url
        Sisitems['seedurl'] = 'sis001.com/forum/'+ response.xpath("//div[@class='box postattachlist']/dl[@class='t_attachlist']/dt/a[2]/@href").extract()[0]
        Sisitems['likes'] = response.xpath("//span[@class='postratings']/a[@id='ajax_thanks']/span/text()").extract()[0]
        yield Sisitems
