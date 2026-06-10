# §3.2 The Three Tracking Docs

> Part of [Compass](../../SKILL.md) §3 — Implementation.
> Introduces the three tracking docs every project implementation needs, plus an optional cross-session permanent-memory extension.

---

## Why you need tracking docs

The conversation window gets context-compacted, restarted across days, reopened as a new session. If every decision, every bit of progress, every PRD cross-reference lives only in the conversation, next time you come back there's nothing left.

The core principle of tracking docs: **write major decisions to a file, don't rely on conversation memory; when you contradict yourself, the written record wins.**

These three docs form the "daily work carrier" — update after every slice you finish, read first when you start the next.

---

## The three docs at a glance

| Doc | Purpose | When to update |
|---|---|---|
| `progress.md` | Current progress + todo | Update immediately after every slice |
| `development-log.md` | Decision log + deviation log | Append on every decision or deviation found |
| `prd-checklist.md` | PRD section ↔ implementation map (200+ items) | Check off every completed item; add new items immediately |

All three live for "the project's duration" — archive at project end, but never skip mid-project.

---

## §3.2.1 `progress.md` — current progress + todo

**Purpose**: anyone (including future you) opens this file and knows within 30 seconds where the project stands, what's next, and whether it's stuck.

**Core blocks**:

- **Current phase**: e.g. "implementing PRD §X (slice 3 / 8)"
- **Done**: list committed slices (with commit hash or date)
- **In progress**: the slice you're working on right now, with PRD section anchor
- **Todo**: the slices planned next (in order)
- **Blockers**: awaiting ruling, missing data, external dependency not yet available

**Update cadence**:
- Update "Done" and "In progress" immediately after every slice
- Before any interruption (context about to fill, session switch) you MUST update "In progress" — this is the key to re-anchoring
- Don't duplicate `development-log.md`'s decision details in here

---

## §3.2.2 `development-log.md` — decision + deviation log

**Purpose**: append-only ledger. Records "why you did this" rather than "what you did".

**Must record**:

| Type | Example |
|---|---|
| Tech-choice decision | "chose X over Y because ___" |
| Interpretation of a vague PRD point | "PRD didn't spell out A vs B, took the more concrete side and flagged it" (see [§5 Conflict Handling](../05_conflict_handling/_index.md) §5.1.1) |
| PRD bug flag | "PRD §X contradicts §Y, logged and awaiting ruling" (see [§5 Conflict Handling](../05_conflict_handling/_index.md) §5.1.2) |
| Gap-fill implementation | "PRD didn't say it but implemented Z, rationale ___, awaiting ruling" (see [§5 Conflict Handling](../05_conflict_handling/_index.md) §5.1.3) |
| Self-corrected deviation | "found slice N deviated from PRD §X.Y, corrected" |

**Writing style**:
- Append-only, never edit old entries (to correct, append a new entry pointing at the old one)
- Each entry carries a date + PRD anchor
- Don't write "finished foo.py" — that's progress, which belongs in `progress.md`

---

## §3.2.3 `prd-checklist.md` — PRD ↔ implementation map

**Purpose**: break the PRD into 200+ checkable line items, each mapped to implementation. **This is the physical carrier of the "done means compare" discipline.**

**Why 200+ items**: coarse granularity (e.g. one "implement the API" line) makes you think you're done when you've actually missed half. Fine granularity forces you to confirm item by item.

**Typical columns**:

