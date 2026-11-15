---
title: Business Understanding Folder
description: 'What belongs in business-understanding/: concepts, metric definitions, Normality baselines and Dependency links, and what does not belong.'
purpose: Keep the stable how-the-business-works layer separate from performance conclusions.
when_to_use: Open before adding a concept, metric definition, Normality entry or Dependency link.
last_modified: 2026-11-14
---

# Business Understanding (`business-understanding/`)

**Business Understanding** is the stable "how this business works" layer—the shared vocabulary, validated math, normal baselines, and causal/structural links between metrics.

- **ID prefix:** `BU-<ULID>.yaml`
- **Schemas:**
  - `schemas/concept.schema.json` — Plain-English concepts (`definition`, `interpretation`, `positive_signal`, `negative_signal`, `agent_reuse`, `boundaries`).
  - `schemas/metric-definition.schema.json` — Validated formulas (`calculation`, `validated_by`, `known_issues`).
  - `schemas/normality.schema.json` — What normal looks like (`normal_pattern`, relative `materiality_threshold`, `conditions`).
  - `schemas/dependency-link.schema.json` — Explicit links between metrics/concepts (`drives`, `offsets`, `lags`, `constrains`, `independent`).

---

## What deserves to be in `business-understanding/`? (Strict bar)
Apply the litmus test: **"Would this still be true next period unless the business structure or accounting/reporting rules change?"**
1. **Concepts & Metrics** must have a clear definition, a specific `agent_reuse` trigger (when to load), and—for metrics—a `validated_by` check that passes against real Record data.
2. **Normality** must come from historical backfill or a ratified owner statement, expressed as shares, directions, or relative thresholds—never raw dollar numbers.
3. **Dependency Links** must be explicitly stated by the owner, docs, or confirmed by `Learn`. Unlinked pairs stay `unknown` so `Think` cross-checks them lightly.

## What does NOT belong in `business-understanding/`
- **Performance conclusions that new quarterly data could argue against** → goes in `beliefs/` (`BEL-`).
- **Absolute numbers** (e.g., *"\$50M threshold"*) → use relative/policy thresholds; raw values stay in `record/`.
- **How experts sequence questions or format reports** → goes in `reasoning-patterns/` (`RP-`) or `editorial/` (`ED-`).
- **Anything that serves no `LENS-` deliverable** → out of scope; drop it.

---

## How it connects to the rest of the brain
- Every entry names at least one `LENS-` ID in `serves_task`.
- `Beliefs` must draw on at least two `BU-` entries (`source_concepts`) and a `Normality` baseline (`normal_baseline`).
- `Think` uses `agent_reuse` in `index.yaml` to load relevant `BU-` entries and follows `dependency-link`s during investigation.
