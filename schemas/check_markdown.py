#!/usr/bin/env python3
"""Check that every Markdown file starts with front matter in the Agent Skills format.

Usage:
  python schemas/check_markdown.py <file or folder> [...] check every.md file
  python schemas/check_markdown.py --list <file or folder> [...] print only name and description (what an agent reads first)
"""
import datetime
import os
import re
import sys

import yaml

ALLOWED = {"name", "description", "metadata", "license", "compatibility", "allowed-tools"}
NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
MAX_NAME, MAX_DESCRIPTION = 64, 1024
SKIP_DIRS = {".git", "node_modules", "__pycache__", ".venv", "venv"}


def markdown_files(roots):
    for root in roots:
        if os.path.isfile(root):
            if root.endswith(".md"):
                yield root
            continue
        if not os.path.isdir(root):
            raise SystemExit(f"no such file or folder: {root}")
        for folder, dirs, files in os.walk(root):
            dirs[:] = sorted(d for d in dirs if d not in SKIP_DIRS)
            for name in sorted(files):
                if name.endswith(".md"):
                    yield os.path.join(folder, name)


def read_front_matter(path):
    """Return (dict, error). Reads only the lines up to the closing --- line."""
    with open(path, encoding="utf-8") as f:
        if f.readline().rstrip("\n") != "---":
            return None, "no front matter: the file must start with a --- line"
        block = []
        for line in f:
            if line.rstrip("\n") == "---":
                break
            block.append(line)
        else:
            return None, "front matter is not closed by a --- line"
    try:
        data = yaml.safe_load("".join(block))
    except yaml.YAMLError as e:
        return None, f"front matter is not valid YAML: {e}"
    if not isinstance(data, dict):
        return None, "front matter is not a key-value block"
    return data, None


def problems(path, data):
    out = []
    extra = sorted(set(data) - ALLOWED)
    if extra:
        out.append(f"keys outside the standard: {', '.join(extra)} (extra details go under `metadata`)")
    name = data.get("name")
    if not isinstance(name, str) or not NAME_RE.match(name) or len(name) > MAX_NAME:
        out.append("`name` must be lowercase letters, digits and single hyphens, at most 64 characters")
    elif os.path.basename(path) == "SKILL.md" and name != os.path.basename(os.path.dirname(os.path.abspath(path))):
        out.append("a skill's `name` must match its folder name")
    desc = data.get("description")
    if not isinstance(desc, str) or not desc.strip():
        out.append("missing or empty `description`")
    else:
        if len(desc) > MAX_DESCRIPTION:
            out.append(f"`description` is {len(desc)} characters; the limit is {MAX_DESCRIPTION}")
        if "use when" not in desc.lower():
            out.append("`description` must say what the file is and when to use it (\"... Use when...\")")
    meta = data.get("metadata")
    if not isinstance(meta, dict):
        out.append("missing `metadata` map")
        return out
    if any(not isinstance(v, str) for v in meta.values()):
        out.append("`metadata` values must be strings (quote dates)")
    lm = meta.get("last_modified")
    day = None
    if isinstance(lm, str) and re.fullmatch(r"\d{4}-\d{2}-\d{2}", lm):
        try:
            day = datetime.date.fromisoformat(lm)
        except ValueError:
            day = None
    if day is None:
        out.append("`metadata.last_modified` must be a quoted date in YYYY-MM-DD form")
    elif day > datetime.date.today():
        out.append("`metadata.last_modified` is in the future")
    return out


def main(argv):
    list_mode = "--list" in argv
    roots = [a for a in argv if not a.startswith("--")] or ["."]
    failed = 0
    for path in markdown_files(roots):
        data, err = read_front_matter(path)
        if list_mode:
            if err:
                print(f"{path}\n !! {err}\n")
                failed += 1
            else:
                print(f"{path}\n name: {data.get('name')}\n description: {data.get('description')}\n")
            continue
        issues = [err] if err else problems(path, data)
        if issues:
            failed += 1
            print(f"FAIL {path}")
            for issue in issues:
                print(f" {issue}")
    if not list_mode:
        print(f"{'FAIL' if failed else 'OK'}: {failed} file(s) with problems")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
