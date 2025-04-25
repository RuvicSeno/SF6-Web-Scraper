import requests
from bs4 import BeautifulSoup
import re

def scrape_street_fighter_6():
    url = "https://streetfighter.fandom.com/wiki/Street_Fighter_6"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print("Failed to retrieve the webpage.")
        return

    soup = BeautifulSoup(response.text, "html.parser")

    title_tag = soup.find("h1", class_="page-header__title")
    title = title_tag.text.strip() if title_tag else "N/A"

    infobox = soup.find("aside", class_="portable-infobox")
    details = {}

    if infobox:
        for row in infobox.find_all("div", class_="pi-item"):
            label = row.find("h3", class_="pi-data-label")
            value = row.find("div", class_="pi-data-value")

            if label and value:
                key = label.text.strip()
                val = value.get_text(separator=", ").strip()
                details[key] = val

    release_date = details.get("Release date", details.get("Release Date", "N/A"))
    if release_date != "N/A":
        release_date = " ".join(release_date.split())
        date_match = re.search(r"\b\w+ \d{1,2}, \d{4}\b", release_date)
        release_date = date_match.group(0) if date_match else "N/A"

    keyFeatures_section = soup.find("span", id="Gameplay")
    keyFeatures_text = "N/A"

    if keyFeatures_section:
        paragraph = keyFeatures_section.find_next("p")
        if paragraph:
            keyFeatures_text = paragraph.text.strip()

    platforms = details.get("Platform(s)", "N/A")
    if platforms != "N/A":
        platforms = " ".join(platforms.split())

    data = {
        "Title": title,
        "Release Date": release_date,
        "Developers": details.get("Developer(s)", "N/A"),
        "Publishers": details.get("Publisher(s)", "N/A"),
        "Platforms": platforms,
        "KeyFeatures": keyFeatures_text,
    }

    return data

if __name__ == "__main__":
    scraped_data = scrape_street_fighter_6()
    if scraped_data:
        for key, value in scraped_data.items():
            print(f"{key}: {value}")
