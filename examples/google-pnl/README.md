# Worked example: Alphabet quarterly P&L

A small brain built on Alphabet's reported results, 2023-Q4 to 2026-Q3, so you can see the framework against numbers you already know.

- **`data/`** is the Record: the reported quarterly P&L and its sources. See `data/SOURCES.md` for where each number came from and how it was checked. The brain points to this data and never copies a value from it.
- **`brain/`** is the memory built on top: one Lens deliverable (quarterly P&L review commentary), four Record entries, eleven Business Understanding entries, and four Beliefs entries (three beliefs and one open question).

## What the beliefs say

Each comes from a pattern across the 12 quarters that no single release states:

1. Cloud's operating margin has risen or held flat every quarter as revenue scaled.
2. Costs held at the Alphabet level have taken a larger share of revenue since 2025-Q3, so consolidated margin improves less than segment margins.
3. In quarters where other income swings, net income and EPS say little about operating performance.

All three sit at `provisional`: they are supported by three or more independent quarters but have not passed the blind pass and contradiction search that `established` requires (SPEC §5.2), and `example-owner` is a placeholder.

## What is deliberately missing

There are no Reasoning Patterns or Editorial rules. Those record how your analysts think and write, and cannot be read off public data. Run `learn` on your team's own commentary to build them (SPEC §6.2, step 5).

## Try it

```bash
python schemas/validate.py examples/google-pnl/brain
```

Then ask your agent to run `think` on the next quarter's release against this brain, and compare what it asks and says with what your team would.
