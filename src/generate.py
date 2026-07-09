from rate_limiter import wait_for_rate_limit
import time
from google.genai.errors import ClientError
from retriever import load_chunks, build_chroma_index
import os
from dotenv import load_dotenv
import google.genai as genai

load_dotenv()

client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))
MODEL_NAME = "gemini-2.5-flash"

def build_prompt(query, retrieved_chunks):
    context_text = "\n\n---\n\n".join(
        f"[Source: {chunk['source']}]\n{chunk['text']}"
        for chunk in retrieved_chunks
    )

    prompt = f"""You are an ADHD psychoeducation assistant. Answer the question using ONLY the information in the CONTEXT below. 

Rules:
- If the context does not contain enough information to answer, say "I don't have enough information to answer that confidently."
- Do not use any outside knowledge beyond what's in the context.
- Be clear, concise, and avoid clinical jargon.
- This is general information, not a diagnosis or medical advice — do not tell the user they do or don't have ADHD.

CONTEXT:
{context_text}

QUESTION:
{query}

ANSWER:"""
    return prompt

def generate_answer(query, retrieved_chunks, max_retries=5):
    prompt = build_prompt(query, retrieved_chunks)

    for attempt in range(max_retries):
        try:
            wait_for_rate_limit()   # <-- added this line
            response = client.models.generate_content(
                model=MODEL_NAME,
                contents=prompt
            )
            return response.text
        except ClientError as e:
            if "429" in str(e) or "RESOURCE_EXHAUSTED" in str(e):
                wait_time = 25
                print(f"    Rate limited, waiting {wait_time}s (attempt {attempt+1}/{max_retries})...")
                time.sleep(wait_time)
            else:
                raise

    raise Exception("Max retries exceeded for generate_answer")
def retrieve_and_answer(query, collection, top_k=5):
    results = collection.query(query_texts=[query], n_results=top_k)

    retrieved_chunks = []
    for i, doc_text in enumerate(results["documents"][0]):
        source = results["metadatas"][0][i]["source"]
        retrieved_chunks.append({"source": source, "text": doc_text})

    answer = generate_answer(query, retrieved_chunks)
    return answer, retrieved_chunks
if __name__ == "__main__":
    chunks = load_chunks()
    collection = build_chroma_index(chunks)

    test_query = "What are common myths about ADHD?"
    answer, sources = retrieve_and_answer(test_query, collection)

    print("Question:", test_query)
    print("\nAnswer:", answer)
    print("\nSources used:")
    for s in sources:
        print(" -", s["source"])

