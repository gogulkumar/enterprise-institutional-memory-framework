---
name: google-pnl-example
description: Example brain built by running Build setup and Learn on original Alphabet
  earnings transcript PDFs. Use when inspecting source-derived knowledge and its learning
  records.
metadata:
  last_modified: '2026-11-14'
---

# Alphabet P&L example

The original Q1, Q2 and Q3 2025 earnings transcripts are downloaded in `data/raw/`. `data/raw/manifest.json` records their official URLs, file sizes, page counts and SHA-256 hashes. Page-marked extraction is in `data/extracted/`.

`brain/` was freshly copied from `templates/brain/` and populated through the repository’s Build setup and chronological Learn workflow. It contains 21 knowledge entries, four source records, three mechanism links, their impact scopes, and three open questions. Proposals, independent reads, sealed predictions, comparisons and structured run reports are retained in `brain/passes/`; the generated index and change log record applied changes. Q1 began without a prediction; Q2 and Q3 predictions were sealed before their clean readers ran. No held-out evaluation is claimed.

The source documents are external management work. No internal team thinking pattern, judgment, response preference or procedure was fabricated. Those folders retain the template structure; missing owner evidence and setup details are recorded in the questions log. Metric definitions remain unvalidated against internal data. The public-document learning is executed, while the owner-reviewed Build pilot remains incomplete.

The earlier manually constructed brain and its helper files are preserved in `data/previous-manual-example.zip` and were excluded from this learning run. Existing historical CSVs were not used as fresh-run evidence.

```bash
python3 schemas/validate.py examples/google-pnl/brain --check
```
