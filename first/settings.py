# Scrapy settings for first project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html
#

BOT_NAME = 'board_get'
BOT_VERSION = '1.0'

SPIDER_MODULES = ['first.spiders']
NEWSPIDER_MODULE = 'first.spiders'
DEFAULT_ITEM_CLASS = 'first.items.Board'
USER_AGENT = 'Mozilla/5.0 (X11; Linux x86_64; rv:31.0) Gecko/20100101 Firefox/31.0 Iceweasel/31.7.0'

ITEM_PIPELINES = ['first.pipelines.FirstPipeline']

FEED_EXPORTERS = {
    'csv': 'first.pipelines.ProductCSVExporter',

}

DEFAULT_REQUEST_HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en',
}

EXPORT_FIELDS = [
    'content',
    'price',
    'old_price',
    'pagetitle',
    'boatyear',
    'boatbrand',
    'boatmodel',
    'boatlength',
    'boatwidth',
    'boatmotor',
    'boattype',
    'parent',
    'template',
    'from_url',
    'url0',
    'url1',
    'url2',
    'url3',
    'url4',
    'url5',
    'url6',
    'url7',
    'url8',
    'url9',
    'url10',
    'url11',
    'url12',
    'url13',
    'url14',
    'url15',
    'url16',
    'url17',
    'url18',
    'url19',
    'url20',
    'url21',
    'url22',
    'url23',
    'url24',
    'url25',
    'url26',
    'url27',
    'url28',
    'url29',
    'url30',
    'url31',
    'url32',
    'url33',
    'url34',
    'url35',
    'url36',
    'url37',
    'url38',
    'url39',
    'url40',
    'name',
]

IMAGES_STORE = './'
CSV_DELIMITER = "|"
