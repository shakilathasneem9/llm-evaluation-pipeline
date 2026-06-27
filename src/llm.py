from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(
    base_url=os.getenv("OPENAI_BASE_URL"),
    api_key=os.getenv("OPENAI_API_KEY")
)

def ask_llm(question):
    response = client.chat.completions.create(
        model="llama-3.2-3b-instruct",
        messages=[
            {"role": "user", "content": question}
        ],
        temperature=0
    )
    return response.choices[0].message.content


if __name__ == "__main__":
    print(ask_llm("What is the capital of France?"))