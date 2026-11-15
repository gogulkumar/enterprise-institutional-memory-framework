---
title: Proposals Folder
description: 'What lives in proposals/: pending changes to the brain, one file each, plus the pending and rejected subfolders.'
purpose: Explain that Build and Think only propose and that the single applier writes memory.
when_to_use: Open when writing, applying or reviewing a proposal.
last_modified: 2026-11-14
---

# Proposals (`proposals/`)

**What lives here:** Pending changes to the brain, one file per change (`<ULID>.yaml`). Neither `Build` nor `Think` edits memory directly—they write proposals here for the single applier in `skills/learn/SKILL.md`.

- **Schema:** `schemas/proposal.schema.json` (`action`, `target`, `payload`, `evidence`, `needs_ratification`).
- **Subfolders:**
  - `pending/` — High-stakes proposals waiting for human owner approval (e.g., promoting to `established`, resolving `contested`, redefining a metric, or loading a new `RP-` / `ED-` rule).
  - `rejected/` — Proposals that failed schema validation or were declined by the owner.

