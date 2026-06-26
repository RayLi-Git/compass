# §5 Conflict Handling｜PRD Conflict Handling

> When the PRD doesn't match reality, route the conflict to different handling tracks — so you don't stop where you shouldn't, or push through where you should stop.

## What this chapter covers

### Delivered (v0.2.0 / Phase 1) — static PRD three-track
- [§5.1 PRD vague / bug / gap: three-track handling](01_vague_bug_gap.md)
  - §5.1.1 Vague (any reading works → don't stop, take the more concrete one)
  - §5.1.2 Bug (no reading works → stop and await ruling)
  - §5.1.3 Gap + implementation is better (keep + flag + await ruling, 6-gate check)
  - §5.1.4 Three-track handling quick-reference table

### Delivered (v0.5.0 / Phase 2) — dynamic conflicts
- [§5.2 PRD changes mid-flight](02_prd_change.md) (PRD version bumps halfway through, five-step change protocol + impact analysis)
- [§5.3 Cross-document conflict](03_cross_document.md) (PRD vs ADR vs API contract vs ERD, prioritize by "whose domain")
- [§5.4 Multi-PRD dependencies](04_multi_prd.md) (dependency ordering across sub-PRDs and shared-contract consistency)

## When to load

- During implementation you find "the PRD is unclear / self-contradictory / missing something" → §5.1
- PRD bumps version mid-flight → §5.2 (Phase 2)
- PRD conflicts with other design documents → §5.3 (Phase 2)

## 🔗 Related
- [§1 Core principles](../01_foundations/01_principles.md) — principles #5/6/7/8 map to this chapter's three-track handling and the YAGNI fallback
- [§3.5 YAGNI](../03_implementation/05_yagni.md) — "not in the PRD and not needed" goes to YAGNI, the flip side of §5.1.3 "gap enhancement"
