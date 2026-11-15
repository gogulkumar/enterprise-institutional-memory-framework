"""Deterministic operational pipeline for the Enterprise Institutional Memory Framework.

Why this file exists:
  The AI agent is meant to spend its reasoning on understanding the business,
  spotting patterns, and answering questions honestly—not on file-locking,
  generating 26-character ULIDs, computing SHA-256 hashes, or scanning large
  YAML indexes by hand.

  This module handles the deterministic mechanics of the brain's lifecycle:
    1. `ulid` — Mint valid IDs for new entries and Learn passes.
    2. `seal` / — Lock a Learn pass's prediction before the blind read,
       `verify-seal` then prove it was not edited before comparing against reality.
    3. `apply` — Run the single Applier over `brain/proposals/`: apply
                       approved updates, park human-ratification items, log to
                       `logs/changes.md`, and regenerate `index.yaml`.
    4. `query` — Filter `brain/index.yaml` by clearance, situation,
                       deliverable, or metric so the agent loads only what
                       the current task needs—even as the brain scales.

Usage:
  python3 pipelines/brain.py ulid
  python3 pipelines/brain.py seal <pass_dir>
  python3 pipelines/brain.py verify-seal <pass_dir>
  python3 pipelines/brain.py apply <brain_dir> [--today YYYY-MM-DD]
  python3 pipelines/brain.py query <brain_dir> [--clearance <level>] [--situation <name>] [--deliverable <name>] [--metric <name>] [--include-observations]
"""
import argparse
import datetime as dt
import hashlib
import os
import pathlib
import secrets
import shutil
import subprocess
import sys
import time
import tempfile
import copy
import importlib.util

# Crockford Base32 alphabet used for all framework ULIDs (excludes I, L, O, U to avoid ambiguity).
CROCKFORD = "0123456789ABCDEFGHJKMNPQRSTVWXYZ"

# Maps each entry ID prefix to its home folder inside a `brain/` directory.
# Keeping this mapping in code guarantees proposals always land in the right component folder.
FOLDERS = {
    "BV": "reasoning/business-view",
    "TP": "reasoning/thinking-patterns",
    "JD": "reasoning/judgments",
    "RS": "reasoning/response-style",
    "KB": "knowledge",
    "DM": "dependency-map",
    "PR": "procedures",
    "SRC": "sources",
    "TR": "logs/traces",
    "Q": "logs/questions",
    "TS": "tests/scenarios",
    "RN": "tests/runs",
}

# Locate `schemas/validate.py` relative to the repository root so the Applier can
# validate the entire brain and regenerate `index.yaml` after applying changes.
REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent
VALIDATE_PY = REPO_ROOT / "schemas" / "validate.py"


def make_ulid() -> str:
    """Generate a 26-character Crockford Base32 ULID (48-bit timestamp + 80-bit randomness)."""
    ts_ms = int(time.time() * 1000) # Millisecond timestamp keeps IDs roughly sortable by creation time.
    rand_bits = secrets.randbits(80) # Cryptographic randomness prevents collisions across parallel passes.
    val = (ts_ms << 80) | rand_bits # Pack 128 bits into one integer.
    chars = []
    for _ in range(26): # Extract 26 5-bit chunks from least-significant to most-significant.
        chars.append(CROCKFORD[val & 31])
        val >>= 5
    return "".join(reversed(chars)) # Reverse so timestamp characters come first.


def cmd_ulid(_args) -> int:
    """Print a fresh ULID so the agent never invents malformed IDs."""
    print(make_ulid())
    return 0


def cmd_seal(args) -> int:
    """Seal a Learn pass's prediction before the clean sub-agent performs its blind read."""
    pass_dir = pathlib.Path(args.pass_dir)
    pred = pass_dir / "prediction.yaml"
    if not pred.exists():
        print(f"ERROR: {pred} not found", file=sys.stderr)
        return 1
    # Hash the exact bytes of prediction.yaml so any post-hoc edit is immediately detectable.
    digest = hashlib.sha256(pred.read_bytes()).hexdigest()
    (pass_dir / "prediction.sha256").write_text(digest + "\n")
    print(f"Sealed {pred} -> {digest}")
    return 0


