import json
import time
import os
from datetime import datetime

import pandas as pd

from llm import ask_llm
from report import generate_html_report

# ======================================================
# DATASETS
# ======================================================

DATASETS = [
    "dataset/general.json",
    "dataset/math.json",
    "dataset/coding.json",
    "dataset/reasoning.json",
    "dataset/redteam.json",
]

results = []

# ======================================================
# EVALUATE ALL DATASETS
# ======================================================

for dataset_path in DATASETS:

    dataset_name = os.path.basename(dataset_path).replace(".json", "").upper()

    print("\n" + "=" * 70)
    print(f"STARTING DATASET : {dataset_name}")
    print("=" * 70)

    # -------------------------
    # Load Dataset
    # -------------------------
    try:
        with open(dataset_path, "r", encoding="utf-8-sig") as f:
            dataset = json.load(f)

    except FileNotFoundError:
        print(f"❌ File not found: {dataset_path}")
        continue

    except json.JSONDecodeError as e:
        print(f"❌ Invalid JSON in {dataset_path}")
        print(e)
        continue

    # -------------------------
    # Evaluate Questions
    # -------------------------
    for i, item in enumerate(dataset, start=1):

        # Support both dataset formats
        if "question" in item:
            question = item["question"]
            expected = item["expected"]
        else:
            question = item["prompt"]
            expected = item["expected_behavior"]

        print(f"[{dataset_name}] {i}/{len(dataset)}")

        start = time.time()

        try:
            actual = ask_llm(question)
        except Exception as e:
            print("❌", e)
            actual = ""

        latency = round(time.time() - start, 2)

        is_correct = expected.lower() in actual.lower()

        print(
            f"Question : {question}\n"
            f"Latency  : {latency:.2f} sec\n"
            f"Result   : {'✅ Correct' if is_correct else '❌ Incorrect'}"
        )

        print("-" * 70)

        results.append(
            {
                "Dataset": dataset_name,
                "Question": question,
                "Expected": expected,
                "Actual": actual,
                "Correct": is_correct,
                "Latency": latency,
            }
        )

# ======================================================
# DATAFRAME
# ======================================================

if len(results) == 0:
    print("❌ No evaluation results generated.")
    exit()

df = pd.DataFrame(results)

# ======================================================
# METRICS
# ======================================================

accuracy = df["Correct"].mean() * 100

avg_latency = df["Latency"].mean()
min_latency = df["Latency"].min()
max_latency = df["Latency"].max()

total_questions = len(df)

correct_answers = int(df["Correct"].sum())
incorrect_answers = total_questions - correct_answers

hallucinations = (
    df.apply(
        lambda x: x["Expected"].lower() not in x["Actual"].lower(),
        axis=1,
    )
).sum()

hallucination_rate = hallucinations / total_questions * 100

pass_fail = "PASS ✅" if accuracy >= 95 else "FAIL ❌"

# ======================================================
# SAVE REPORTS
# ======================================================

os.makedirs("reports", exist_ok=True)

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

history_file = f"reports/results_{timestamp}.csv"

df.to_csv(history_file, index=False)
df.to_csv("reports/results.csv", index=False)

# ======================================================
# HTML REPORT
# ======================================================

generate_html_report(
    df=df,
    accuracy=accuracy,
    hallucination_rate=hallucination_rate,
    avg_latency=avg_latency,
    min_latency=min_latency,
    max_latency=max_latency,
    pass_fail=pass_fail,
)

# ======================================================
# SUMMARY
# ======================================================

print("\n")
print("=" * 70)
print("LLM EVALUATION SUMMARY")
print("=" * 70)

print(f"Datasets Evaluated : {len(DATASETS)}")
print(f"Total Questions    : {total_questions}")
print(f"Correct Answers    : {correct_answers}")
print(f"Incorrect Answers  : {incorrect_answers}")

print("-" * 70)

print(f"Accuracy           : {accuracy:.2f}%")
print(f"Hallucination Rate : {hallucination_rate:.2f}%")

print("-" * 70)

print(f"Average Latency    : {avg_latency:.2f} sec")
print(f"Fastest Response   : {min_latency:.2f} sec")
print(f"Slowest Response   : {max_latency:.2f} sec")

print("-" * 70)

print(f"Overall Status     : {pass_fail}")

print("=" * 70)

print("\nReports Generated Successfully")
print(f"Latest CSV : reports/results.csv")
print(f"History    : {history_file}")
print("HTML       : reports/report.html")