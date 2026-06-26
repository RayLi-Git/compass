# Scripts — Compass Tooling Script Examples

> **Reference implementations** for Compass §11 Tooling (M-007 / M-008 / M-010). The `.example` suffix means these are skeleton examples, not drop-in products — every project's PRD structure differs, so adjust the regex / parser to your needs.

---

## Files

| File | Rule | What it does |
|---|---|---|
| `audit_prd_vs_code.example.py` | M-008 reverse audit | Reads config file `compass-audit.json`, compares "what the PRD lists" vs "what the code implements", prints gaps, exit code signals alignment |
| `expand_checklist.example.py` | M-007 anti-aggregation | Expands a PRD markdown table row by row into "one checkbox per line" |
| `commit-msg-lint.sh` | M-010 commit gate | git `commit-msg` hook; blocks commits containing subjective completion words (complete/done…) |

---

## M-008 reverse audit (requires config file)

`audit_prd_vs_code.example.py` is **config-driven** — it doesn't guess your project structure, it reads a `compass-audit.json`. **With no config file it prints an example and exits 2** (by design, not a failure).

```bash
# 1. Copy the example config to your project root, edit to match your PRD / code structure
cp templates/audit-config.example.json compass-audit.json

# 2. Run (exit 0 = aligned; 1 = there are gaps where "PRD lists it but code doesn't implement it"; 2 = config missing)
python3 scripts/audit_prd_vs_code.example.py

# Run only one check
python3 scripts/audit_prd_vs_code.example.py --section=endpoints
```

Config file fields (see [`../templates/audit-config.example.json`](../templates/audit-config.example.json)):
- `prd_path` — PRD markdown path
- `checks[]` — one group per check: `name` / `prd_regex` (pull items from the PRD) / `code_glob` (which code files to scan) / `code_regex` (pull implementations from the code)

> The example regex targets a FastAPI + SQL migration layout; switch to your stack and you must change the regex.
>
> ⚠️ **Known limitation**: the example endpoint check matches the path only and does not distinguish the HTTP method (`GET /users` and `POST /users` are treated as the same item, so a method mismatch is not flagged). For method sensitivity, have the regex capture "method + path" as one string (normalize the code-side method case).

## M-007 anti-aggregation checklist expansion

```bash
python3 scripts/expand_checklist.example.py PRD.md > prd-checklist.md
# Optional: --section-header "§19 endpoints" tags each row with a label
```

## M-010 commit message gate

```bash
cp scripts/commit-msg-lint.sh .git/hooks/commit-msg
chmod +x .git/hooks/commit-msg
# After this, commit messages containing "complete/all/done/finished…" get blocked, requiring a concrete count instead
```

---

## Environment requirements

- Python 3 (standard library only, no pip dependencies) — the two `.py` files
- bash — `commit-msg-lint.sh`
- All file reads are UTF-8 (scripts already specify `encoding="utf-8"`)

See [§11.1 Tooling enforcement M-007 ~ M-010](../references/11_tooling/01_m007_to_m010.md).
