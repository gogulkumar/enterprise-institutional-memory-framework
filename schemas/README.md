---
name: schemas-and-validators
description: Guide to the JSON Schemas that define every kind of brain entry, the validator that checks a brain against the rules and rebuilds its lookup index, and the checker for Markdown front matter. Use when writing or debugging a brain entry, explaining a validation error, or before running schemas/validate.py or schemas/check_markdown.py.
metadata:
  last_modified: "2026-11-14"
---

# Schemas

JSON Schema (draft 2020-12) for every entry kind in SPEC section 6. Fields follow SPEC sections 6.1 to 6.5; where they disagree, SPEC wins and the schema is the bug.

## Header blocks

| Schema | Block (SPEC 6.1) | Used by |
|---|---|---|
| `base` | id, kind, version, title, sensitivity, recorded_at | every entry |
| `scope` | scope | reasoning entries, procedures, knowledge base |
| `time` | valid_from, valid_to, last_supported, review_window | reasoning, procedures, dependency map, knowledge base |
| `governed` | provenance, trust, sureness, owner, events, last_confirmed_by_owner, open_questions, related | reasoning, procedures, dependency map |
| `provenance` | provenance only | knowledge base |

## Entry schemas

Each schema is named for one prefix and kind (SPEC 6.5); every entry states its `kind`.

| Prefix | Schemas |
|---|---|
| `BV` `TP` `JD` `RS` | `business-view`, `thinking-pattern`, `judgment`, `response-style` |
| `PR` | `procedure` |
| `KB` | `kb-concept`, `kb-metric-definition`, `kb-table-structure`, `kb-source-of-truth`, `kb-business-event`, `kb-known-issue`, `kb-calendar-point`, `kb-deliverable-profile`, `kb-template` |
| `DM` | `dm-link`, `dm-impact-scope` |
| `SRC` | `src-artifact`, `src-approved-location`, `src-tool-contract`, `src-authority-rule` |
| `TR` `Q` `TS` `RN` | `log-trace`, `log-question`, `log-scenario`, `log-test-run` |
| governance | `proposal`, `match-ledger-row` |

Change records are lines in `logs/changes.md`, not separate files; the validator checks each line's format.

## The validator

```bash
python schemas/validate.py brain/                       # validate and regenerate index.yaml
python schemas/validate.py brain/ --check                # validate only
python schemas/validate.py brain/ --today 2026-12-31     # compute relevance as of a date
```

Beyond the schemas it checks:
- each entry sits in its folder (SPEC 15.1) and its file is named by its id
- every id it mentions exists, and every event id is registered by exactly one business event
- two business events with the same period and the same affected metrics (a split event)
- sensitivity is a configured level and never lower than its sources
- trust against SPEC 7.1: case counts from distinct events and periods, the owner's word, inference-only entries held below `established`, pattern-origin entries needing the owner, and other people's work capped at `observation`
- proposals, match ledger rows and change-log lines

When everything passes it writes `index.yaml` (SPEC 15.3): situations, deliverables and metrics maps, plus one row per entry with its trust, sureness, sensitivity and computed relevance. Logs and held-out tests are never indexed. It ignores `archive/`, `passes/` and `.applier.lock`.

Requires `pyyaml`, `jsonschema` and `referencing`.

## Checking Markdown front matter

`check_markdown.py` verifies that every Markdown file starts with the front matter in SPEC section 16.

```bash
python schemas/check_markdown.py .          # check every .md file
python schemas/check_markdown.py --list .   # print only the front matter, which is what an agent reads at run time
```
