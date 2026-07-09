from rate_limiter import wait_for_rate_limit
import time
from google.genai.errors import ClientError
import os
import re
from dotenv import load_dotenv
import google.genai as genai

load_dotenv()

client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))
MODEL_NAME = "gemini-2.5-flash"

def split_into_claims(answer_text):
    # Split on sentence-ending punctuation, keep it simple
    sentences = re.split(r'(?<=[.!?])\s+', answer_text.strip())
    # Filter out empty or very short fragments (like bullet symbols alone)
    claims = [s.strip() for s in sentences if len(s.strip()) > 10]
    return claims

import json

def verify_answer(answer_text, context_chunks, max_retries=5):
    claims = split_into_claims(answer_text)
    context_text = "\n\n".join(chunk["text"] for chunk in context_chunks)

    claims_list = "\n".join(f"{i+1}. {c}" for i, c in enumerate(claims))

    prompt = f"""You are a fact-checking assistant. Given the CONTEXT and a list of CLAIMS, determine if each claim is supported by the context.

Respond with ONLY a JSON array, one entry per claim, in this exact format:
[{{"claim_number": 1, "verdict": "SUPPORTED"}}, {{"claim_number": 2, "verdict": "UNSUPPORTED"}}]

Verdict must be one of: SUPPORTED, UNSUPPORTED, PARTIAL.

CONTEXT:
{context_text}

CLAIMS:
{claims_list}

JSON RESPONSE:"""

    for attempt in range(max_retries):
        try:
            wait_for_rate_limit()
            response = client.models.generate_content(
                model=MODEL_NAME,
                contents=prompt
            )
            raw_text = response.text.strip()
            # Strip markdown code fences if present
            raw_text = raw_text.replace("```json", "").replace("```", "").strip()
            verdicts = json.loads(raw_text)
            break
        except ClientError as e:
            if "429" in str(e) or "RESOURCE_EXHAUSTED" in str(e):
                wait_time = 30
                print(f"    Rate limited, waiting {wait_time}s (attempt {attempt+1}/{max_retries})...")
                time.sleep(wait_time)
            else:
                raise
    else:
        raise Exception("Max retries exceeded for verify_answer")

    flagged = []
    annotated = answer_text
    for v in verdicts:
        idx = v["claim_number"] - 1
        if idx < len(claims) and v["verdict"] != "SUPPORTED":
            claim_text = claims[idx]
            flagged.append({"claim": claim_text, "verdict": v["verdict"]})
            annotated = annotated.replace(claim_text, claim_text + f" [⚠️ {v['verdict']}]")

    return {
        "original_answer": answer_text,
        "annotated_answer": annotated,
        "total_claims": len(claims),
        "flagged_claims": flagged,
        "hallucination_rate": len(flagged) / len(claims) if claims else 0
    }

if __name__ == "__main__":
    test_context = [
        {"source": "test.txt", "text": "ADHD is a neurodevelopmental disorder involving inattention, hyperactivity, and impulsivity. It is not caused by bad parenting."}
    ]
    test_answer = "ADHD is caused by bad parenting. It involves inattention and hyperactivity. ADHD is more common in left-handed people."

    result = verify_answer(test_answer, test_context)

    print("Original answer:", result["original_answer"])
    print("\nAnnotated answer:", result["annotated_answer"])
    print("\nHallucination rate:", result["hallucination_rate"])
    print("\nFlagged claims:")
    for f in result["flagged_claims"]:
        print(f" - [{f['verdict']}] {f['claim']}")