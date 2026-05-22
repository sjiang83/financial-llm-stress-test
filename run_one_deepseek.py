import os
import json
import sys
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

sample_id = sys.argv[1] if len(sys.argv) > 1 else "S001"

api_key = os.getenv("DEEPSEEK_API_KEY")
model = os.getenv("DEEPSEEK_MODEL", "deepseek-chat")

if not api_key:
    raise ValueError("DEEPSEEK_API_KEY not found in .env")

client = OpenAI(
    api_key=api_key,
    base_url="https://api.deepseek.com"
)

with open("prompts/evidence_prompt.txt", "r", encoding="utf-8-sig") as f:
    system_prompt = f.read()

target_sample = None

with open("data/samples.jsonl", "r", encoding="utf-8-sig") as f:
    for line in f:
        item = json.loads(line)
        if item["sample_id"] == sample_id:
            target_sample = item
            break

if target_sample is None:
    raise ValueError(f"Sample not found: {sample_id}")

user_prompt = f"""
Sample ID:
{target_sample["sample_id"]}

Target field:
{target_sample["target_field"]}

Question:
{target_sample["question"]}

Text:
{target_sample["text"]}
"""

response = client.chat.completions.create(
    model=model,
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ],
    response_format={"type": "json_object"},
    temperature=0,
    max_tokens=500
)

print(response.choices[0].message.content)
