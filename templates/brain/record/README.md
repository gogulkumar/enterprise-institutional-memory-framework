---
title: Record Folder
description: 'What belongs in record/: pointers to documents and data, tool contracts and source authority rules, never copied numbers.'
purpose: Keep the pointer layer to real-world truth separate from interpretation.
when_to_use: Open before registering an artifact, tool contract or source authority rule.
last_modified: 2026-11-14
---

# Record (`record/`)

The **Record** is the brain's pointer layer to real-world truth. It tells the agent **where** facts, documents, and data tools live, and **which source wins** when two disagree.

- **ID prefix:** `REC-<ULID>.yaml`
- **Schemas:**
  - `schemas/record-artifact.schema.json` — Source documents and datasets (`type`, `business_area`, `period`, `event_ids`, `version`, `location`, `authority_rank`).
  - `schemas/tool-contract.schema.json` — Data tools and APIs (`can_establish`, `cannot_establish`, `access_boundary`).
  - `schemas/source-authority.schema.json` — Tie-breaker rules (`question_type`, `preferred_source`, `fallback_order`, `reason`).

---

## What deserves to be in `record/`? (Strict bar)
An entry belongs here **only if it is one of**:
1. **An original artifact** (filing, report, table, dataset) with a concrete `location`, `period`, `event_ids`, and `authority_rank`.
2. **A tool contract** that explicitly states both what the tool *can* establish and what it *cannot* establish.
3. **A source-authority rule** that names a single winning source for a specific `question_type`.

## What does NOT belong in `record/`
- **Copied numbers, tables, or document text** → leave them in the source system; only store the pointer.
- **Business definitions or metric formulas** → goes in `business-understanding/` (`BU-`).
- **Multi-quarter interpretations or patterns** → goes in `beliefs/` (`BEL-`).
- **Summaries of what a document says** → goes in `passes/` during `Learn`, never in `record/`.

---

## How it connects to the rest of the brain
- Every entry across the brain cites `REC-` IDs in `provenance` and inherits the highest `sensitivity` of its sources.
- `Belief` evidence ledgers (`beliefs/ledger/`) link each piece of evidence to `(record_id, event_id)`.
- `Think` only queries tools within their `can_establish` and `access_boundary` limits.
