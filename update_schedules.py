import requests
from bs4 import BeautifulSoup

BASE_URL = "https://www.freisinger-stadtwerke.de"
PAGE_URL = BASE_URL + "/de/Stadtbus-Parkhaeuser/Stadtbus/Fahrplaene-gueltig-ab-15.12.2024/"
TXT_FILE = "freising-bus-schedules.txt"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

def fetch_links():
    response = requests.get(PAGE_URL, headers=HEADERS)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    
    result = []

    for a in soup.find_all("a", href=True):
        href = a["href"]
        text = a.get_text(strip=True)

        if href.endswith(".pdf") and text.lower().startswith("bus"):
            full_url = href if href.startswith("http") else BASE_URL + href
            result.append((text, full_url))

    return result

def save_schedule_file(entries):
    with open(TXT_FILE, "w", encoding="utf-8") as f:
        f.write("🚌 Актуальные расписания Stadtbus Freising (с 15.12.2024)\n")
        f.write("Источник: официальный сайт Stadtwerke Freising\n")
        f.write(PAGE_URL + "\n\n")
        f.write("### 🚍 Stadtbus\n\n")
        for name, link in entries:
            f.write(f"📄 {name}\n")
            f.write(f"🔗 {link}\n\n")

if __name__ == "__main__":
    data = fetch_links()
    save_schedule_file(data)
    print(f"✅ Сохранено {len(data)} маршрутов в {TXT_FILE}")
