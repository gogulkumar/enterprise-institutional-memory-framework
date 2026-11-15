---
title: 'Enterprise Institutional Memory Framework: Overview'
description: 'Plain-English overview of the framework: a brain that learns how its owner sees the business, thinks, decides and responds, from any text they produce, and the four skills that run it.'
purpose: Entry point for people deciding whether and how to adopt the framework.
when_to_use: Open first when new to the framework or when you need the quickstart steps. For exact rules, read SPEC.md instead.
last_modified: 2026-11-14
---

# Enterprise Institutional Memory Framework

An AI model already knows how to reason. What it does not know is **how your people reason about your business**: what they treat as normal, the first questions they ask when a number looks wrong, which explanations they check first, what they decide is big enough to mention, and how they say it to each audience.

Today that lives in people's heads. This framework turns it into an **institutional brain**: a governed memory your agent learns from any text its owner produces (reports, drafts, emails, chats, rough notes, corrections) and reasons with when anyone asks a question.

- **[SPEC.md](./SPEC.md)**: the complete rulebook.
- **[skills/](./skills/)**: the four playbooks your agent runs: [`build`](./skills/build/SKILL.md), [`learn`](./skills/learn/SKILL.md), [`think`](./skills/think/SKILL.md) and [`prove`](./skills/prove/SKILL.md).
- **[templates/brain/](./templates/brain/)**: an empty brain to copy.
- **[examples/google-pnl/](./examples/google-pnl/)**: a worked brain on Alphabet's quarterly P&L, with the data.
- **[MIGRATION.md](./MIGRATION.md)**: what changed from v1.

Every Markdown file starts with a short front-matter block (title, description, purpose, when to use it, last modified; see [SPEC section 16](./SPEC.md)). An agent reads only that block first and opens the rest of a file when the task matches. `python schemas/check_markdown.py --list .` prints just those blocks.

---

## What is inside a brain?

At the centre is the owner's reasoning, in four parts. Everything else supports it.

| Part | The plain question it answers |
|---|---|
| **Business view** | **How do they see the business?** What is normal, what usually drives each area, what is fragile, what they watch first. |
| **Thinking patterns** | **How do they work through a problem?** Their first questions, what makes them suspicious, which explanations they test and in what order, and when they stop. |
| **Judgments** | **How do they decide?** What is big enough to mention, timing or permanent, when a cause can be stated, what to leave out, when to escalate. |
| **Response style** | **How do they answer?** What they lead with, always include, never say, and how they word uncertainty, for each audience. |

| Supporting store | What it holds |
|---|---|
| **Knowledge base** | Definitions of terms and metrics, tables, sources of truth, the calendar, business events, known issues, deliverable profiles. |
| **Dependency map** | What affects what, and what else changes when one thing moves. |
| **Procedures** | Step-by-step instructions for producing each deliverable, pointing to the reasoning they apply. |
| **Sources** | A record of every text read and where it came from. |

Numbers are never stored. They stay in your data systems and are queried when needed.

---

## How the four skills work together

1. **Build** *(once)*: sets up the brain, then runs a pilot on one deliverable until the brain can reason and produce the way its owner does.
2. **Learn** *(whenever the owner gives the agent a text or corrects it)*: predicts what the text will show, reads it with fresh eyes, works out the thinking behind it, and turns that into reviewable proposals. A rough note is as welcome as a finished report.
3. **Think** *(whenever someone asks)*: answers with the owner's reasoning, whether or not the question belongs to a deliverable, and says plainly when the brain cannot support an answer.
4. **Prove** *(on a schedule)*: tests the brain on periods it never learned from: does it reason like the owner, and does it produce what the owner produced?

---

## How trust works

An entry earns trust from **distinct business events**, not from how many documents mention it, and from the owner's own word. The owner's statement or confirmation counts most. A pattern the agent only inferred stays a candidate until the owner confirms it. Every answer says how sure it is, and the owner approves the changes that matter. The exact rules are in [SPEC section 7](./SPEC.md).

---

## Quickstart

1. Copy `templates/brain/` into your agent's workspace as `brain/`.
2. Fill in `brain/config.yaml` with the owner and a backup reviewer.
3. Give your agent the four skills in `skills/`, with file access, data access, and the ability to start a clean sub-agent.
4. Run **build**.
5. Run **learn** whenever the owner shares a text or corrects the agent, and **think** whenever someone asks.
6. Validate the brain and refresh its index at any time:
   ```bash
   python schemas/validate.py brain/
   ```
