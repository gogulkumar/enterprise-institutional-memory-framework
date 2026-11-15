# Pipelines (`pipelines/`)

Executable Python tooling that handles the deterministic mechanics of the institutional brain so the AI agent can focus 100% on reasoning about the business.

## Why this exists
The institutional brain relies on strict invariants—unbiased blind reads (sealed predictions), single-writer proposal application, audit logging, and clearance-filtered index lookups. Leaving those mechanics to LLM prose introduces formatting and locking bugs. Keeping them in `pipelines/` makes the brain reliable at scale.

## Setup
Install the Python dependencies from the repo root:
```bash
pip install -r requirements.txt
```

## Files
- **[`brain.py`](./brain.py)** — Operational CLI for:
  - `ulid` — Mint valid 26-character Crockford Base32 IDs.
  - `seal` / `verify-seal` — Lock `prediction.yaml` before a `Learn` blind read and verify it before comparison.
  - `apply` — Run the single Applier over `brain/proposals/` and `brain/proposals/pending/`, append to `logs/changes.md`, archive retired entries, and regenerate `index.yaml` via `schemas/validate.py`. Automatically reclaims stale `.applier.lock` files left behind by crashed processes.
  - `query` — Filter `brain/index.yaml` by `sensitivity` clearance, `situation`, `deliverable`, or `metric` so `Think` loads only what the task needs.

## Operational Gotchas to Keep in Mind
1. **Single-brain ID scope:** `schemas/validate.py` resolves all IDs within one `brain/` directory. Connected deliverables (such as a Data Pipeline and a P&L deliverable) must live inside the same `brain/` folder (using `deliverable_owners` in `config.yaml` for separate team ownership).
2. **Host sub-agent isolation:** Blind reads in `Learn` and `Think` only prevent confirmation bias if your agent runtime spawns a clean sub-agent with **zero** memory entries in context—do not run blind reads inside the main conversation window.
