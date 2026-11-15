---
title: Reasoning Patterns Folder
description: 'What belongs in reasoning-patterns/: how experts sequence questions and judge materiality, attribution, escalation and stopping.'
purpose: Keep expert investigation habits as questions to consider, never rigid commands.
when_to_use: Open before writing or reviewing a Reasoning Pattern.
last_modified: 2026-11-14
---

# Reasoning Patterns (`reasoning-patterns/`)

**Reasoning Patterns** capture how domain experts actually investigate a problem—the order in which they ask questions and the rules they use to judge materiality, attribution, escalation, and when to stop.

- **ID prefix:** `RP-<ULID>.yaml`
- **Schemas:**
  - `schemas/inquiry-chain.schema.json` — Ordered investigation steps (`trigger`, `question_sequence`, `why_this_order`, `conditions`, `exceptions`).
  - `schemas/judgment-rule.schema.json` — Decision rules (`situation`, `rule_type`: `materiality | attribution | escalation | stopping`, `rule`, `conditions`, `counter_examples`).

---

## What deserves to be a Reasoning Pattern? (Strict bar)
An entry belongs here **only if**:
1. **Repeatable expert behavior:** It has been observed across **two or more independent events**, or explicitly given by the domain expert during `Build` Step 5.
2. **Scoped & conditional:** It states clear `conditions` and `exceptions` / `counter_examples` so the agent knows when *not* to apply it.
3. **Human-ratified:** It cannot be loaded by `Think` until the human owner approves it.

## What does NOT belong in `reasoning-patterns/`
- **Hardcoded commands or scripts** → `Think` treats every `RP-` as a *question to consider*, never a blind command.
- **Report formatting or audience tone rules** → goes in `editorial/` (`ED-`).
- **Business facts or metric formulas** → goes in `business-understanding/` (`BU-`).
- **One-off ad-hoc checks from a single task** → discard after the task.

---

## How it connects to the rest of the brain
- `LENS-` procedures cite `RP-` IDs in `question_sources` rather than rewriting reasoning steps inline.
- `Think` loads ratified `RP-` entries during Steps 4–7 to rank and investigate questions and enforce stopping rules.
