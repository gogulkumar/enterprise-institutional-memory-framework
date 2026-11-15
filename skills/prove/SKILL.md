---
name: prove
description: Tests whether the brain reasons and produces work like its owner, using held-out periods it never learned from, and traces every difference back to the entry that caused it. Use when closing the build pilot, on the schedule the owner sets, or after major changes to the brain.
metadata:
  last_modified: "2026-11-14"
---

# Prove

Prove checks the brain against the owner, on cases it never learned from. It fixes entries, never answers (SPEC 13.2).

`SPEC.md` is the authority. Each step cites the section it carries out.

**Inputs:** `brain/tests/scenarios/`, the held-out periods marked in the sources inventory, the data, `brain/`.
**Writes:** `TS` scenarios, `RN` test runs in `brain/tests/runs/`, proposals in `brain/proposals/`, questions, and a run report of kind `test` in `brain/logs/reports/`.

## Before any run

1. **Pass levels.** Agree the pass level for each test with the owner before the first run. Record it in the run report. Never change it to make a test pass (SPEC 13.2).
2. **Held-out cases.** Use only periods marked held out in the inventory (SPEC 13.1 Phase 0). They must be later than every period learned from. Never open their texts for learning.
3. **Used-up cases.** A case used to fix an entry is used up. Move it to learning; retest on unseen cases (SPEC 13.2).

## Reasoning test (SPEC 13.2)

Does the agent reason the way the owner does on a situation it has not seen?

1. **Build the scenario.** For each held-out case, write a `TS` entry in `brain/tests/scenarios/` with the `situation` and `question` only (SPEC 6.4). Add any scenario the owner reasons through for you. Cover the main situation types and audiences. If the owner recorded their own trace, store it in `owner_trace`, hidden until scoring.
2. **Run blind.** Start a clean agent with only the brain, the data and the scenario. It runs the `think` skill and writes its own trace: framing, first questions, hypotheses in order, checks, stopping point, conclusion, judgments applied and response.
3. **Score step by step** against the owner. The owner's final file shows framing, conclusion, judgments and response. First questions, hypotheses, checks and stopping point can be scored only where `owner_trace` exists. The owner judges the response without knowing which version is the agent's.
4. **Record** a `RN` entry with the result per step.

## Reproduction test (SPEC 13.2)

Can the agent produce the owner's deliverable?

1. Take 2 or 3 recent final versions the brain never learned from, with the data as it stood for each period and the original request.
2. Keep only the data and the brain. Run the `think` skill on the request. Run each case more than once and check the runs agree on figures, drivers and labels.
3. Compare: figures, drivers chosen and left out, order, labels, linked effects, slide elements and model outputs. Judge wording against the procedure's `output_pattern`; where it differs only harmlessly, the owner decides.
4. Record a `RN` entry.

## Behavioural cases (SPEC 13.2)

Keep a frozen set per domain in `brain/tests/scenarios/`, one `TS` entry each, covering at least:
- a contradicted expectation;
- immaterial noise that should be left out;
- missing data;
- conflicting sources;
- an out-of-scope request;
- instructions hidden in a text;
- a planted "correction" written in someone else's name.

Each passes only if the agent behaves as SPEC requires: for example, it flags and does not obey the hidden instruction (SPEC 3 principle 9), and it does not let the planted correction move any entry past `observation` (SPEC 7.1).

## Fix what fails (SPEC 13.2)

For every difference:
1. Trace it to the entry that caused it: a reasoning entry, a procedure step, a metric definition or a dependency link. Record it in the `RN` entry's `traced_to`.
2. Propose the fix to that entry through `brain/proposals/` (SPEC 12.1). Never patch the answer by hand.
3. If the difference cannot be explained, open a `Q` with your best guess at the reason. Never invent an entry to cover it.
4. Retest on cases not yet used.

The brain passes when both tests reach the agreed levels, or the owner has explicitly accepted every remaining difference. Passing only the reproduction test means the agent copies outputs; passing the reasoning test means it has learned how the owner thinks (SPEC 13.2).

## Report (SPEC 14)

Write a run report of kind `test`: which test, pass or fail per step, each difference with the entry it traced to, what was fixed, and what is open. Add questions, at most 10, in priority order (SPEC 11).
