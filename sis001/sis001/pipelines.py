# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import os

import MySQLdb
import scrapy
from scrapy.exceptions import DropItem
from scrapy.pipelines.images import ImagesPipeline, ImageException
import time


class Sis001Pipeline(object):
    def process_item(self, item, spider):
        self.insert_sql(item)

    def insert_sql(self, item):
        db = MySQLdb.connect(host="localhost", user="root", passwd="root", db="test", use_unicode=True, charset="utf8")
        cursor = db.cursor()
        field = '(title,site,seedurl,likes,fileattr,type,size,translation,time,downtimes,page)'
        sqlstr = ''' INSERT INTO sis %s VALUES ("%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s")''' % (
            field, item['title'].encode('utf-8'), item['site'], item['seedurl'].encode('utf-8'),
            item['likes'].encode('utf-8'), item['fileattr'].encode('utf-8'), item['type'].encode('utf-8'),
            item['size'].encode('utf-8'), item['translation'], item['time'].encode('utf-8'),
            item['downtimes'].encode('utf-8'),item['page'].encode('utf-8'))
        try:
            cursor.execute(sqlstr)
            db.commit()
        except MySQLdb.Error, e:
            print "MySQL Error %d: %s" % (e.args[0], e.args[1])
            db.rollback()  # 回滚rollback()
        db.close()





    # def get_media_requests(self, item, info):
    #     self.insert_sql(item)
    #     # yield scrapy.Request('http://' + item['seedurl'])
    #     for p in item['image_urls']:
    #         yield scrapy.Request('http://' + p)

    # def item_completed(self, results, item, info):
    #     image_paths = [x['path'] for ok, x in results if ok]
    #     if not image_paths:
    #         raise DropItem("Item contains no images")
    #     item['image_paths'] = image_paths
    #     return item


