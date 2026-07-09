import re

def strip_xml_to_text(xml_string):
    text = re.sub(r"<[^>]+>", " ", xml_string)
    text = re.sub(r"\s+", " ", text).strip()
    return text

pmc_ids = {
    "adhd_epigenetics_review": "PMC4585002",
    "adhd_global_burden_disease": "PMC11983595",
}

for name in pmc_ids:
    with open(f"data/raw/{name}.xml", "r", encoding="utf-8") as f:
        xml_text = f.read()
    plain_text = strip_xml_to_text(xml_text)
    with open(f"data/raw/{name}.txt", "w", encoding="utf-8") as f:
        f.write(plain_text)
    print(f"Converted {name}.txt ({len(plain_text)} chars)")