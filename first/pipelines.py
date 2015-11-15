from scrapy.contrib.pipeline.images import ImagesPipeline
from scrapy.http import Request
#from PIL import Image
#import sys
import MySQLdb
#import hashlib
#from cStringIO import StringIO
import re

class FirstPipeline(ImagesPipeline):
    CONVERTED_ORIGINAL = re.compile('.jpg$')
    def get_media_requests(self, item, info):
        return [Request(x, meta={'image_names': item["url"]})
                for x in item.get('url', [])]

    # this is where the image is extracted from the HTTP response
    def get_images(self, response, request, info):
        for key, image, buf, in super(FirstPipeline, self).get_images(response, request, info):
            if self.CONVERTED_ORIGINAL.match(key):
                key = self.change_filename(key, response)
            yield key, image, buf

    def change_filename(self, key, response):
        return "fff/%s.jpg" % response.meta['image_names'][0]

class SQLStore(object):
    def __init__(self):
        self.conn = MySQLdb.connect(user='root', passwd='coolC00l', db='katerusaru_ktusa', host='localhost', charset="utf8", use_unicode=True)
        self.cursor = self.conn.cursor()

    def process_item(self, items, spider):
        if spider.name in ['images']:
            return items
        try:
            query_keys = ''
            query_value = ''
            for key in items:
                query_keys += MySQLdb.escape_string(key)+', '
                query_value += "\""+MySQLdb.escape_string(items[key])+"\", "
            q = """INSERT INTO modx_ms2_products(%s) VALUES (%s)""" % (query_keys[:-2], query_value[:-2])
            #print q
            self.cursor.execute(q)
            #$print query_keys
            #print query_value
            self.conn.commit()
        except MySQLdb.Error, e:
            print "Error %d: %s" % (e.args[0], e.args[1])
        return items