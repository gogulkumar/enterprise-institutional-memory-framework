---
title: Beliefs Folder
description: 'What belongs in beliefs/: the Master Test, the Belief, Story Thread and evidence ledger formats, and what does not belong.'
purpose: Keep Beliefs to durable cross-event patterns and stop single facts or definitions drifting in.
when_to_use: Open before writing or reviewing a Belief, Story Thread or evidence ledger.
last_modified: 2026-11-14
---

# Beliefs (`beliefs/`)

**Beliefs** hold durable interpretations learned across multiple business events, plus open **Story Threads** carried forward across periods until resolved.

- **ID prefix:** `BEL-<ULID>.yaml`
- **Schemas:**
  - `schemas/belief.schema.json` — Learned patterns (`statement`, `why_it_matters`, `source_concepts`, `normal_baseline`, `watch_condition`, `evolution_trail`).
  - `schemas/story-thread.schema.json` — Open questions (`question`, `expectation`, `what_would_resolve_it`).
  - `schemas/evidence-ledger.schema.json` — Stored at `beliefs/ledger/BEL-<ULID>.yaml`; maps `(record_id, event_id)` as `supporting`, `caution`, or `contradicting`.

---

## What deserves to be a Belief? (Strict bar — The Master Test)
An interpretation belongs in `beliefs/` **only if ALL THREE are true** (SPEC §4.5):
1. **Cross-document synthesis:** It says something no single source document states on its own.
2. **Grounded in `BU-`:** It draws on at least two Business Understanding entries (`source_concepts`).
3. **Actionable:** It implies a concrete reading rule or action for a named `LENS-` deliverable (`serves_task`).

Every Belief also carries a `normal_baseline` and a `watch_condition` (what evidence would break or demote it); the schema requires both.

*(For Story Threads: it must be an open question that matters beyond a single task and states `what_would_resolve_it`.)*

## What does NOT belong in `beliefs/`
- **Single-period results or one-off facts** → stays in `record/` or discarded.
- **Definitions or formulas** → goes in `business-understanding/` (`BU-`).
- **Blended performance + management spin** → keep beliefs about *business performance* separate from beliefs about *management narrative*.
- **Personal opinions with no `REC-` or `expert:` provenance** → rejected.

---

## How it connects to the rest of the brain
- Climbs the trust ladder (`observation` → `candidate` → `provisional` → `established`) counted in distinct `event_id`s—not document count.
- `Think` uses the entry's `trust` and `relevance` (`current` vs. `stale`) to choose exact wording (*"suggests"*, *"accounts for"*, *"because"*).
