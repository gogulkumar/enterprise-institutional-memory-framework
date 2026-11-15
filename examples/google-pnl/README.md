---
title: 'Worked Example: Alphabet Quarterly P&L'
description: 'Guide to the Alphabet quarterly P&L example: where the data is, what each store in the brain holds, the three patterns, the pasted-note walkthrough, and how Think would use it.'
purpose: Show the framework applied to results readers already know.
when_to_use: Open to see a populated brain or to compare it with your own.
last_modified: 2026-11-14
---

# Worked example: Alphabet quarterly P&L

A brain built on **12 quarters of Alphabet's reported results (2023-Q4 to 2026-Q3)**, plus one pasted note from the owner. It shows every store in SPEC section 5 holding real entries, how trust is earned, and what is still waiting for the owner.

## 1. Where the numbers live (`data/`)

The brain stores no figures. They stay in [`data/`](./data/):
- [`quarterly_pnl.csv`](./data/quarterly_pnl.csv): reported revenue, segment operating income, the consolidated income statement and EPS for 12 quarters.
- [`one_offs.csv`](./data/one_offs.csv): charges and below-the-line items the releases call out.
- [`SOURCES.md`](./data/SOURCES.md): the SEC filings behind each number and the checks run on them.

## 2. What is in the brain (`brain/`)

| Store | What is here |
|---|---|
| `sources/` | The SEC releases (authored by the company), the dataset, a lookup tool contract, the rule that the filings win, the approved data folder, and the owner's pasted note |
| `knowledge/` | Four concepts (Services, Cloud, Alphabet-level activities, other income), the operating margin definition, two known issues, the source of truth, the deliverable profile, and one business event per quarter (the registry of events) |
| `reasoning/business-view/` | Four normal ranges checked against the data (Services seasonality, Cloud margin, Alphabet-level share, net income to operating income) and three patterns found across quarters |
| `reasoning/thinking-patterns/`, `judgments/`, `response-style/` | The owner's pasted-note rules, and three placeholders (see below) |
| `dependency-map/` | Alphabet-level costs offset segment operating income; other income is independent of operating margin |
| `procedures/` | How the quarterly commentary is produced |
| `logs/` | Two open questions and the change log |
| `proposals/pending/` | A promotion waiting for the owner |

### The three patterns, in plain English
1. **Cloud margin rises with scale.** Cloud's operating margin rose or held flat every quarter as revenue grew, so read a Cloud revenue beat as margin-positive unless the margin actually falls.
2. **Alphabet-level costs drag consolidated margin.** Unallocated costs have taken a larger share of revenue since 2025-Q3, so consolidated margin improves less than segment margins suggest.
3. **Other income distorts net income and EPS.** In quarters where equity securities swing, net income and EPS say little about operating performance.

All three are checked against the data and sit at `candidate`. Patterns found across events need the owner's ratification before `established` (SPEC section 7.1). The four normal ranges are `established`: each holds across four or more quarters in two or more periods, with a data check.

The proposal in `proposals/pending/` asks the owner to promote the Cloud pattern. Both gates have been run, and their results are in the proposal: a blind pass by a fresh agent with no brain, and a contradiction search over the data.

### The pasted note (SPEC section 9.4)
The owner pasted: *"When a cost line comes in under forecast, I check whether the budget owner already told me about a timing slip before I call it a saving. Don't call it a saving in the weekly until I've checked."* It became a source record, a thinking pattern, two judgments (driver classification and framing), a response style with a `never_say`, and one open question. These entries are in the owner's own words, so they are `stated` and `established` within the scope given (the weekly).

> **Placeholders:** the quarterly-commentary thinking pattern, the cause-attribution judgment, the leadership response style and the procedure were written for this example and never confirmed by a real owner. They are `inferred` and sit at `observation`, which means the agent never uses them on their own. Public filings cannot show how your analysts think or write; replace them by running `learn` on your own team's commentary and confirming the results.

## 3. How `think` would use this brain

Asked about a new quarter, the agent checks readiness, loads the business view for the area, frames the release against the normal ranges, and follows the owner's thinking pattern for the situation. Where it would need a placeholder or a candidate to decide an answer, it says so and asks the owner (SPEC section 10). It words each point by trust and sureness and attaches a handover note.

## 4. Validate it

```bash
pip install jsonschema pyyaml
python schemas/validate.py examples/google-pnl/brain
```

The validator checks every entry against its schema and the trust rules, then regenerates `index.yaml`.
