---
title: Change Log
description: Append-only log of every change applied to this brain, one line per change.
purpose: Audit trail of what changed, when, why and what caused it.
when_to_use: Open to audit a change. The applier appends to it and updates last_modified; never edit past lines.
last_modified: 2026-11-14
---

# Change log

One line per change (SPEC section 6.4):
`CH-<ULID> | date | entry | before | after | reason | caused_by`

