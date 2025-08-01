import requests
from bs4 import BeautifulSoup

URL = "https://www.freisinger-stadtwerke.de/de/Stadtbus-Parkhaeuser/Stadtbus/Fahrplaene-gueltig-ab-15.12.2024/"

def fetch_pdfs():
    res = requests.get(URL)
    res.raise_for_status()
    soup = BeautifulSoup(res.text, "html.parser")
    links = soup.find_all("a", href=True)

    output = []
    section = None

    for link in links:
        href = link["href"]
        if not href.endswith(".pdf"):
            continue
        label = link.get_text(strip=True)
        url = href if href.startswith("http") else "https://www.freisinger-stadtwerke.de" + href

        if "RufTaxi" in label:
            if section != "RufTaxi":
                output.append("\n### 🚕 RufTaxi\n")
                section = "RufTaxi"
        elif "X660" in label or "ExpressBus" in label:
            if section != "ExpressBus":
                output.append("\n### 🚀 ExpressBus\n")
                section = "ExpressBus"
        elif "Verstärker" in label:
            if section != "Verstärker":
                output.append("\n### 🚌 Verstärkerbus\n")
                section = "Verstärker"
        elif "650" in label or "651" in label:
            if section != "Innenstadtbusse":
                output.append("\n### 🏙 Innenstadtbusse\n")
                section = "Innenstadtbusse"
        elif "635" in label:
            if section != "Flughafenbus":
                output.append("\n### ✈️ Flughafenbus\n")
                section = "Flughafenbus"
        else:
            if section != "Stadtbus":
                output.append("\n### 🚍 Stadtbus\n")
                section = "Stadtbus"

        output.append(f"📄 {label}\n🔗 {url}\n")

    with open("freising-bus-schedules.txt", "w", encoding="utf-8") as f:
        f.write("### 🚌 Актуальные расписания Stadtbus Freising (с 15.12.2024)\n")
        f.write("Источник: https://www.freisinger-stadtwerke.de/de/Stadtbus-Parkhaeuser/Stadtbus/Fahrplaene-gueltig-ab-15.12.2024/\n\n")
        f.write("\n".join(output))

if __name__ == "__main__":
    fetch_pdfs()
