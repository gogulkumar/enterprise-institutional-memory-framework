---
title: Lens Folder
description: 'What belongs in lens/: recurring deliverables with their audience, scope and procedure, and the bar an entry must meet.'
purpose: Stop the brain turning into an open-ended wiki by tying everything to a named deliverable.
when_to_use: Open before adding or reviewing a deliverable.
last_modified: 2026-11-14
---

# Lens (`lens/`)

The **Lens** is the boundary of the entire brain. It defines **what work this brain exists to produce** so the brain never turns into an open-ended wiki.

- **Schema:** `schemas/lens-deliverable.schema.json`
- **ID prefix:** `LENS-<ULID>.yaml`
- **Also here:** `context-needs.md` (tracks which knowledge each Lens still needs: `have`, `partial`, `missing`).

---

## What deserves to be a Lens? (Strict bar)
An entry belongs in `lens/` **only if ALL FOUR are true**:
1. **Recurring deliverable or decision:** Real people ask for it repeatedly (e.g., weekly pipeline health review, quarterly P&L commentary, monthly forecast check)—not a one-off ad-hoc question.
2. **Named audience:** You can name who reads it and what decision they make from it.
3. **Clear boundary & "done" rule:** It has a single `governing_question`, an explicit `out_of_scope` / `boundary`, and a `completion_rule` so the agent knows when to stop.
4. **Owned by a real person:** Someone can judge whether the output is good or bad.

## What does NOT belong in `lens/`
- **A raw data source or table** → goes in `record/` (`REC-`).
- **A metric formula or business term** → goes in `business-understanding/` (`BU-`).
- **A multi-quarter pattern or hypothesis** → goes in `beliefs/` (`BEL-`).
- **A general topic** (e.g., *"Cloud"* or *"Data Engineering"*) with no deliverable, audience, or decision → **rejected**. A topic is not a Lens.

---

## How the Lens locks the rest of the brain
Every governed entry in `business-understanding/`, `beliefs/`, `reasoning-patterns/`, and `editorial/` **must** name at least one `LENS-` ID in `serves_task`.
- If a piece of knowledge helps produce a Lens deliverable, it enters the brain.
- If it serves **no** Lens deliverable, it stays in `record/` or is discarded.
