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

hallucinations = (
    df.apply(
        lambda row: row["Expected"].lower() not in row["Actual"].lower(),
        axis=1,
    )
).sum()

hallucination_rate = hallucinations / total_questions * 100

status = "✅ PASS" if accuracy >= 95 else "❌ FAIL"

# -----------------------------
# Dataset-wise Metrics
# -----------------------------
dataset_accuracy = (
    df.groupby("Dataset")["Correct"]
      .mean()
      .mul(100)
      .round(2)
      .reset_index()
)

dataset_accuracy.columns = ["Dataset", "Accuracy (%)"]

dataset_latency = (
    df.groupby("Dataset")["Latency"]
      .mean()
      .round(2)
      .reset_index()
)

dataset_latency.columns = ["Dataset", "Average Latency (sec)"]

dataset_questions = (
    df.groupby("Dataset")
      .size()
      .reset_index(name="Questions")
)

# -----------------------------
# Title
# -----------------------------
st.title("📊 LLM Evaluation Dashboard")

st.write(
    "Evaluate the performance of a Large Language Model using a benchmark dataset."
)

st.divider()

# -----------------------------
# Metric Cards
# -----------------------------
col1, col2, col3, col4 = st.columns(4)

col1.metric("Accuracy", f"{accuracy:.2f}%")
col2.metric("Questions", total_questions)
col3.metric("Correct", correct_answers)
col4.metric("Incorrect", incorrect_answers)

st.divider()

col5, col6, col7, col8 = st.columns(4)

col5.metric("Average Latency", f"{avg_latency:.2f} sec")
col6.metric("Fastest Response", f"{min_latency:.2f} sec")
col7.metric("Slowest Response", f"{max_latency:.2f} sec")
col8.metric("Hallucination Rate", f"{hallucination_rate:.2f}%")

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
# Dataset-wise Accuracy
# -----------------------------
st.subheader("📊 Dataset-wise Accuracy")

st.dataframe(
    dataset_accuracy,
    use_container_width=True,
    hide_index=True
)

st.bar_chart(
    dataset_accuracy.set_index("Dataset")
)

st.divider()

# -----------------------------
# Dataset-wise Average Latency
# -----------------------------
st.subheader("⏱️ Dataset-wise Average Latency")

st.dataframe(
    dataset_latency,
    use_container_width=True,
    hide_index=True
)

st.bar_chart(
    dataset_latency.set_index("Dataset")
)

st.divider()

# -----------------------------
# Dataset-wise Question Count
# -----------------------------
st.subheader("📚 Dataset-wise Question Count")

st.dataframe(
    dataset_questions,
    use_container_width=True,
    hide_index=True
)

st.bar_chart(
    dataset_questions.set_index("Dataset")
)

st.divider()

# -----------------------------
# Latency per Question
# -----------------------------
st.subheader("📈 Latency per Question")

latency_df = df[["Question", "Latency"]].set_index("Question")

st.bar_chart(latency_df)

st.divider()

# -----------------------------
# Correct vs Incorrect
# -----------------------------
st.subheader("✅ Correct vs Incorrect")

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

st.dataframe(
    df["Latency"].describe().to_frame(),
    use_container_width=True
)

st.divider()

# -----------------------------
# Full Evaluation Results
# -----------------------------
st.subheader("📋 Evaluation Results")

st.dataframe(
    df,
    use_container_width=True
)

st.divider()

# -----------------------------
# Download CSV
# -----------------------------
st.download_button(
    label="📥 Download Results CSV",
    data=df.to_csv(index=False),
    file_name="results.csv",
    mime="text/csv"
)