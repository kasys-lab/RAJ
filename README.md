# Retrieval-Augmented Relevance Judgment for Specialized Domains

```bash
.
├── data
│   ├── nfcorpus_bm25.trec
│   ├── nfcorpus_qrel.jsonl
│   └── sample
│       ├── covid_generated_definiton.txt
│       ├── nfcorpus_generated_definiton.txt
│       └── robust_generated_definiton.txt
├── prompt
│   ├── prompt_frame.py
│   └── prompt_parts.py
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
│   │   ├── generate_batch_file.py
│   │   └── main.py
│   └── relevance_judgment
│       ├── evaluate.py
│       ├── generate_batch_file.py
│       └── main.py
├── utils
│   ├── __init__.py
│   └── request.py
└── uv.lock
```
