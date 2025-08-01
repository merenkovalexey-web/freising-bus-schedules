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

def fetch_schedule_entries():
    response = requests.get(PAGE_URL, headers=HEADERS)
    soup = BeautifulSoup(response.content, "html.parser")

    result = {}
    current_category = None

    for element in soup.find_all(["h3", "ul"]):
        if element.name == "h3":
            heading_text = element.get_text(strip=True)
            if heading_text in ICONS:
                current_category = heading_text
        elif element.name == "ul" and current_category:
            for li in element.find_all("li"):
                a_tag = li.find("a", href=True)
                if a_tag and a_tag["href"].endswith(".pdf"):
                    title = a_tag.get_text(strip=True)
                    href = a_tag["href"]
                    full_url = href if href.startswith("http") else BASE_URL + href
                    result.setdefault(current_category, []).append((title, full_url))
    return result

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
    data = fetch_schedule_entries()
    write_schedule_file(data)
    print("✅ Готово: файл freising-bus-schedules.txt обновлён.")
