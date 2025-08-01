import requests
import re

BASE_URL = "https://www.freisinger-stadtwerke.de"
PAGE_URL = BASE_URL + "/de/Stadtbus-Parkhaeuser/Stadtbus/Fahrplaene-gueltig-ab-15.12.2024/"
TXT_FILE = "freising-bus-schedules.txt"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115 Safari/537.36"
}

def fetch_pdf_links():
    response = requests.get(PAGE_URL, headers=HEADERS)
    response.raise_for_status()
    matches = re.findall(r'href="([^"]+?(\d{3})-ab-15\.12\.2024\.pdf)"', response.text)
    links = []
    for href, bus_number in matches:
        full_url = href if href.startswith("http") else BASE_URL + href
        links.append((bus_number, full_url))
    return links

def save_schedule_file(links):
    with open(TXT_FILE, "w", encoding="utf-8") as f:
        f.write("🚌 Актуальные расписания Stadtbus Freising (с 15.12.2024)\n")
        f.write("Источник: официальный сайт Stadtwerke Freising\n")
        f.write(f"{PAGE_URL}\n\n")
        f.write("### 🚍 Stadtbus\n\n")

        for bus_number, url in sorted(links):
            f.write(f"📄 Bus {bus_number}\n")
            f.write(f"Маршрут: Автобусный маршрут №{bus_number} по городу Фрайзинг\n")
            f.write(f"🔗 {url}\n\n")

if __name__ == "__main__":
    print("🔄 Получаем ссылки...")
    bus_links = fetch_pdf_links()
    print(f"✅ Найдено {len(bus_links)} ссылок")
    save_schedule_file(bus_links)
    print(f"📁 Сохранено в файл: {TXT_FILE}")
