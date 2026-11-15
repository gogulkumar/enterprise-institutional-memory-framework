---
title: Archive Folder
description: 'What the archive holds: retired entries, expired observations and historical entries, kept for audit and never deleted.'
purpose: Explain why entries move here and what the validator ignores.
when_to_use: Open when moving an entry to the archive or looking up a retired one.
last_modified: 2026-11-14
---

# Archive (`archive/`)

**What lives here:** Retired entries, expired observations, and historical entries whose `valid_to` date has passed.

Entries are moved here by the applier—never deleted—so the brain keeps a complete audit trail. Files here are excluded from `index.yaml` and ignored by `schemas/validate.py`.

