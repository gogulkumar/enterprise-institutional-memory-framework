---
title: Learn Passes Folder
description: 'What lives in passes/: temporary working folders for each Learn run, such as the sealed prediction and the blind read output.'
purpose: Explain what a pass folder holds and that the validator ignores it.
when_to_use: Open when starting a Learn pass or cleaning up old passes.
last_modified: 2026-11-14
---

# Learn Passes (`passes/`)

**What lives here:** Temporary working folders created during each `Learn` run (`LP-<ULID>/`), holding:
- `prediction.yaml` and `prediction.sha256` (sealed before reading the document)
- `read.yaml` (output of the clean sub-agent's blind read)
- `questions_for_owner.md` / `gate_queue.md` (if any)

Ignored by `schemas/validate.py`. Can be pruned once a pass is applied.

