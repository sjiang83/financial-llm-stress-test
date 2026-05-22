import json
import csv

samples_path = "data/samples.jsonl"
truth_path = "data/ground_truth.csv"

sample_ids = []

print("Checking samples.jsonl...")

with open(samples_path, "r", encoding="utf-8-sig") as f:
    for line_no, line in enumerate(f, start=1):
        line = line.strip()
        if not line:
            continue
        try:
            item = json.loads(line)
        except json.JSONDecodeError as e:
            print(f"JSON error at line {line_no}: {e}")
            raise

        required = ["sample_id", "case_type", "company", "question", "text", "target_field"]
        for key in required:
            if key not in item:
                raise ValueError(f"Missing {key} in sample line {line_no}")

        sample_ids.append(item["sample_id"])

print(f"samples.jsonl valid rows: {len(sample_ids)}")
print("Sample IDs:", sample_ids)

print("\nChecking ground_truth.csv...")

truth_ids = []

with open(truth_path, "r", encoding="utf-8-sig", newline="") as f:
    reader = csv.DictReader(f)
    for row in reader:
        truth_ids.append(row["sample_id"])

print(f"ground_truth.csv valid rows: {len(truth_ids)}")
print("Truth IDs:", truth_ids)

if set(sample_ids) != set(truth_ids):
    raise ValueError("Sample IDs do not match between samples.jsonl and ground_truth.csv")

print("\nAll checks passed.")
