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
USER_AGENT = '%s/%s' % (BOT_NAME, BOT_VERSION)

ITEM_PIPELINES = ['first.pipelines.FirstPipeline']

FEED_EXPORTERS = {
    'csv': 'first.pipelines.ProductCSVExporter',

}

EXPORT_FIELDS = [
    'content',
    'price',
    'old_price',
    'pagetitle',
    'boatyear',
    'gallery',
    'boatbrand',
    'boatmodel',
    'boatlength',
    'boatwidth',
    'boatmotor',
    'boattype',
    'parent',
    'template',
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
CSV_DELIMITER = "\t"
