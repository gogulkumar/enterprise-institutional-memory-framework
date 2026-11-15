#!/usr/bin/env python3
"""Validate a brain against SPEC v2 and regenerate its index.yaml.

Usage:
  python schemas/validate.py <brain dir> [--check] [--today YYYY-MM-DD]

--check validates without writing index.yaml; --today computes relevance as of a date.
Exits 1 if any problem is found; index.yaml is written only when everything passes.
"""
import argparse
import datetime as dt
import json
import pathlib
import re
import sys

import yaml
from jsonschema import Draft202012Validator
from referencing import Registry, Resource

HERE = pathlib.Path(__file__).resolve().parent
ULID = r"[0-9A-HJKMNP-TV-Z]{26}"
PREFIXES = ["BV", "TP", "JD", "RS", "KB", "DM", "PR", "SRC", "TR", "Q", "CH", "TS", "RN"]
ID_RE = re.compile(rf"^({'|'.join(PREFIXES)})-{ULID}$")
EVT_RE = re.compile(r"^EVT-(\d{4}(?:-Q[1-4]|-\d{2}(?:-\d{2})?)?)-[A-Za-z0-9][A-Za-z0-9_-]*$")
PROPOSAL_FILE_RE = re.compile(rf"^{ULID}\.yaml$")

# SPEC 6.5 kinds, and the SPEC 15.1 folder each prefix lives in.
KINDS = {
    "BV": {"business_view": "business-view"},
    "TP": {"thinking_pattern": "thinking-pattern"},
    "JD": {"judgment": "judgment"},
    "RS": {"response_style": "response-style"},
    "PR": {"procedure": "procedure"},
    "KB": {k: "kb-" + k.replace("_", "-") for k in [
        "concept", "metric_definition", "table_structure", "source_of_truth", "business_event", "known_issue",
        "calendar_point", "deliverable_profile", "template"]},
    "DM": {"link": "dm-link", "impact_scope": "dm-impact-scope"},
    "SRC": {k: "src-" + k.replace("_", "-") for k in ["artifact", "approved_location", "tool_contract", "authority_rule"]},
    "TR": {"trace": "log-trace"},
    "Q": {"question": "log-question"},
    "TS": {"scenario": "log-scenario"},
    "RN": {"test_run": "log-test-run"},
}
FOLDERS = {
    "BV": "reasoning/business-view", "TP": "reasoning/thinking-patterns", "JD": "reasoning/judgments",
    "RS": "reasoning/response-style", "KB": "knowledge", "DM": "dependency-map", "PR": "procedures",
    "SRC": "sources", "TR": "logs/traces", "Q": "logs/questions", "TS": "tests/scenarios", "RN": "tests/runs",
}
REASONING = {"BV", "TP", "JD", "RS"}
GOVERNED = REASONING | {"PR", "DM"}
TIMED = GOVERNED | {"KB"}
INDEXED = GOVERNED | {"KB", "SRC"}  # logs and held-out tests are never loaded for reasoning
TRUST_RANK = {"observation": 0, "candidate": 1, "established": 2}
DEFAULT_CONFIG = {
    "owner": "", "candidate_events": 2, "established_events": 4, "established_periods": 2, "observation_expiry": 2,
    "sensitivity_levels": ["public", "internal", "confidential", "restricted"], "period_length": "1q",
    "review_windows": {},
}
DEFAULT_WINDOWS = {  # SPEC 7.3
    "metric_definition": "period", "known_issue": "period", "source_of_truth": "period", "calendar_point": "period",
    "judgment": "4q", "thinking_pattern": "4q", "response_style": "4q", "business_view": "4q",
    "link": "4q", "impact_scope": "4q", "business_event": "none", "default": "4q",
}
DAYS = {"d": 1, "w": 7, "m": 30, "q": 91, "y": 365}


