import requests
from bs4 import BeautifulSoup

BASE_URL = "https://www.freisinger-stadtwerke.de"
PAGE_URL = BASE_URL + "/de/Stadtbus-Parkhaeuser/Stadtbus/Fahrplaene-gueltig-ab-15.12.2024/"
TXT_FILE = "freising-bus-schedules.txt"

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

ICONS = {
    "Stadtbus": "🚍",
    "Innenstadtbusse": "🚌",
    "Flughafenbus": "✈️",
    "RufTaxi": "🚖",
    "ExpressBus": "🚅",
    "Verstärkerbus": "🔁"
}

def fetch_links_by_category():
    response = requests.get(PAGE_URL, headers=HEADERS)
    response.raise_for_status()
    soup = BeautifulSoup(response.content, "html.parser")

    categories = {}
    current_category = None

    for element in soup.select("h3, li a"):
        if element.name == "h3":
            current_category = element.get_text(strip=True)
            if current_category not in categories:
                categories[current_category] = []
        elif element.name == "a" and element.get("href", "").endswith(".pdf") and current_category:
            title = element.get_text(strip=True)
            href = element["href"]
            full_url = href if href.startswith("http") else BASE_URL + href
            categories[current_category].append((title, full_url))

    return categories

def write_schedule_file(data):
    with open(TXT_FILE, "w", encoding="utf-8") as f:
        f.write("🚌 Актуальные расписания Stadtbus Freising (с 15.12.2024)\n")
        f.write("Источник: официальный сайт Stadtwerke Freising\n")
        f.write(PAGE_URL + "\n\n")

        for category, entries in data.items():
            icon = ICONS.get(category, "📁")
            f.write(f"### {icon} {category}\n\n")
            for title, url in entries:
                f.write(f"📄 {title}\n")
                f.write(f"🔗 {url}\n\n")

if __name__ == "__main__":
    links = fetch_links_by_category()
    write_schedule_file(links)
    print("✅ Готово: файл freising-bus-schedules.txt создан.")
