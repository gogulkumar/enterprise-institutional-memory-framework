---
title: 'Worked Example: Alphabet Quarterly P&L'
description: 'Guide to the Alphabet quarterly P&L example: where the data is, what each brain folder holds, the three beliefs, and how Think would use it.'
purpose: Show the framework applied to results readers already know.
when_to_use: Open to see a populated brain or to compare it with your own.
last_modified: 2026-11-14
---

# Worked Example: Alphabet Quarterly P&L Brain

This is a complete, end-to-end example of an institutional brain built on **12 quarters of Alphabet's reported results (2023-Q4 to 2026-Q3)**. It shows how every piece of the framework connects in practice—from raw source data to a finished deliverable and a pending human approval.

---

## 1. Where the numbers live (`data/`)
The brain itself stores **zero raw dollar figures**. All numbers stay in [`data/`](./data/):
- [`data/quarterly_pnl.csv`](./data/quarterly_pnl.csv) — Reported revenue, segment operating income, consolidated income statement, and EPS across 12 quarters.
- [`data/one_offs.csv`](./data/one_offs.csv) — Specific charges and below-the-line items called out in the SEC releases.
- [`data/SOURCES.md`](./data/SOURCES.md) — Exact SEC Form 8-K filings and arithmetic checks verifying the data.

---

## 2. What is inside the brain (`brain/`)
Every one of the six framework components is populated and wired together:

| Folder | What is in it here | Plain-English role |
|---|---|---|
| [`lens/`](./brain/lens/) | `LENS-01KGP...001` + [`context-needs.md`](./brain/lens/context-needs.md) | Defines the deliverable (*Quarterly P&L review commentary*), who reads it, what is out of scope, and tracks which knowledge is `have`, `partial`, or `missing`. |
| [`record/`](./brain/record/) | `REC-01KGP...001` to `004` | Registers the SEC filings, CSV data, a lookup tool contract (explicitly stating it *cannot* explain *why* a line moved), and the rule that SEC filings outrank working CSVs. |
| [`business-understanding/`](./brain/business-understanding/) | `BU-01KGP...001` to `011` | Defines segments (Services, Cloud, Alphabet-level, other income), validated margin formulas, normal seasonal bands (e.g., Q4 Services step-up), and metric links. |
| [`beliefs/`](./brain/beliefs/) | `BEL-01KGP...001` to `004` + [`ledger/`](./brain/beliefs/ledger/) | Three multi-quarter patterns (`provisional`) and one open Story Thread (`BEL-...004`), each backed by quarter-by-quarter evidence rows. |
| [`reasoning-patterns/`](./brain/reasoning-patterns/) | `RP-01KGP...001`, `002` | An inquiry chain (*when consolidated margin surprises, check Alphabet-level costs first*) and a stopping rule (*report "attributed, cause unverified" if the filing doesn't state a reason*). |
| [`editorial/`](./brain/editorial/) | `ED-01KGP...001` | Tells the agent to lead with the biggest abnormal movement for finance leadership, always reconcile segments to consolidated operating income, and skip routine seasonal noise. |

> **Placeholders:** the reasoning-pattern and editorial entries (`RP-`, `ED-`) are illustrative, written for this example under a placeholder owner (`example-owner`). Public filings cannot show how your analysts actually think or write, so these were not captured from a real expert. Replace them by running `build` Step 5 and `learn` Step 5 on your own team's commentary.

### The three learned Beliefs in plain English
1. **Cloud margin scales with revenue** (`BEL-01KGP...001`, `provisional`): Cloud's operating margin rose or held flat in every quarter as revenue grew—so treat a Cloud revenue beat as margin-positive unless margin actually drops.
2. **Alphabet-level costs drag consolidated margin** (`BEL-01KGP...002`, `provisional`): Unallocated corporate costs have taken a larger share of revenue since 2025-Q3, meaning consolidated margin improves less than segment margins suggest.
3. **Other income distorts net income & EPS** (`BEL-01KGP...003`, `provisional`): In quarters where equity securities swing, net income and EPS tell you very little about core operating performance.

### Governance in action
- [`brain/match_ledger.yaml`](./brain/match_ledger.yaml) and [`brain/changelog.md`](./brain/changelog.md) show the audit trail from backfilling the 12 quarters.
- [`brain/proposals/pending/01KGP000000000000000000001.yaml`](./brain/proposals/pending/01KGP000000000000000000001.yaml) shows a proposal to promote `BEL-01KGP...001` from `provisional` (*"accounts for"*) to `established` (*"because"*). Both SPEC §5.2 gates were run first (a blind pass by a fresh agent with no brain, and a contradiction search over the data); their results sit in `payload.gates`, and the owner decides whether to ratify.

---

## 3. How `Think` uses this brain on a new quarter
If you ask an agent to run **`Think`** on a new quarter's release against this brain:
1. It checks [`lens/context-needs.md`](./brain/lens/context-needs.md) and [`index.yaml`](./brain/index.yaml) to confirm it has enough coverage.
2. A clean sub-agent reads the new release with **zero memory** so it isn't biased.
3. The main agent compares that blind read against `BU-` Normality bands and `BEL-` expectations, investigates surprises using `RP-01KGP...001` (checking Alphabet-level costs before blaming segments), and stops at `RP-01KGP...002` if no cause is stated.
4. It formats the brief using `ED-01KGP...001`—using *"accounts for"* (not *"because"*) since the beliefs are still `provisional`—and writes any new conclusions back to `brain/proposals/`.

---

## 4. Validate and try it yourself

Check that all entries, references, ledgers, and proposals pass the schemas and refresh `index.yaml`:
```bash
pip install jsonschema pyyaml
python schemas/validate.py examples/google-pnl/brain
```

Then ask your agent to run `skills/think/SKILL.md` on a new quarter's earnings release using `examples/google-pnl/brain` and compare what it asks, what it skips, and how it writes against what a finance analyst would produce.
