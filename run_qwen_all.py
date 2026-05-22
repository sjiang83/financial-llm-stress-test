import os
import json
import time
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

api_key = os.getenv("QWEN_API_KEY")
model = os.getenv("QWEN_MODEL", "qwen-flash")
base_url = os.getenv("QWEN_BASE_URL", "https://dashscope.aliyuncs.com/compatible-mode/v1")

if not api_key:
    raise ValueError("QWEN_API_KEY not found. Set it in PowerShell or .env.")

client = OpenAI(
    api_key=api_key,
    base_url=base_url
)

samples_path = "data/samples.jsonl"
prompt_path = "prompts/evidence_prompt.txt"
output_dir = Path("results/raw_outputs/qwen/evidence")
output_dir.mkdir(parents=True, exist_ok=True)

with open(prompt_path, "r", encoding="utf-8-sig") as f:
    system_prompt = f.read()

samples = []

with open(samples_path, "r", encoding="utf-8-sig") as f:
    for line in f:
        if line.strip():
            samples.append(json.loads(line))

print(f"Loaded {len(samples)} samples.")
print(f"Using model: {model}")

for sample in samples:
    sample_id = sample["sample_id"]
    output_path = output_dir / f"{sample_id}.json"

    if output_path.exists():
        print(f"Skip {sample_id}: output already exists")
        continue

    user_prompt = f"""
Sample ID:
{sample["sample_id"]}

Target field:
{sample["target_field"]}

Question:
{sample["question"]}

Text:
{sample["text"]}
"""

    print(f"Running {sample_id}...")

    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0,
            max_tokens=500
        )

        content = response.choices[0].message.content

        record = {
            "sample_id": sample_id,
            "model": model,
            "prompt_type": "evidence",
            "raw_output": content
        }

        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(record, f, ensure_ascii=False, indent=2)

        print(f"Saved {output_path}")

    except Exception as e:
        print(f"Error on {sample_id}: {e}")

    time.sleep(1)

print("Done.")
