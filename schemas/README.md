---
title: 'Schemas: Index and Usage'
description: Index of the JSON Schemas that check each memory entry type, and how to run the brain validator and the Markdown checker.
purpose: Tell readers which schema checks which entry and how to validate a brain or the documents.
when_to_use: Open when writing or debugging an entry, or when running schemas/validate.py or schemas/check_markdown.py.
last_modified: 2026-11-14
---

# Schemas

JSON Schema (draft 2020-12) for every entry type in SPEC §4. Field definitions follow SPEC §4; where they disagree, SPEC wins and the schema is the bug.

| Schema | Used for |
|---|---|
| `base-header`, `governed-header` | Headers composed into every entry (SPEC §4.1) |
| `lens-deliverable` | `lens/` (deliverable with nested procedure) |
| `record-artifact`, `tool-contract`, `source-authority` | `record/` |
| `concept`, `metric-definition`, `normality`, `dependency-link` | `business-understanding/` |
| `belief`, `story-thread` | `beliefs/` |
| `evidence-ledger` | `beliefs/ledger/<belief id>.yaml` |
| `inquiry-chain`, `judgment-rule` | `reasoning-patterns/` |
| `editorial-rule` | `editorial/` |
| `proposal` | `proposals/`, `proposals/pending/`, `proposals/rejected/` |
| `match-ledger-row` | each row of `match_ledger.yaml` |

An entry's type is found from its id prefix and folder; it must match exactly one schema for that prefix.

## Validate a brain

```bash
pip install jsonschema pyyaml
python schemas/validate.py path/to/brain
```

The validator checks:
- every entry against its schema
- that referenced ids exist
- ledger and proposal file names
- that each entry's `sensitivity` is a configured level and never lower than its sources

If everything passes, it regenerates `index.yaml`, with relevance computed from `last_confirmed`, `review_window` and `valid_to`. Use `--check` to validate without writing, and `--today YYYY-MM-DD` to compute relevance as of a given date. It ignores `archive/`, `passes/` and `.applier.lock`.

## Checking Markdown front matter

`check_markdown.py` verifies that every Markdown file starts with the front matter defined in SPEC §10 (`title`, `description`, `purpose`, `when_to_use`, `last_modified`; `SKILL.md` also needs `name`). It rejects a missing block, an empty key, a description over 300 characters, and a `last_modified` that is malformed or in the future.

```bash
python schemas/check_markdown.py .          # check every .md file
python schemas/check_markdown.py --list .   # print only the front matter, which is what an agent reads at run time
```
