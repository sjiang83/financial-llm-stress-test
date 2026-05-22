import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

api_key = os.getenv("DEEPSEEK_API_KEY")
model = os.getenv("DEEPSEEK_MODEL", "deepseek-v4-flash")

if not api_key:
    raise ValueError("DEEPSEEK_API_KEY not found in .env")

client = OpenAI(
    api_key=api_key,
    base_url="https://api.deepseek.com"
)

response = client.chat.completions.create(
    model=model,
    messages=[
        {"role": "user", "content": "Return only JSON: {\"status\":\"ok\"}"}
    ],
    response_format={"type": "json_object"},
    max_tokens=100
)

print(response.choices[0].message.content)
