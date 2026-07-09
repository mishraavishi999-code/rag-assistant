import requests
from bs4 import BeautifulSoup

url = "https://www.cdc.gov/adhd/data/index.html"
headers = {"User-Agent": "Mozilla/5.0 (research project; academic use)"}
response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, "html.parser")

# CDC pages put the real content inside the main article area —
# grab the main content div and strip nav/footer junk
main_content = soup.find("main") or soup.find("article") or soup.body
text = main_content.get_text(separator="\n", strip=True)

with open("data/raw/cdc_adhd_data_stats.txt", "w", encoding="utf-8") as f:
    f.write(text)

print("Saved:", len(text), "characters")