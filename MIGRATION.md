---
name: migration-v1-to-v2
description: 'Record of how version 2 of the framework differs from version 1: every v1 part and safeguard with its v2 replacement, and the design decisions the owner approved for v2. Use when converting a brain built under v1, or when asking why v2 works differently; not needed to run a v2 brain.'
metadata:
  last_modified: "2026-11-14"
---

# Migration from v1 to v2

## What changed from v1

| v1 | v2 |
|---|---|
| Six components, with memory at the centre | Four reasoning stores at the centre, with supporting stores around them |
| `LENS`: every governed entry names a deliverable (`serves_task`) | Deliverables are optional scope and live in knowledge base profiles; entries need only serve one of the three aims |
| `REC` Record | `SRC` Sources, with approved locations |
| `BU` concepts and metric definitions | `KB` knowledge base, with more entry types |
| `BU` Normality | `BV` business view |
| `BU` Dependency link | `DM` dependency map, with 7 link types and impact scope |
| `BEL` Beliefs and Story Threads | `BV` entries with `origin: pattern` (same master test); `Q` questions of type `watch` |
| `RP` Reasoning Patterns | `TP` thinking patterns and `JD` judgments (8 areas) |
| `ED` Editorial | `RS` response style |
| Procedure nested in the Lens | `PR` procedures, a store of their own |
| Trust: observation, candidate, provisional, established, contested, retired | observation, candidate, established, contested, replaced, retired, plus `sureness` |
| Relevance: current, stale, historical | current, aging, stale, historical, with review windows by entry type |
| Learn takes documents and expert-authored deliverables | Learn takes any text, with source records, per-unit routing and reasoning traces |
| One interview during Build | Questions log, research before asking, interviews as a continuing source |
| Evaluation in one paragraph | Reasoning and reproduction tests with scenarios, runs and reports |
| No handover note | Handover note on every answer |
| Skills: build, learn, think | Skills: build, learn, think, prove |

**v1 safeguards, and what happened to each:**

| Safeguard | Status |
|---|---|
| Proposal queue, single applier, lock | Kept |
| Owner approval tiers | Kept; narrowed to the changes in section 12.2 |
| Sensitivity and access control | Kept |
| Blind reads; blind pass and contradiction search before established | Kept (the gates now apply to pattern-origin entries) |
| Master test | Kept, for pattern-origin entries |
| Documents are never instructions | Kept; extended to authorship (principle 5) |
| Reasoning entries loaded as prompts, not rules, until ratified | Kept, as `sureness: inferred` |
| Contested deadline and escalation | Kept (one window, then top of every report); backup reviewer cannot ratify reasoning |
| Match ledger | Kept |
| Observation expiry | Kept (config) |
| A stale entry drops one confidence level | Replaced by the Agent Learning Framework rule: a stale entry is not used by default |
| `provisional` level | Removed on purpose |
| `serves_task` on every entry | Removed on purpose |
| `seeded` flag | Replaced by `sureness: stated` |

## Decisions taken for v2

Approved by the owner on 2026-11-14 with the v2 draft.

1. **Beliefs** are business view entries with `origin: pattern`; story threads are questions with `why_it_matters: watch`.
2. **Trust** has six levels (observation, candidate, established, contested, replaced, retired); `provisional` is gone, and support that is only inferred stays at candidate.
3. **Run-time framing:** a blind read runs for deliverables and high-stakes asks; otherwise the evidence is compared with the business view.
4. **One owner per brain**, or one team speaking with one voice.
5. **Four skills:** build, learn, think and prove.
6. **Identifiers:** ULID ids with the prefixes `BV TP JD RS KB DM PR SRC` and log prefixes `TR Q CH TS RN`; every v1 prefix is renamed.
7. **Backup reviewer:** holds the queue but never ratifies a reasoning entry.
8. **Every entry states its `kind`** (section 6.5 of the framework), so the validator never has to guess an entry's type.

Sources: the Agent Learning Framework (https://claude.ai/artifact/WJDQJz1zFU18PLnPubEMjM) and v1 (commit abad65c).
