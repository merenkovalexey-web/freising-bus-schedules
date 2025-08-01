import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

BASE_URL = "https://www.freisinger-stadtwerke.de"
PAGE_URL = BASE_URL + "/de/Stadtbus-Parkhaeuser/Stadtbus/Fahrplaene-gueltig-ab-15.12.2024/"
TXT_FILE = "freising-bus-schedules.txt"

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

CATEGORIES = {
    "Stadtbus": "🚍 Stadtbus",
    "Innenstadtbusse": "🚌 Innenstadtbusse",
    "Flughafenbus": "✈️ Flughafenbus",
    "RufTaxi": "🚕 RufTaxi",
    "ExpressBus": "🚄 ExpressBus",
    "Verstaerkerfahrten": "📚 Verstärkerbus"
}


def fetch_pdf_links():
    response = requests.get(PAGE_URL, headers=HEADERS)
    soup = BeautifulSoup(response.text, "html.parser")
    schedule = {}

    for a in soup.find_all("a", href=True):
        href = a["href"]
        text = a.get_text(strip=True)

        if not href.endswith(".pdf"):
            continue

        full_url = urljoin(BASE_URL, href)

        # Определяем категорию
        category = next(
            (name for key, name in CATEGORIES.items() if key.lower() in href.lower()),
            "📁 Другое"
        )

        # Добавляем в список по категории
        schedule.setdefault(category, []).append((text, full_url))

    if not schedule:
        raise ValueError("❌ Таблица с расписаниями не найдена")

    return schedule


def save_schedule_file(schedule):
    with open(TXT_FILE, "w", encoding="utf-8") as f:
        f.write("🚌 Актуальные расписания Stadtbus Freising (с 15.12.2024)\n")
        f.write("Источник: официальный сайт Stadtwerke Freising\n")
        f.write(PAGE_URL + "\n\n")

        for category, entries in schedule.items():
            f.write(f"### {category}\n\n")
            for name, link in entries:
                f.write(f"📄 {name}:\n🔗 {link}\n\n")


if __name__ == "__main__":
    schedule_data = fetch_pdf_links()
    save_schedule_file(schedule_data)
    print(f"✅ Обновлено: {len(schedule_data)} категорий маршрутов сохранено в {TXT_FILE}")
