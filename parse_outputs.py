import json
import csv
import sys
from pathlib import Path

model_name = sys.argv[1] if len(sys.argv) > 1 else "deepseek"

input_dir = Path(f"results/raw_outputs/{model_name}/evidence")
output_dir = Path("results/parsed_outputs")
output_dir.mkdir(parents=True, exist_ok=True)

output_csv = output_dir / f"{model_name}_evidence_parsed.csv"

def normalize_value(value, unit):
    if value is None:
        return None

    try:
        num = float(value)
    except (ValueError, TypeError):
        return value

    unit_lower = str(unit).lower()

    if "million" in unit_lower:
        return int(num * 1_000_000)
    if "billion" in unit_lower:
        return int(num * 1_000_000_000)
    if "thousand" in unit_lower:
        return int(num * 1_000)

    return num

rows = []

for path in sorted(input_dir.glob("S*.json")):
    with open(path, "r", encoding="utf-8") as f:
        record = json.load(f)

    sample_id = record["sample_id"]
    model = record["model"]
    prompt_type = record["prompt_type"]
    raw_output = record["raw_output"]

    try:
        parsed = json.loads(raw_output)
        json_valid = True
    except json.JSONDecodeError:
        parsed = {}
        json_valid = False

    value = parsed.get("value")
    unit = parsed.get("unit")
    normalized_value = normalize_value(value, unit)

    rows.append({
        "sample_id": sample_id,
        "model": model,
        "prompt_type": prompt_type,
        "target_field": parsed.get("target_field"),
        "value": value,
        "unit": unit,
        "normalized_value": normalized_value,
        "source_quote": parsed.get("source_quote"),
        "answerable": parsed.get("answerable"),
        "json_valid": json_valid
    })

with open(output_csv, "w", encoding="utf-8", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=[
        "sample_id",
        "model",
        "prompt_type",
        "target_field",
        "value",
        "unit",
        "normalized_value",
        "source_quote",
        "answerable",
        "json_valid"
    ])
    writer.writeheader()
    writer.writerows(rows)

print(f"Parsed {len(rows)} files.")
print(f"Saved to {output_csv}")
