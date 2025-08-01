import requests
import re
from urllib.parse import urljoin

BASE_URL = "https://www.freisinger-stadtwerke.de"
PAGE_URL = BASE_URL + "/de/Stadtbus-Parkhaeuser/Stadtbus/Fahrplaene-gueltig-ab-15.12.2024/"
TXT_FILE = "freising-bus-schedules.txt"

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

def fetch_pdf_links():
    response = requests.get(PAGE_URL, headers=HEADERS)
    response.raise_for_status()

    matches = re.findall(r'href="([^"]+?(\d{3,4}.*?)\.pdf)"', response.text)
    links = []

    for href, filename in matches:
        full_url = href if href.startswith("http") else urljoin(BASE_URL, href)
        links.append((filename, full_url))

    return links

def save_schedule_file(links):
    with open(TXT_FILE, "w", encoding="utf-8") as f:
        f.write("🚌 Актуальные расписания Stadtbus Freising (с 15.12.2024)\n")
        f.write("Источник: официальный сайт Stadtwerke Freising\n\n")
        f.write("### 🚍 Stadtbus\n\n")

        for filename, url in sorted(links):
            f.write(f"📄 {filename.replace('-', ' ')}\n")
            f.write(f"Маршрут: {filename}.pdf\n")
            f.write(f"🔗 {url}\n\n")

if __name__ == "__main__":
    pdf_links = fetch_pdf_links()
    save_schedule_file(pdf_links)
    print(f"✅ Сохранено {len(pdf_links)} маршрутов в {TXT_FILE}")
