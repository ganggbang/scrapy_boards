from scrapy.contrib.pipeline.images import ImagesPipeline
from scrapy.http import Request
from PIL import Image
from cStringIO import StringIO
import re

class FirstPipeline(ImagesPipeline):
    CONVERTED_ORIGINAL = re.compile('.jpg$')
 
    def get_media_requests(self, item, info):
        return [Request(x, meta={'image_names': item["url"]})
                for x in item.get('url', [])]

    # this is where the image is extracted from the HTTP response
    def get_images(self, response, request, info):
        #print response

        for key, image, buf, in super(FirstPipeline, self).get_images(response, request, info):
            if self.CONVERTED_ORIGINAL.match(key):
                key = self.change_filename(key, response)
            yield key, image, buf

    def change_filename(self, key, response):

        return "fff/%s.jpg" % response.meta['image_names'][0]