def load_validators():
    schemas = {p.name: json.loads(p.read_text()) for p in HERE.glob("*.schema.json")}
    registry = Registry().with_resources((n, Resource.from_contents(s)) for n, s in schemas.items())
    return {n[: -len(".schema.json")]: Draft202012Validator(s, registry=registry) for n, s in schemas.items()}


def plain(value):
    """YAML turns unquoted dates into date objects; schemas expect strings."""
    if isinstance(value, (dt.date, dt.datetime)):
        return value.isoformat()
    if isinstance(value, dict):
        return {k: plain(v) for k, v in value.items()}
    if isinstance(value, list):
        return [plain(v) for v in value]
    return value


def load_yaml(path):
    with open(path, encoding="utf-8") as f:
        return plain(yaml.safe_load(f))


def window_days(window, config):
    if window in (None, "none"):
        return None
    if window == "period":
        window = config["period_length"]
    return int(window[:-1]) * DAYS[window[-1]]


def to_date(value):
    try:
        return dt.date.fromisoformat(str(value)[:10])
    except ValueError:
        return None


def relevance(entry, today, config):
    """SPEC 7.3: historical once valid_to is set; otherwise by age against the review window."""
    if entry.get("valid_to"):
        return "historical"
    kind = entry["kind"]
    windows = {**DEFAULT_WINDOWS, **(config.get("review_windows") or {})}
    days = window_days(entry.get("review_window") or windows.get(kind, windows["default"]), config)
    if days is None:
        return "current"
    dates = [to_date(entry.get("last_supported")), to_date(entry.get("last_confirmed_by_owner"))]
    dates = [d for d in dates if d] or [to_date(entry.get("recorded_at"))]
    age = (today - max(d for d in dates if d)).days
    if age > days:
        return "stale"
    return "aging" if age > days / 2 else "current"


