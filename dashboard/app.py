import streamlit as st
import pandas as pd

# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title="LLM Evaluation Dashboard",
    page_icon="📊",
    layout="wide"
)

# -----------------------------
# Load Results
# -----------------------------
df = pd.read_csv("reports/results.csv")

# -----------------------------
# Calculate Metrics
# -----------------------------
accuracy = df["Correct"].mean() * 100

total_questions = len(df)

correct_answers = int(df["Correct"].sum())

incorrect_answers = total_questions - correct_answers

avg_latency = df["Latency"].mean()

max_latency = df["Latency"].max()

min_latency = df["Latency"].min()

hallucinations = 0

for _, row in df.iterrows():

    if row["Expected"].lower() not in row["Actual"].lower():
        hallucinations += 1

hallucination_rate = hallucinations / total_questions * 100

status = "✅ PASS" if accuracy >= 95 else "❌ FAIL"

# -----------------------------
# Title
# -----------------------------
st.title("📊 LLM Evaluation Dashboard")

st.write("Evaluate the performance of a Large Language Model using a benchmark dataset.")

st.divider()

# -----------------------------
# Metric Cards
# -----------------------------
col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Accuracy",
    f"{accuracy:.2f}%"
)

col2.metric(
    "Questions",
    total_questions
)

col3.metric(
    "Correct",
    correct_answers
)

col4.metric(
    "Incorrect",
    incorrect_answers
)

st.divider()

col5, col6, col7, col8 = st.columns(4)

col5.metric(
    "Average Latency",
    f"{avg_latency:.2f} sec"
)

col6.metric(
    "Fastest Response",
    f"{min_latency:.2f} sec"
)

col7.metric(
    "Slowest Response",
    f"{max_latency:.2f} sec"
)

col8.metric(
    "Hallucination Rate",
    f"{hallucination_rate:.2f}%"
)

st.divider()

# -----------------------------
# Overall Status
# -----------------------------
st.subheader("Overall Evaluation")

if accuracy >= 95:
    st.success(status)
else:
    st.error(status)

st.divider()

# -----------------------------
# Latency Chart
# -----------------------------
st.subheader("📈 Latency per Question")

latency_df = df[["Question", "Latency"]].set_index("Question")

st.bar_chart(latency_df)

st.divider()

# -----------------------------
# Correct vs Incorrect Chart
# -----------------------------
st.subheader("📊 Correct vs Incorrect")

chart_df = pd.DataFrame(
    {
        "Count": [
            correct_answers,
            incorrect_answers
        ]
    },
    index=[
        "Correct",
        "Incorrect"
    ]
)

st.bar_chart(chart_df)

st.divider()

# -----------------------------
# Latency Statistics
# -----------------------------
st.subheader("⏱️ Latency Statistics")

st.write(df["Latency"].describe())

st.divider()

# -----------------------------
# Full Evaluation Table
# -----------------------------
st.subheader("📋 Evaluation Results")

st.dataframe(
    df,
    use_container_width=True
)

# -----------------------------
# Download CSV
# -----------------------------
st.download_button(
    label="📥 Download Results CSV",
    data=df.to_csv(index=False),
    file_name="results.csv",
    mime="text/csv"
)