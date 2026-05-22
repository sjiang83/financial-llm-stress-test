import csv
import json
from pathlib import Path

parsed_path = Path("results/parsed_outputs/deepseek_evidence_parsed.csv")
truth_path = Path("data/ground_truth.csv")
samples_path = Path("data/samples.jsonl")

output_dir = Path("results/evaluation")
output_dir.mkdir(parents=True, exist_ok=True)
output_path = output_dir / "deepseek_evidence_eval.csv"

def to_bool(x):
    return str(x).strip().lower() == "true"

def normalize_number(x):
    if x is None:
        return None
    x = str(x).strip()
    if x == "" or x.lower() == "null":
        return None
    try:
        return float(x)
    except ValueError:
        return x

# Load ground truth
truth = {}
with open(truth_path, "r", encoding="utf-8-sig", newline="") as f:
    reader = csv.DictReader(f)
    for row in reader:
        truth[row["sample_id"]] = row

# Load original sample text
sample_texts = {}
with open(samples_path, "r", encoding="utf-8-sig") as f:
    for line in f:
        if line.strip():
            item = json.loads(line)
            sample_texts[item["sample_id"]] = item["text"]

rows = []

with open(parsed_path, "r", encoding="utf-8-sig", newline="") as f:
    reader = csv.DictReader(f)
    for pred in reader:
        sample_id = pred["sample_id"]
        gt = truth[sample_id]
        original_text = sample_texts[sample_id]

        pred_value = normalize_number(pred["normalized_value"])
        expected_value = normalize_number(gt["expected_value"])

        pred_answerable = to_bool(pred["answerable"])
        expected_answerable = to_bool(gt["answerable"])

        value_correct = pred_value == expected_value
        answerable_correct = pred_answerable == expected_answerable

        pred_quote = str(pred["source_quote"]).strip()
        expected_quote = str(gt["expected_quote"]).strip()

        if not expected_answerable:
            quote_correct = True
        else:
            quote_correct = pred_quote != "" and pred_quote in original_text

        exact_quote_match = pred_quote == expected_quote

        overall_correct = value_correct and answerable_correct and quote_correct

        rows.append({
            "sample_id": sample_id,
            "case_type": gt["case_type"],
            "target_field": gt["target_field"],
            "expected_value": gt["expected_value"],
            "predicted_value": pred["normalized_value"],
            "value_correct": value_correct,
            "expected_answerable": gt["answerable"],
            "predicted_answerable": pred["answerable"],
            "answerable_correct": answerable_correct,
            "expected_quote": expected_quote,
            "predicted_quote": pred_quote,
            "quote_correct": quote_correct,
            "exact_quote_match": exact_quote_match,
            "json_valid": pred["json_valid"],
            "overall_correct": overall_correct
        })

with open(output_path, "w", encoding="utf-8", newline="") as f:
    fieldnames = [
        "sample_id",
        "case_type",
        "target_field",
        "expected_value",
        "predicted_value",
        "value_correct",
        "expected_answerable",
        "predicted_answerable",
        "answerable_correct",
        "expected_quote",
        "predicted_quote",
        "quote_correct",
        "exact_quote_match",
        "json_valid",
        "overall_correct"
    ]
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)

total = len(rows)
correct = sum(1 for r in rows if r["overall_correct"])

print(f"Evaluated {total} rows.")
print(f"Overall correct: {correct}/{total} = {correct / total:.2%}")
print(f"Saved to {output_path}")
