# Sử dụng image của Python
FROM python:3.12-slim

# Cài đặt các thư viện cần thiết
RUN pip install --upgrade pip
COPY requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt

# Sao chép mã nguồn vào container
COPY . /app
WORKDIR /app

# Chạy Scrapy
CMD ["scrapy", "crawl", "mycaulong"]
