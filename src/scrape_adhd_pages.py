import requests

def fetch_pmc_fulltext(pmcid):
    # pmcid example: "PMC4585002"
    url = f"https://www.ebi.ac.uk/europepmc/webservices/rest/{pmcid}/fullTextXML"
    r = requests.get(url, timeout=20)
    return r.text

pmc_ids = {
    "adhd_epigenetics_review": "PMC4585002",
    "adhd_global_burden_disease": "PMC11983595",
}

for name, pmcid in pmc_ids.items():
    try:
        xml_text = fetch_pmc_fulltext(pmcid)
        with open(f"data/raw/{name}.xml", "w", encoding="utf-8") as f:
            f.write(xml_text)
        print(f"Saved {name}.xml ({len(xml_text)} chars)")
    except Exception as e:
        print(f"FAILED {name}: {e}")