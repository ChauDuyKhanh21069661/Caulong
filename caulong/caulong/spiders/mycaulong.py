import scrapy  # Nhập mô-đun scrapy để sử dụng các chức năng của nó.
from caulong.items import CauLongItem  # Nhập CauLongItem từ module items, để lưu trữ dữ liệu cào.

class MycaulongSpider(scrapy.Spider):  # Định nghĩa một lớp Spider mới, kế thừa từ scrapy.Spider.
    name = "mycaulong"  # Đặt tên cho spider này, tên này sẽ được sử dụng khi chạy spider.
    allowed_domains = ["shopvnb.com"]  # Danh sách các miền mà spider này được phép truy cập.

    def start_requests(self):  # Phương thức khởi động các yêu cầu đầu tiên.
        base_url = "https://shopvnb.com/vot-cau-long.html?page{}"  # Đường dẫn cơ bản để truy cập trang sản phẩm.
        for page_num in range(1, 60):  # Lặp qua các số trang từ 1 đến 59.
            yield scrapy.Request(url=base_url.format(page_num), callback=self.parse)  # Tạo yêu cầu cho mỗi trang và định nghĩa callback là phương thức parse.

    def parse(self, response):  # Phương thức xử lý phản hồi từ các yêu cầu.
        courseList = response.xpath('//html/body/div[2]/div[1]/div/div[1]/div/div/div/div/div/div/div/div/a[2]/@href').getall()  # Lấy tất cả các liên kết đến các sản phẩm từ HTML.
        for courseItem in courseList:  # Lặp qua danh sách các liên kết sản phẩm.
            item = CauLongItem()  # Tạo một đối tượng mới của CauLongItem để lưu trữ thông tin sản phẩm.
            item['courseUrl'] = response.urljoin(courseItem)  # Lưu URL sản phẩm vào item, sử dụng urljoin để tạo URL đầy đủ.
            request = scrapy.Request(url=response.urljoin(courseItem), callback=self.parseCourseDetailPage)  # Tạo yêu cầu mới để truy cập trang chi tiết sản phẩm.
            request.meta['datacourse'] = item  # Lưu item vào meta của yêu cầu để truyền dữ liệu sang phương thức xử lý tiếp theo.
            yield request  # Gửi yêu cầu.

    def parseCourseDetailPage(self, response):  # Phương thức xử lý phản hồi từ trang chi tiết sản phẩm.
        item = response.meta['datacourse']  # Lấy item đã lưu từ meta của yêu cầu trước đó.
        # Lấy các thông tin chi tiết sản phẩm bằng cách sử dụng XPath và lưu vào item.
        item['ma'] = response.xpath('normalize-space(string(//div[@class="sku-product clearfix"]/span[2]/span))').get()  # Mã sản phẩm.
        item['tensp'] = response.xpath('normalize-space(string(//div[@class="details-pro col-12 col-md-6 col-lg-7"]/h1))').get()  # Tên sản phẩm.
        item['gia'] = response.xpath('normalize-space(string(//div[@class="price-box clearfix"]/span[1]/span/span))').get()  # Giá sản phẩm.
        item['thuongHieu'] = response.xpath('normalize-space(string(//div[@class="inventory_quantity"]/span[1]/a))').get()  # Thương hiệu sản phẩm.
        item['tinhTrang'] = response.xpath('normalize-space(string(//div[@class="inventory_quantity"]/span[3]/span[2]))').get()  # Tình trạng sản phẩm.
        item['trinhDo'] = response.xpath('normalize-space(string(//*[@id="tab_thong_so"]/div/table/tbody/tr[1]/td[2]))').get()  # Trình độ sản phẩm.
        item['noiDung'] = response.xpath('normalize-space(string(//*[@id="tab_thong_so"]/div/table/tbody/tr[2]/td[2]))').get()  # Nội dung sản phẩm.
        item['phongCach'] = response.xpath('normalize-space(string(//*[@id="tab_thong_so"]/div/table/tbody/tr[3]/td[2]))').get()  # Phong cách sản phẩm.
        item['doCung'] = response.xpath('normalize-space(string(//*[@id="tab_thong_so"]/div/table/tbody/tr[4]/td[2]))').get()  # Độ cứng của sản phẩm.
        item['diemCanBang'] = response.xpath('normalize-space(string(//*[@id="tab_thong_so"]/div/table/tbody/tr[5]/td[2]))').get()  # Điểm cân bằng của sản phẩm.
        item['trongLuong'] = response.xpath('normalize-space(string(//*[@id="tab_thong_so"]/div/table/tbody/tr[6]/td[2]))').get()  # Trọng lượng sản phẩm.
        item['thongTin'] = response.xpath('normalize-space(string(//*[@id="content"]/div/div/div/p/span/span))').get()  # Thông tin thêm về sản phẩm.
        yield item  # Gửi item chứa dữ liệu sản phẩm ra ngoài.
