# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/topics/items.html

from scrapy.item import Item, Field

class Website(Item):
    name = Field()
    description = Field()
    url = Field()

class Board(Item):
    article = Field()
    price = Field()
    old_price = Field()
    weight = Field()
    image = Field()
    thumb = Field()
    vendor = Field()
    made_in = Field()
    new = Field()
    popular = Field()
    favorite = Field()
    tags = Field()
    color = Field()
    size = Field()
    source = Field()
    boatyear = Field()
    boatbrand = Field()
    boatmodel = Field()
    boatlength = Field()
    boatwidth = Field()
    boatmotor = Field()
    boattype = Field()
