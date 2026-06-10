# Templates — Compass Tracking Doc Templates

> Tracking-doc templates that Compass §3.2 depends on, plus the config example for §11 reverse audit. Copy into your project (`.claude/` or project root), then fill in.

---

## Files

| File | Maps to | Purpose |
|---|---|---|
| `progress.md.template` | [§3.2](../references/03_implementation/02_tracking_docs.md) | Progress + todo + in-progress (the §9.3 handoff recovery indicator) |
| `development-log.md.template` | [§3.2](../references/03_implementation/02_tracking_docs.md) / [§5](../references/05_conflict_handling/_index.md) | Decisions + PRD Ambiguity / Issues / Gaps log |
| `prd-checklist.md.template` | [§3.2](../references/03_implementation/02_tracking_docs.md) / [§11 M-007](../references/11_tooling/01_m007_to_m010.md) | PRD section ↔ implementation mapping (one line per item, no aggregation) |
| `audit-config.example.json` | [§11 M-008](../references/11_tooling/01_m007_to_m010.md) | Config example for the reverse-audit script `audit_prd_vs_code.example.py` |

> 📌 No template yet for cross-session permanent memory (auto memory) — for now, build it manually following the "cross-session memory" note at the end of [§3.2 Tracking Docs](../references/03_implementation/02_tracking_docs.md).

---

## Usage

```bash
cp templates/progress.md.template .claude/progress.md
cp templates/development-log.md.template .claude/development-log.md
cp templates/prd-checklist.md.template .claude/prd-checklist.md
cp templates/audit-config.example.json compass-audit.json   # edit to match your PRD/code structure
```

`prd-checklist.md` can be auto-expanded from the PRD table with [`../scripts/expand_checklist.example.py`](../scripts/README.md), avoiding hand-copied missing lines.
