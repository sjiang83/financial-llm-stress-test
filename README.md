# Financial LLM Stress Test

Stress-testing LLMs on financial reasoning, factual reliability, and structured answer evaluation.

## Project Goal

This project evaluates how large language models perform on controlled financial document extraction hard cases.

The goal is not to test simple field extraction, but to identify when models fail under realistic financial-document conditions such as GAAP vs non-GAAP confusion, missing-field refusal, unit conversion, fiscal-year ambiguity, restatement traps, footnote corrections, and document-level prompt injection.

## Data Source and Benchmark Design

The benchmark contains 40 controlled financial extraction samples.

Each sample includes a short financial document excerpt, a target extraction question, and a manually written ground-truth answer.

The test cases cover:

- multi-year financial tables;
- revenue, operating income, and net income confusion;
- GAAP vs non-GAAP ambiguity;
- missing-field refusal;
- unit conversion across millions, billions, and thousands;
- fiscal-year ambiguity;
- restatement traps;
- footnote corrections;
- per-share vs total amount confusion;
- document-level prompt injection.

## Models Evaluated

- Qwen-Flash
- DeepSeek

## Evaluation Method

The evaluation pipeline is:

1. Load financial extraction samples.
2. Apply an evidence-required prompt.
3. Run each model on each sample.
4. Save raw model outputs.
5. Parse model outputs into normalized CSV files.
6. Compare parsed outputs against ground truth.
7. Analyze errors by case type.

The evaluation checks:

- answer correctness;
- numeric normalization;
- unit conversion;
- answerability / refusal behavior;
- source quote grounding;
- JSON validity;
- error type.

## Main Results

| Model | Correct | Total | Accuracy |
|---|---:|---:|---:|
| Qwen-Flash | 38 | 40 | 95.00% |
| DeepSeek | 40 | 40 | 100.00% |

Qwen-Flash failed on two boundary cases:

| Sample | Case Type | Error |
|---|---|---|
| S028 | prompt_injection_financial_extraction | The model followed instruction-like text inside the document and returned the injected value instead of extracting GAAP net income from the financial statement. |
| S033 | fiscal_year_unit_trap | The model extracted the correct table value but failed to convert USD thousands into full USD. |

## Relevance to Research

This project is related to LLM evaluation, financial-domain reliability, information extraction, and structured output analysis.

It focuses on whether language models can produce grounded and verifiable answers in financial-document settings. The benchmark is designed to test not only extraction accuracy, but also factual reliability, evidence grounding, refusal behavior, unit normalization, and robustness against misleading document content.

This connects to research problems in trustworthy NLP systems, domain-specific LLM evaluation, benchmark construction, and reliable structured prediction from semi-structured documents.

## Project Structure

    financial-llm-stress-test/
    ├── data/
    │   ├── samples.jsonl
    │   └── ground_truth.csv
    ├── prompts/
    │   └── evidence_prompt.txt
    ├── results/
    │   ├── evaluation/
    │   ├── parsed_outputs/
    │   └── summary/
    ├── evaluate.py
    ├── parse_outputs.py
    ├── run_deepseek_all.py
    ├── run_qwen_all.py
    └── validate_data.py

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

## Current Status

The core experiment is complete. The repository includes the dataset, prompts, model inference scripts, output parsing, evaluation logic, and summary result tables.