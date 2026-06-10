# §3 Implementation｜in-flight SOP

> The discipline for landing a PRD: absorb the spec, track every decision, build bottom-up, and compare-fix each slice so drift never accumulates.

## This chapter covers

- [01_prd_intake.md](01_prd_intake.md) — Fully absorb the PRD before any code; output a feature checklist + empty skeleton, not logic.
- [02_tracking_docs.md](02_tracking_docs.md) — The three tracking docs (progress / development-log / prd-checklist) plus optional cross-session memory.
- [03_implementation_order.md](03_implementation_order.md) — Bottom-up ordering (infra → security → business → integration → frontend), test-first safety modules, dependency version-locking.
- [04_compare_fix_loop.md](04_compare_fix_loop.md) — The 12-step complete → compare-against-PRD → fix → accept loop run after every block, plus the user acceptance gate.
- [05_yagni.md](05_yagni.md) — An explicit "don't write" list for code / files / dependencies the PRD never asked for.

## When to load

- Starting implementation of a PRD — read 01 before writing anything, then set up the tracking docs in 02.
- Mid-implementation: deciding what to build next (03), wrapping up a slice (04), or resisting scope creep (05).
- You notice drift from the spec accumulating, or you're about to add something the PRD never specified.

## 🔗 Related
- [§4 Quality Gates](../04_quality_gates/_index.md) — the DoD hard gates the compare-fix loop depends on.
- [§5 Conflict Handling](../05_conflict_handling/_index.md) — where PRD vague / bug / gap cases route to.
