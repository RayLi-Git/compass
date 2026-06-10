#!/usr/bin/env python3
"""
audit_prd_vs_code.example.py — Compass M-008 reverse audit

[WHAT]
  Compares "items listed in the PRD" against "items actually implemented in code", surfacing three categories of difference:
    ✅ aligned            — in PRD and also in code (aligned)
    ❌ in PRD but not code — written in PRD but not implemented in code (a gap that fails DoD)
    ⚠️ in code but not PRD — present in code but not written in PRD (run the six §5.1.3 gates first; most out-of-scope additions should be cut, only small principle-aligned reinforcements are kept pending a ruling)

[WHY — which M rule it maps to]
  M-008 "reverse audit": ordinary checks only confirm "PRD→code" (whether anything was missed);
  the reverse audit also checks "code→PRD" (whether anything not authorized by the PRD was sneaked in).
  The former guards DoD completeness, the latter guards YAGNI / §5.1.3 out-of-scope.

[HOW TO CONFIGURE]
  This script is project-agnostic: all regex, paths, and globs come from a config file,
  the script itself hard-codes no PRD structure for any specific project.
  The config file name is fixed as compass-audit.json (same directory as this script or the current working directory),
  or you can specify the path with --config. The config file uses JSON (via stdlib json, no pyyaml dependency).
  See CONFIG_EXAMPLE below for a schema example.

[HOW TO RUN]
  python3 audit_prd_vs_code.example.py                 # run all checks
  python3 audit_prd_vs_code.example.py --section=tables # run only the check named tables
  python3 audit_prd_vs_code.example.py --config path/to/compass-audit.json

[EXIT CODES]
  0 — no "in PRD but not code" gaps (there may still be ⚠️ warnings, but they don't block)
  1 — at least one check has an "in PRD but not code" gap (DoD not met)
  2 — config file missing or unparseable (prints an explanation + a copy-pasteable JSON example)

Depends only on the Python standard library (argparse / json / re / pathlib / sys).
"""

import argparse
import json
import re
import sys
from pathlib import Path

# The Windows console default encoding may be cp950 / cp1252, which cannot encode result characters like ✅ / ❌.
# If unhandled, the print line throws UnicodeEncodeError and crashes the script mid-run, exiting with exit 1 —
# and exit 1 in this script semantically means "the PRD has a gap", which would misreport a fully aligned project as having a gap.
# So force stdout / stderr to UTF-8 here; if reconfigure fails (not a TextIO, or an old version) silently skip.
for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8")
    except (AttributeError, ValueError):
        pass

# Default config file name (fixed). Search order: --config > current working directory > script directory.
DEFAULT_CONFIG_NAME = "compass-audit.json"

# Example printed for the user to copy directly when the config file is missing.
CONFIG_EXAMPLE = """{
  "prd_path": "PRD.md",
  "checks": [
    {
      "name": "endpoints",
      "prd_regex": "`(?:GET|POST|PUT|PATCH|DELETE)\\\\s+(/[\\\\w/{}-]+)`",
      "code_glob": "backend/**/*.py",
      "code_regex": "@app\\\\.(?:get|post|put|patch|delete)\\\\(\\\"(/[\\\\w/{}-]+)\\\""
    },
    {
      "name": "tables",
      "prd_regex": "(?:table)\\\\s+`(\\\\w+)`",
      "code_glob": "migrations/**/*.sql",
      "code_regex": "CREATE\\\\s+TABLE\\\\s+(?:IF\\\\s+NOT\\\\s+EXISTS\\\\s+)?`?(\\\\w+)`?"
    }
  ]
}"""


def die_no_config(searched):
    """Config file missing: print explanation + example, return exit code 2."""
    print("❌ Could not find config file compass-audit.json.", file=sys.stderr)
    print("   Tried the following locations:", file=sys.stderr)
    for p in searched:
        print(f"     - {p}", file=sys.stderr)
    print("", file=sys.stderr)
    print("Please create compass-audit.json in the project root; example content (copy and modify directly):",
          file=sys.stderr)
    print("", file=sys.stderr)
    print(CONFIG_EXAMPLE, file=sys.stderr)
    print("", file=sys.stderr)
    print("Hint: all regex / glob come from the config file; this script is project-agnostic.", file=sys.stderr)
    sys.exit(2)


def find_config(explicit):
    """Search for the config file in order; if not found return (None, list of locations tried)."""
    candidates = []
    if explicit:
        candidates.append(Path(explicit))
    else:
        candidates.append(Path.cwd() / DEFAULT_CONFIG_NAME)
        candidates.append(Path(__file__).resolve().parent / DEFAULT_CONFIG_NAME)
    for c in candidates:
        if c.is_file():
            return c, candidates
    return None, candidates


