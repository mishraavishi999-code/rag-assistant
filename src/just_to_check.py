import requests

urls_to_check = [
    "https://chadd.org/about-adhd/myths-and-misunderstandings/",
    "https://chadd.org/attention-article/ten-myths-about-adhd-and-why-they-are-wrong/",
    "https://chadd.org/attention-article/myths-about-adhd-can-cause-our-early-deaths/",
    "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4585002/",
    "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC11983595/",
    "https://applications.emro.who.int/docs/EMRPUB_leaflet_2019_mnh_214_en.pdf",
]

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"
}

for url in urls_to_check:
    try:
        r = requests.get(url, headers=headers, timeout=15)
        print(f"{url}\n  Status: {r.status_code} | Length: {len(r.text)}\n")
    except Exception as e:
        print(f"{url}\n  ERROR: {e}\n")