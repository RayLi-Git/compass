# §11 Tooling｜Tool Enforcement M-007 ~ M-010

> Replace "rely on humans remembering" discipline with "rely on exit code / git hook / TodoWrite" mechanical enforcement. Discipline has limits; tools are reliable.

## This chapter covers

- [§11.1 The 4 tool enforcement rules (M-007 ~ M-010)](01_m007_to_m010.md) — anti-aggregation checklist, reverse audit, TodoWrite, commit subjective-word ban

## Executable script examples

Reference implementations of the §11.1 rules, in [`/scripts/`](../../scripts/README.md):

| Script | Rule | What it does |
|---|---|---|
| `audit_prd_vs_code.example.py` | M-008 | config-driven reverse audit (reads `compass-audit.json`); PRD-listed vs code-implemented, exit code signals alignment |
| `expand_checklist.example.py` | M-007 | expands PRD table rows into one checkbox per line |
| `commit-msg-lint.sh` | M-010 | git hook blocking commits containing subjective completion words |

Config example: [`/templates/audit-config.example.json`](../../templates/README.md)

## When to load

- Want to upgrade some discipline from "rely on remembering" to "tool blocks it"
- Building a reverse audit / checklist expansion / commit lint

## 🔗 Related
- [§4.1 DoD](../04_quality_gates/01_dod.md) — reverse audit exit 0 (promote to Required once script exists)
- [§3.2 Tracking docs](../03_implementation/02_tracking_docs.md) — checklist granularity (M-007)
