import requests
from bs4 import BeautifulSoup

headers = {"User-Agent": "Mozilla/5.0 (research project; academic use)"}

html_pages = {
    "nimh_adhd_overview": "https://www.nimh.nih.gov/health/topics/attention-deficit-hyperactivity-disorder-adhd",
    "nimh_adhd_what_to_know": "https://www.nimh.nih.gov/health/publications/attention-deficit-hyperactivity-disorder-what-you-need-to-know",
    "nimh_adhd_adults": "https://www.nimh.nih.gov/health/publications/adhd-what-you-need-to-know",
}

for name, page_url in html_pages.items():
    try:
        r = requests.get(page_url, headers=headers, timeout=15)
        s = BeautifulSoup(r.text, "html.parser")
        main = s.find("main") or s.find("article") or s.body
        text = main.get_text(separator="\n", strip=True)
        with open(f"data/raw/{name}.txt", "w", encoding="utf-8") as f:
            f.write(text)
        print(f"Saved {name} ({len(text)} chars)")
    except Exception as e:
        print(f"FAILED {name}: {e}")