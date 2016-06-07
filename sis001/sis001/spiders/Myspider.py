# coding=utf-8
# from lxml import etree
import re
import urllib
import urllib2

import scrapy

from sis001.items import Sis001Item

class MySpider(scrapy.Spider):
    name = 'sis001'
    allowed_domains = ['sis001.com']
    start_urls = ['http://sis001.com/forum/forum-143-1.html']

    def parse(self, response):
        i = 0
        siteitems = {}
        nextpage = response.xpath("//div[@class='pages_btns'][2]/div[@class='pages']/a[@class='next']/@href").extract()[0]
        if response.url == self.start_urls[0]:
            pagexpath = "//table[@id='forum_143'][4]/tbody/tr/th[@class='new']/span/a/@href"
            title = "//table[@id='forum_143'][4]/tbody/tr/th[@class='new']/span/a/text()"
            sizeandattr = "//table[@id='forum_143'][4]/tbody/tr/td[@class='nums'][2]/text()"
        else:
            pagexpath = "//tbody/tr/th/span[1]/a/@href"
            title = "//tbody/tr/th/span[1]/a/text()"
            sizeandattr = "//table[@id='forum_143']/tbody/tr/td[@class='nums'][2]/text()"
        for p in response.xpath(pagexpath).extract():
            siteitems['title'] = response.xpath(title).extract()[i]
            if len(response.xpath(sizeandattr).extract()) >= i:
                siteitems['size'] = response.xpath(sizeandattr).extract()[i].split('/')[0]
                siteitems['fileattr'] = response.xpath(sizeandattr).extract()[i].split('/')[1]
            else:
                siteitems['size'] = ''
                siteitems['fileattr'] = ''
            i += 1
            siteitems['page'] = nextpage
            yield scrapy.Request('http://sis001.com/forum/' + p, meta=siteitems, callback=self.parseItem)
        if nextpage:
            yield scrapy.Request('http://sis001.com/forum/' + nextpage, callback=self.parse)

    def parseItem(self, response):
        Sisitems = Sis001Item()
        tmpitem = response.meta
        Sisitems['fileattr'] = tmpitem['fileattr']
        Sisitems['size'] = tmpitem['size']
        Sisitems['title'] = tmpitem['title']
        Sisitems['page'] = tmpitem['page']
        Sisitems['translation'] = self.Gtranslate(tmpitem['title'])
        Sisitems['type'] = response.xpath("//*[@id='wrapper']/div/form/div/h1/a/text()").extract()[0]
        Sisitems['time'] = response.xpath("//div[@class='box postattachlist']/dl[@class='t_attachlist']/dd/p/text()").extract()[0].split(',')[0]
        Sisitems['downtimes'] = response.xpath("//div[@class='box postattachlist']/dl[@class='t_attachlist']/dd/p/text()").extract()[0].split(',')[1].split(':')[1]
        self.logger.info('a response from %s has arrived', response.url)
        Sisitems['site'] = response.url
        #Sisitems['image_urls'] = response.xpath("//td[@class='postcontent']/div[@class='postmessage defaultpost']/div/img/@src").extract()
        Sisitems['seedurl'] = 'sis001.com/forum/' + response.xpath(
            "//div[@class='box postattachlist']/dl[@class='t_attachlist']/dt/a[2]/@href").extract()[0]
        Sisitems['likes'] = response.xpath("//span[@class='postratings']/a[@id='ajax_thanks']/span/text()").extract()[0]
        yield Sisitems

    def Gtranslate(self, text):
        Gtext = text
        # hl:浏览器、操作系统语言，默认是zh-CN
        # ie:默认是UTF-8
        # text：就是要翻译的字符串
        # langpair:语言对，即'en'|'zh-CN'表示从英语到简体中文
        values = {}
        values['hl'] = 'zh-CN'
        values['ie'] = 'UTF-8'
        values['text'] = Gtext
        values['langpair'] = "'ja'|'zh-CN'"
        # URL用来存储谷歌翻译的网址
        url = 'http://translate.google.cn/'
        # 将values中的数据通过urllib.urlencode转义为URL专用的格式然后赋给data存储
        newvalue = {}
        for k, v in values.iteritems():
            newvalue[k] = unicode(v).encode('utf-8')
        data = urllib.urlencode(newvalue)
        # 然后用URL和data生成一个request
        req = urllib2.Request(url, data)
        # 伪装一个IE6.0浏览器访问，如果不伪装，谷歌将返回一个403错误
        browser = 'Mozilla/4.0 (Windows; U;MSIE 6.0; Windows NT 6.1; SV1; .NET CLR 2.0.50727)'
        req.add_header('User-Agent', browser)
        # 向谷歌翻译发送请求
        response = urllib2.urlopen(req)
        # 读取返回页面，然后我们就从这个HTML页面中截取翻译过来的字符串即可
        html = response.read()
        # tree = etree.HTML(html)
        # pi = tree.xpath('//*[@id="gt-c"]/script[3]/text()')
        # pi = pi.encode('utf-8')
        # 使用正则表达式匹配<=TRANSLATED_TEXT=)。而翻译后的文本是'TRANSLATED_TEXT='等号后面的内容
        p = re.compile(r"(?<=TRANSLATED_TEXT=).*?;")
        m = p.search(html)
        chineseText = m.group(0).strip(';')
        chineseText = chineseText.replace('\'', '')
        return chineseText
