import pdfplumber
import requests

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"
}

pdf_url = "https://web.archive.org/web/20250216004614/https://d393uh8gb46l22.cloudfront.net/wp-content/uploads/2018/06/ATTN_06_13_BROWN_ADHD_MYTHS.pdf"

r = requests.get(pdf_url, headers=headers, timeout=20)
with open("data/raw/chadd_ten_myths.pdf", "wb") as f:
    f.write(r.content)

with pdfplumber.open("data/raw/chadd_ten_myths.pdf") as pdf:
    text = "\n".join(page.extract_text() or "" for page in pdf.pages)

with open("data/raw/chadd_ten_myths.txt", "w", encoding="utf-8") as f:
    f.write(text)

print(f"Saved chadd_ten_myths.txt ({len(text)} chars)")