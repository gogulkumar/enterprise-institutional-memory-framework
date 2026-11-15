#!/usr/bin/env python3
"""Check that every Markdown file starts with the front matter defined in SPEC section 10.

Usage:
  python schemas/check_markdown.py <dir> [<dir> ...]          check every .md file
  python schemas/check_markdown.py --list <dir> [<dir> ...]   print only the front matter (what an agent reads at run time)
"""
import datetime
import os
import re
import sys

import yaml

REQUIRED = ["title", "description", "purpose", "when_to_use", "last_modified"]
MAX_DESCRIPTION = 300
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
    required = REQUIRED + (["name"] if os.path.basename(path) == "SKILL.md" else [])
    for key in required:
        value = data.get(key)
        if value is None or (isinstance(value, str) and not value.strip()):
            out.append(f"missing or empty `{key}`")
    desc = data.get("description")
    if isinstance(desc, str) and len(desc) > MAX_DESCRIPTION and os.path.basename(path) != "SKILL.md":
        out.append(f"`description` is {len(desc)} characters; the limit is {MAX_DESCRIPTION}")
    lm = data.get("last_modified")
    if lm is not None:
        if isinstance(lm, datetime.date):
            day = lm
        else:
            try:
                day = datetime.date.fromisoformat(str(lm)) if re.fullmatch(r"\d{4}-\d{2}-\d{2}", str(lm)) else None
            except ValueError:
                day = None
        if day is None:
            out.append("`last_modified` must be a date in YYYY-MM-DD form")
        elif day > datetime.date.today():
            out.append("`last_modified` is in the future")
    return out


def main(argv):
    list_mode = "--list" in argv
    roots = [a for a in argv if not a.startswith("--")] or ["."]
    failed = 0
    for path in markdown_files(roots):
        data, err = read_front_matter(path)
        if list_mode:
            if err:
                print(f"{path}\n  !! {err}\n")
                failed += 1
            else:
                print(f"{path}")
                for key in ["title", "description", "when_to_use", "last_modified"]:
                    print(f"  {key}: {data.get(key)}")
                print()
            continue
        issues = [err] if err else problems(path, data)
        if issues:
            failed += 1
            print(f"FAIL {path}")
            for issue in issues:
                print(f"  {issue}")
    if not list_mode:
        print(f"{'FAIL' if failed else 'OK'}: {failed} file(s) with problems")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
