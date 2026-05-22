import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

api_key = os.getenv("QWEN_API_KEY")
model = os.getenv("QWEN_MODEL", "qwen-flash")
base_url = os.getenv("QWEN_BASE_URL", "https://dashscope.aliyuncs.com/compatible-mode/v1")

if not api_key:
    raise ValueError("QWEN_API_KEY not found in .env")

client = OpenAI(
    api_key=api_key,
    base_url=base_url
)

response = client.chat.completions.create(
    model=model,
    messages=[
        {"role": "user", "content": "Return only JSON: {\"status\":\"ok\"}"}
    ],
    temperature=0,
    max_tokens=100
)

print(response.choices[0].message.content)
