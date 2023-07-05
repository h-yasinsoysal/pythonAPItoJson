import datetime
import time
import requests
import pandas as pd
import json
import os

def get_raw_json_from_api(url):
    headers = {
        'Host': 'dummyjson.com', # API Alan Adı Adresi
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/113.0',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'tr-TR,tr;q=0.8,en-US;q=0.5,en;q=0.3',
        'Accept-Encoding': 'gzip, deflate, br',
        'X-Bone-Limit': '1000',  # API listeleme limitine göre ayarla
        'X-Bone-PageIndex': '1',
        'x-bone-sortBy': 'undefined',
        'x-bone-sortDirection': 'undefined',
        'Origin': 'https://dummyjson.com', # API Alan Adı Adresi
        'Connection': 'keep-alive',
        'Referer': 'https://dummyjson.com', # API Alan Adı Adresi
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-site'
    }

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        raw_json = response.content.decode('utf-8')
        return raw_json
    else:
        print("API'den veri alınamadı. Hata kodu:", response.status_code)
        return None

def export_raw_json_to_file(raw_json_data, file_name):
    file_path = os.path.join(json_folder, file_name)
    with open(file_path, 'w') as file:
        file.write(raw_json_data)
        print("Raw JSON verisi '{}' dosyasına kaydedildi.".format(file_name))

# JSON dosyalarının CSV'ye dönüştürme fonksiyonu
def convert_jsons_to_csv(json_folder, csv_folder):
    # JSON dosyalarının bulunduğu klasörü tarayın
    for filename in os.listdir(json_folder):
        if filename.endswith('.json'):
            json_file = os.path.join(json_folder, filename)

            # CSV dosyasının adını oluştur
            csv_filename = os.path.splitext(filename)[0] + '.csv'
            csv_file = os.path.join(csv_folder, csv_filename)

            # JSON dosyasını CSV'ye dönüştür
            convert_json_to_csv(json_file, csv_file)

# JSON formatının okunma işlemi
def convert_json_to_csv(json_file, csv_file):
    # JSON dosyasını oku
    with open(json_file, 'r') as file:
        json_data = json.load(file)

    # JSON verisini veri çerçevesine dönüştür
    dataframe = pd.json_normalize(json_data)

    # CSV dosyasına yaz
    dataframe.to_csv(csv_file, index=False)
    print(f"{json_file} başarıyla CSV'ye dönüştürüldü.")

def run_code_between_hours(start_hour, end_hour):
    while True:
        current_hour = datetime.datetime.now().time().hour

        if start_hour <= current_hour < end_hour:
            for url in api_urls:
                raw_json = get_raw_json_from_api(url)
                if raw_json is not None:
                    file_name = url.split('/')[-1] + '.json'  # API URL'sindeki son operatör işaretçisine göre değiştirin. Örn: "/products/1" veya /products/page=1

                    export_raw_json_to_file(raw_json, file_name)

            convert_jsons_to_csv(json_folder, csv_folder)

# 2 Saatte bir veri tazelemesi
        time.sleep(7200)

# Saat aralığını belirleyin (örneğin, 9:00'dan 17:00'ye kadar)
start_hour = 8
end_hour = 21

# API Endpoint bağlantısını veya bağlantılarını yazınız
api_urls = [
    "https://dummyjson.com/products/1"
]

# JSON ve CSV dosyalarının kaydedileceği klasörleri belirleyin
json_folder = 'json_files'
csv_folder = 'csv_files'

# Klasörleri oluşturun (dosya varsa siler)
os.makedirs(json_folder, exist_ok=True)
os.makedirs(csv_folder, exist_ok=True)

# Kodu belirli saatler arasında çalıştırın
run_code_between_hours(start_hour, end_hour)