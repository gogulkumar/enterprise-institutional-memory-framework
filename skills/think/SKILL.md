---
name: think
description: Answers a question or produces a deliverable by reasoning the way the owner does, using their business view, thinking patterns, judgments and response style, and attaches a handover note saying how sure each point is. Use whenever the owner or someone they approve asks a question or requests a deliverable, including questions that match no deliverable.
metadata:
  last_modified: "2026-11-14"
---

# Think

Think answers by reasoning with the brain's reasoning model, not from old files. It never edits memory: what it learns goes back as proposals (SPEC 3 principle 8).

`SPEC.md` is the authority. Each step cites the section it carries out.

**Inputs:** the ask; the new evidence, if any; `brain/`; `brain/config.yaml`.
**Writes:** the answer, a handover note, proposals in `brain/proposals/`, questions in `brain/logs/questions/`.

## Loading entries

- First drop every entry above the requester's clearance (SPEC 12.3). The answer inherits the highest sensitivity of the entries used.
- Find entries through `brain/index.yaml`, in the load order of SPEC 15.3. Open only the files a step needs. If you need an entry the index does not point to, propose an index fix and note it.
- Use only entries valid for the period the question is about; for a past period, use the versions valid then, including those in `brain/archive/` (SPEC 7.3).

## Steps

1. **Understand the ask.** Who is asking, what they need, by when, for which audience. Load the matching `RS` entry. If the ask is a deliverable, load its `KB` `deliverable_profile` and its `PR` procedures. If it matches no deliverable, carry on: answer from the reasoning model (SPEC 10 step 1).

2. **Check readiness** (SPEC 10 step 2).
   - *Sufficient:* a `TP` at `candidate` or above fits the situation, the `BV` for the area is current, and the metrics needed have validated definitions and data access.
   - *Partial:* one of those is missing; answer with a caveat that names it.
   - *Insufficient:* say what is missing, offer to find out, open a `Q` entry, and stop. Do not answer as if from the owner's reasoning (SPEC 3 principle 10).

3. **Load the business view** for the area: what is normal, what usually drives it, what is fragile. Check `KB` calendar points, recent business events and known issues that could explain or distort the picture (SPEC 10 step 3).

4. **Frame from the evidence** (SPEC 10 step 4).
   - For a deliverable, or when the owner's escalation judgments mark the ask as high-stakes: a clean sub-agent reads the new evidence with no brain entries and reports what stands out.
   - Otherwise: compare the evidence with what the business view says is normal, and note what stands out.
   What stands out becomes input to the first questions.

5. **Pick the thinking pattern** for the situation. If none fits, say so, use the closest one with a caveat, and flag it in the handover note (SPEC 10 step 5).

6. **Run it** (SPEC 10 step 6). Ask its `first_questions`, watch its `suspicion_triggers`, test its `hypotheses_in_order` with the `checks` given, pulling data through validated metric definitions and checking with code. Stop when `stop_when` is met. Where no investigation-priority judgment sets the order, rank questions by relevance, materiality, uncertainty, information value, then feasibility. For each unlinked pair of numbers you touch, run a light cross-check (SPEC 8).

7. **Apply the judgments** at every decision point: materiality, classification, attribution, framing, inclusion, escalation, presentation. With no established cause-attribution judgment, state a cause only as attributed and unverified (SPEC 10 step 7).

8. **Check the dependency map:** what else this affects, and who else needs to know (SPEC 10 step 8).

9. **Respond** in the owner's style (`RS`). Word each point by its trust and sureness (SPEC 10 step 9, SPEC 7.1 and 7.2): established plainly, candidates with a caveat, inferred entries flagged. Contested entries are not used: say the situation is contested (SPEC 7.1). If performance and self-description entries disagree, show both (SPEC 6.2). Never put a figure in an entry; figures in the answer come from the data.

10. **Hand over** (SPEC 10 step 10). Attach the handover note below. Propose what was learned (confirmations, contradictions, new observations, story threads) to `brain/proposals/`. A correction from the owner goes through the `learn` skill.

**For a deliverable, also:** re-validate every metric definition it uses, follow its procedures step by step, and run every `self_checks` item before handover (SPEC 10).

## Stop and ask the owner first

Before responding, stop and ask if any condition in SPEC 10's stop-and-ask list holds. In short: a deciding step rests on an observation, contested, stale or inferred entry; a number does not reproduce; a material driver has no evidence; an escalation judgment fires; the impact scope needs an unrequested change; or no pattern fits and the stakes are high. Otherwise do not interrupt; put it in the handover note.

## Handover note (SPEC 14)

Attach to every answer:
- entries used that were candidates or inferred;
- every caveat added, and why;
- any escalation triggered;
- the impact scope: what else this affects and who should know;
- anything left blank rather than guessed, with its `Q` id.

## Final check

- [ ] Clearance filter applied before loading
- [ ] Readiness stated; insufficient asks stopped with a question
- [ ] Thinking pattern named, or "none fits" flagged
- [ ] Every cause worded per the attribution judgment
- [ ] Wording matches trust and sureness
- [ ] Handover note attached; write-backs proposed
