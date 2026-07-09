import os
os.environ["ANONYMIZED_TELEMETRY"] = "False"
import json
import chromadb
from chromadb.utils import embedding_functions
from rank_bm25 import BM25Okapi

from chromadb.config import Settings



CHUNKS_PATH = "data/processed/chunks.json"
CHROMA_DB_PATH = "data/processed/chroma_db"

client = chromadb.PersistentClient(
    path=CHROMA_DB_PATH,
    settings=Settings(anonymized_telemetry=False)
)

def load_chunks():
    with open(CHUNKS_PATH, "r", encoding="utf-8") as f:
        return json.load(f)
    

def build_chroma_index(chunks):
    client = chromadb.PersistentClient(path=CHROMA_DB_PATH)

    embedding_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
        model_name="all-MiniLM-L6-v2"
    )

    # Delete old collection if it exists, so re-running doesn't duplicate
    try:
        client.delete_collection("adhd_chunks")
    except Exception:
        pass

    collection = client.create_collection(
        name="adhd_chunks",
        embedding_function=embedding_fn
    )

    ids = [c["id"] for c in chunks]
    documents = [c["text"] for c in chunks]
    metadatas = [{"source": c["source"]} for c in chunks]

    collection.add(ids=ids, documents=documents, metadatas=metadatas)
    print(f"Chroma index built with {len(chunks)} chunks")
    return collection

def build_bm25_index(chunks):
    tokenized_corpus = [c["text"].lower().split() for c in chunks]
    bm25 = BM25Okapi(tokenized_corpus)
    print(f"BM25 index built with {len(chunks)} chunks")
    return bm25

# if __name__ == "__main__":
#     chunks = load_chunks()
#     print(f"Loaded {len(chunks)} chunks")

#     chroma_collection = build_chroma_index(chunks)
#     bm25_index = build_bm25_index(chunks)

#     print("\nBoth indexes built successfully.")

if __name__ == "__main__":
    chunks = load_chunks()
    print(f"Loaded {len(chunks)} chunks")

    chroma_collection = build_chroma_index(chunks)
    bm25_index = build_bm25_index(chunks)

    print("\nBoth indexes built successfully.")

    # --- Quick test query ---
    test_query = "What are common myths about ADHD?"
    results = chroma_collection.query(query_texts=[test_query], n_results=3)

    print(f"\nTest query: '{test_query}'")
    print("Top 3 results:\n")
    for i, doc in enumerate(results["documents"][0]):
        source = results["metadatas"][0][i]["source"]
        print(f"{i+1}. [{source}]")
        print(f"   {doc[:200]}...\n")