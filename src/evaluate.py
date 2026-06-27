import json
import time
import os
from datetime import datetime

import pandas as pd

from llm import ask_llm
from report import generate_html_report


# -----------------------------
# Load Dataset
# -----------------------------
with open("dataset/golden_dataset.json", "r", encoding="utf-8") as f:
    dataset = json.load(f)

results = []
correct = 0

# -----------------------------
# Evaluate Questions
# -----------------------------
for item in dataset:

    question = item["question"]
    expected = item["expected"]

    start = time.time()

    actual = ask_llm(question)

    latency = round(time.time() - start, 2)

    is_correct = expected.lower() in actual.lower()

    if is_correct:
        correct += 1

    results.append(
        {
            "Question": question,
            "Expected": expected,
            "Actual": actual,
            "Correct": is_correct,
            "Latency": latency,
        }
    )

# -----------------------------
# Convert to DataFrame
# -----------------------------
df = pd.DataFrame(results)

# -----------------------------
# Metrics
# -----------------------------
accuracy = df["Correct"].mean() * 100

avg_latency = df["Latency"].mean()
max_latency = df["Latency"].max()
min_latency = df["Latency"].min()

total_questions = len(df)

correct_answers = int(df["Correct"].sum())
incorrect_answers = total_questions - correct_answers

# -----------------------------
# Hallucination Rate
# -----------------------------
hallucinations = 0

for _, row in df.iterrows():

    if row["Expected"].lower() not in row["Actual"].lower():
        hallucinations += 1

hallucination_rate = (hallucinations / total_questions) * 100

# -----------------------------
# Pass / Fail
# -----------------------------
pass_fail = "PASS ✅" if accuracy >= 95 else "FAIL ❌"

# -----------------------------
# Save Reports
# -----------------------------
os.makedirs("reports", exist_ok=True)

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

history_filename = f"reports/results_{timestamp}.csv"

# Save timestamped history
df.to_csv(history_filename, index=False)

# Save latest results
df.to_csv("reports/results.csv", index=False)

# -----------------------------
# Generate HTML Report
# -----------------------------
generate_html_report(
    df=df,
    accuracy=accuracy,
    hallucination_rate=hallucination_rate,
    avg_latency=avg_latency,
    min_latency=min_latency,
    max_latency=max_latency,
    pass_fail=pass_fail,
)

# -----------------------------
# Print Summary
# -----------------------------
print("\n" + "=" * 55)
print("           LLM Evaluation Summary")
print("=" * 55)

print(f"Total Questions      : {total_questions}")
print(f"Correct Answers      : {correct_answers}")
print(f"Incorrect Answers    : {incorrect_answers}")

print("-" * 55)

print(f"Accuracy             : {accuracy:.2f}%")
print(f"Hallucination Rate   : {hallucination_rate:.2f}%")

print("-" * 55)

print(f"Average Latency      : {avg_latency:.2f} sec")
print(f"Fastest Response     : {min_latency:.2f} sec")
print(f"Slowest Response     : {max_latency:.2f} sec")

print("-" * 55)

print(f"Overall Status       : {pass_fail}")

print("=" * 55)

print(f"\n✅ Latest CSV Report   : reports/results.csv")
print(f"✅ History CSV Report  : {history_filename}")
print("✅ HTML Report         : reports/report.html")