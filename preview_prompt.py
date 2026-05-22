import json

sample_id = "S001"
prompt_path = "prompts/evidence_prompt.txt"
samples_path = "data/samples.jsonl"

# 读取 prompt
with open(prompt_path, "r", encoding="utf-8-sig") as f:
    system_prompt = f.read()

# 读取指定 sample
target_sample = None

with open(samples_path, "r", encoding="utf-8-sig") as f:
    for line in f:
        item = json.loads(line)
        if item["sample_id"] == sample_id:
            target_sample = item
            break

if target_sample is None:
    raise ValueError(f"Sample not found: {sample_id}")

# 拼接成模型输入
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
