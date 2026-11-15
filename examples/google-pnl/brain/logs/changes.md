---
title: Change Log
description: Append-only log of every change applied to this brain, one line per change.
purpose: Audit trail of what changed, when, why and what caused it.
when_to_use: Open to audit a change. The applier appends to it and updates last_modified; never edit past lines.
last_modified: 2026-11-14
---

# Change log

One line per change (SPEC section 6.4):
`CH-<ULID> | date | entry | before | after | reason | caused_by`

CH-01KGP000000000000000000001 | 2026-11-14 | SRC-01KGP000000000000000000001 | none | created (artifact) | registers the source of every reported figure | v2 migration of the v1 example
CH-01KGP000000000000000000002 | 2026-11-14 | SRC-01KGP000000000000000000002 | none | created (artifact) | registers the working dataset that checks are run against | v2 migration of the v1 example
CH-01KGP000000000000000000003 | 2026-11-14 | SRC-01KGP000000000000000000003 | none | created (tool_contract) | registers what the data tool can and cannot establish | v2 migration of the v1 example
CH-01KGP000000000000000000004 | 2026-11-14 | SRC-01KGP000000000000000000004 | none | created (authority_rule) | says which source wins for reported figures | v2 migration of the v1 example
CH-01KGP000000000000000000005 | 2026-11-14 | SRC-01KGP000000000000000000005 | none | created (approved_location) | approves the example data folder | v2 migration of the v1 example
CH-01KGP000000000000000000006 | 2026-11-14 | SRC-01KGP000000000000000000006 | none | created (artifact) | pasted note walkthrough, SPEC 9.4 step 1 | pasted note
CH-01KGP000000000000000000007 | 2026-11-14 | KB-01KGP000000000000000000001 | none | created (concept) | concept from the v1 business understanding | v2 migration of the v1 example
CH-01KGP000000000000000000008 | 2026-11-14 | KB-01KGP000000000000000000002 | none | created (concept) | concept from the v1 business understanding | v2 migration of the v1 example
CH-01KGP000000000000000000009 | 2026-11-14 | KB-01KGP000000000000000000003 | none | created (concept) | concept from the v1 business understanding | v2 migration of the v1 example
CH-01KGP000000000000000000010 | 2026-11-14 | KB-01KGP000000000000000000004 | none | created (concept) | concept from the v1 business understanding | v2 migration of the v1 example
CH-01KGP000000000000000000011 | 2026-11-14 | KB-01KGP000000000000000000005 | none | created (metric_definition) | metric definition validated: segment operating income plus Alphabet-level activities equals reported consolidated operating income in all 12 quarters | v2 migration of the v1 example
CH-01KGP000000000000000000012 | 2026-11-14 | KB-01KGP000000000000000000006 | none | created (known_issue) | known issue split out of the v1 metric definition | v2 migration of the v1 example
CH-01KGP000000000000000000013 | 2026-11-14 | KB-01KGP000000000000000000007 | none | created (known_issue) | known issue split out of the v1 metric definition | v2 migration of the v1 example
CH-01KGP000000000000000000014 | 2026-11-14 | KB-01KGP000000000000000000008 | none | created (source_of_truth) | source of truth from the v1 authority rule | v2 migration of the v1 example
CH-01KGP000000000000000000015 | 2026-11-14 | KB-01KGP000000000000000000009 | none | created (deliverable_profile) | deliverable profile from the v1 Lens | v2 migration of the v1 example
CH-01KGP000000000000000000016 | 2026-11-14 | KB-01KGP000000000000000000010 | none | created (business_event) | registers the event for one quarter's release | v2 migration of the v1 example
CH-01KGP000000000000000000017 | 2026-11-14 | KB-01KGP000000000000000000011 | none | created (business_event) | registers the event for one quarter's release | v2 migration of the v1 example
CH-01KGP000000000000000000018 | 2026-11-14 | KB-01KGP000000000000000000012 | none | created (business_event) | registers the event for one quarter's release | v2 migration of the v1 example
CH-01KGP000000000000000000019 | 2026-11-14 | KB-01KGP000000000000000000013 | none | created (business_event) | registers the event for one quarter's release | v2 migration of the v1 example
CH-01KGP000000000000000000020 | 2026-11-14 | KB-01KGP000000000000000000014 | none | created (business_event) | registers the event for one quarter's release | v2 migration of the v1 example
CH-01KGP000000000000000000021 | 2026-11-14 | KB-01KGP000000000000000000015 | none | created (business_event) | registers the event for one quarter's release | v2 migration of the v1 example
CH-01KGP000000000000000000022 | 2026-11-14 | KB-01KGP000000000000000000016 | none | created (business_event) | registers the event for one quarter's release | v2 migration of the v1 example
CH-01KGP000000000000000000023 | 2026-11-14 | KB-01KGP000000000000000000017 | none | created (business_event) | registers the event for one quarter's release | v2 migration of the v1 example
CH-01KGP000000000000000000024 | 2026-11-14 | KB-01KGP000000000000000000018 | none | created (business_event) | registers the event for one quarter's release | v2 migration of the v1 example
CH-01KGP000000000000000000025 | 2026-11-14 | KB-01KGP000000000000000000019 | none | created (business_event) | registers the event for one quarter's release | v2 migration of the v1 example
CH-01KGP000000000000000000026 | 2026-11-14 | KB-01KGP000000000000000000020 | none | created (business_event) | registers the event for one quarter's release | v2 migration of the v1 example
CH-01KGP000000000000000000027 | 2026-11-14 | KB-01KGP000000000000000000021 | none | created (business_event) | registers the event for one quarter's release | v2 migration of the v1 example
CH-01KGP000000000000000000028 | 2026-11-14 | BV-01KGP000000000000000000001 | none | created (business_view, trust established) | normal range from the v1 Normality, established by cases with a data check | v2 migration of the v1 example
CH-01KGP000000000000000000029 | 2026-11-14 | BV-01KGP000000000000000000002 | none | created (business_view, trust established) | normal range from the v1 Normality, established by cases with a data check | v2 migration of the v1 example
CH-01KGP000000000000000000030 | 2026-11-14 | BV-01KGP000000000000000000003 | none | created (business_view, trust established) | normal range from the v1 Normality, established by cases with a data check | v2 migration of the v1 example
CH-01KGP000000000000000000031 | 2026-11-14 | BV-01KGP000000000000000000004 | none | created (business_view, trust established) | normal range from the v1 Normality, established by cases with a data check | v2 migration of the v1 example
CH-01KGP000000000000000000032 | 2026-11-14 | BV-01KGP000000000000000000005 | none | created (business_view, trust candidate) | pattern from v1 belief; candidate until the owner ratifies (SPEC 7.1) | v2 migration of the v1 example
CH-01KGP000000000000000000033 | 2026-11-14 | BV-01KGP000000000000000000006 | none | created (business_view, trust candidate) | pattern from v1 belief; candidate until the owner ratifies (SPEC 7.1) | v2 migration of the v1 example
CH-01KGP000000000000000000034 | 2026-11-14 | BV-01KGP000000000000000000007 | none | created (business_view, trust candidate) | pattern from v1 belief; candidate until the owner ratifies (SPEC 7.1) | v2 migration of the v1 example
CH-01KGP000000000000000000035 | 2026-11-14 | DM-01KGP000000000000000000001 | none | created (link, trust established) | v1 `constrains` link mapped to `offsets`, the v2 type the calculation supports | v2 migration of the v1 example
CH-01KGP000000000000000000036 | 2026-11-14 | DM-01KGP000000000000000000002 | none | created (link, trust established) | v1 `independent` link kept as `independent` | v2 migration of the v1 example
CH-01KGP000000000000000000037 | 2026-11-14 | TP-01KGP000000000000000000001 | none | created (thinking_pattern, trust observation) | placeholder from the v1 inquiry chain; never confirmed by a real owner | v2 migration of the v1 example
CH-01KGP000000000000000000038 | 2026-11-14 | JD-01KGP000000000000000000001 | none | created (judgment, trust observation) | placeholder from the v1 stopping rule; never confirmed by a real owner | v2 migration of the v1 example
CH-01KGP000000000000000000039 | 2026-11-14 | RS-01KGP000000000000000000001 | none | created (response_style, trust observation) | placeholder from the v1 editorial rule; never confirmed by a real owner | v2 migration of the v1 example
CH-01KGP000000000000000000040 | 2026-11-14 | PR-01KGP000000000000000000001 | none | created (procedure, trust observation) | procedure from the v1 Lens; never confirmed by a real owner | v2 migration of the v1 example
CH-01KGP000000000000000000041 | 2026-11-14 | TP-01KGP000000000000000000002 | none | created (thinking_pattern, trust established) | pasted note walkthrough, SPEC 9.4 step 3 | pasted note
CH-01KGP000000000000000000042 | 2026-11-14 | JD-01KGP000000000000000000002 | none | created (judgment, trust established) | pasted note walkthrough, SPEC 9.4 step 3 | pasted note
CH-01KGP000000000000000000043 | 2026-11-14 | JD-01KGP000000000000000000003 | none | created (judgment, trust established) | pasted note walkthrough, SPEC 9.4 step 3 | pasted note
CH-01KGP000000000000000000044 | 2026-11-14 | RS-01KGP000000000000000000002 | none | created (response_style, trust established) | pasted note walkthrough, SPEC 9.4 step 3 | pasted note
CH-01KGP000000000000000000045 | 2026-11-14 | Q-01KGP000000000000000000001 | none | created (question) | story thread from v1, now a watch question | v2 migration of the v1 example
CH-01KGP000000000000000000046 | 2026-11-14 | Q-01KGP000000000000000000002 | none | created (question) | pasted note walkthrough, SPEC 9.4 step 5 | pasted note
