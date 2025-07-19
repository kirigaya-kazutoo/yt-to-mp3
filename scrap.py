from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time

# Mengonfigurasi opsi Chrome untuk mode headless (tanpa tampilan GUI)
chrome_options = Options()
chrome_options.add_argument("--headless")  # Menjalankan browser tanpa tampilan
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")

# Tentukan lokasi Chrome yang diinstal di SageMaker
chrome_options.binary_location = "/usr/bin/chromium-browser"

# Setup WebDriver menggunakan ChromeDriver yang sudah terinstal
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

# Akses halaman yang diinginkan
url = 'https://gis.bnpb.go.id/arcgis/apps/sites/?fromEdit=true#/public/pages/data-bencana'
driver.get(url)

# Tunggu beberapa detik agar halaman bisa sepenuhnya dimuat
time.sleep(5)

# Ambil tabel dari halaman setelah ter-render
tables = driver.find_elements(By.TAG_NAME, "table")

# Jika tabel ditemukan, ambil data dari tabel pertama
if tables:
    table = tables[0]
    rows = table.find_elements(By.TAG_NAME, "tr")
    
    # Ambil header tabel
    headers = [header.text for header in rows[0].find_elements(By.TAG_NAME, "th")]

    # Ambil data dari setiap baris
    data = []
    for row in rows[1:]:
        cols = row.find_elements(By.TAG_NAME, "td")
        data.append([col.text for col in cols])
    
    # Konversi data menjadi DataFrame
    df = pd.DataFrame(data, columns=headers)
    print(df.head())  # Tampilkan 5 baris pertama
else:
    print("Tidak ada tabel ditemukan di halaman.")

# Tutup browser setelah selesai
driver.quit()
