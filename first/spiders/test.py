# -*- coding:utf8 -*-

import re

#from first.items import FirstItem
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
import os.path

import sys
reload(sys)
sys.setdefaultencoding('utf8')

class TestLoader(XPathItemLoader):
    default_input_processor = MapCompose(lambda s: re.sub('(<.*?>|\t|[^a-zA-Z0-9_\/., :-\|]| {2,})', '', s.strip()))
    default_output_processor = Join('\t')

class TestSpider(CrawlSpider):
    name = 'scraby'
    mode = None
    file_path = "./list_urls.txt"
    allowed_domains = ["ebay.com", "copart.com", "www.manheimglobaltrader.com", "boattrader.com"]
    list_from_file = []

    def __init__(self, mode=None, file_path=None,*args, **kwargs):
        super(TestSpider, self).__init__(*args, **kwargs)
        self.mode = mode
        if file_path is not None:
            self.file_path = file_path
        if os.path.exists(self.file_path):
            if self.mode == "from_list":
                #l = [line.strip() for line in open(self.file_path, 'r')]
                for line in open(self.file_path, 'r'):
                    self.list_from_file=line
                    self.start_urls.append(line.strip().split(';')[2])
                print(self.start_urls)
                

            else:
                self.rules = (
                      Rule(SgmlLinkExtractor(restrict_xpaths = ('//h3[@class=\'lvtitle\']/a')), callback = 'parse_item_ebay'),
                      Rule(SgmlLinkExtractor(restrict_xpaths = ('//td[@class=\'pagn-next\']/a')), follow=True),
                      Rule(SgmlLinkExtractor(restrict_xpaths = ('//li[@class=\'lot-desc\']/a')), callback = 'parse_item_copart'),
                      Rule(SgmlLinkExtractor(restrict_xpaths = ('//a[@class=\'pager-next\']')), follow=True),
                      Rule(SgmlLinkExtractor(restrict_xpaths = ('//table[@class=\'search_list_container\']/tr/td[1]/table/tr/td/a')), callback = 'parse_item_manheimglobaltrader'),
                      Rule(SgmlLinkExtractor(restrict_xpaths = ('(//input[@value=\'Next\'])[2]')), follow=True),
                      Rule(SgmlLinkExtractor(restrict_xpaths = ('//li/div[@class=\'inner\']/a')), callback = 'parse_item_boattrader'),
                      Rule(SgmlLinkExtractor(restrict_xpaths = ('//a[contains(text(),\'>\')]')), follow=True),
                )

                self.start_urls = [
                    "https://www.manheimglobaltrader.com/bu/search?se_search_unit_code[]=BO&flag_search_submit=y&offset=1&limit=500",
                    "http://www.copart.com/us/search?companyCode_vf=US&Sort=sd&LotTypes=M&YearFrom=2000&YearTo=2016&Make=&RadioGroup=Location&YardNumber=&States=&PostalCode=&Distance=500&searchTitle=2000-2016%2C%2C&cn=2000-2016%2C%2C",
                    "http://www.ebay.com/sch/Boats-/26429/i.html?rt=nc&LH_BIN=1&_trksid=p2045573.m1684",
                    "http://www.boattrader.com/search-results/NewOrUsed-any/Type-small+boats/Category-all/Radius-200/Sort-Length:DESC",
                ]
                return self.parse_start_url
                
        else:
            print "File %s not exist!\n" % self.file_path


    def parse(self, response):
        if self.mode == "from_list":
            if response.url.startswith("http://www.ebay.com"):
                return self.parse_item_ebay(response)
            elif response.url.startswith("http://www.copart.com"):
                return self.parse_item_copart(response)
            elif response.url.startswith("http://www.boattrader.com"):
                return self.parse_item_boattrader
            elif response.url.startswith("https://www.manheimglobaltrader.com"):
                return self.parse_item_manheimglobaltrader
        else:
            print "here!"

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
        blocks = charact.xpath('td').extract()
        #print blocks
        count = 0
        for block in blocks:
            count += 1
            txt_td = re.sub('<.*?>|\s','',block.strip())
            txt_td = txt_td.encode('utf-8')
            #print txt_td
            #print text
            m = re.search(r'^(?i)'+text,txt_td)
            if m:
                if len(blocks) > count:
                    return re.sub('<.*?>|\s{2,}','',blocks[count].strip())
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
        price = re.sub('[^\d+\.]','',txt)
        #price = re.sub(',','.',price)
        return price

    def parse_item_ebay(self, response):
        sel = Selector(response)
        characts = sel.xpath('//div[@class=\'itemAttr\']/div/table/tr')

        items = []
        item = Board()

        lines = self.list_from_file.split('\r\n')
        for line in lines:
            l = line.split(';')
            if response.url == l[2].strip():
                item['parent'] = l[0]
                item['boattype'] = l[1]
        
        item['from_url'] = response.url

        item['boatmodel'] = ''
        item['boatyear'] = ''
        item['boatbrand'] = ''
        item['old_price'] = self.parse_item_ebay_price(response)

        for charact in characts:
            f = self.get_char_field_ebay(charact, 'Seller Notes')
            if self.is_notnull_item(f):
                item['content'] = f

            f = self.get_char_field_ebay(charact, 'Year')
            if self.is_notnull_item(f):
                item['boatyear'] = re.sub("[^\d]","",f)

            f = self.get_char_field_ebay(charact, 'Model')
            if self.is_notnull_item(f):
                item['boatmodel'] = f

            f = self.get_char_field_ebay(charact, 'Модель')
            if self.is_notnull_item(f):
                item['boatmodel'] = f

            f = self.get_char_field_ebay(charact, 'Make')
            if self.is_notnull_item(f):
                item['boatbrand'] = f

            f = self.get_char_field_ebay(charact, 'Изготовитель')
            if self.is_notnull_item(f):
                item['boatbrand'] = f

            f = self.get_char_field_ebay(charact, 'Length')
            if self.is_notnull_item(f):
                item['boatlength'] = re.sub("[^\d\.]","",f)

            #item[''] = self.get_char_field_ebay(charact, 'Beam')
            #item[''] = self.get_char_field_ebay(charact, 'Use')
            #item[''] = self.get_char_field_ebay(charact, 'Hull Material')
            #item[''] = self.get_char_field_ebay(charact, 'Primary Fuel Type')
            #item[''] = self.get_char_field_ebay(charact, 'Fuel Capacity')
            f = self.get_char_field_ebay(charact, 'Type')
            if self.is_notnull_item(f):
                item['boattype'] = f
            f = self.get_char_field_ebay(charact, 'Тип')
            if self.is_notnull_item(f):
                item['boattype'] = f
        items.append(item)

        sel = Selector(response)
        imgs2 = sel.xpath('//img[@class=\"img img300\"]')

        if len(imgs2) > 1:
            del imgs2[-1]

        imgs = sel.xpath('//tr/td[@class=\'tdThumb\']/div/img')
        imgs.extend(imgs2)


        items = []

        #img_index = 0

        x = 0
        for img in imgs:
            x = x + 1
            if x > 41:
                break
            item_image_index = "gallery%s" % x
            item_url_index = "url%s" % x

            tmp = ''.join(img.xpath('@src').extract())
            if len(tmp) == 0:
                continue

            item[item_url_index] = img.xpath('@src').extract()
            item[item_image_index] = img.xpath('@src').extract()

            tmp = ''.join(item[item_url_index])
            m = re.search('\w+\.com',tmp)
            if m:
                item['name'] = m.group(0)
                m = re.search('(\/[0-9,A-Za-z\-\_\~]+\/[0-9,A-Za-z\-\_\~]+|[0-9,A-Za-z\-\_\~]+).jpg$',item[item_image_index][0])
                
                if m:
                    item[item_image_index] = "/tmp/%s/%s" % (item['name'], m.group(0))
                    item[item_image_index] = re.sub('//','/',item[item_image_index])
                    item[item_image_index] = re.sub('s-l300.','s-l1600_'+str(x)+'.',item[item_image_index])
                    item[item_image_index] = re.sub('s-l64.','s-l1600_'+str(x)+'.',item[item_image_index])

                    item[item_url_index] = re.sub('s-l300.','s-l1600.',item[item_url_index][0])
                    item[item_url_index] = re.sub('s-l64.','s-l1600.',item[item_url_index])

                    #item[item_url_index] = re.sub('s-l300.','s-l500.',item[item_url_index][0])
                    #print item
                    #x += 1


        items.append(item)

        return items

    def parse_item_copart_price(self, response):
        sel = Selector(response)
        txt = sel.xpath('//div/span[@class=\'bid\']').extract()
        if len(txt) > 0:
            tt = ''.join(txt[0])
            txt = re.sub('<.*?>','',tt)
            price = re.sub('[^\d+\.,]','',txt)
            return price
        return

    def get_copart_titlehead(self, response):
        sel = Selector(response)
        txt = sel.xpath('//div[@id=\'TitleHead\']/h2').extract()

        if len(txt) > 0:
            tt = ''.join(txt[0])
            txt = re.sub('<.*?>','',tt)
            return txt
        return

    def parse_item_copart(self, response):
        sel = Selector(response)
        characts = sel.xpath('//div[@class=\'lot-display-list\']/div')

        titlehead = self.get_copart_titlehead(response)
        print titlehead

        items = []
        item = Board()

        line = self.list_from_file.split(';')
        if response.url == line[2].strip():
            item['parent'] = line[0]
            item['boattype'] = line[1]

        item['boatmodel'] = re.sub('^\d+\s','',titlehead)
        m = re.search('^\d+\s',titlehead)
        if m:
            item['boatyear'] = m.group(0)
        item['boatbrand'] = ''
        item['old_price'] = self.parse_item_copart_price(response)
        item['from_url'] = response.url

        print item

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

            tmp = ''.join(img.xpath('@src').extract())
            if len(tmp) == 0:
                continue

            item[item_image_index] = img.xpath('@src').extract()
            item[item_url_index] = img.xpath('@src').extract()

            item[item_image_index] = ['http:' + x for x in item[item_url_index]]
            item[item_url_index] = ['http:' + x for x in item[item_url_index]]
            m = re.search('\w+\.com',tmp)
            if m:
                item['name'] = m.group(0)
                if m:
                    m = re.search('(\/[0-9,a-z\-\_]+\/[0-9,a-z\-\_]+|[0-9,a-z\-\_]+).jpg$',item[item_image_index][0], flags=re.IGNORECASE)
                    item[item_image_index] = "/tmp/%s/%s" % (item['name'], m.group(0))
                    item[item_image_index] = re.sub('//','/',item[item_image_index])
                    item[item_image_index] = re.sub('.jpg$','X.JPG',item[item_image_index], flags=re.IGNORECASE)
                    item[item_url_index] = re.sub('.jpg$','X.JPG',item[item_url_index][0], flags=re.IGNORECASE)
                    #print item[item_url_index]
                    img_index += 1
        items.append(item)
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
        #<span class="bd-price contact-toggle">
        sel = Selector(response)
        txt = sel.xpath('//div/span[@class=\'bd-price contact-toggle\']').extract()
        if txt:
            tt = ''.join(txt[0])
            txt = re.sub('<.*?>','',tt)
            price = re.sub('[^\d+\.,]','',txt)
        else:
            price = 0
        #print price
        #return price

        return price

    def parse_item_boattrader(self, response):
        sel = Selector(response)
        characts = sel.xpath('//div[@class=\'collapsible open\']/table/tbody/tr')

        items = []
        item = Board()

        item['boatmodel'] = ''
        item['boatyear'] = ''
        item['boatbrand'] = ''
        item['old_price'] = self.parse_boattrader_price(response)
        item['from_url'] = response.url

        for charact in characts:
            f = self.get_char_field_boattrader(charact, 'Class')
            if self.is_notnull_item(f):
                item['boattype'] = re.sub("^\s","",f)
            f = self.get_char_field_boattrader(charact, 'Category')
            if self.is_notnull_item(f):
                item['boattype'] = re.sub("^\s","",f)
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

        sel = Selector(response)

        imgs = sel.xpath('//div[@class=\'carousel\']/ul/li')
        items = []
        img_index = 0

        for img in imgs:

            if img_index > 41:
                break
            item_image_index = "gallery%s" % img_index
            item_url_index = "url%s" % img_index

            tmp = ''.join(img.xpath('@data-src_w0').extract())
            if len(tmp) == 0:
                continue

            item[item_image_index] = img.xpath('@data-src_w0').extract()
            item[item_url_index] = img.xpath('@data-src_w0').extract()

            m = re.search('.*.jpg',item[item_url_index][0])
            if m:
                item[item_url_index][0] = m.group(0)
                #print item[item_image_index]
                tmp = ''.join(item[item_image_index])
                m = re.search('\w+\.com',tmp)
                if m:
                    item['name'] = m.group(0)
                    if m:
                        m = re.search('(\/[0-9,a-z\-\_]+\/[0-9,a-z\-\_]+|[0-9,a-z\-\_]+).jpg',item[item_image_index][0].lower())
                        item[item_image_index] = "/tmp/%s/%s" % (item['name'], m.group(0))
                        item[item_image_index] = re.sub('//','/',item[item_image_index])
                        item[item_url_index] = item[item_url_index][0]
                        img_index += 1

        items.append(item)

        return items

    def parse_item_manheimglobaltrader(self, response):
        sel = Selector(response)
        characts = sel.xpath('//div[@class=\'top\']/table/tr')

        items = []
        item = Board()
        item['boatmodel'] = ''
        item['boatyear'] = ''
        item['boatbrand'] = ''
        item['old_price'] = self.parse_manheimglobaltrader_price(response)
        item['from_url'] = response.url

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

            tmp = ''.join(img.xpath('@href').extract())
            if len(tmp) == 0:
                continue

            item[item_image_index] = img.xpath('@href').extract()
            item[item_url_index] = img.xpath('@href').extract()

            tmp = ''.join(item[item_image_index])
            m = re.search('\w+\.com',tmp)
            if m:
                item['name'] = m.group(0)
                if m:
                    m = re.search('(\/[0-9,a-z\-\_]+\/[0-9,a-z\-\_]+|[0-9,a-z\-\_]+).jpg$',item[item_image_index][0].lower())
                    item[item_image_index] = "/tmp/%s/%s" % (item['name'], m.group(0))
                    item[item_image_index] = re.sub('//','/',item[item_image_index])
                    item[item_url_index] = item[item_url_index][0]
                    img_index += 1

        items.append(item)

        return items
