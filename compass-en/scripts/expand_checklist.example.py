#!/usr/bin/env python3
"""expand_checklist.example.py — Compass Phase 4 / M-007 anti-aggregation.

WHAT
----
Read a PRD markdown file, find the markdown tables within it (lines starting
with "|"), skip the header row and separator rows (like "|---|---|"), and
expand each "data row" into a checklist with
**one checkbox per line**:

    - [ ] <section> | <first meaningful cell>

REFERENCE / EXAMPLE PURPOSE
---------------------------
This file's extension is `.example.py`; it is a reference implementation. It
can be run directly with the python3 standard library and does not depend on
any pip packages. Adjust it to your own project's PRD structure; do not assume
columns are fixed.

WHY (corresponding to the M-007 rule)
-------------------------------------
M-007 "anti-aggregation": PRDs often contain a single line like
"12 endpoints ⬜" — such aggregated entries hide 12 todos behind one checkbox,
making it easy for the whole batch to be treated as "done" during acceptance.
This tool spreads it out into 12 independent ⬜ items,
so that no single unfinished item can hide.

HOW TO CONFIGURE
----------------
This tool is driven by "command-line flags" and does not hardcode any specific
project's PRD structure in the program:

    --section-header TEXT   The section label prefixed to each checklist item
                            (defaults to the nearest markdown heading "# / ## ...")
    --cell-index N          Which column of the data row to take as content
                            (0-based, default 0; skips empty columns to find
                            the first meaningful one)
    --min-cols N            Table rows with fewer than N columns are treated as
                            noise and skipped (default 1)

HOW TO RUN
----------
    python3 expand_checklist.example.py PRD.md > prd-checklist.md
    python3 expand_checklist.example.py PRD.md --section-header "API" --cell-index 1

EXIT CODES
----------
    0  Success (a table was found and output, or the file is readable but has
       no table — prints a hint to stderr)
    1  Argument error / missing input file (prints usage and config example)
    2  Input file does not exist or cannot be read
"""

import sys
import os
import argparse

# The Windows console may default to cp950 / cp1252, which cannot encode emoji
# (like 🟢/🪤) and similar characters found in a PRD.
# If unhandled, this throws a UnicodeEncodeError mid-print and crashes, producing
# "partial output + truncation" or "apparently no output", making the user think
# the expansion failed. So force stdout / stderr to UTF-8; on failure (non-TextIO
# or old version) silently skip.
for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8")
    except (AttributeError, ValueError):
        pass


def split_row(line):
    """Split a markdown table row into a list of cells (strip leading/trailing pipes and whitespace)."""
    s = line.strip()
    if s.startswith("|"):
        s = s[1:]
    if s.endswith("|"):
        s = s[:-1]
    return [c.strip() for c in s.split("|")]


def is_separator_row(cells):
    """Determine whether this is a separator row, like |---|:--:|---|. Allows -, :, and whitespace."""
    seen = False
    for c in cells:
        if c == "":
            continue
        if set(c) <= set("-:"):
            seen = True
        else:
            return False
    return seen


def first_meaningful_cell(cells, start_index):
    """Find the first non-empty column starting from start_index; if none found, fall back to any non-empty column."""
    for i in range(start_index, len(cells)):
        if cells[i]:
            return cells[i]
    for c in cells:
        if c:
            return c
    return ""


def expand(lines, default_section, cell_index, min_cols):
    """Scan all lines and return a list of expanded checklist strings."""
    out = []
    current_section = default_section
    in_table = False
    header_consumed = False

    for raw in lines:
        line = raw.rstrip("\n")
        stripped = line.strip()

        # Track the nearest markdown heading as the section label (unless the user specified one)
        if stripped.startswith("#") and default_section is None:
            current_section = stripped.lstrip("#").strip() or current_section
            in_table = False
            header_consumed = False
            continue

        if stripped.startswith("|"):
            cells = split_row(line)
            if not in_table:
                # The first line of the table = header, skip it
                in_table = True
                header_consumed = True
                continue
            if is_separator_row(cells):
                continue
            if len([c for c in cells if c]) < min_cols:
                continue
            content = first_meaningful_cell(cells, cell_index)
            if not content:
                continue
            section = current_section if current_section else "(no-section)"
            out.append("- [ ] {} | {}".format(section, content))
        else:
            # Leaving the table block
            in_table = False
            header_consumed = False

    return out


def print_config_example(stream):
    stream.write(
        "Usage:\n"
        "  python3 expand_checklist.example.py PRD.md > prd-checklist.md\n\n"
        "Config example:\n"
        "  --section-header \"API endpoints\"   give each checklist item a fixed section label\n"
        "  --cell-index 1                      take the 2nd column as content (0-based)\n"
        "  --min-cols 2                        rows with fewer than 2 non-empty columns are treated as noise\n"
    )


def main(argv):
    parser = argparse.ArgumentParser(
        add_help=True,
        description="M-007 anti-aggregation: expand a PRD table into one checkbox per line.",
    )
    parser.add_argument("input", nargs="?", help="path to the input PRD markdown file")
    parser.add_argument("--section-header", default=None,
                        help="fixed section label (defaults to the nearest markdown heading)")
    parser.add_argument("--cell-index", type=int, default=0,
                        help="which column of the data row to take as content (0-based, default 0)")
    parser.add_argument("--min-cols", type=int, default=1,
                        help="rows with fewer than N non-empty columns are treated as noise and skipped (default 1)")
    args = parser.parse_args(argv[1:])

    if not args.input:
        sys.stderr.write("[expand] Error: missing input file argv[1].\n\n")
        print_config_example(sys.stderr)
        return 1

    if not os.path.isfile(args.input):
        sys.stderr.write("[expand] Error: input file not found: {}\n".format(args.input))
        return 2

    try:
        with open(args.input, "r", encoding="utf-8") as f:
            lines = f.readlines()
    except (OSError, UnicodeDecodeError) as e:
        sys.stderr.write("[expand] Error: cannot read {}: {}\n".format(args.input, e))
        return 2

    items = expand(lines, args.section_header, args.cell_index, args.min_cols)

    if not items:
        sys.stderr.write(
            "[expand] Hint: no markdown table data rows found in {}.\n"
            "         Make sure the file has tables starting with '|', or adjust --min-cols / --cell-index.\n"
            .format(args.input)
        )
        return 0

    for item in items:
        sys.stdout.write(item + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
