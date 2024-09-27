# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import scrapy
import pymongo
import json
import os  # Thêm import os để sử dụng biến môi trường
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem
import csv

class MongoDBCauLongPipeline:
    def __init__(self):
        # Lấy URI từ biến môi trường
        mongo_uri = os.getenv("MONGO_URI", "mongodb://mongo:27017")
        self.client = pymongo.MongoClient(mongo_uri)  # Kết nối đến MongoDB
        self.db = self.client['dbcaulong']  # Create Database      

    def process_item(self, item, spider):
        collection = self.db['tblcaulong']  # Create Collection or Table
        try:
            collection.insert_one(dict(item))
            return item
        except Exception as e:
            raise DropItem(f"Error inserting item: {e}")

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
            writer.writerow(dict(item))  # Sử dụng dict(item) để ghi vào CSV
        return item
