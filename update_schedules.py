import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from datetime import datetime

# URL-адреса
BASE_URL = "https://www.freisinger-stadtwerke.de"
PAGE_URL = BASE_URL + "/de/Stadtbus-Parkhaeuser/Stadtbus/Fahrplaene-gueltig-ab-15.12.2024/"
TXT_FILE = "freising-bus-schedules.txt"

# Заголовок User-Agent (чтобы избежать блокировок)
HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

# Категории для сортировки маршрутов
CATEGORIES = {
    "Stadtbus": "🚍 Stadtbus",
    "Innenstadtbusse": "🚌 Innenstadtbusse",
    "Flughafenbus": "✈️ Flughafenbus",
    "RufTaxi": "🚕 RufTaxi",
    "ExpressBus": "🚄 ExpressBus",
    "Verstaerkerfahrten": "📚 Verstärkerbus"
}


# Получить список PDF-файлов с маршрутом
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


# Сохранить файл с расписанием
def save_schedule_file(schedule):
    with open(TXT_FILE, "w", encoding="utf-8") as f:
        f.write("🚌 Актуальные расписания Stadtbus Freising (с 15.12.2024)\n")
        f.write("Источник: официальный сайт Stadtwerke Freising\n")
        f.write(PAGE_URL + "\n\n")

        for category, entries in schedule.items():
            f.write(f"### {category}\n\n")
            for name, link in entries:
                f.write(f"📄 {name}:\n🔗 {link}\n\n")

        # ✅ Добавляем дату и время последнего обновления
        now = datetime.now().strftime("%d.%m.%Y %H:%M")
        f.write(f"🕓 Последнее обновление: {now}\n")


# Главный запуск
if __name__ == "__main__":
    schedule_data = fetch_pdf_links()
    save_schedule_file(schedule_data)
    print(f"✅ Обновлено: {len(schedule_data)} категорий маршрутов сохранено в {TXT_FILE}")
