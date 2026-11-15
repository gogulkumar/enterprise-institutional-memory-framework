---
title: 'Enterprise Institutional Memory Framework: Overview'
description: 'Plain-English overview of the framework: what an institutional brain holds, how the three skills keep it current, how trust is earned, and a quickstart.'
purpose: Entry point for people deciding whether and how to adopt the framework.
when_to_use: Open first when new to the framework or when you need the quickstart steps. For exact rules, read SPEC.md instead.
last_modified: 2026-11-14
---

# Enterprise Institutional Memory Framework

An AI model already knows how to reason. What it does not know is **how your company works**: what your metrics actually mean, which report to trust when two numbers disagree, what a normal quarter looks like, and how your best people investigate a surprise.

Today, that knowledge lives in people's heads and in old decks nobody rereads. This framework turns it into a **living institutional brain**—a structured memory that your AI agent reads when doing work and updates automatically every time a new document or report arrives.

- **[SPEC.md](./SPEC.md)** — The complete rulebook: what goes into the brain, how trust is earned, and how the three processes work.
- **[skills/](./skills/)** — The three playbooks your agent runs: [`build`](./skills/build/SKILL.md), [`learn`](./skills/learn/SKILL.md), and [`think`](./skills/think/SKILL.md).
- **[templates/brain/](./templates/brain/)** — An empty brain folder you copy to start a new domain.
- **[examples/google-pnl/](./examples/google-pnl/)** — A worked example built on Alphabet's quarterly P&L.

Every Markdown file starts with a short front-matter block (title, description, purpose, when to use it, last modified; see [SPEC §10](./SPEC.md)). An agent reads only that block first and opens the rest of a file when the task matches. `python schemas/check_markdown.py --list .` prints just those blocks.

---

## What is inside a brain?

Every brain you create (copied from [`templates/brain/`](./templates/brain/), or seen populated in [`examples/google-pnl/brain/`](./examples/google-pnl/brain/)) is organized into six folders, each answering one plain question:

| Component | The plain question it answers |
|---|---|
| **Lens** (`lens/`) | **What is the work for?** Which recurring reports or decisions this brain supports, who reads them, and what "done" looks like. |
| **Record** (`record/`) | **Where is the truth?** Links to source documents and data tools, plus rules for which source wins when two disagree. |
| **Business Understanding** (`business-understanding/`) | **How does the business work?** Plain definitions of terms and metrics, what "normal" looks like, and which metrics move together. |
| **Beliefs** (`beliefs/`) | **What have we learned across time?** Durable patterns no single document states on its own, plus open questions we are still watching. |
| **Reasoning Patterns** (`reasoning-patterns/`) | **How do our experts think?** The order in which experts ask questions, what counts as big enough to care about, and when to stop. |
| **Editorial Judgment & Voice** (`editorial/`) | **How do we communicate?** What to lead with, what to always include, and what to leave out for each audience. |

---

## How the three skills work together

You do not hand-build or manually maintain this memory. Three processes keep it running as part of normal work:

1. **Build** *(run once per domain)* — Sets up the brain for a team's deliverables: defines what reports it must support, registers the trusted data sources, loads basic definitions, learns from past periods, and interviews your domain experts to fill in what documents don't say.
2. **Learn** *(runs on every new document)* — Before reading a new document, the agent predicts what it expects to see based on current memory. Then a fresh sub-agent with no memory reads the document objectively. Every gap between the prediction and the actual document becomes a signal to update memory through a reviewable proposal queue.
3. **Think** *(runs on every task)* — When asked to produce a report or answer a question, the agent checks whether it has enough knowledge to answer honestly, reads the new data without bias, investigates only the surprises that matter, and writes the final output using confidence words matched to how proven each belief is.

---

## How trust works

Not every idea in the brain is treated as fact. Every learned entry climbs one trust ladder based on **distinct business events** (for example, three separate quarters—not three different decks about the same quarter):

1. **Observation** *(1 event)* — Noted internally, never cited in final reports. Expires if not seen again.
2. **Candidate** *(2 events)* — Early pattern. Agent writes *"suggests"*.
3. **Provisional** *(3+ events across 2+ periods, or an expert-approved seed)* — Working rule. Agent writes *"accounts for"*.
4. **Established** *(independently verified and human-approved)* — Proven rule. Agent writes *"because"*.

If a new event contradicts an entry, it becomes **Contested** for a human owner to resolve. High-stakes changes—like promoting a belief to `established`, changing a metric's definition, or adopting a new expert rule—always wait for human approval.

---

## Quickstart

1. Copy `templates/brain/` into your agent's workspace as `brain/`.
2. Fill in `brain/config.yaml` with the human owner, backup reviewer, and review windows.
3. Give your agent the three skills in `skills/` (with file access, tool access, and the ability to run a clean sub-agent).
4. Run **Build** on one recurring deliverable using a few past periods of documents.
5. Wire **Learn** to run whenever a new document arrives, and **Think** to run whenever a task arrives.
6. Validate the brain structure and refresh its lookup index at any time:
   ```bash
   python schemas/validate.py brain/
   ```
