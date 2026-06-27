import pandas as pd


def generate_html_report(df, accuracy, hallucination_rate,
                         avg_latency, min_latency,
                         max_latency, pass_fail):

    html = f"""
    <html>

    <head>

        <title>LLM Evaluation Report</title>

        <style>

            body {{
                font-family: Arial;
                margin:40px;
                background:#f8f9fa;
            }}

            h1 {{
                color:#2c3e50;
            }}

            table {{
                border-collapse:collapse;
                width:100%;
                margin-top:20px;
            }}

            th,td {{
                border:1px solid #ddd;
                padding:10px;
                text-align:left;
            }}

            th {{
                background:#4CAF50;
                color:white;
            }}

            tr:nth-child(even){{
                background:#f2f2f2;
            }}

            .card{{
                background:white;
                padding:20px;
                border-radius:10px;
                margin-bottom:20px;
                box-shadow:0px 0px 8px rgba(0,0,0,0.15);
            }}

        </style>

    </head>

    <body>

    <h1>📊 LLM Evaluation Report</h1>

    <div class="card">

    <h2>Summary</h2>

    <p><b>Accuracy:</b> {accuracy:.2f}%</p>

    <p><b>Status:</b> {pass_fail}</p>

    <p><b>Hallucination Rate:</b> {hallucination_rate:.2f}%</p>

    <p><b>Average Latency:</b> {avg_latency:.2f} sec</p>

    <p><b>Fastest Response:</b> {min_latency:.2f} sec</p>

    <p><b>Slowest Response:</b> {max_latency:.2f} sec</p>

    </div>

    {df.to_html(index=False)}

    </body>

    </html>

    """

    with open("reports/report.html", "w", encoding="utf-8") as f:
        f.write(html)

    print("HTML Report Generated!")