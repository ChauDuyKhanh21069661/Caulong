import scrapy
from caulong.items import CauLongItem

class MycaulongSpider(scrapy.Spider):
    name = "mycaulong"
    allowed_domains = ["shopvnb.com"]
    
    def start_requests(self):
        base_url = "https://shopvnb.com/vot-cau-long.html?page={}"
        for page_num in range(1, 60):  # Assuming there are 18 pages
            yield scrapy.Request(url=base_url.format(page_num), callback=self.parse)

    def parse(self, response):
        courseList = response.xpath('//html/body/div[2]/div[1]/div/div[1]/div/div/div/div/div/div/div/div/a[2]/@href').getall()
        for courseItem in courseList:
            item = CauLongItem()
            item['courseUrl'] = response.urljoin(courseItem)
            request = scrapy.Request(url = response.urljoin(courseItem), callback=self.parseCourseDetailPage)
            request.meta['datacourse'] = item
            yield request
    
    def parseCourseDetailPage(self, response):
        item = response.meta['datacourse']
        # Lấy các thông tin chi tiết sản phẩm
        item['ma'] = response.xpath('normalize-space(string(//div[@class="sku-product clearfix"]/span[2]/span))').get()
        item['tensp'] = response.xpath('normalize-space(string(//div[@class="details-pro col-12 col-md-6 col-lg-7"]/h1))').get()
        item['gia'] = response.xpath('normalize-space(string(//div[@class="price-box clearfix"]/span[1]/span/span))').get()
        item['thuongHieu'] = response.xpath('normalize-space(string(//div[@class="inventory_quantity"]/span[1]/a))').get()
        item['tinhTrang'] = response.xpath('normalize-space(string(//div[@class="inventory_quantity"]/span[3]/span[2]))').get()
        item['trinhDo'] = response.xpath('normalize-space(string(//*[@id="tab_thong_so"]/div/table/tbody/tr[1]/td[2]))').get()
        item['noiDung'] = response.xpath('normalize-space(string(//*[@id="tab_thong_so"]/div/table/tbody/tr[2]/td[2]))').get()
        item['phongCach'] = response.xpath('normalize-space(string(//*[@id="tab_thong_so"]/div/table/tbody/tr[3]/td[2]))').get()
        item['doCung'] = response.xpath('normalize-space(string(//*[@id="tab_thong_so"]/div/table/tbody/tr[4]/td[2]))').get()
        item['diemCanBang'] = response.xpath('normalize-space(string(//*[@id="tab_thong_so"]/div/table/tbody/tr[5]/td[2]))').get()
        item['trongLuong'] = response.xpath('normalize-space(string(//*[@id="tab_thong_so"]/div/table/tbody/tr[6]/td[2]))').get()
        item['thongTin'] = response.xpath('normalize-space(string(//*[@id="content"]/div/div/div/p/span/span))').get()
        yield item
