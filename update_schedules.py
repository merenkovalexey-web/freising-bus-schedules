import requests
from bs4 import BeautifulSoup
import os

# URL страницы с PDF
BASE_URL = "https://www.freisinger-stadtwerke.de"
TARGET_PAGE = f"{BASE_URL}/de/Stadtbus-Parkhaeuser/Stadtbus/Fahrplaene-gueltig-ab-15.12.2024/"

# Файл для сохранения ссылок
OUTPUT_FILE = "freising-bus-schedules.txt"

# Заголовок, чтобы притвориться обычным браузером
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115 Safari/537.36"
}

def fetch_pdfs():
    print("🔄 Загружаем страницу расписаний...")
    res = requests.get(TARGET_PAGE, headers=HEADERS)
    res.raise_for_status()

    soup = BeautifulSoup(res.text, "html.parser")
    pdf_links = []

    for link in soup.find_all("a", href=True):
        href = link["href"]
        if href.endswith(".pdf"):
            full_url = BASE_URL + href if href.startswith("/") else href
            pdf_links.append(full_url)

    return pdf_links

def save_to_file(links):
    print(f"💾 Сохраняем {len(links)} ссылок в файл '{OUTPUT_FILE}'...")
    with open(OUTPUT_FILE, "w") as f:
        for url in links:
            f.write(url + "\n")
    print("✅ Готово!")

def main():
    print("🚍 Обновление расписаний Stadtbus Freising...")
    links = fetch_pdfs()
    save_to_file(links)

if __name__ == "__main__":
    main()
