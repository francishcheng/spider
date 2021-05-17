# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class PachongItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    RecordID = scrapy.Field() 
    ItemID  = scrapy.Field() 
    BatchID = scrapy.Field() 
    sSampleID= scrapy.Field() 
    sItemName= scrapy.Field() 
    sBatchCode= scrapy.Field() 
    sTime= scrapy.Field() 
    Concentration  = scrapy.Field() 
    Judge= scrapy.Field() 
    CValue= scrapy.Field() 
    TValue = scrapy.Field() 
    SNcode = scrapy.Field()
    sTimeNumber = scrapy.Field()
    points = scrapy.Field()
    address = scrapy.Field()
    data_bight = scrapy.Field()
    create_time = scrapy.Field() 
