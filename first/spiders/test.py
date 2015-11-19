# -*- coding:utf8 -*-

import re

#from first.items import FirstItem
from first.items import Website
from decimal import Decimal
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

class TestSpider(CrawlSpider):
    name = 'scraby'
    allowed_domains = ["ebay.com", "copart.com", "www.manheimglobaltrader.com", "boattrader.com"]
    start_urls = ["https://www.manheimglobaltrader.com/bu/search?se_search_unit_code[]=BO&flag_search_submit=y",
                "http://www.copart.com/us/search?companyCode_vf=US&Sort=sd&LotTypes=M&YearFrom=2000&YearTo=2016&Make=&RadioGroup=Location&YardNumber=&States=&PostalCode=&Distance=500&searchTitle=2000-2016%2C%2C&cn=2000-2016%2C%2C",
                "http://www.ebay.com/sch/Boats-/26429/i.html?rt=nc&LH_BIN=1&_trksid=p2045573.m1684"
                "http://www.boattrader.com/search-results/NewOrUsed-any/Type-all/Category-all/Radius-200/Sort-Length:DESC"]
    rules = (
        #Rule(SgmlLinkExtractor(restrict_xpaths = ('//h3/a')), callback = 'parse_item_ebay'),
        #Rule(SgmlLinkExtractor(restrict_xpaths = ('//li[@class=\'lot-desc\']/a')), callback = 'parse_item_copart'),
        Rule(SgmlLinkExtractor(restrict_xpaths = ('//td/table[@class=\'search_name_cell\']/tr/td/a')), callback = 'parse_item_manheimglobaltrader'),
        #Rule(SgmlLinkExtractor(restrict_xpaths = ('//div/a')), callback = 'parse_item_boattrader'),
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


    def parse_item_ebay_price(self, response):
        sel = Selector(response)
        txt = sel.xpath('//span[@class=\'notranslate\']').extract()

        tt = ''.join(txt[0])
        txt = re.sub('<.*?>','',tt)
        price = re.sub('[^\d+]','',txt)
        return price

    def parse_item_ebay(self, response):
        # hxs = HtmlXPathSelector(response)
        # l = TestLoader(FirstItem(), hxs)
        # l.add_xpath('name', '//div[@class=\'itemAttr\']/div/table/tr/td')
        sel = Selector(response)
        characts = sel.xpath('//div[@class=\'itemAttr\']/div/table/tr')

        items = []
        item = Board()

        item['price'] = self.parse_item_ebay_price(response)

        for charact in characts:

            f = self.get_char_field_ebay(charact, 'Seller Notes')
            if self.is_notnull_item(f):
                item['content'] = f
            f = self.get_char_field_ebay(charact, 'year')
            if self.is_notnull_item(f):
                item['boatyear'] = re.sub("[^\d]","",f)
            f = self.get_char_field_ebay(charact, 'Model')
            if self.is_notnull_item(f):
                item['boatmodel'] = f
            f = self.get_char_field_ebay(charact, 'Make')
            if self.is_notnull_item(f):
                item['boatbrand'] = f
            f = self.get_char_field_ebay(charact, 'Length')
            if self.is_notnull_item(f):
                item['boatlength'] = re.sub("[^\d]","",f)
            #item[''] = self.get_char_field_ebay(charact, 'Beam')
            #item[''] = self.get_char_field_ebay(charact, 'Use')
            #item[''] = self.get_char_field_ebay(charact, 'Hull Material')
            #item[''] = self.get_char_field_ebay(charact, 'Primary Fuel Type')
            #item[''] = self.get_char_field_ebay(charact, 'Fuel Capacity')
            f = self.get_char_field_ebay(charact, 'Engine Type')
            if self.is_notnull_item(f):
                item['boattype'] = f
        items.append(item)


        sel = Selector(response)
        imgs = sel.xpath('//tr/td[@class=\'tdThumb\']/div/img')
        items = []

        img_index = 0

        for img in imgs:

            if img_index > 41:
                break
            item_image_index = "gallery%s" % img_index
            item_url_index = "url%s" % img_index
            item[item_url_index] = img.xpath('@src').extract()
            item[item_image_index] = img.xpath('@src').extract()

            tmp = ''.join(item[item_url_index])
            m = re.search('\w+\.com',tmp)
            if m:
                item['name'] = m.group(0)
                if m:
                    m = re.search('(\/[0-9,a-z\-\_]+\/[0-9,a-z\-\_]+|[0-9,a-z\-\_]+).jpg$',item[item_image_index][0].lower())
                    item[item_image_index] = "%s/%s" % (item['name'], m.group(0))
                    img_index += 1

        items.append(item)
        return items

    def parse_item_copart_price(self, response):
        sel = Selector(response)
        txt = sel.xpath('//div/span[@class=\'bid\']').extract()
        tt = ''.join(txt[0])
        txt = re.sub('<.*?>','',tt)
        price = re.sub('[^\d+]','',txt)

        #print price

        return price

    def parse_item_copart(self, response):
        sel = Selector(response)
        characts = sel.xpath('//div[@class=\'lot-display-list\']/div')

        items = []
        item = Board()
        item['price'] = self.parse_item_copart_price(response)

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
                item['content'] = f
        items.append(item)


        sel = Selector(response)
        imgs = sel.xpath('//div[@class=\'navigation\']/div/ul/li/img')
        items = []

        img_index = 0
        for img in imgs:

            if img_index > 41:
                break
            item_image_index = "gallery%s" % img_index
            item_url_index = "url%s" % img_index
            item[item_image_index] = img.xpath('@src').extract()
            item[item_url_index] = img.xpath('@src').extract()

            tmp = ''.join(item[item_image_index])
            if len(tmp) == 0:
                continue

            item[item_url_index] = ['http:' + x for x in item[item_url_index]]
            m = re.search('\w+\.com',tmp)
            if m:
                item['name'] = m.group(0)
                if m:
                    m = re.search('(\/[0-9,a-z\-\_]+\/[0-9,a-z\-\_]+|[0-9,a-z\-\_]+).jpg$',item[item_image_index][0].lower())
                    item[item_image_index] = "%s/%s" % (item['name'], m.group(0))
                    img_index += 1
        items.append(item)
        return items




        return items

    def is_notnull_item(self, str):
        if(len(str) > 0):
            return True
        return False

    def parse_manheimglobaltrader_price(self, response):
        price = 0
        # sel = Selector(response)
        # #<span class="bid">$6,200 USD</span>
        # characts = sel.xpath('//span[@class=\'bid\']')

        # print characts
        # for charact in characts:
        #     price = '1'

        return price

    def get_char_field_boattrader(self, charact, text):
        #print charact
        if len(charact.xpath('th')) > 0:
            block_find = charact.xpath('th')[0].re(r'(?i)' + text)
            if len(block_find) > 0:
                txt = self.list_xpath_to_str(charact,'td')
                #print txt
                return txt
        return ''

    def parse_boattrader_price(self, response):
        price = 0
        return price

    def parse_item_boattrader(self, response):
        sel = Selector(response)
        characts = sel.xpath('//div[@class=\'collapsible open\']/table/tbody/tr')

        items = []
        item = Board()
        item['price'] = self.parse_boattrader_price(response)

        for charact in characts:
            f = self.get_char_field_boattrader(charact, 'Class')
            if self.is_notnull_item(f):
                item['boattype'] = f
            f = self.get_char_field_boattrader(charact, 'Category')
            if self.is_notnull_item(f):
                item['boattype'] = f
            f = self.get_char_field_boattrader(charact, 'Year')
            if self.is_notnull_item(f):
                item['boatyear'] = re.sub("[^\d]","",f)
            f = self.get_char_field_boattrader(charact, 'Make')
            if self.is_notnull_item(f):
                item['boatbrand'] = f
            f = self.get_char_field_boattrader(charact, 'Length')
            if self.is_notnull_item(f):
                item['boatlength'] = re.sub("[^\d]","",f)
            #f = self.get_char_field_boattrader(charact, 'Propulsion Type')
            #if self.is_notnull_item(f):
            #    item['boattype'] = f
            #f = self.get_char_field_boattrader(charact, 'Hull Material')
            #if self.is_notnull_item(f):
            #    item['boattype'] = f
            #f = self.get_char_field_boattrader(charact, 'Fuel Type')
            #if self.is_notnull_item(f):
            #    item['boattype'] = f
            #f = self.get_char_field_boattrader(charact, 'Location')
            #if self.is_notnull_item(f):
            #    item['boattype'] = f
        items.append(item)
        return items

    def parse_item_manheimglobaltrader(self, response):
        sel = Selector(response)
        characts = sel.xpath('//div[@class=\'top\']/table/tr')

        items = []
        item = Board()
        item['price'] = self.parse_manheimglobaltrader_price(response)

        for charact in characts:
            #item[''] = self.get_char_field_manheimglobaltrader(charact, 'Engine Volume:')
            #item[''] = self.get_char_field_manheimglobaltrader(charact, 'Doors')

            f = self.get_char_field_manheimglobaltrader(charact, 'Unit Type')
            if self.is_notnull_item(f):
                item['boattype'] = f
            f = self.get_char_field_manheimglobaltrader(charact, 'Year')
            if self.is_notnull_item(f):
                item['boatyear'] = re.sub("[^\d]","",f)
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


        sel = Selector(response)
        imgs = sel.xpath('//li/a[@class=\'thumb\']')
        items = []

        img_index = 0

        for img in imgs:

            if img_index > 41:
                break
            item_image_index = "gallery%s" % img_index
            item_url_index = "url%s" % img_index
            item[item_image_index] = img.xpath('@href').extract()
            item[item_url_index] = img.xpath('@href').extract()

            tmp = ''.join(item[item_image_index])
            m = re.search('\w+\.com',tmp)
            if m:
                item['name'] = m.group(0)
                if m:
                    m = re.search('(\/[0-9,a-z\-\_]+\/[0-9,a-z\-\_]+|[0-9,a-z\-\_]+).jpg$',item[item_image_index][0].lower())
                    item[item_image_index] = "%s/%s" % (item['name'], m.group(0))
                    img_index += 1

        items.append(item)

        return items
