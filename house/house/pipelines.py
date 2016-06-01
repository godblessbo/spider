# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from twisted.enterprise import adbapi
from scrapy.utils.project import get_project_settings


class HousePipeline(object):
    # The table you items.FundItem class map to, my table is named fund
    def __init__(self):
        settings = get_project_settings()
        dbargs = settings.get('DB_CONNECT')
        db_server = settings.get('DB_SERVER')
        dbpool = adbapi.ConnectionPool(db_server, **dbargs)
        self.dbpool = dbpool


#
# db = MySQLdb.connect("localhost","testuser","test123","TESTDB" )
#
# # prepare a cursor object using cursor() method
# cursor = db.cursor()
#
# # Drop table if it already exist using execute() method.
# cursor.execute("DROP TABLE IF EXISTS EMPLOYEE")
#
# # Create table as per requirement
# sql = """CREATE TABLE EMPLOYEE (
#          FIRST_NAME  CHAR(20) NOT NULL,
#          LAST_NAME  CHAR(20),
#          AGE INT,
#          SEX CHAR(1),
#          INCOME FLOAT )"""
#
# cursor.execute(sql)
#
# # disconnect from server
# db.close()








    def __del__(self):
        self.dbpool.close()

    def process_item(self, item, spider):
        d = self.dbpool.runInteraction(self.insert_data, item, spider)
        return d

    def insert_data(self, conn, item, spider):
            field = "(website,title,money,village,location,size,room,setting ,nowtime,owner)"
            sql = ''' INSERT INTO houseitem %s VALUES ("%s","%s","%s","%s","%s","%s","%s","%s","%s","%s")''' % (
                field, item['website'], item['title'], item['money'], item['village'], item['location'], item['size'],
                item['room'], item['setting'], item['nowtime'], item['owner'])
            conn.execute(sql)
