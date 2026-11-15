---
title: Example Brain Changelog
description: Append-only log of applied changes in the Alphabet example brain.
purpose: Show what an audit trail looks like after a backfill pass.
when_to_use: Open to see how applied changes are logged; the applier appends to it.
last_modified: 2026-11-14
---

# Changelog

Applied changes, append-only. One line per change:
`date | proposal id | action | target | ratified_by`


2026-11-14 | 01KGP000000000000000000101 | create | LENS-01KGP000000000000000000001 | example-owner
2026-11-14 | 01KGP000000000000000000102 | create | BU-01KGP000000000000000000002 | example-owner
2026-11-14 | 01KGP000000000000000000103 | promote | BEL-01KGP000000000000000000001 (observation to provisional) | automatic
2026-11-14 | 01KGP000000000000000000104 | promote | BEL-01KGP000000000000000000002 (observation to provisional) | automatic
2026-11-14 | 01KGP000000000000000000105 | promote | BEL-01KGP000000000000000000003 (observation to provisional) | automatic
