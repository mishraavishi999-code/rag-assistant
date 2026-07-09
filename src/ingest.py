import os
import re
import json

RAW_DIR = "data/raw"
PROCESSED_DIR = "data/processed"
CHUNK_SIZE = 400        # approx words per chunk
CHUNK_OVERLAP = 50      # words of overlap between chunks

def load_text_files(folder):
    """Load every .txt file in the folder into a dict {filename: text}"""
    docs = {}
    for filename in os.listdir(folder):
        if filename.endswith(".txt"):
            path = os.path.join(folder, filename)
            with open(path, "r", encoding="utf-8") as f:
                docs[filename] = f.read()
    return docs

def chunk_text(text, chunk_size=CHUNK_SIZE, overlap=CHUNK_OVERLAP):
    """Split text into overlapping word-based chunks"""
    words = text.split()
    chunks = []
    start = 0
    while start < len(words):
        end = start + chunk_size
        chunk_words = words[start:end]
        chunks.append(" ".join(chunk_words))
        start += (chunk_size - overlap)
    return chunks


def process_all_documents():
    docs = load_text_files(RAW_DIR)
    print(f"Loaded {len(docs)} documents from {RAW_DIR}")

    all_chunks = []   # will hold dicts: {id, source, text}
    chunk_id = 0

    for filename, text in docs.items():
        chunks = chunk_text(text)
        print(f"  {filename}: {len(chunks)} chunks")
        for chunk in chunks:
            all_chunks.append({
                "id": f"chunk_{chunk_id:04d}",
                "source": filename,
                "text": chunk
            })
            chunk_id += 1

    # Save all chunks as one JSON file
    output_path = os.path.join(PROCESSED_DIR, "chunks.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(all_chunks, f, indent=2)

    print(f"\nTotal chunks created: {len(all_chunks)}")
    print(f"Saved to: {output_path}")
    return all_chunks

if __name__ == "__main__":
    process_all_documents()

    