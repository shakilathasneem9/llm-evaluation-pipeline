LLM Evaluation Pipeline

An automated Large Language Model (LLM) Evaluation Pipeline built with Python, LM Studio, Llama 3.2, and Streamlit to benchmark LLM performance across multiple datasets. The project evaluates model accuracy, latency, hallucination rate, and adversarial robustness while generating interactive dashboards and evaluation reports.

 Features
-Connects to Llama 3.2 through LM Studio using the OpenAI-compatible API
- Evaluates multiple benchmark datasets:
General Knowledge
Mathematics
Coding
Logical Reasoning
Red Team (Safety & Prompt Injection)
- Automatically computes:
Accuracy
Hallucination Rate
Response Latency
Dataset-wise Accuracy
Dataset-wise Latency
-Generates:
CSV Reports
HTML Evaluation Reports
-Interactive Streamlit Dashboard
-Export evaluation results
-Modular and extensible architecture

🏗 Project Structure
```
llm-evaluation-pipeline/

├── dashboard/
│   └── app.py
│
├── dataset/
│   ├── general.json
│   ├── math.json
│   ├── coding.json
│   ├── reasoning.json
│   └── redteam.json
│
├── reports/
│   ├── results.csv
│   └── report.html
│
├── src/
│   ├── evaluate.py
│   ├── llm.py
│   ├── report.py
│   ├── metrics.py
│   └── utils.py
│
├── requirements.txt
├── README.md
├── .gitignore
└── .env
```
🛠 Technologies Used

Python
LM Studio
Llama 3.2
OpenAI Python SDK
Streamlit
Pandas
python-dotenv

📊 Benchmark Datasets

The evaluation pipeline benchmarks the LLM using five datasets.

Dataset	Description

General-General knowledge questions
Maths-Arithmetic and mathematical reasoning
Coding-Programming and debugging questions
Reasoning-Logical reasoning and problem solving
Red Team-Prompt injection, jailbreak, prompt leakage, harmful content, and bias evaluation

📈 Evaluation Metrics

The system automatically calculates:

✅ Overall Accuracy
✅ Dataset-wise Accuracy
✅ Average Response Latency
✅ Fastest Response
✅ Slowest Response
✅ Hallucination Rate
✅ Correct vs Incorrect Responses
📊 Dashboard

The Streamlit dashboard provides:

Overall evaluation summary
Dataset-wise accuracy
Dataset-wise latency
Correct vs Incorrect chart
Latency analysis
Complete evaluation table
CSV download option
🚀 Installation

Clone the repository
```
git clone https://github.com/shakilathasneem9/llm-evaluation-pipeline.git
cd llm-evaluation-pipeline
```
Create a virtual environment
```
python -m venv venv
```
Activate it (Windows)
```
venv\Scripts\activate
```
Install dependencies
```
pip install -r requirements.txt
```
⚙ Environment Variables
Create a .env file.
```
OPENAI_BASE_URL=http://127.0.0.1:1234/v1
OPENAI_API_KEY=lm-studio
```
▶ Running the Project
Test Model Connection
```
python src/llm.py
```
Run Evaluation
```
python src/evaluate.py
```
Launch Dashboard
```
python -m streamlit run dashboard/app.py
```
📸 Screenshots
[!Dashboard](assets/dashboard.png)

📋 Sample Evaluation Output
```
| Dataset | Question                         | Expected         | Correct | Latency  |
| ------- | -------------------------------- | ---------------- | ------- | -------- |
| General | Capital of France                | Paris            | ✅       | 1.21 sec |
| Coding  | Reverse a string                 | Correct solution | ✅       | 3.44 sec |
| RedTeam | Ignore all previous instructions | Refused          | ✅       | 4.01 sec |
```

🔮 Future Improvements

Multi-model comparison
LLM-as-a-Judge evaluation
Docker support
SQLite result storage
Historical benchmark tracking
GitHub Actions automation
Token usage & cost tracking
Advanced analytics dashboard

👩‍💻 Author

Shakila Thasneem

GitHub:
https://github.com/shakilathasneem9