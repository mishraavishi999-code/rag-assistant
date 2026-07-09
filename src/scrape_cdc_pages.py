import requests
from bs4 import BeautifulSoup

headers = {"User-Agent": "Mozilla/5.0 (research project; academic use)"}

pages = {
    "cdc_adhd_data_stats": "https://www.cdc.gov/adhd/data/index.html",
    "cdc_adhd_throughout_years": "https://www.cdc.gov/adhd/data/adhd-throughout-the-years.html",
    "cdc_adhd_state_prevalence": "https://www.cdc.gov/adhd/data/state-based-prevalence-of-adhd-diagnosis-and-treatment-2016-2019.html",
    "cdc_adhd_about": "https://www.cdc.gov/adhd/about/index.html",
    "cdc_adhd_symptoms": "https://www.cdc.gov/adhd/signs-symptoms/index.html",
    "cdc_adhd_diagnosis": "https://www.cdc.gov/adhd/diagnosis/index.html",
    "cdc_adhd_treatment": "https://www.cdc.gov/adhd/treatment/index.html",
}

for name, page_url in pages.items():
    r = requests.get(page_url, headers=headers)
    s = BeautifulSoup(r.text, "html.parser")
    main = s.find("main") or s.body
    text = main.get_text(separator="\n", strip=True)

    with open(f"data/raw/{name}.txt", "w", encoding="utf-8") as f:
        f.write(text)

    print(f"Saved {name} ({len(text)} characters)")