def cmd_verify_seal(args) -> int:
    """Verify prediction.yaml against prediction.sha256 before comparing prediction vs. blind read."""
    pass_dir = pathlib.Path(args.pass_dir)
    pred = pass_dir / "prediction.yaml"
    seal = pass_dir / "prediction.sha256"
    if not pred.exists() or not seal.exists():
        print("ERROR: prediction.yaml or prediction.sha256 missing", file=sys.stderr)
        return 1
    expected = seal.read_text().strip()
    actual = hashlib.sha256(pred.read_bytes()).hexdigest()
    if actual != expected:
        print(f"FAIL: seal mismatch (expected {expected}, got {actual})", file=sys.stderr)
        return 1
    print(f"OK: seal verified ({actual})")
    return 0


def _require_yaml():
    """Import PyYAML lazily so stdlib-only commands (`ulid`, `seal`, `verify-seal`) work anywhere."""
    try:
        import yaml # noqa: F401
        return yaml
    except ImportError:
        print("ERROR: pyyaml is required for this command (pip install pyyaml jsonschema)", file=sys.stderr)
        sys.exit(1)


def _find_entry_file(brain: pathlib.Path, entry_id: str) -> pathlib.Path | None:
    """Resolve an entry ID (e.g., BV-01... or PR-01...) to its YAML file path inside `brain/`."""
    prefix = entry_id.split("-")[0]
    folder = FOLDERS.get(prefix)
    if not folder:
        return None
    root = brain / folder
    direct = root / f"{entry_id}.yaml"
    if direct.exists():
        return direct
    # Support nested deliverable subfolders (e.g., procedures/quarterly-pnl-review/PR-....yaml).
    matches = list(root.rglob(f"{entry_id}.yaml"))
    return matches[0] if matches else None


def _append_changelog(brain, today, prop_id, action, target, ratified_by):
    """Write the v2 CH format; preserve the exact proposal as the change source."""
    path = brain / "logs" / "changes.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    line = f"CH-{make_ulid()} | {today} | {target} | before {action} | after {action} | {ratified_by} | {prop_id}\n"
    text = path.read_text() if path.exists() else ""
    import re
    text = re.sub(r'(last_modified:)[^\n]*', lambda m: m[1] + ' "' + today + '"', text, count=1)
    path.write_text(text + line)


def _apply_one_proposal(brain, prop, today, yaml):
    """Apply v2 fields only. The caller validates the complete staged batch."""
    action, target = prop["action"], prop["target"]
    payload = dict(prop.get("payload") or {})
    for key in ("pass_id", "ledger_kind", "gates", "note"):
        payload.pop(key, None)
    if action == "create":
        prefix = target.split("-")[0]
        new_id = payload.get("id") or (f"{prefix}-{make_ulid()}" if target.endswith("-new") else target)
        if not target.endswith("-new") and new_id != target:
            raise ValueError("create payload id differs from target")
        if _find_entry_file(brain, new_id):
            raise ValueError(f"create would overwrite existing entry {new_id}")
        entry = dict(payload, id=new_id)
        entry.setdefault("recorded_at", today + "T00:00:00Z")
        dest = brain / FOLDERS[prefix] / f"{new_id}.yaml"
    else:
        dest = _find_entry_file(brain, target)
        if dest is None:
            raise ValueError(f"target {target} not found")
        previous = yaml.safe_load(dest.read_text())
        entry = copy.deepcopy(previous)
        entry.update(payload)
        entry["id"] = target
        entry["version"] = previous["version"] + 1
        entry["recorded_at"] = today + "T00:00:00Z"
        if action == "contradict":
            entry["trust"] = "contested"
        elif action == "retire":
            entry["trust"] = "retired"
        # Only positive confirmations count as supporting events, never contradictions.
        if action == "confirm":
            if "last_supported" in entry:
                entry["last_supported"] = today
            if "events" in entry:
                entry["events"] = list(dict.fromkeys(entry["events"] + [e["event_id"] for e in prop["evidence"] if e.get("event_id")]))
        arch = brain / "archive" / f"{target}.v{previous['version']}.yaml"
        arch.parent.mkdir(parents=True, exist_ok=True)
        historical = dict(previous)
        if "valid_from" in historical and historical.get("valid_to") is None:
            historical["valid_to"] = today
        arch.write_text(yaml.safe_dump(historical, sort_keys=False, allow_unicode=True))
        if action == "retire":
            dest.unlink()
            dest = brain / "archive" / f"{target}.yaml"
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(yaml.safe_dump(entry, sort_keys=False, allow_unicode=True))
    return entry["id"]


