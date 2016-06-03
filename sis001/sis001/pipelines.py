# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import MySQLdb


class Sis001Pipeline(object):
    def process_item(self, item, spider):
        db = MySQLdb.connect(host="localhost", user = "root", passwd = "root", db = "iproject",use_unicode=True, charset="utf8")
        cursor = db.cursor()
        field = '(title,site,seedurl,likes,fileattr,type,size)'
        sqlstr =''' INSERT INTO sis %s VALUES ("%s","%s","%s","%s","%s","%s","%s")''' % (
                field, item['title'], item['site'], item['seedurl'], item['likes'], item['fileattr'], item['type'],
                item['size'])
        try:
            cursor.execute(sqlstr)
            db.commit()
        except MySQLdb.Error, e:
            print "MySQL Error %d: %s" % (e.args[0], e.args[1])
            db.rollback()   #回滚rollback()
        db.close()
