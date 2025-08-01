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

    categorized = {
        "Stadtbus": [],
        "RufTaxi": [],
        "Express": [],
        "Schulbus": [],
        "Sonstiges": []
    }

    for a in soup.find_all("a", href=True):
        href = a["href"]
        text = a.get_text(strip=True)

        if not href.endswith(".pdf"):
            continue

        full_url = href if href.startswith("http") else BASE_URL + href

        # Категоризация по ключевым словам
        if "ruftaxi" in text.lower():
            categorized["RufTaxi"].append((text, full_url))
        elif "express" in text.lower():
            categorized["Express"].append((text, full_url))
        elif "schulbus" in text.lower() or "schule" in text.lower():
            categorized["Schulbus"].append((text, full_url))
        elif "bus" in text.lower():
            categorized["Stadtbus"].append((text, full_url))
        else:
            categorized["Sonstiges"].append((text, full_url))

    return categorized

def save_schedule_file(data):
    with open(TXT_FILE, "w", encoding="utf-8") as f:
        f.write("🚌 Актуальные расписания Stadtbus Freising (с 15.12.2024)\n")
        f.write("Источник: официальный сайт Stadtwerke Freising\n")
        f.write(PAGE_URL + "\n\n")

        for section, entries in data.items():
            icon = {
                "Stadtbus": "🚍",
                "RufTaxi": "🚖",
                "Express": "🚅",
                "Schulbus": "🚸",
                "Sonstiges": "📦"
            }.get(section, "📁")

            f.write(f"### {icon} {section}\n\n")
            for name, url in entries:
                f.write(f"📄 {name}\n")
                f.write(f"🔗 {url}\n\n")

if __name__ == "__main__":
    links_by_category = fetch_links()
    save_schedule_file(links_by_category)
    total = sum(len(v) for v in links_by_category.values())
    print(f"✅ Сохранено {total} ссылок в {TXT_FILE}")
