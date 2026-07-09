import requests
from bs4 import BeautifulSoup

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"
}

archive_pages = {
    "chadd_myths_misunderstandings": "https://web.archive.org/web/2024/https://chadd.org/about-adhd/myths-and-misunderstandings/",
    "chadd_ten_myths": "https://web.archive.org/web/2024/https://chadd.org/attention-article/ten-myths-about-adhd-and-why-they-are-wrong/",
    "chadd_myths_early_deaths": "https://web.archive.org/web/2024/https://chadd.org/attention-article/myths-about-adhd-can-cause-our-early-deaths/",
}

for name, page_url in archive_pages.items():
    try:
        r = requests.get(page_url, headers=headers, timeout=20)
        s = BeautifulSoup(r.text, "html.parser")
        main = s.find("main") or s.find("article") or s.body
        text = main.get_text(separator="\n", strip=True)
        with open(f"data/raw/{name}.txt", "w", encoding="utf-8") as f:
            f.write(text)
        print(f"Saved {name} ({len(text)} chars)")
    except Exception as e:
        print(f"FAILED {name}: {e}")