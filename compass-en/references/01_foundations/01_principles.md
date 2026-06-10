# §1.1 Core Principles + Five-Stage Overview

> Part of [Compass](../../SKILL.md) §1 — Foundations.
> This doc covers the 10 core principles of PRD-driven development, plus an overview map that breaks the whole process into five stages.

---

The spirit of PRD-driven development is to make the "spec → code" transformation a repeatable, verifiable, traceable pipeline. No deviation is judged from memory — you always go back to the PRD and compare. This doc gives you two things: (1) the 10 principles you must internalize before starting; (2) a five-stage terrain map of the whole process, so you always know which cell you're standing in.

For detailed operational procedures, see the later chapters (§2 Stage 0 PRD intake, §3 Stage 1 tracking skeleton, §4 Stage 2–4 implementation loop, §5 conflict handling, etc.).

---

## 0. Core Principles (10)

| # | Principle | Notes |
|---|---|---|
| 1 | PRD is the single source of truth | Any deviation is corrected against the PRD; never rely on memory or guesswork |
| 2 | Done means done, no half-finished work | Ship in small slices, but every slice must be complete; **no "half-finished staging"** (e.g. dropping a fake endpoint that only returns 200 and circling back to fill in the logic later) |
| 3 | Compare on completion | After each slice, immediately re-check the corresponding PRD section, confirm consistency before moving on |
| 4 | Record on deviation | Any inconsistency / internal PRD contradiction gets written into the development log |
| 5 | Ambiguous PRD → take the more concrete side | See the "ambiguous clause" handling in [§5 Conflict Handling](../05_conflict_handling/01_vague_bug_gap.md) |
| 6 | PRD bug → stop first, await ruling | See the "PRD bug" handling in [§5 Conflict Handling](../05_conflict_handling/01_vague_bug_gap.md) |
| 7 | PRD gap + better implementation → run the "gap enhancement" process | **Don't just cut it with YAGNI** — record it first and await ruling, see [§5 Conflict Handling](../05_conflict_handling/01_vague_bug_gap.md) |
| 8 | Strict YAGNI | Don't build what the PRD doesn't ask for (details in [§3.5 YAGNI](../03_implementation/05_yagni.md)) |
| 9 | Each stage completion requires user testing | After passing DoD, stop and list detailed test steps; don't advance to the next stage until it passes |
| 10 | Write key context to persistent memory | Write to cross-session persistent memory after startup / major decisions (mechanism varies by environment) |

### Principle #2 elaboration

"No half-finished work" doesn't forbid shipping in small slices — it forbids making **"placeholder now, fill in later" the norm**. Concrete red flags:

- An endpoint is opened but the handler is `return {"ok": True}`, with the excuse "I'll add the logic in the next slice"
- A DB schema column is added but no read/write path uses it
- A class / function is written but the body is `pass` or `raise NotImplementedError`
- Commit messages show "WIP" / "this for now" / "circle back later" for the 2nd time or more

These all get caught by the DoD checks in [§5 Conflict Handling](../05_conflict_handling/01_vague_bug_gap.md) and [§3 Implementation Loop](../03_implementation/_index.md).

---

## 1. Process Overview (Five Stages)

```
Stage 0: Absorb the PRD       → full read + decompose into feature list
Stage 1: Build tracking skeleton → progress file / development log / PRD checklist
Stage 2: Implement in PRD order  → from infrastructure up to top-level features, in order
Stage 3: Compare-fix loop        → re-check against PRD immediately after each feature slice
Stage 4: Final full alignment    → full PRD vs code validation, patch gaps
```

### The Compass chapters each stage maps to

| Stage | Name | Main action | Chapter |
|---|---|---|---|
| 0 | Absorb the PRD | Full read, decompose feature list, identify ambiguities/contradictions | [§3 PRD Intake](../03_implementation/01_prd_intake.md) |
| 1 | Build tracking skeleton | The three tracking docs in place (progress / log / checklist) | [§3 Tracking Docs](../03_implementation/02_tracking_docs.md) |
| 2 | Implement in order | Bottom-up, security modules test-first | [§3 Implementation Loop](../03_implementation/_index.md) |
| 3 | Compare on completion | Run DoD at each slice's wrap-up, re-check against PRD | [§3 Compare-Fix Loop](../03_implementation/04_compare_fix_loop.md) |
| 4 | Final alignment | Reverse audit script scans the whole project, patches gaps | [§11.1 Reverse Audit M-008](../11_tooling/01_m007_to_m010.md) |

### Hard rules between stages

- **Can't enter Stage 1 until Stage 0 is done**: you haven't even finished the feature list — what tracking skeleton are you building?
- **Can't enter Stage 2 until Stage 1 is done**: without a PRD checklist, the DoD comparison has no baseline to compare against.
- **Each feature is one loop between Stage 2 → 3**: it's not "write everything first, then compare."
- **Before Stage 4 you must revisit all [SKIPPED] / [SKIPPED-PRD] markers**: every skipped record must be closed out.

---

## 2. When this process doesn't apply

In the following situations this process is too heavy — don't force it (but [Sentinel's thinking OS](../../SKILL.md) still runs persistently):

- Chit-chat, pure docs / typo fixes
- Pure bug fixes (no new feature, no corresponding PRD section)
- Exploratory prototypes (spec still diverging)
- Early-stage projects with frequently-changing specs (PRD not stable enough to be a contract)

Decision criterion: **is there a PRD you'd be willing to use as the "after-the-fact acceptance basis"?** If not, don't force it.

---

## 🔗 Related Compass sections
- [§3 PRD Intake](../03_implementation/01_prd_intake.md) — detailed approach for Stage 0
- [§3 Tracking Docs](../03_implementation/02_tracking_docs.md) — the three tracking docs for Stage 1
- [§3 Implementation Loop](../03_implementation/_index.md) — the implement + compare loop for Stages 2–3
- [§5 Conflict Handling](../05_conflict_handling/01_vague_bug_gap.md) — conflict-handling details for principles #5, #6, #7
- [§3.5 YAGNI](../03_implementation/05_yagni.md) — the enforcement boundary for principle #8
- [§11.1 Reverse Audit M-008](../11_tooling/01_m007_to_m010.md) — the reverse audit tool for Stage 4 final alignment

## 📝 Status
v0.2.0 (Phase 1: ported from prior SOP, generalized and de-privatized).
