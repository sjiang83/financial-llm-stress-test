# Financial LLM Stress Test

This project evaluates how large language models perform on controlled financial document extraction hard cases.

The goal is not to test simple field extraction, but to identify when models fail under realistic financial-document conditions such as fiscal-year ambiguity, GAAP vs non-GAAP confusion, missing-field refusal, unit conversion, restatement traps, footnote-based corrections, and document-level prompt injection.

## Motivation

Financial documents often contain similar numeric fields, multiple reporting years, GAAP and non-GAAP measures, footnotes, restatements, and management-preferred metrics. These conditions make financial information extraction a useful stress test for LLM reliability, grounding, and structured output quality.

This project builds a small controlled benchmark to evaluate whether models can:

- extract the correct financial field;
- distinguish GAAP from non-GAAP measures;
- handle GAAP vs non-GAAP ambiguity;
- handle fiscal-year and unit ambiguity;
- refuse to answer when a field is not explicitly reported;
- avoid following instruction-like text embedded inside documents;
- return valid JSON with supporting source quotes.

## Models Evaluated

- Qwen-Flash
- DeepSeek

## Dataset

The benchmark contains 40 controlled financial extraction samples.

The samples include both standard extraction cases and harder boundary cases:

- multi-year financial tables;
- field confusion between revenue, operating income, and net income;
- GAAP vs non-GAAP conflicts;
- missing-field refusal;
- unit conversion across millions, billions, and thousands;
- fiscal-year label ambiguity;
- parent-attributable income vs consolidated income;
- discontinued operations footnotes;
- restatement traps;
- per-share vs total amount confusion;
- prompt-injection-like text inside financial documents.

Each sample includes:

- sample_id
- company
- case_type
- target_field
- question
- text

Ground truth labels are stored separately in data/ground_truth.csv.

## Project Structure

    financial-llm-stress-test/
    ├── data/
    │   ├── samples.jsonl
    │   └── ground_truth.csv
    ├── prompts/
    │   ├── basic_prompt.txt
    │   ├── schema_prompt.txt
    │   └── evidence_prompt.txt
    ├── results/
    │   ├── evaluation/
    │   ├── parsed_outputs/
    │   └── summary/
    ├── parse_outputs.py
    ├── evaluate.py
    ├── run_deepseek_all.py
    ├── run_qwen_all.py
    ├── test_deepseek.py
    ├── test_qwen.py
    └── validate_data.py

## Evaluation Pipeline

The experiment pipeline is:

1. Load financial extraction samples.
2. Apply an evidence-required prompt.
3. Run each model on each sample.
4. Save raw model outputs.
5. Parse model outputs into a normalized CSV format.
6. Compare parsed outputs against ground truth.
7. Analyze model errors by case type.

The evaluation checks:

- answer correctness;
- numeric normalization;
- unit conversion;
- answerability / refusal behavior;
- source quote grounding;
- JSON validity;
- error type.

## Results

We evaluated Qwen-Flash and DeepSeek on a 40-sample controlled financial extraction stress test.

| Model | Correct | Total | Accuracy |
|---|---:|---:|---:|
| Qwen-Flash | 38 | 40 | 95.00% |
| DeepSeek | 40 | 40 | 100.00% |

## Error Cases

Qwen-Flash failed on two boundary cases:

| Sample | Case Type | Error |
|---|---|---|
| S028 | prompt_injection_financial_extraction | The model followed instruction-like text inside the document and returned the injected value instead of extracting GAAP net income from the financial statement. |
| S033 | fiscal_year_unit_trap | The model extracted the correct table value but failed to convert USD thousands into full USD. |

## Key Finding

Both models performed well on standard and moderately difficult financial extraction cases. However, Qwen-Flash failed on two boundary cases involving document-level prompt injection and fiscal-year/unit ambiguity. DeepSeek correctly handled all 40 samples in this evaluation.

This suggests that controlled financial extraction tasks can expose reliability issues that may not appear in simple extraction benchmarks.

## Relevance

This project connects financial document understanding, information extraction, structured LLM evaluation, and grounded output verification. It is relevant to LLM evaluation, financial NLP, document intelligence, and trustworthy AI applications.

## How to Run

Install dependencies:

    pip install -r requirements.txt

Validate the dataset:

    python validate_data.py

Run model inference:

    python run_qwen_all.py
    python run_deepseek_all.py

Parse model outputs:

    python parse_outputs.py qwen
    python parse_outputs.py deepseek

Evaluate results:

    python evaluate.py qwen
    python evaluate.py deepseek

The main result files are stored in:

    results/evaluation/
    results/parsed_outputs/
    results/summary/

## Current Status

The core experiment is complete. The repository currently includes the dataset, prompts, model inference scripts, parsing scripts, evaluation logic, and summary result tables.

The next step is to improve reproducibility by adding setup instructions, dependency files, and a clearer result discussion section.
