---
name: brain-change-log
description: Append-only list of every change applied to this brain, one line per change giving the date, the entry changed, before and after, the reason and what caused it. Use when auditing why an entry looks the way it does; only the applier writes to it.
metadata:
  last_modified: "2026-11-14"
---

# Change log

One line per change (SPEC section 6.4):
`CH-<ULID> | date | entry | before | after | reason | caused_by`

