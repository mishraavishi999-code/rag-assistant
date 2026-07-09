import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))

import csv
import json
import time
from retriever import load_chunks, build_chroma_index
from generate import generate_answer, retrieve_and_answer
from verify import verify_answer

RESULTS_PATH = "eval/results/eval_results.json"

def load_test_questions(path="eval/test_questions.csv"):
    questions = []
    with open(path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            questions.append(row)
    return questions

def load_existing_results():
    if os.path.exists(RESULTS_PATH):
        with open(RESULTS_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def save_results(results):
    os.makedirs("eval/results", exist_ok=True)
    with open(RESULTS_PATH, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)

def run_evaluation():
    print("Loading chunks and building index...")
    chunks = load_chunks()
    collection = build_chroma_index(chunks)

    questions = load_test_questions()
    results = load_existing_results()
    done_ids = {r["id"] for r in results}

    for q in questions:
        if q["id"] in done_ids:
            print(f"Skipping Q{q['id']} (already done)")
            continue

        print(f"\nProcessing Q{q['id']}: {q['question']}")

        try:
            naive_answer, retrieved_chunks = retrieve_and_answer(q["question"], collection)
            verification = verify_answer(naive_answer, retrieved_chunks)

            result = {
                "id": q["id"],
                "question": q["question"],
                "category": q["category"],
                "expected_behavior": q["expected_behavior"],
                "naive_answer": naive_answer,
                "verified_answer": verification["annotated_answer"],
                "total_claims": verification["total_claims"],
                "flagged_claims": len(verification["flagged_claims"]),
                "hallucination_rate": verification["hallucination_rate"],
                "sources_used": list(set(c["source"] for c in retrieved_chunks))
            }
            results.append(result)
            save_results(results)   # save immediately after each question
            print(f"  Saved. ({len(results)}/{len(questions)} done)")

        except Exception as e:
            print(f"  FAILED on Q{q['id']}: {e}")
            print("  Progress saved so far. Re-run the script later to resume.")
            save_results(results)
            raise  # stop here, but everything up to now is saved

    print(f"\n\nAll done. Results saved to {RESULTS_PATH}")
    return results

def print_summary(results):
    total = len(results)
    if total == 0:
        print("No results yet.")
        return
    avg_hallucination_rate = sum(r["hallucination_rate"] for r in results) / total

    print("\n" + "="*50)
    print("EVALUATION SUMMARY")
    print("="*50)
    print(f"Total questions evaluated: {total}")
    print(f"Average hallucination rate: {avg_hallucination_rate:.2%}")

    print("\nBy category:")
    categories = set(r["category"] for r in results)
    for cat in categories:
        cat_results = [r for r in results if r["category"] == cat]
        avg_rate = sum(r["hallucination_rate"] for r in cat_results) / len(cat_results)
        print(f"  {cat}: {len(cat_results)} questions, avg hallucination rate: {avg_rate:.2%}")

if __name__ == "__main__":
    results = run_evaluation()
    print_summary(results)