def walk_strings(value, skip_keys=()):
    if isinstance(value, str):
        yield value
    elif isinstance(value, dict):
        for k, v in value.items():
            if k not in skip_keys:
                yield from walk_strings(v, skip_keys)
    elif isinstance(value, list):
        for v in value:
            yield from walk_strings(v, skip_keys)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("brain")
    ap.add_argument("--check", action="store_true", help="validate without writing index.yaml")
    ap.add_argument("--today", help="compute relevance as of this date (YYYY-MM-DD)")
    args = ap.parse_args()
    brain = pathlib.Path(args.brain)
    today = dt.date.fromisoformat(args.today) if args.today else dt.date.today()
    validators = load_validators()
    problems, warnings = [], []

    def bad(where, msg):
        problems.append(f"{where}: {msg}")

    def warn(where, msg):
        warnings.append(f"{where}: {msg}")

    config = dict(DEFAULT_CONFIG)
    if (brain / "config.yaml").exists():
        config.update({k: v for k, v in (load_yaml(brain / "config.yaml") or {}).items() if v is not None})
    levels = config["sensitivity_levels"]
    owner = (config.get("owner") or "").strip()

    # 1. Load every entry and check its place and schema.
    entries = {}
    for prefix, folder in FOLDERS.items():
        root = brain / folder
        if not root.exists():
            continue
        for path in sorted(root.rglob("*.yaml")):
            rel = path.relative_to(brain)
            data = load_yaml(path)
            if not isinstance(data, dict):
                bad(rel, "not a YAML mapping")
                continue
            eid = data.get("id", "")
            if not ID_RE.match(str(eid)):
                bad(rel, f"id {eid!r} is not <prefix>-<ULID>")
                continue
            if eid.split("-")[0] != prefix:
                bad(rel, f"a {eid.split('-')[0]} entry does not belong in {folder}/")
            if path.stem != eid:
                bad(rel, f"file name must be {eid}.yaml")
            kind = data.get("kind")
            if kind is None:
                bad(rel, "missing `kind` (SPEC 6.5)")
                continue
            schema = KINDS[prefix].get(kind)
            if schema is None:
                bad(rel, f"kind {kind!r} is not allowed for prefix {prefix} (SPEC 6.5)")
                continue
            for err in sorted(validators[schema].iter_errors(data), key=lambda e: list(e.path)):
                bad(rel, f"{'/'.join(map(str, err.path)) or '(entry)'}: {err.message}")
            if eid in entries:
                bad(rel, f"duplicate id {eid} (also {entries[eid]['_file']})")
            data["_file"] = str(rel)
            entries[eid] = data

    # 1b. The archive (SPEC 6.5, 15.1): `<id>.yaml` or `<id>.v<n>.yaml`, schema-checked, kept out of the index.
    archived = set()
    arch_re = re.compile(rf"^((?:{'|'.join(PREFIXES)})-{ULID})(?:\.v\d+)?\.yaml$")
    for path in sorted((brain / "archive").rglob("*.yaml")) if (brain / "archive").exists() else []:
        rel = path.relative_to(brain)
        m = arch_re.match(path.name)
        data = load_yaml(path)
        if not m or not isinstance(data, dict) or data.get("id") != m.group(1):
            bad(rel, "an archived entry is named `<id>.yaml` or `<id>.v<n>.yaml` and keeps its id")
            continue
        schema = KINDS.get(m.group(1).split("-")[0], {}).get(data.get("kind"))
        if schema is None:
            bad(rel, f"kind {data.get('kind')!r} is not allowed for this prefix (SPEC 6.5)")
            continue
        for err in validators[schema].iter_errors(data):
            bad(rel, f"{'/'.join(map(str, err.path)) or '(entry)'}: {err.message}")
        archived.add(m.group(1))

    # 1c. Nothing outside the SPEC 15.1 layout.
    allowed_top = {"config.yaml", "index.yaml", "match_ledger.yaml", ".applier.lock", "README.md", "sources", "reasoning",
                   "knowledge", "dependency-map", "procedures", "tests", "logs", "proposals", "passes", "archive"}
    for p in sorted(brain.iterdir()) if brain.exists() else []:
        if p.name not in allowed_top and not p.name.startswith("."):
            bad(p.name, "not part of the brain layout (SPEC 15.1)")
    loaded = {e["_file"] for e in entries.values()}
    for path in sorted(brain.rglob("*.yaml")):
        rel = path.relative_to(brain)
        top = rel.parts[0]
        if top in ("archive", "proposals", "passes") or str(rel) in ("config.yaml", "index.yaml", "match_ledger.yaml"):
            continue
        if str(rel) not in loaded and not any(str(rel).startswith(f + "/") and str(rel) in loaded for f in FOLDERS.values()):
            if not str(rel).startswith("logs/reports/"):
                bad(rel, "unexpected file: entries live in their store's folder, named by id (SPEC 15.1)")

    # 2. Event registry (SPEC 6.3, 7.1).
    registry = {}
    for e in entries.values():
        if e.get("kind") == "business_event" and e.get("event_id"):
            if e["event_id"] in registry:
                bad(e["_file"], f"event {e['event_id']} is registered twice (also {registry[e['event_id']]['_file']})")
            registry[e["event_id"]] = e
    events = [e for e in entries.values() if e.get("kind") == "business_event"]
    for i, a in enumerate(events):
        for b in events[i + 1:]:
            if a.get("affected") and set(a.get("periods", [])) == set(b.get("periods", [])) \
                    and set(a.get("affected", [])) == set(b.get("affected", [])):
                bad(b["_file"], f"possible duplicate event: {b.get('event_id')} has the same period and affected "
                                f"metrics as {a.get('event_id')}; one event may not be split into several ids")

    # 3. References: every id-shaped or EVT-shaped string must resolve.
    for eid, e in entries.items():
        skip = ("id", "event_id") if e.get("kind") == "business_event" else ("id",)
        for s in walk_strings({k: v for k, v in e.items() if k != "_file"}, skip):
            if ID_RE.match(s) and s not in entries and s not in archived:
                bad(e["_file"], f"refers to {s}, which does not exist")
            if EVT_RE.match(s) and s not in registry:
                bad(e["_file"], f"event {s} is not registered by any business event")

    # 4. Sensitivity never lower than its sources (SPEC 12.3).
    def level(x):
        return levels.index(x) if x in levels else None

    for e in entries.values():
        if level(e.get("sensitivity")) is None:
            bad(e["_file"], f"sensitivity {e.get('sensitivity')!r} is not in config sensitivity_levels")
            continue
        for src in e.get("provenance", []) or []:
            s = entries.get(src)
            if s and level(s.get("sensitivity")) is not None and level(s["sensitivity"]) > level(e["sensitivity"]):
                bad(e["_file"], f"sensitivity {e['sensitivity']} is lower than its source {src} ({s['sensitivity']})")

    # 5. Trust rules (SPEC 7.1, 7.2).
    for e in entries.values():
        if e["_file"].split("/")[0] not in ("reasoning", "procedures", "dependency-map"):
            continue
        prefix = e["id"].split("-")[0]
        if prefix not in GOVERNED:
            continue
        trust, sureness = e.get("trust"), e.get("sureness")
        evts = set(e.get("events") or [])
        periods = {EVT_RE.match(x).group(1) for x in evts if EVT_RE.match(x)}
        confirmed = str(e.get("last_confirmed_by_owner", "never")) != "never"
        prov = e.get("provenance") or []
        owner_marks = [str(p)[len("owner:"):] for p in prov if str(p).startswith("owner:")]
        if owner and any(m != owner for m in owner_marks):
            bad(e["_file"], f"provenance names an owner other than the configured owner {owner!r}")
        owner_sourced = (bool(owner_marks) and (not owner or all(m == owner for m in owner_marks))) or (
            bool(owner) and any(entries.get(p, {}).get("author") == owner for p in prov))
        if sureness == "stated" and not owner_sourced:
            bad(e["_file"], "sureness is `stated` but no provenance is the owner or a text the owner authored")
        owner_word = (sureness == "stated" and owner_sourced) or confirmed
        window = window_days(e.get("review_window") or {**DEFAULT_WINDOWS, **(config.get("review_windows") or {})}.get(
            e["kind"], DEFAULT_WINDOWS["default"]), config)
        last = max([d for d in (to_date(e.get("last_supported")), to_date(e.get("recorded_at"))) if d], default=today)
        if trust == "observation":
            limit = config["observation_expiry"] * window_days("period", config)
            if (today - last).days > limit:
                bad(e["_file"], f"observation unsupported for over {config['observation_expiry']} periods; retire it (SPEC 7.1)")
        if trust == "replaced" and not e.get("valid_to"):
            bad(e["_file"], "a `replaced` entry needs `valid_to`, the date the newer version takes over (SPEC 7.1)")
        if trust == "retired":
            bad(e["_file"], "a `retired` entry belongs in archive/ (SPEC 7.1)")
        if trust == "contested" and window and (today - last).days > window:
            warn(e["_file"], "contested for longer than one review window; put it at the top of the next report (SPEC 7.1)")
        rank = TRUST_RANK.get(trust)
        if rank is None:
            continue
        if rank > 0 and not owner_sourced and not confirmed and sureness != "checked":
            bad(e["_file"], f"trust `{trust}` rests only on other people's work, which can support an entry "
                            "up to `observation` unless it is checked against the data (SPEC 7.1)")
        if trust == "candidate" and len(evts) < config["candidate_events"] and not owner_word:
            bad(e["_file"], f"`candidate` needs {config['candidate_events']} independent events or the owner's word; "
                            f"it has {len(evts)}")
        if trust == "established":
            calc_link = e.get("kind") == "link" and e.get("type") == "calculated_from" and sureness == "checked"
            spread = max(len(periods), len(set((e.get("scope") or {}).get("situations") or [])))
            by_cases = (len(evts) >= config["established_events"] and spread >= config["established_periods"]
                        and sureness == "checked")
            if sureness == "inferred" and not confirmed:
                bad(e["_file"], "an entry supported only by inference cannot be `established` until the owner "
                                "confirms it (SPEC 7.1)")
            elif not (owner_word or by_cases or calc_link):
                bad(e["_file"], f"`established` needs the owner's word, or {config['established_events']} events across "
                                f"{config['established_periods']} periods with a data check; it has {len(evts)} events "
                                f"across {len(periods)} periods, sureness `{sureness}`")
            if e.get("kind") == "business_view" and e.get("origin") == "pattern" and not confirmed:
                bad(e["_file"], "a pattern-origin business view needs the owner's ratification before `established`")

    # 6. Proposals, the match ledger and the change log.
    for path in sorted((brain / "proposals").rglob("*.yaml")) if (brain / "proposals").exists() else []:
        rel = path.relative_to(brain)
        if not PROPOSAL_FILE_RE.match(path.name):
            bad(rel, "a proposal file is named by a bare ULID")
        data = load_yaml(path)
        errs = list(validators["proposal"].iter_errors(data))
        for err in errs:
            bad(rel, f"{'/'.join(map(str, err.path)) or '(proposal)'}: {err.message}")
        if errs or not isinstance(data, dict):
            continue
        # The payload must fit the target's schema (SPEC 12.1): a full entry for create, merged fields otherwise.
        target, payload = str(data.get("target", "")), dict(data.get("payload") or {})
        meta = {k: payload.pop(k) for k in ("pass_id", "ledger_kind", "gates", "note") if k in payload}
        prefix = target.split("-")[0]
        if data.get("action") == "create":
            candidate = dict(payload, id=payload.get("id") or f"{prefix}-{'0' * 26}")
        elif target in entries:
            candidate = {k: v for k, v in {**entries[target], **payload}.items() if k != "_file"}
        else:
            bad(rel, f"target {target} does not exist")
            continue
        schema = KINDS.get(prefix, {}).get(candidate.get("kind"))
        if schema is None:
            bad(rel, f"payload kind {candidate.get('kind')!r} is not allowed for {prefix} (SPEC 6.5)")
            continue
        for err in validators[schema].iter_errors(plain(candidate)):
            bad(rel, f"payload {'/'.join(map(str, err.path)) or '(entry)'}: {err.message}")
    if (brain / "match_ledger.yaml").exists():
        rows = load_yaml(brain / "match_ledger.yaml") or []
        if not isinstance(rows, list):
            bad("match_ledger.yaml", "must be a list of rows")
            rows = []
        for i, row in enumerate(rows):
            for err in validators["match-ledger-row"].iter_errors(row):
                bad("match_ledger.yaml", f"row {i + 1}: {err.message}")
            if isinstance(row, dict) and row.get("matched_entry") and row["matched_entry"] not in entries:
                bad("match_ledger.yaml", f"row {i + 1}: matched_entry {row['matched_entry']} does not exist")
    changes = brain / "logs" / "changes.md"
    if changes.exists():
        text = changes.read_text(encoding="utf-8")
        body = text.split("\n---\n", 1)[1] if text.startswith("---\n") and "\n---\n" in text else text
        seen_change = False
        for n, line in enumerate(body.splitlines(), 1):
            s = line.strip()
            if not s or s.startswith("#"):
                continue
            if not s.startswith("CH"):
                if seen_change:  # prose is allowed only in the header, before the first change line
                    bad("logs/changes.md", f"line {n}: not a change line")
                continue
            seen_change = True
            fields = [f.strip() for f in s.split("|")]
            if len(fields) != 7 or not re.match(rf"^CH-{ULID}$", fields[0]) or not to_date(fields[1]):
                bad("logs/changes.md", f"line {n}: must be `CH-<ULID> | date | entry | before | after | reason | caused_by`")
            elif fields[2] not in entries and fields[2] not in archived:
                bad("logs/changes.md", f"line {n}: entry {fields[2]} does not exist")

    if problems:
        print(f"FAIL {brain}: {len(problems)} problem(s)")
        for p in problems:
            print("  " + p)
        return 1

    # 7. Index (SPEC 15.3).
    rows, situations, deliverables, metrics = [], {}, {}, {}
    for eid, e in sorted(entries.items()):
        prefix = eid.split("-")[0]
        if prefix not in INDEXED:
            continue
        row = {"id": eid, "kind": e["kind"], "file": e["_file"], "sensitivity": e["sensitivity"]}
        if "scope" in e:
            row["scope"] = e["scope"]
        if prefix in GOVERNED:
            row.update(trust=e.get("trust"), sureness=e.get("sureness"))
        if prefix in TIMED:
            row["relevance"] = relevance(e, today, config)
        rows.append(row)

        def add(situation, key):
            situations.setdefault(situation, {"thinking_patterns": [], "business_views": [], "judgments": [],
                                              "response_styles": []})[key].append(eid)

        key = {"TP": "thinking_patterns", "BV": "business_views", "JD": "judgments", "RS": "response_styles"}.get(prefix)
        if key:
            names = set((e.get("scope") or {}).get("situations") or [])
            if prefix in ("TP", "RS") and e.get("situation"):
                names.add(e["situation"])
            for s in sorted(names):
                add(s, key)
                if prefix == "TP":
                    for j in e.get("judgments_applied") or []:
                        if j not in situations[s]["judgments"]:
                            situations[s]["judgments"].append(j)
                    for r in e.get("related") or []:
                        if r.startswith("BV-") and r not in situations[s]["business_views"]:
                            situations[s]["business_views"].append(r)
    for e in entries.values():
        if e.get("kind") == "deliverable_profile":
            inputs = list(e.get("inputs", []))
            for pid in e.get("procedures", []):
                inputs += [i for i in entries.get(pid, {}).get("inputs", []) or [] if i not in inputs]
            deliverables[e["name"]] = {
                "profile": e["id"], "procedures": e.get("procedures", []),
                "metric_definitions": [i for i in inputs if entries.get(i, {}).get("kind") == "metric_definition"],
                "scoped_entries": sorted(x["id"] for x in entries.values()
                                         if e["name"] in ((x.get("scope") or {}).get("deliverables") or [])),
            }
    for e in entries.values():
        if e.get("kind") == "metric_definition":
            mid = e["id"]
            metrics[e["name"]] = {
                "definition": mid,
                "links": sorted(x["id"] for x in entries.values() if x.get("kind") == "link" and mid in (x.get("from"), x.get("to"))),
                "used_in": sorted(x["id"] for x in entries.values()
                                  if x.get("kind") in ("procedure", "deliverable_profile") and mid in (x.get("inputs") or [])),
                "known_issues": sorted(x["id"] for x in entries.values()
                                       if x.get("kind") == "known_issue" and mid in (x.get("affects") or [])),
            }
    index = {"generated": today.isoformat(), "situations": situations, "deliverables": deliverables,
             "metrics": metrics, "entries": rows}
    header = (
        "# Generated by schemas/validate.py. Do not edit by hand (SPEC 15.3).\n"
        "# Drop entries above the requester's clearance first, then load in this order: the situation's thinking\n"
        "# pattern and response style; the business view and judgments; for a deliverable its profile and procedures;\n"
        "# metric definitions and known issues; dependency links and impact scope.\n"
    )
    if not args.check:
        with open(brain / "index.yaml", "w", encoding="utf-8") as f:
            f.write(header)
            yaml.safe_dump(index, f, sort_keys=False, allow_unicode=True, width=120)
    print(f"OK {brain}: {len(entries)} entries, {len(registry)} events"
          + ("" if args.check else ", index.yaml regenerated"))
    for w in warnings:
        print("  warning: " + w)
    return 0


if __name__ == "__main__":
    sys.exit(main())
