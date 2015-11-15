# -*- coding:utf8 -*-

import re

#from first.items import FirstItem
from first.items import Website
from first.items import Board

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
    name = 'test'
    allowed_domains = ["ebay.com", "copart.com", "www.manheimglobaltrader.com"]
    start_urls = ["https://www.manheimglobaltrader.com/bu/search?se_search_unit_code[]=BO&flag_search_submit=y",
                "http://www.copart.com/us/search?companyCode_vf=US&Sort=sd&LotTypes=M&YearFrom=2000&YearTo=2016&Make=&RadioGroup=Location&YardNumber=&States=&PostalCode=&Distance=500&searchTitle=2000-2016%2C%2C&cn=2000-2016%2C%2C",
                "http://www.ebay.com/sch/Boats-/26429/i.html?rt=nc&LH_BIN=1&_trksid=p2045573.m1684"]
    rules = (
        Rule(SgmlLinkExtractor(restrict_xpaths = ('//h3/a')), callback = 'parse_item_ebay'),
        Rule(SgmlLinkExtractor(restrict_xpaths = ('//li[@class=\'lot-desc\']/a')), callback = 'parse_item_copart'),
        Rule(SgmlLinkExtractor(restrict_xpaths = ('//td/table[@class=\'search_name_cell\']/tr/td/a')), callback = 'parse_item_manheimglobaltrader'),
    )


    def list_xpath_to_str(self, charact, xpath):
        txt = charact.xpath(xpath).extract()
        tt = ''.join(txt)
        txt = re.sub('<.*?>','',tt)
        return txt

    def get_char_field_copart(self, charact, text):
        if len(charact.xpath('label')) > 0:
            #print text
            block_find = charact.xpath('label')[0].re(r'(?i)' + text)
            if len(block_find) > 0:
                txt = self.list_xpath_to_str(charact,'text()')
                return txt
        return ''

    def get_char_field_ebay(self, charact, text):
        if len(charact.xpath('td')) > 0:
            block_find = charact.xpath('td')[0].re(r'(?i)' + text)
            if len(block_find) > 0:
                txt = self.list_xpath_to_str(charact,'td[2]/span')
                return txt
        return ''

    def get_char_field_manheimglobaltrader(self, charact, text):
        if len(charact.xpath('td')) > 0:
            block_find = charact.xpath('td')[0].re(r'(?i)' + text)
            if len(block_find) > 0:
                txt = self.list_xpath_to_str(charact,'td[2]')
                return txt
        return ''


    def parse_item_ebay(self, response):
        # hxs = HtmlXPathSelector(response)
        # l = TestLoader(FirstItem(), hxs)
        # l.add_xpath('name', '//div[@class=\'itemAttr\']/div/table/tr/td')
        sel = Selector(response)
        characts = sel.xpath('//div[@class=\'itemAttr\']/div/table/tr')

        items = []
        item = Board()
        item['source'] = 'ebay'
        for charact in characts:

            f = self.get_char_field_ebay(charact, 'Seller Notes')
            if self.is_notnull_item(f):
                item['article'] = f
            f = self.get_char_field_ebay(charact, 'year')
            if self.is_notnull_item(f):
                item['boatyear'] = f
            f = self.get_char_field_ebay(charact, 'Model')
            if self.is_notnull_item(f):
                item['boatmodel'] = f
            f = self.get_char_field_ebay(charact, 'Make')
            if self.is_notnull_item(f):
                item['boatbrand'] = f
            f = self.get_char_field_ebay(charact, 'Length')
            if self.is_notnull_item(f):
                item['boatlength'] = f
            #item[''] = self.get_char_field_ebay(charact, 'Beam')
            #item[''] = self.get_char_field_ebay(charact, 'Use')
            #item[''] = self.get_char_field_ebay(charact, 'Hull Material')
            #item[''] = self.get_char_field_ebay(charact, 'Primary Fuel Type')
            #item[''] = self.get_char_field_ebay(charact, 'Fuel Capacity')
            f = self.get_char_field_ebay(charact, 'Engine Type')
            if self.is_notnull_item(f):
                item['boattype'] = f
        items.append(item)
        return items
        #return l.load_item()

    def parse_item_copart(self, response):
        # hxs = HtmlXPathSelector(response)
        # l = TestLoader(FirstItem(), hxs)
        # l.add_xpath('name', '//div[@class=\'lot-display-list\']/div')
        # return l.load_item()
        sel = Selector(response)
        characts = sel.xpath('//div[@class=\'lot-display-list\']/div')

        items = []
        item = Board()
        item['source'] = 'copart'
        for charact in characts:
            #item[''] = self.get_char_field_copart(charact, 'Doc Type')
            #item[''] = self.get_char_field_copart(charact, 'Odometer')
            #item[''] = self.get_char_field_copart(charact, 'Primary Damage')
            #item[''] = self.get_char_field_copart(charact, 'Secondary Damage')
            #item[''] = self.get_char_field_copart(charact, 'Est. Retail Value')
            #item[''] = self.get_char_field_copart(charact, 'Repair Est')
            #item[''] = self.get_char_field_copart(charact, 'VIN')
            #item[''] = self.get_char_field_copart(charact, 'Body Style')
            f = self.get_char_field_copart(charact, 'Color')
            if self.is_notnull_item(f):
                item['color'] = f
            if self.is_notnull_item(f):
                item['boattype'] = f
            f = self.get_char_field_copart(charact, 'Engine Type')
            #item[''] = self.get_char_field_copart(charact, 'Drive')
            #item[''] = self.get_char_field_copart(charact, 'Cylinder')
            #item[''] = self.get_char_field_copart(charact, 'Fuel')
            #item[''] = self.get_char_field_copart(charact, 'Keys')
            #item[''] = self.get_char_field_copart(charact, 'Downloads')
            f = self.get_char_field_copart(charact, 'Notes')
            if self.is_notnull_item(f):
                item['article'] = f
        items.append(item)
        return items

    def is_notnull_item(self, str):
        if(len(str) > 0):
            return True
        return False

    def parse_item_manheimglobaltrader_images(self, response):
        sel = Selector(response)
        imgs = sel.xpath('//li/a[@class=\'thumb\']')
        items = []
        for img in imgs:
            item = Website()
            item['url'] = img.xpath('@href').extract()
            item['name'] = img.xpath('@href').extract()
            print(img.xpath('@href').extract())
            items.append(item)
        return items

    def parse_item_manheimglobaltrader(self, response):
        sel = Selector(response)
        characts = sel.xpath('//div[@class=\'top\']/table/tr')

        items = []
        item = Board()
        item['source'] = 'manheimglobaltrader'
        for charact in characts:
            #item[''] = self.get_char_field_manheimglobaltrader(charact, 'Engine Volume:')
            #item[''] = self.get_char_field_manheimglobaltrader(charact, 'Doors')

            f = self.get_char_field_manheimglobaltrader(charact, 'Unit Type')
            if self.is_notnull_item(f):
                item['boattype'] = f
            f = self.get_char_field_manheimglobaltrader(charact, 'Year')
            if self.is_notnull_item(f):
                item['boatyear'] = f
            f = self.get_char_field_manheimglobaltrader(charact, 'Make')
            if self.is_notnull_item(f):
                item['boatbrand'] = f
            f = self.get_char_field_manheimglobaltrader(charact, 'Model')
            if self.is_notnull_item(f):
                item['boatmodel'] = f

            #item[''] = self.get_char_field_manheimglobaltrader(charact, 'VIN')
            #item[''] = self.get_char_field_manheimglobaltrader(charact, 'Body')
            #item[''] = self.get_char_field_manheimglobaltrader(charact, 'Transmission')

            f = self.get_char_field_manheimglobaltrader(charact, 'Exterior Color')
            if self.is_notnull_item(f):
                item['color'] = f
            #item[''] = self.get_char_field_manheimglobaltrader(charact, 'Interior Color')
            #item[''] = self.get_char_field_manheimglobaltrader(charact, 'Interior Type')
            #item[''] = self.get_char_field_manheimglobaltrader(charact, 'Engine Volume')
            #item[''] = self.get_char_field_manheimglobaltrader(charact, 'Engine Fuel')
            #item[''] = self.get_char_field_manheimglobaltrader(charact, 'Condition Grade')
            #item[''] = self.get_char_field_manheimglobaltrader(charact, 'Lot ID')
            #item[''] = self.get_char_field_manheimglobaltrader(charact, 'Salvage')
            #item[''] = self.get_char_field_manheimglobaltrader(charact, 'Audio')
            #item[''] = self.get_char_field_manheimglobaltrader(charact, 'Top Style')
            #item[''] = self.get_char_field_manheimglobaltrader(charact, 'Drivetrain')
            #item[''] = self.get_char_field_manheimglobaltrader(charact, 'Trim')
            #item[''] = self.get_char_field_manheimglobaltrader(charact, 'Odometer')
            #item[''] = self.get_char_field_manheimglobaltrader(charact, 'Salvage Description')
            #item[''] = self.get_char_field_manheimglobaltrader(charact, 'Driving Side')
        items.append(item)
        return items
