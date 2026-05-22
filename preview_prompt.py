import json
import sys

sample_id = sys.argv[1] if len(sys.argv) > 1 else "S001"
prompt_path = "prompts/evidence_prompt.txt"
samples_path = "data/samples.jsonl"

with open(prompt_path, "r", encoding="utf-8-sig") as f:
    system_prompt = f.read()

target_sample = None

with open(samples_path, "r", encoding="utf-8-sig") as f:
    for line in f:
        item = json.loads(line)
        if item["sample_id"] == sample_id:
            target_sample = item
            break

if target_sample is None:
    raise ValueError(f"Sample not found: {sample_id}")

final_prompt = f"""
{system_prompt}

Sample ID:
{target_sample["sample_id"]}

Target field:
{target_sample["target_field"]}

Question:
{target_sample["question"]}

Text:
{target_sample["text"]}
"""

print(final_prompt)
