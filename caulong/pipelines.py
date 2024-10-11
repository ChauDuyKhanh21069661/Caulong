import scrapy
import pymongo
import psycopg2  # Kết nối tới PostgreSQL
import json
import csv
from scrapy.exceptions import DropItem

class MongoDBCauLongPipeline:
    def __init__(self):
        # Kết nối tới MongoDB
        self.client = pymongo.MongoClient('mongodb://localhost:27017')
        self.db = self.client['dbcaulong']  # Tạo hoặc kết nối Database

    def process_item(self, item, spider):
        # Lưu item vào MongoDB
        collection = self.db['tblcaulong']  # Tạo hoặc kết nối Collection
        try:
            collection.insert_one(dict(item))
            return item
        except Exception as e:
            raise DropItem(f"Error inserting item: {e}")

    def close_spider(self, spider):
        # Sau khi spider chạy xong, thực hiện lấy và xử lý dữ liệu từ MongoDB
        self.process_data_from_mongodb()

    def process_data_from_mongodb(self):
        # Bước 1: Lấy dữ liệu từ MongoDB
        collection = self.db['tblcaulong']
        # Xóa các bản ghi có bất kỳ trường nào là null hoặc rỗng
        collection.delete_many({
            "$or": [
                {key: {"$in": [None, ""]}} for key in collection.find_one().keys()
            ]
        })

        # Bước 2: Lấy dữ liệu sau khi đã xóa
        data = collection.find()

        # Bước 2: Xử lý dữ liệu null và chuẩn bị dữ liệu
        processed_data = self.process_data(data)

        # Bước 3: Lưu dữ liệu đã xử lý vào PostgreSQL
        self.save_to_postgres(processed_data)

    def process_data(self, data):
        # Tạo danh sách lưu dữ liệu đã xử lý
        processed = []
        for item in data:
            # Kiểm tra và xử lý trường 'trongLuong'
            if 'trongLuong' in item and item['trongLuong']:
                weight_lines = self.split_weight(item['trongLuong'])
                for weight_type, weight_range in weight_lines:
                    new_item = {key: value for key, value in item.items() if value not in (None, '')}  # Bản sao item không có giá trị None hoặc rỗng
                    new_item['weight_type'] = weight_type
                    new_item['weight_range'] = weight_range

                    # Kiểm tra xem new_item có ít nhất một giá trị hợp lệ không
                    if any(new_item.values()):  # Nếu có ít nhất một giá trị hợp lệ
                        processed.append(new_item)  # Thêm item đã tách vào danh sách
            else:
                # Nếu không có trường 'trongLuong', giữ nguyên item gốc và kiểm tra
                cleaned_item = {key: value for key, value in item.items() if value not in (None, '')}  # Xóa giá trị None hoặc rỗng
                # Kiểm tra nếu cleaned_item có ít nhất một giá trị hợp lệ
                if any(cleaned_item.values()):  # Nếu có ít nhất một giá trị hợp lệ
                    processed.append(cleaned_item)  # Chỉ thêm nếu cleaned_item không rỗng

        return processed

    def split_weight(self, weight_string):
        # Tách chuỗi trọng lượng thành các dòng riêng biệt
        weights = weight_string.split(',')
        weight_lines = []
        for weight in weights:
            key_value = weight.strip().split(':')
            if len(key_value) == 2:  # Kiểm tra xem có 2 phần tử không
                weight_type = key_value[0].strip()
                weight_range = key_value[1].strip()
                weight_lines.append((weight_type, weight_range))  # Thêm cặp (type, range) vào danh sách
        return weight_lines

    def save_to_postgres(self, data):
        # Kết nối tới PostgreSQL
        conn = psycopg2.connect(
            dbname="caulongdb",  # Tên cơ sở dữ liệu của bạn
            user="postgres",      # Tên người dùng của bạn
            password="bin01042003",  # Mật khẩu của bạn
            host="localhost"
        )
        cursor = conn.cursor()

        # Tạo bảng nếu chưa có
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS caulong (
                ma VARCHAR(255),
                tensp VARCHAR(255),
                gia VARCHAR(255),
                thuongHieu VARCHAR(255),
                courseUrl VARCHAR(255),
                tinhTrang VARCHAR(255),
                trinhDo VARCHAR(255),
                noiDung TEXT,
                phongCach VARCHAR(255),
                doCung VARCHAR(255),
                diemCanBang VARCHAR(255),
                weight_type VARCHAR(10),  -- Cột cho loại trọng lượng
                weight_range VARCHAR(20),  -- Cột cho khoảng trọng lượng
                thongTin TEXT
            )
        ''')

        # Chèn dữ liệu đã xử lý vào bảng PostgreSQL
        for item in data:
            cursor.execute('''
                INSERT INTO caulong_processed (ma, tensp, gia, thuongHieu, courseUrl, tinhTrang, trinhDo, noiDung, phongCach, doCung, diemCanBang, weight_type, weight_range, thongTin)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ''', (
                item.get('ma'),
                item.get('tensp'),
                item.get('gia'),
                item.get('thuongHieu'),
                item.get('courseUrl'),
                item.get('tinhTrang'),
                item.get('trinhDo'),
                item.get('noiDung'),
                item.get('phongCach'),
                item.get('doCung'),
                item.get('diemCanBang'),
                item.get('weight_type'),
                item.get('weight_range'),
                item.get('thongTin')
            ))

        # Lưu thay đổi và đóng kết nối
        conn.commit()
        cursor.close()
        conn.close()

class JsonDBCauLongPipeline:
    def process_item(self, item, spider):
        with open('caulong.json', 'a', encoding='utf-8') as file:
            line = json.dumps(dict(item), ensure_ascii=False) + '\n'
            file.write(line)
        return item

class CSVDBCauLongPipeline:
    def process_item(self, item, spider):
        with open('caulong.csv', 'a', encoding='utf-8', newline='') as csvfile:
            fieldnames = ['ma', 'tensp', 'gia', 'thuongHieu', 'courseUrl', 'tinhTrang', 'trinhDo', 'noiDung', 'phongCach', 'doCung', 'diemCanBang', 'trongLuong', 'thongTin']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=',')
            # Kiểm tra nếu file CSV chưa có header thì ghi header
            if csvfile.tell() == 0:
                writer.writeheader()
            writer.writerow(item)
        return item