def _is_pid_alive(pid: int) -> bool:
    """Return True if a process with `pid` is still running on this host."""
    try:
        os.kill(pid, 0)
        return True
    except ProcessLookupError:
        return False
    except PermissionError:
        return True


def cmd_apply(args):
    """Validate a staged proposal batch before publishing any memory changes."""
    yaml = _require_yaml()
    brain = pathlib.Path(args.brain_dir).resolve()
    today = args.today or dt.date.today().isoformat()
    lock = brain / ".applier.lock"
    try:
        with lock.open("x") as f:
            f.write(f"pid={os.getpid()} started={today}\n")
    except FileExistsError:
        print(f"ERROR: applier lock exists: {lock}", file=sys.stderr)
        return 1
    try:
        spec = importlib.util.spec_from_file_location("brain_validation", VALIDATE_PY)
        validation = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(validation)
        validators = validation.load_validators()
        props = sorted((brain / "proposals").glob("*.yaml"))
        if not props:
            print("No automatic proposals queued; pending approvals remain pending.")
            return 0
        with tempfile.TemporaryDirectory(prefix="brain-apply-") as tmp:
            stage = pathlib.Path(tmp) / "brain"
            shutil.copytree(brain, stage, ignore=shutil.ignore_patterns(".applier.lock"))
            applied = parked = 0
            for original in props:
                prop_path = stage / "proposals" / original.name
                prop = validation.load_yaml(prop_path)
                errors = list(validators["proposal"].iter_errors(prop))
                if errors:
                    raise ValueError(f"{original.name}: " + errors[0].message)
                action = prop["action"]
                # Never trust a false needs_ratification flag to bypass high-stakes review.
                high_stakes = action in {"replace", "redefine", "demote", "retire", "promote"}
                if prop["needs_ratification"] or high_stakes:
                    dest = stage / "proposals" / "pending" / original.name
                    dest.parent.mkdir(parents=True, exist_ok=True)
                    prop_path.replace(dest)
                    parked += 1
                    continue
                final = _apply_one_proposal(stage, prop, today, yaml)
                pass_id = (prop.get("payload") or {}).get("pass_id")
                if not isinstance(pass_id, str) or not pass_id.startswith("LP-"):
                    pass_id = "LP-" + make_ulid()
                dest = stage / "passes" / pass_id / "applied" / original.name
                dest.parent.mkdir(parents=True, exist_ok=True)
                prop_path.replace(dest)
                _append_changelog(stage, today, original.stem, action, final, "auto")
                applied += 1
            result = subprocess.run([sys.executable, str(VALIDATE_PY), str(stage), "--today", today], capture_output=True, text=True)
            if result.returncode:
                raise ValueError(result.stdout + result.stderr)
            # All mutations passed the same validator used by the repository; preserve non-entry files.
            for path in stage.rglob("*"):
                if path.is_file():
                    dest = brain / path.relative_to(stage)
                    dest.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(path, dest)
            for original in props:
                if not (stage / "proposals" / original.name).exists():
                    original.unlink(missing_ok=True)
            print(f"Applied={applied}, pending={parked}; complete staged brain validated.")
        return 0
    except Exception as exc:
        print(f"ERROR: batch left unapplied: {exc}", file=sys.stderr)
        return 1
    finally:
        lock.unlink(missing_ok=True)