def load_config(path):
    """Read the JSON config. Any parse failure goes to exit 2."""
    try:
        text = path.read_text(encoding="utf-8")
        cfg = json.loads(text)
    except (OSError, json.JSONDecodeError) as e:
        print(f"❌ Could not parse config file {path}: {e}", file=sys.stderr)
        print("", file=sys.stderr)
        print("Correct format example:", file=sys.stderr)
        print(CONFIG_EXAMPLE, file=sys.stderr)
        sys.exit(2)
    if not isinstance(cfg, dict) or "checks" not in cfg:
        print("❌ Config file is missing the required field 'checks' (should be an array).", file=sys.stderr)
        print(CONFIG_EXAMPLE, file=sys.stderr)
        sys.exit(2)
    return cfg


def extract_from_text(text, pattern):
    """Apply the regex to a single text, returning the set of extracted items.
    If the regex has a capture group take group(1), otherwise take the whole match."""
    found = set()
    for m in re.finditer(pattern, text):
        item = m.group(1) if m.groups() else m.group(0)
        if item:
            found.add(item.strip())
    return found


def extract_prd_items(prd_path, pattern):
    """Extract the set of items from the PRD file. If the PRD doesn't exist, treat it as an empty set and warn."""
    p = Path(prd_path)
    if not p.is_file():
        print(f"⚠️ Could not find PRD file {prd_path} (treated as empty set)", file=sys.stderr)
        return set()
    try:
        text = p.read_text(encoding="utf-8", errors="replace")
    except OSError as e:
        print(f"⚠️ Failed to read PRD file {prd_path}: {e}", file=sys.stderr)
        return set()
    return extract_from_text(text, pattern)


def extract_code_items(code_glob, pattern):
    """Walk matching files with pathlib glob/rglob and extract the set of code-side items.
    Supports ** recursion (via rglob)."""
    found = set()
    base = Path(".")
    # With ** rglob is more natural; pathlib's glob also supports **, so we hand it to glob directly here.
    try:
        files = list(base.glob(code_glob))
    except (ValueError, re.error) as e:
        print(f"⚠️ Invalid glob pattern '{code_glob}': {e}", file=sys.stderr)
        return found
    for f in files:
        if not f.is_file():
            continue
        try:
            text = f.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        found |= extract_from_text(text, pattern)
    return found


def run_check(check, prd_path):
    """Run a single check; return whether there is an "in PRD but not code" gap (bool)."""
    name = check.get("name", "<unnamed>")
    prd_regex = check.get("prd_regex")
    code_glob = check.get("code_glob")
    code_regex = check.get("code_regex")

    print(f"\n=== check: {name} ===")
    missing_fields = [k for k in ("prd_regex", "code_glob", "code_regex")
                      if not check.get(k)]
    if missing_fields:
        print(f"  ⚠️ Incomplete config, skipping. Missing fields: {', '.join(missing_fields)}")
        return False

    prd_set = extract_prd_items(prd_path, prd_regex)
    code_set = extract_code_items(code_glob, code_regex)

    aligned = sorted(prd_set & code_set)
    prd_only = sorted(prd_set - code_set)   # ❌ DoD gap
    code_only = sorted(code_set - prd_set)  # ⚠️ possible §5.1.3 out-of-scope

    print(f"  PRD lists {len(prd_set)} items; code implements {len(code_set)} items.")

    if aligned:
        print(f"  ✅ aligned ({len(aligned)}): {', '.join(aligned)}")
    if prd_only:
        print(f"  ❌ in PRD but not code ({len(prd_only)}): "
              f"{', '.join(prd_only)}")
        print("     → These PRD requirements are not yet implemented; DoD not met.")
    if code_only:
        print(f"  ⚠️ in code but not PRD ({len(code_only)}): "
              f"{', '.join(code_only)}")
        print("     → Run the six §5.1.3 gates first: most out-of-scope additions (new endpoint/table/field/dependency/API change) should be cut, only small principle-aligned reinforcements are kept pending a ruling.")
    if not (aligned or prd_only or code_only):
        print("  (No matching items on either the PRD or code side; please check whether the regex is correct)")

    return bool(prd_only)


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="M-008 reverse audit: compare items listed in the PRD vs implemented in code.")
    parser.add_argument("--config", default=None,
                        help="config file path (defaults to looking for compass-audit.json)")
    parser.add_argument("--section", default=None,
                        help="run only the single check with the given name")
    args = parser.parse_args(argv)

    config_path, searched = find_config(args.config)
    if config_path is None:
        die_no_config(searched)

    cfg = load_config(config_path)
    prd_path = cfg.get("prd_path", "PRD.md")
    checks = cfg.get("checks", [])

    if args.section:
        checks = [c for c in checks if c.get("name") == args.section]
        if not checks:
            print(f"❌ Could not find a check named '{args.section}' in the config file.",
                  file=sys.stderr)
            sys.exit(2)

    print(f"Compass M-008 reverse audit — config file: {config_path}")
    print(f"PRD: {prd_path}")

    has_gap = False
    for check in checks:
        if run_check(check, prd_path):
            has_gap = True

    print("\n" + "=" * 40)
    if has_gap:
        print("Result: ❌ PRD gap exists (in PRD but not code) — DoD not met.")
        sys.exit(1)
    print("Result: ✅ No PRD gap.")
    sys.exit(0)


if __name__ == "__main__":
    main()
