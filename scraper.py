import requests
from bs4 import BeautifulSoup
import sqlite3
from datetime import datetime

# URL RSS Feed
RSS_URL = "https://www.antaranews.com/rss/terkini.xml"

def setup_database():
    conn = sqlite3.connect('news_database.db')
    cursor = conn.cursor()
    # Buat tabel jika belum ada
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS articles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            link TEXT,
            pub_date TEXT,
            scraped_at TEXT
        )
    ''')
    conn.commit()
    return conn

def scrape_rss_soup():
    conn = setup_database()
    cursor = conn.cursor()
    
    print(f"[*] Menghubungi RSS Feed: {RSS_URL}...")
    
    # Headers standar agar tidak diblokir
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    try:
        response = requests.get(RSS_URL, headers=headers, timeout=10)
        response.raise_for_status()
        
        # RAHASIA SUKSES: Gunakan 'xml' atau 'html.parser' dari BeautifulSoup
        # Ini akan menangani error "invalid token" secara otomatis
        soup = BeautifulSoup(response.content, 'xml')
        
        items = soup.find_all('item')
        print(f"[*] Ditemukan {len(items)} berita. Menyimpan ke SQL...")
        
        count = 0
        for item in items:
            # Gunakan try-except per item agar 1 data error tidak mematikan semua
            try:
                title = item.find('title').text.strip()
                link = item.find('link').text.strip()
                pub_date = item.find('pubDate').text.strip()
                scraped_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                
                # Cek duplikasi
                cursor.execute("SELECT id FROM articles WHERE link = ?", (link,))
                if cursor.fetchone() is None:
                    cursor.execute('''
                        INSERT INTO articles (title, link, pub_date, scraped_at)
                        VALUES (?, ?, ?, ?)
                    ''', (title, link, pub_date, scraped_at))
                    count += 1
            except Exception as e:
                continue # Skip item yang rusak
        
        conn.commit()
        print(f"[+] SUKSES BESAR! {count} berita baru berhasil disimpan ke database.")

    except Exception as e:
        print(f"[!] Error Global: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    scrape_rss_soup()