| Column | Description |
|---|---|
| PRD section | §X.Y.Z anchor |
| Item description | A one-sentence verifiable requirement |
| Implementation | File path / function name / commit hash |
| Status | ⬜ not done / 🟡 in progress / 🟢 done / 🔴 [SKIPPED-PRD] |
| Evidence | Test ID / screenshot / command run (see Sentinel's three-tier evidence grading) |
| Notes | Deviation, TODO, items awaiting ruling |

**Granularity rule**: every item must be a single "verifiable" behavior, not a catch-all. For the detailed granularity-split rules (1 item per ~30 lines of PRD, anti-aggregation of items), see [§11.1 Tooling Enforcement M-007](../11_tooling/01_m007_to_m010.md).

**Tooling assist**:
- Use a **PRD-table expansion script** to auto-generate a first-draft checklist skeleton from the PRD markdown, then refine by hand
- Use a **reverse-audit script** to scan the codebase (e.g. your backend framework's route definitions / schema definitions) and compare against the checklist for missing items — this cures "implemented it but forgot to add it to the checklist"

**Core rules**:
- Check off every completed item + fill the evidence column
- Not all checked = "PRD §X implementation" is NOT done
- Reverse audit finds implementation present but checklist missing — add the item immediately, not "fill it in once finished"
- PRD didn't say it but you implemented it → go to [§5 Conflict Handling §5.1.3](../05_conflict_handling/_index.md)

---

## How the three docs work together

```
              ┌──────────────────────┐
              │   PRD (the contract)  │
              └──────────┬───────────┘
                         │ expand
                         ▼
              ┌──────────────────────┐
              │  prd-checklist.md    │  ← granular map (200+ items)
              └──────────┬───────────┘
                         │ each slice done
            ┌────────────┼────────────┐
            ▼            ▼            ▼
    progress.md   development-log.md  commit
    (where now)   (why this way)    (physical snapshot)
```

- **`progress.md` tells you "now"**
- **`development-log.md` tells you "why"**
- **`prd-checklist.md` tells you "what's left"**

You can't drop any of the three. With only `progress.md`, when you revisit a decision you won't remember why. With only `development-log.md`, you lose your current position. With only `prd-checklist.md`, you won't know which slice to work next.

---

## APPENDIX — optional extension: cross-session permanent memory

The three docs are the "project-duration" work carrier, but some facts **never change across the whole project lifecycle** — e.g. the project slug, core architecture decisions, inviolable domain constraints. Re-explaining this stuff every new session wastes context.

**Mechanism**: many AI coding environments offer **cross-session persistent memory** (mechanism varies by setup — could be Claude Code's memory directory, an IDE plugin's workspace memory, or a self-built prompt-injection layer). Any storage layer that "auto-loads when a new conversation opens" counts.

**When to write to memory**:

| Trigger | Action |
|---|---|
| Project kickoff | Create a project-level memory file recording the invariant facts (slug / core architecture / domain constraints) |
| Core rule changes | Update the corresponding memory block |
| User explicitly says "note this down / don't forget" | Write immediately, don't batch |
| After a major decision (e.g. platform change, PRD bug resolved with solution X) | Update the "decision log" block |
| Major phase complete | Update the "progress status" block (one line is enough) |

**What to write / what not to write**:

- ✅ Do write: invariant facts, core architecture decisions, domain constraints, project identity
- ❌ Don't write: daily progress details (that's `progress.md`'s job), the full reasoning behind a decision (that's `development-log.md`'s job), PRD item mapping (that's `prd-checklist.md`'s job)

**Division of labor with the three docs**:

| Doc | Lifespan | Purpose |
|---|---|---|
| Cross-session memory | Persists across sessions | Invariant facts you must know at startup |
| `progress.md` | Project duration | Current progress + todo |
| `development-log.md` | Project duration | Decision + deviation log |
| `prd-checklist.md` | Project duration | Granular map |

> **Core principle**: memory is "the top-level context", the three tracking docs are "the daily work carrier". Memory **points to** the tracking docs, it **does not replace** them.

**Update cadence**:
- Don't touch memory on every small change (it'd duplicate `progress.md`)
- But "major phase complete" must update "progress status" once
- When updating, change the "record date" field

If your environment has no native memory mechanism, fall back to second-best: maintain a `PROJECT_CONTEXT.md` in the project root and proactively read it at the start of every new session.

---

## 🔗 Related Compass sections
- [§3 Implementation index](../03_implementation/_index.md) — the three docs are the discipline carrier of the implementation phase
- [§5 Conflict Handling](../05_conflict_handling/_index.md) — handling flow for `development-log.md` deviation entries (§5.1.1 / §5.1.2 / §5.1.3)
- Sentinel's diagnosis phase — the two case-file docs (debug-log.md / patterns.md) complement the three docs

## 📝 Status
v0.2.0 (Phase 1: ported from prior SOP, generalized and de-privatized).
