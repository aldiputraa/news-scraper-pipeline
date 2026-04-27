import requests
from bs4 import BeautifulSoup
import sqlite3 # Import library SQL
from datetime import datetime

def setup_database():
    # Menghubungkan ke database (akan otomatis membuat file jika belum ada)
    conn = sqlite3.connect('news_database.db')
    cursor = conn.cursor()
    # Membuat tabel jika belum ada
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS articles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            category TEXT,
            link TEXT,
            scraped_at TEXT
        )
    ''')
    conn.commit()
    return conn

def scrape_to_sql():
    conn = setup_database()
    cursor = conn.cursor()
    
    url = "https://antaranews.com"
    headers = {'User-Agent': 'Mozilla/5.0'}

    try:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        articles = soup.find_all('article', class_='simple-post')
        
        print(f"[*] Mengambil data dan menyimpan ke SQL...")

        for article in articles:
            title = article.find('h3').text.strip()
            link = article.find('a')['href']
            category = article.find('span', class_='genre').text.strip()
            scraped_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # Simpan data ke tabel SQL
            cursor.execute('''
                INSERT INTO articles (title, category, link, scraped_at)
                VALUES (?, ?, ?, ?)
            ''', (title, category, link, scraped_at))
        
        conn.commit()
        print(f"[+] Berhasil! Data tersimpan di news_database.db")

    except Exception as e:
        print(f"[!] Error: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    scrape_to_sql()
