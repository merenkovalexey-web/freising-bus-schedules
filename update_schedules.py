import requests
from bs4 import BeautifulSoup
import re

BASE_URL = "https://www.freisinger-stadtwerke.de"
PAGE_URL = BASE_URL + "/de/Stadtbus-Parkhaeuser/Stadtbus/Fahrplaene-gueltig-ab-15.12.2024/"
TXT_FILE = "freising-bus-schedules.txt"

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

CATEGORY_ICONS = {
    "Stadtbus": "🚍",
    "Innenstadtbusse": "🚌",
    "Flughafenbus": "✈️",
    "RufTaxi": "🚖",
    "ExpressBus": "🚅",
    "Verstärkerbus": "🚌",
}

def fetch_schedule_entries():
    response = requests.get(PAGE_URL, headers=HEADERS)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")

    schedule = {}
    current_category = None

    for tag in soup.find_all(["h3", "a"]):
        if tag.name == "h3":
            category = tag.get_text(strip=True)
            if category in CATEGORY_ICONS:
                current_category = category
                schedule[current_category] = []
        elif tag.name == "a" and current_category:
            href = tag.get("href")
            if href and href.endswith(".pdf") and "Fahrplaene" in href:
                full_url = href if href.startswith("http") else BASE_URL + href
                title = tag.get_text(strip=True)
                schedule[current_category].append((title, full_url))

    if not schedule:
        raise ValueError("❌ Таблица с расписаниями не найдена")

    return schedule


def save_schedule_file(schedule_data):
    with open(TXT_FILE, "w", encoding="utf-8") as f:
        f.write("🚌 Актуальные расписания Stadtbus Freising (с 15.12.2024)\n")
        f.write("Источник: официальный сайт Stadtwerke Freising\n")
        f.write(f"{PAGE_URL}\n\n")

        for category, entries in schedule_data.items():
            icon = CATEGORY_ICONS.get(category, "")
            f.write(f"### {icon} {category}\n\n")
            for name, link in entries:
                f.write(f"📄 {name}\n")
                f.write(f"🔗 {link}\n\n")


if __name__ == "__main__":
    schedule_data = fetch_schedule_entries()
    save_schedule_file(schedule_data)
    print(f"✅ Успешно обновлено: {len(sum(schedule_data.values(), []))} маршрутов → {TXT_FILE}")
