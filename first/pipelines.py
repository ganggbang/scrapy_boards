# from types import *
#from scrapy.exporter import CsvItemExporter
#from scrapy.contrib.exporter import CsvItemExporter
import re

from scrapy.conf import settings
from scrapy.contrib.exporter import CsvItemExporter
from scrapy.contrib.pipeline.images import ImagesPipeline
from scrapy.http import Request

class FirstPipeline(ImagesPipeline):
    CONVERTED_ORIGINAL = re.compile('.jpg$')
    def get_media_requests(self, item, info):
        item.setdefault('pagetitle', item['boatyear']+' '+item['boatbrand']+' '+item['boatmodel'])
        item.setdefault('parent', '1653')
        item.setdefault('template', '5')

        return [Request(''.join(v), meta={'item': item})
            for x,v in item.items() if x.startswith('url')]

    def get_images(self, response, request, info):

        for key, image, buf, in super(FirstPipeline, self).get_images(response, request, info):
            #if self.CONVERTED_ORIGINAL.match(key):
            
            for (x, item) in response.meta['item'].items():
                if x.startswith('url'):    
                    if request.url == response.meta['item'][x]:
                        m = re.search('(\/[0-9,A-Za-z\-\_\~]+\/[0-9,A-Za-z\-\_\~]+|[0-9,A-Za-z\-\_\~]+).jpg$',response.meta['item'][x], flags=re.IGNORECASE)
                        if m:
                            key = "%s/%s" % (response.meta['item']['name'], m.group(0))
                            key = re.sub('//','/',key)
                            break
            yield key, image, buf

class ProductCSVExporter(CsvItemExporter):

     def __init__(self, *args, **kwargs):
        kwargs['fields_to_export'] = settings.getlist('EXPORT_FIELDS') or None
        kwargs['encoding'] = settings.get('EXPORT_ENCODING', 'utf-8')
        delimiter = settings.get('CSV_DELIMITER', '|')
        kwargs['delimiter'] = delimiter
        kwargs['include_headers_line'] = False
        super(ProductCSVExporter, self).__init__(*args, **kwargs)
