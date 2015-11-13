# -*- coding:utf8 -*-

import re

from first.items import FirstItem
from first.items import Website
from first.items import Board

from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.loader import XPathItemLoader
from scrapy.contrib.loader.processor import Compose
from scrapy.contrib.loader.processor import MapCompose
from scrapy.contrib.loader.processor import TakeFirst
from scrapy.contrib.loader.processor import Join
from scrapy.selector import Selector
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.selector import HtmlXPathSelector

class TestLoader(XPathItemLoader):
    default_input_processor = MapCompose(lambda s: re.sub('(<.*?>|\t|[^a-zA-Z0-9_\/., :-\|]| {2,})', '', s.strip()))
    default_output_processor = Join('\t')

# "http://www.ebay.com/sch/Boats-/26429/i.html?rt=nc&LH_BIN=1&_trksid=p2045573.m1684",
# "http://www.copart.com/us/search?companyCode_vf=US&Sort=sd&LotTypes=M&YearFrom=2000&YearTo=2016&Make=&RadioGroup=Location&YardNumber=&States=&PostalCode=&Distance=500&searchTitle=2000-2016%2C%2C&cn=2000-2016%2C%2C",
#"https://www.manheimglobaltrader.com/bu/search?se_search_unit_code[]=BO&flag_search_submit=y",

