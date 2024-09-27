# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class CauLongItem(scrapy.Item):
    ma = scrapy.Field()
    tensp = scrapy.Field()
    gia = scrapy.Field()
    thuongHieu = scrapy.Field()
    tinhTrang = scrapy.Field()
    trinhDo = scrapy.Field()
    noiDung = scrapy.Field()
    phongCach = scrapy.Field()
    doCung = scrapy.Field()
    courseUrl = scrapy.Field()
    diemCanBang = scrapy.Field()
    trongLuong = scrapy.Field()
    thongTin = scrapy.Field()