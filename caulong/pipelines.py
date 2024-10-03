# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import scrapy
import pymongo
import json
# from bson.objectid import ObjectId
# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem
import csv
import os


class MongoDBCauLongPipeline:
    def __init__(self):
        self.client = pymongo.MongoClient('mongodb://10.173.127.37:27017')
        self.db = self.client['dbcaulong'] #Create Database      
        pass
    def process_item(self, item, spider):
        print(f"Processing item: {item}")  # Log item đang xử lý
        collection = self.db['tblcaulong']  # Tạo collection
        try:
            collection.insert_one(dict(item))  # Chèn item vào collection
            print(f"Inserted item into MongoDB: {item}")  # Log sau khi chèn thành công
            return item
        except Exception as e:
            print(f"Error inserting item: {e}")  # Log lỗi nếu có
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
            fieldnames = ['ma','tensp','gia','thuongHieu','courseUrl','tinhTrang','trinhDo','noiDung','phongCach','doCung','diemCanBang','trongLuong','thongTin']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=',')
            # Kiểm tra nếu file CSV chưa có header thì ghi header
            if csvfile.tell() == 0:
                writer.writeheader()
            writer.writerow(item)
        return item
    pass
