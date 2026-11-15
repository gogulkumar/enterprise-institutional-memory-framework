---
name: build
title: "Build: Set Up a Brain"
description: Set up a new institutional brain for one owner. Run once, before any Learn or Think run, to record what the agent may read, inventory the sources, run a pilot on one deliverable, then widen and connect. Implements SPEC 13.1.
purpose: Playbook for taking an empty brain to a tested pilot, following SPEC section 13.1.
when_to_use: Run once per owner when setting up a new brain, and again when the owner asks to widen to a new deliverable (Phase 2) or connect deliverables (Phase 3).
last_modified: 2026-11-14
---

# Build

Build takes an empty `brain/` (copied from `templates/brain/`, SPEC 2) to a pilot that passes both tests, then widens it. It never writes memory directly: every entry it produces is a proposal in `brain/proposals/`, applied by the applier in the `learn` skill (SPEC 12.1).

`SPEC.md` is the authority. Each step below cites the section it carries out.

## Before you start

- Read `brain/config.yaml`. If `owner` or `backup_reviewer` is empty, ask the owner to fill them in and stop (SPEC 15.2).
- Read SPEC sections 1, 3, 5 and 13.1 once in full.
- Run the scope check before every action (SPEC 1).

## Phase 0: set up

1. **Confirm what you can do.** Check and report each capability to the owner: read slides as rendered images, run code on spreadsheets and read their formulas, query the data sources, start a clean sub-agent (SPEC 2 step 3, SPEC 13.1). Report any gap before going on.
2. **Approved locations.** Ask the owner which folders, systems and channels you may read. Propose one `SRC` entry of kind `approved_location` per place (fields: SPEC 6.4), in `brain/sources/`.
3. **Data access.** Ask for access to the data. Until it arrives, ask for an approved read-only snapshot, store it outside `brain/`, and record its source and as-of date (SPEC 5). Use it only to validate metric definitions and run tests.
4. **Authorship.** Ask which authors and files are the owner's. Other people's work can support an entry only up to `observation` (SPEC 7.1).
5. **Sources inventory.** List every available source as a `SRC` entry of kind `artifact` (SPEC 6.4): type, period, author, location, `approved_location`, `deliverable`. Do not read content yet.
6. **Mark held-out periods.** Agree with the owner which recent periods are held out for the tests (SPEC 13.2). Held-out periods must be later than every period you will learn from. Record them in the inventory before reading any file, and never open them for learning.
7. **Event registry.** For each period in the inventory, propose `KB` entries of kind `business_event` for the events the inventory already shows, with ids in the form `EVT-<period>-<slug>` (SPEC 6.5, 7.1).

## Phase 1: pilot

Pick one deliverable with the owner. Everything below is for that deliverable and its situations only.

1. **Deliverable profile.** Read the most recent final version. Propose a `KB` entry of kind `deliverable_profile` (SPEC 6.3). Ask the owner to confirm its purpose and audience.
2. **Metric definitions.** Trace the deliverable's model with code. For every number it shows, propose a `KB` entry of kind `metric_definition` and validate it against the data (SPEC 7.1, checked entries). Record tables as `table_structure`, final sources as `source_of_truth`, hard-coded numbers and broken links as `known_issue`. Never store a figure (SPEC 3 principle 3).
3. **Learn each period, oldest first.** For each non-held-out period, run the `learn` skill on that period's files. Predict before reading once the brain holds relevant entries (SPEC 9 step 2). Use drafts, edits, query histories and emails to check the reconstructions (SPEC 9 step 4).
4. **Confirm in batches.** Send the owner the reconstructed reasoning in run reports, with at most 10 questions per batch (SPEC 11, SPEC 14).
5. **Interview.** When questions build up, or before the pilot tests, ask the owner for an interview (SPEC 11). Use the script below. Record it as a `TR` trace and run `learn` on it; the owner's own statements start entries at `established` within the scope given (SPEC 7.1, rule 1).
6. **Test.** Run the `prove` skill: reasoning test and reproduction test on the held-out periods (SPEC 13.2).
7. **Exit check.** The pilot is complete only when both tests pass and the brain holds at least (SPEC 13.1):
   - a business view entry for each area in scope;
   - a thinking pattern for each main situation;
   - judgments for materiality and for cause attribution;
   - a response style for each audience.
   List what is missing in the run report, and keep going until nothing is.

### Interview script

Prepare questions in priority order: first what changes how you would reason, then what changes a figure, then style (SPEC 11). Ask about concrete cases, never in the abstract.

- **Business view:** "In [period], you treated [line] as normal although it moved. What does normal look like for it, and what usually drives it? What tends to surprise you?"
- **Thinking patterns:** "When [line] is off forecast, what is the first thing you check? What would make you doubt the number? When do you stop digging?"
- **Judgments:** "In [period], you left [driver] out. Why? How big must a movement be before you mention it in [deliverable]? When do you call a cause, and when do you only attribute it?"
- **Response style:** "For [audience], what do you lead with? What do you never say? How do you word uncertainty?"
- **Known traps:** "Which numbers or sources have misled you before?"

Record answers word for word, with their scope (SPEC 11, after an answer).

## Phase 2: widen

Start only after the pilot passes both tests and the owner says to go on (SPEC 13.1). For each new deliverable repeat Phase 1 steps 1 to 7. The stores are shared: do not rebuild the business view, thinking patterns, judgments or response style per deliverable; add scope and conditions to existing entries instead (SPEC 5).

## Phase 3: connect

For every pair of deliverables, propose:
- `DM` links of type `feeds` for what flows from one into the other, and `same_story` where both must explain something the same way (SPEC 8);
- scope updates to thinking patterns and judgments that apply to both;
- `independent` links for pairs with no real connection.

Establish each connection from evidence, never from the deliverables' names (SPEC 8).

## Stop and check in with the owner

Stop building and report if any of these holds (SPEC 13.1):
- predictions have not moved closer to the owner's work over the last ten texts;
- effort is going to something no aim justifies;
- open questions block more than half of the remaining work.

## Build is complete when

- Phases 0 and 1 are done and the pilot exit check passes.
- `python schemas/validate.py brain/` passes.
- The owner has agreed the pass levels for the tests and confirmed the pilot.