def cmd_query(args) -> int:
    """Filter `brain/index.yaml` by clearance, situation, deliverable, or metric so Think loads only what it needs."""
    yaml = _require_yaml()
    brain = pathlib.Path(args.brain_dir)
    config = yaml.safe_load((brain / "config.yaml").read_text()) or {}
    levels = config.get("sensitivity_levels") or ["public", "internal", "confidential", "restricted"]

    # Determine requester's maximum allowed sensitivity rank (defaults to highest if omitted).
    clearance = args.clearance or levels[-1]
    if clearance not in levels:
        print(f"ERROR: unknown clearance '{clearance}' (valid: {levels})", file=sys.stderr)
        return 1
    max_level_idx = levels.index(clearance)

    idx = yaml.safe_load((brain / "index.yaml").read_text()) or {}

    # First pass: drop every entry above requester clearance, and hide unconfirmed `observation`s by default.
    allowed = {}
    for row in idx.get("entries") or []:
        sens = row.get("sensitivity", levels[0])
        if sens in levels and levels.index(sens) > max_level_idx:
            continue
        if row.get("trust") == "observation" and not args.include_observations:
            continue
        allowed[row["id"]] = row

    # Second pass: return only the slices of `index.yaml` matching the requested situation, deliverable, or metric.
    result = {"clearance": clearance}
    if args.situation:
        sit = (idx.get("situations") or {}).get(args.situation, {})
        result["situation"] = {
            k: [allowed[eid] for eid in eids if eid in allowed]
            for k, eids in sit.items()
        }
    if args.deliverable:
        deliv = (idx.get("deliverables") or {}).get(args.deliverable, {})
        filtered = {}
        for k, v in deliv.items():
            if isinstance(v, list):
                filtered[k] = [allowed[eid] for eid in v if eid in allowed]
            elif isinstance(v, str) and v in allowed:
                filtered[k] = allowed[v]
        result["deliverable"] = filtered
    if args.metric:
        met = (idx.get("metrics") or {}).get(args.metric, {})
        filtered = {}
        for k, v in met.items():
            if isinstance(v, list):
                filtered[k] = [allowed[eid] for eid in v if eid in allowed]
            elif isinstance(v, str) and v in allowed:
                filtered[k] = allowed[v]
        result["metric"] = filtered
    if not (args.situation or args.deliverable or args.metric):
        result["entries"] = list(allowed.values())

    print(yaml.safe_dump(result, sort_keys=False, allow_unicode=True))
    return 0


def main() -> int:
    """CLI entrypoint dispatching `ulid`, `seal`, `verify-seal`, `apply`, and `query`."""
    ap = argparse.ArgumentParser(description="Operational pipeline CLI for Institutional Memory brains")
    sub = ap.add_subparsers(dest="cmd", required=True)

    sub.add_parser("ulid", help="Generate a 26-char Crockford Base32 ULID")

    p_seal = sub.add_parser("seal", help="Write prediction.sha256 for a Learn pass")
    p_seal.add_argument("pass_dir")

    p_vseal = sub.add_parser("verify-seal", help="Verify prediction.yaml against prediction.sha256")
    p_vseal.add_argument("pass_dir")

    p_apply = sub.add_parser("apply", help="Run the single Applier over brain/proposals/")
    p_apply.add_argument("brain_dir")
    p_apply.add_argument("--today", help="Override date YYYY-MM-DD")

    p_query = sub.add_parser("query", help="Query brain/index.yaml by clearance, situation, deliverable, or metric")
    p_query.add_argument("brain_dir")
    p_query.add_argument("--clearance", help="Requester sensitivity clearance")
    p_query.add_argument("--situation", help="Situation name from index.yaml")
    p_query.add_argument("--deliverable", help="Deliverable name from index.yaml")
    p_query.add_argument("--metric", help="Metric name from index.yaml")
    p_query.add_argument("--include-observations", action="store_true")

    args = ap.parse_args()
    return {
        "ulid": cmd_ulid,
        "seal": cmd_seal,
        "verify-seal": cmd_verify_seal,
        "apply": cmd_apply,
        "query": cmd_query,
    }[args.cmd](args)


if __name__ == "__main__":
    sys.exit(main())
