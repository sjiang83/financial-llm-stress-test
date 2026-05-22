import json

path = "data/samples.jsonl"
rows = []

with open(path, "r", encoding="utf-8-sig") as f:
    for line in f:
        item = json.loads(line)

        if item["sample_id"] == "S001":
            item["question"] = "Extract Apple's net income for fiscal year 2022 in USD. Convert from USD millions to full USD."

        if item["sample_id"] == "S002":
            item["question"] = "Extract Apple's operating income for fiscal year 2023 in USD. Convert from USD millions to full USD."

        rows.append(item)

with open(path, "w", encoding="utf-8") as f:
    for item in rows:
        f.write(json.dumps(item, ensure_ascii=False) + "\n")

print("Updated S001 and S002 questions.")