class TestSpider(CrawlSpider):
    name = 'test'
    allowed_domains = ["ebay.com", "copart.com", "www.manheimglobaltrader.com"]
    start_urls = ["https://www.manheimglobaltrader.com/bu/search?se_search_unit_code[]=BO&flag_search_submit=y"]
    rules = (
        Rule(SgmlLinkExtractor(restrict_xpaths = ('//h3/a')), callback = 'parse_item_ebay'),
        Rule(SgmlLinkExtractor(restrict_xpaths = ('//li[@class=\'lot-desc\']/a')), callback = 'parse_item_copart'),
        Rule(SgmlLinkExtractor(restrict_xpaths = ('//td/table[@class=\'search_name_cell\']/tr/td/a')), callback = 'parse_item_manheimglobaltrader'),
    )


    def get_char_field_copart(self, charact, text):
        if len(charact.xpath('label')) > 0:
            #print text
            year = charact.xpath('label')[0].re(r'(?i)' + text)
            if len(year) > 0:
                txt = charact.xpath('text()').extract()
                txt = re.sub('<.*?>','',str(txt))
                print txt
        return

    def get_char_field_ebay(self, charact, text):
        if len(charact.xpath('td')) > 0:
            year = charact.xpath('td')[0].re(r'(?i)' + text)
            if len(year) > 0:
                    txt = charact.xpath('td[2]/span').extract()
                    txt = re.sub('<.*?>','',str(txt))
                    print txt
        return

    def get_char_field_manheimglobaltrader(self, charact, text):
        if len(charact.xpath('td')) > 0:
                year = charact.xpath('td')[0].re(r'(?i)' + text)

                if len(year) > 0:
                    #print charact
                    txt = charact.xpath('td[2]').extract()
                    txt = re.sub('<.*?>','',str(txt))
                    #print txt
                    return txt
        return


    def parse_item_ebay(self, response):
        # hxs = HtmlXPathSelector(response)
        # l = TestLoader(FirstItem(), hxs)
        # l.add_xpath('name', '//div[@class=\'itemAttr\']/div/table/tr/td')
        sel = Selector(response)
        characts = sel.xpath('//div[@class=\'itemAttr\']/div/table/tr')

        items = []
        for charact in characts:
            item = Board()
            self.get_char_field_ebay(charact, 'Seller Notes')
            self.get_char_field_ebay(charact, 'year')
            self.get_char_field_ebay(charact, 'Model')
            self.get_char_field_ebay(charact, 'Make')
            self.get_char_field_ebay(charact, 'Length')
            self.get_char_field_ebay(charact, 'Beam')
            self.get_char_field_ebay(charact, 'Use')
            self.get_char_field_ebay(charact, 'Hull Material')
            self.get_char_field_ebay(charact, 'Primary Fuel Type')
            self.get_char_field_ebay(charact, 'Fuel Capacity')
            self.get_char_field_ebay(charact, 'Engine Type')
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
        for charact in characts:
            item = Board()
            self.get_char_field_copart(charact, 'Doc Type')
            self.get_char_field_copart(charact, 'Odometer')
            self.get_char_field_copart(charact, 'Primary Damage')
            self.get_char_field_copart(charact, 'Secondary Damage')
            self.get_char_field_copart(charact, 'Est. Retail Value')
            self.get_char_field_copart(charact, 'Repair Est')
            self.get_char_field_copart(charact, 'VIN')
            self.get_char_field_copart(charact, 'Body Style')
            self.get_char_field_copart(charact, 'Color')
            self.get_char_field_copart(charact, 'Engine Type')
            self.get_char_field_copart(charact, 'Drive')
            self.get_char_field_copart(charact, 'Cylinder')
            self.get_char_field_copart(charact, 'Fuel')
            self.get_char_field_copart(charact, 'Keys')
            self.get_char_field_copart(charact, 'Downloads')
            self.get_char_field_copart(charact, 'Notes')

        return items

    def parse_item_manheimglobaltrader(self, response):

        # hxs = HtmlXPathSelector(response)
        # l = TestLoader(FirstItem(), hxs)
        # l.add_xpath('name', '//div[@class=\'top\']/table/tr/td')
        # sel = Selector(response)
        # imgs = sel.xpath('//li/a[@class=\'thumb\']')
        # items = []
        # for img in imgs:
        #     item = Website()
        #     item['url'] = img.xpath('@href').extract()
        #     item['name'] = img.xpath('@href').extract()
        #     #print(img.xpath('@href').extract())
        #     items.append(item)
        # return items
        sel = Selector(response)
        characts = sel.xpath('//div[@class=\'top\']/table/tr')

        items = []
        for charact in characts:
            item = Board()
            item['year'] = self.get_char_field_manheimglobaltrader(charact, 'Unit Type')
            self.get_char_field_manheimglobaltrader(charact, 'Engine Volume:')
            self.get_char_field_manheimglobaltrader(charact, 'Doors')
            self.get_char_field_manheimglobaltrader(charact, 'Year')
            self.get_char_field_manheimglobaltrader(charact, 'Make')
            self.get_char_field_manheimglobaltrader(charact, 'Model')
            self.get_char_field_manheimglobaltrader(charact, 'VIN')
            self.get_char_field_manheimglobaltrader(charact, 'Body')
            self.get_char_field_manheimglobaltrader(charact, 'Transmission')
            self.get_char_field_manheimglobaltrader(charact, 'Exterior Color')
            self.get_char_field_manheimglobaltrader(charact, 'Interior Color')
            self.get_char_field_manheimglobaltrader(charact, 'Interior Type')
            self.get_char_field_manheimglobaltrader(charact, 'Engine Volume')
            self.get_char_field_manheimglobaltrader(charact, 'Engine Fuel')
            self.get_char_field_manheimglobaltrader(charact, 'Condition Grade')
            self.get_char_field_manheimglobaltrader(charact, 'Lot ID')
            self.get_char_field_manheimglobaltrader(charact, 'Salvage')
            self.get_char_field_manheimglobaltrader(charact, 'Audio')
            self.get_char_field_manheimglobaltrader(charact, 'Top Style')
            self.get_char_field_manheimglobaltrader(charact, 'Drivetrain')
            self.get_char_field_manheimglobaltrader(charact, 'Trim')
            self.get_char_field_manheimglobaltrader(charact, 'Odometer')
            self.get_char_field_manheimglobaltrader(charact, 'Salvage Description')
            self.get_char_field_manheimglobaltrader(charact, 'Driving Side')
            items.append(item)
        return items
