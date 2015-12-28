# Scrapy settings for first project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html
#

BOT_NAME = 'board_get'
BOT_VERSION = '1.0'

#CLOSESPIDER_ITEMCOUNT=10
DOWNLOAD_DELAY = 1

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
    'gallery0',
    'gallery1',
    'gallery2',
    'gallery3',
    'gallery4',
    'gallery5',
    'gallery6',
    'gallery7',
    'gallery8',
    'gallery9',
    'gallery10',
    'gallery11',
    'gallery12',
    'gallery13',
    'gallery14',
    'gallery15',
    'gallery16',
    'gallery17',
    'gallery18',
    'gallery19',
    'gallery20',
    'gallery21',
    'gallery22',
    'gallery23',
    'gallery24',
    'gallery25',
    'gallery26',
    'gallery27',
    'gallery28',
    'gallery29',
    'gallery30',
    'gallery31',
    'gallery32',
    'gallery33',
    'gallery34',
    'gallery35',
    'gallery36',
    'gallery37',
    'gallery38',
    'gallery39',
    'gallery40',
    'name',
]

IMAGES_STORE = './'
CSV_DELIMITER = "|"
