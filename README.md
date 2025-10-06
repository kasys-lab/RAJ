# Retrieval-Augmented Relevance Judgment for Specialized Domains

## Prompts

- Generation Definition
  - `prompt/definition_generation_prompt.md`
- Relevance Judgment
  - `prompt/relevance_judgment_prompt.md`
- Expertise Annotation
  - `prompt/expertise_annotation_prompt.md`

## Directory

```bash
.
├── data
│   ├── nfcorpus_bm25.trec
│   ├── nfcorpus_qrel.jsonl
│   └── sample
│       ├── covid_generated_definition.txt
│       ├── nfcorpus_generated_definition.txt
│       └── robust_generated_definition.txt
├── prompt
│   ├── definition_generation_prompt.md
│   ├── expertise_annotation_prompt.md
│   ├── prompt_frame.py
│   ├── prompt_parts.py
│   └── relevance_judgment_prompt.md
├── pyproject.toml
├── README.md
├── src
│   ├── __init__.py
│   ├── create_eval_dataset
│   │   ├── create_nfcorpus_qrel.py
│   │   └── main.py
│   ├── dataset_handler
│   │   ├── BaseHandler.py
│   │   ├── CovidHandler.py
│   │   ├── NFCorpusHandler.py
│   │   └── RobustHandler.py
│   ├── generate_definition
│   │   ├── create_batch_file.py
│   │   └── main.py
│   └── relevance_judgment
│       ├── evaluate.py
│       ├── create_batch_file.py
│       └── main.py
├── utils
│   ├── __init__.py
│   └── request.py
└── uv.lock
```
