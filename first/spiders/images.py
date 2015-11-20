# -*- coding:utf8 -*-

import re

from first.items import Website
#from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.loader import XPathItemLoader
#from scrapy.contrib.loader.processor import Compose
from scrapy.contrib.loader.processor import MapCompose
#from scrapy.contrib.loader.processor import TakeFirst
from scrapy.contrib.loader.processor import Join
from scrapy.selector import Selector
from scrapy.contrib.spiders import CrawlSpider, Rule
#from scrapy.selector import HtmlXPathSelector

class TestLoader(XPathItemLoader):
    default_input_processor = MapCompose(lambda s: re.sub('(<.*?>|\t|[^a-zA-Z0-9_\/., :-\|]| {2,})', '', s.strip()))
    default_output_processor = Join('\t')

# "http://www.ebay.com/sch/Boats-/26429/i.html?rt=nc&LH_BIN=1&_trksid=p2045573.m1684",
# "http://www.copart.com/us/search?companyCode_vf=US&Sort=sd&LotTypes=M&YearFrom=2000&YearTo=2016&Make=&RadioGroup=Location&YardNumber=&States=&PostalCode=&Distance=500&searchTitle=2000-2016%2C%2C&cn=2000-2016%2C%2C",
#"https://www.manheimglobaltrader.com/bu/search?se_search_unit_code[]=BO&flag_search_submit=y",

class TestSpider(CrawlSpider):
    name = 'images'

    allowed_domains = ["ebay.com", "copart.com", "www.manheimglobaltrader.com", "www.boattrader.com"]
    start_urls = [#"https://www.manheimglobaltrader.com/bu/search?se_search_unit_code[]=BO&flag_search_submit=y",
                #"http://www.copart.com/us/search?companyCode_vf=US&Sort=sd&LotTypes=M&YearFrom=2000&YearTo=2016&Make=&RadioGroup=Location&YardNumber=&States=&PostalCode=&Distance=500&searchTitle=2000-2016%2C%2C&cn=2000-2016%2C%2C",
                "http://www.ebay.com/sch/Boats-/26429/i.html?rt=nc&LH_BIN=1&_trksid=p2045573.m1684"]
    rules = (
        Rule(SgmlLinkExtractor(restrict_xpaths = ('//h3/a')), callback = 'parse_item_ebay_images'),
        #Rule(SgmlLinkExtractor(restrict_xpaths = ('//li[@class=\'lot-desc\']/a')), callback = 'parse_item_copart_images'),
        #Rule(SgmlLinkExtractor(restrict_xpaths = ('//td/table[@class=\'search_name_cell\']/tr/td/a')), callback = 'parse_item_manheimglobaltrader_images'),
    )

    def parse_item_manheimglobaltrader_images(self, response):
        sel = Selector(response)
        imgs = sel.xpath('//li/a[@class=\'thumb\']')
        items = []
        for img in imgs:
            item = Website()
            item['url'] = img.xpath('@href').extract()
            tmp = ''.join(item['url'])
            m = re.search('\w+\.com',tmp)
            item['name'] = m.group(0)
            items.append(item)
        return items

    def parse_item_copart_images(self, response):
        sel = Selector(response)
        #<li data-jcarouselcontrol="true">
        imgs = sel.xpath('//div[@class=\'navigation\']/div/ul/li/img')
        items = []
        for img in imgs:
            #print img
            item = Website()
            item['url'] = img.xpath('@src').extract()
            tmp = ''.join(item['url'])
            if len(tmp) == 0:
                continue

            item['url'] = ['http:' + x for x in item['url']]
            m = re.search('\w+\.com',tmp)
            item['name'] = m.group(0)
            #print item['name']
            items.append(item)
        return items

    def parse_item_ebay_images(self, response):
        sel = Selector(response)
        imgs = sel.xpath('//tr/td[@class=\'tdThumb\']/div/img')
        items = []
        for img in imgs:
            item = Website()
            item['url'] = img.xpath('@src').extract()

            tmp = ''.join(item['url'])
            m = re.search('\w+\.com',tmp)
            item['name'] = m.group(0)

            items.append(item)
        return items
