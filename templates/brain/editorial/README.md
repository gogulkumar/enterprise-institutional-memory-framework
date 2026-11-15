---
title: Editorial Judgment and Voice Folder
description: 'What belongs in editorial/: rules for what to lead with, always include and omit for a given audience.'
purpose: Keep output-shaping rules apart from analysis logic and data definitions.
when_to_use: Open before writing or reviewing an Editorial rule.
last_modified: 2026-11-14
---

# Editorial Judgment & Voice (`editorial/`)

**Editorial Judgment & Voice** captures how deliverables should be structured and phrased for a specific audience—what goes first, what is always included, and what is left out.

- **ID prefix:** `ED-<ULID>.yaml`
- **Schema:** `schemas/editorial-rule.schema.json` (`audience`, `lead_with`, `always_include`, `omit_when`, `structure`).

---

## What deserves to be an Editorial rule? (Strict bar)
An entry belongs here **only if**:
1. **Audience-specific & repeatable:** Observed across **two or more published deliverables** for that audience, or explicitly stated by the owner in `Build` Step 5.
2. **Concrete rules:** Clearly specifies `lead_with`, `always_include`, `omit_when`, and `structure`—not vague advice like *"be clear"*.
3. **Human-ratified:** Loaded by `Think` only after the human owner approves it.

## What does NOT belong in `editorial/`
- **Analytical logic or investigation order** → goes in `reasoning-patterns/` (`RP-`).
- **Trust-level wording rules** (*"suggests"* / *"accounts for"* / *"because"*) → enforced globally by `SPEC.md §5`, not per-audience.
- **Definitions or business rules** → goes in `business-understanding/` (`BU-`).

---

## How it connects to the rest of the brain
- Each rule names the `LENS-` deliverable(s) it serves in `serves_task` and matches the deliverable's `audience`.
- `Think` applies ratified `ED-` rules in Step 8 (`Communicate`) when shaping the final output.
