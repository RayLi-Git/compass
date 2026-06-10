# §5.2 Mid-Flight PRD Changes

> Part of [Compass](../../SKILL.md) §5 — Conflict Handling.
> The SOP assumes the PRD is a static contract; reality is that halfway through, the PRD bumps to v2/v3. This is the most frequent real-world conflict, and Compass has to handle it.

---

## 0. Why this is more dangerous than static conflict

The three conflict types in §5.1 (vague / bug / gap) all assume the **PRD doesn't move** — you just hit problems while reading it. This file handles the case where **the PRD itself is moving**.

> SCOPE: **The PRD isn't Compass's enemy — the PRD changing mid-flight is.**

The three fatal points of a mid-flight PRD change:

- **Completed modules may turn wrong**: what you built and committed against v1 may now behave wrong, use wrong fields, or even be a feature that got cut under v2. It won't throw an error — it just silently fails to match the new contract.
- **Checklist falls out of sync**: prd-checklist.md is still frozen on the v1 rows. The checkmarks you ticked may now be fake checkmarks.
- **Silent drift**: the worst case is that you "casually" absorbed part of the change and missed another part, leaving code that's half v1, half v2, with nothing recording which is which. Three weeks later nobody can reconstruct the original decision.

**Iron rule**: when you spot a PRD change → stop the current implementation immediately, run the protocol below first, do not "casually" absorb it while editing code.

---

## 1. PRD Change Protocol (five steps)

### Step 1: Freeze the current state

**Before** touching anything, commit the current working tree.

```
git add -A
git commit -m "freeze: pre-PRD-v2 state (clean retreat point)"
```

Reason: this is Sentinel's safety net "retreat route." Once you start reworking toward v2, if you find the direction is wrong, you must be able to cleanly roll back to v1's last state. **Stacking a PRD change on a dirty working tree = suicide.**

### Step 2: Diff the PRD (old vs new)

Compare old PRD and new PRD section by section, and bucket every difference into four types:

| Type | Definition | Example |
|---|---|---|
| 🆕 Added | Brand-new feature / field / endpoint | "Add CSV export" |
| ✏️ Modified | Behavior / naming / boundary of an existing spec changed | "Pagination size cap 50 → 100" |
| 🗑️ Deleted | Existing feature cut | "Remove anonymous comments" |
| 💡 Clarified | Behavior unchanged, just an originally-vague point spelled out | "Timeout defined as 30s" |

> Clarifications are the easiest to misjudge as modifications. The test: **if the old implementation still satisfies the new text, it's a clarification; if you must change code to satisfy it, it's a modification.**

### Step 3: Per-item impact analysis

For **each** change, ask two questions: which "completed" modules does it touch? Which "uncompleted" modules does it touch?

- **Touches a completed module** → weigh "rework cost vs blast radius." You may have to reopen a module already marked ✅ — **this is normal, and beats shipping a wrong one.** Roll it back to 🔄 on the checklist; don't pretend it's still correct.
- **Only touches uncompleted modules** → lightest. Update the checklist and implementation order table, keep going, build to the new spec.
- **Deleted features** → if the code is already written, **do not auto-delete.** Confirm with the user first (there may be dependencies; it may just be temporarily hidden). Only act after confirmation, and record in the development log what was deleted and why.

> "Reopen a completed module" sounds painful, but that's exactly why Compass exists: silently shipping code that matches v1 and violates v2 is the root of silent drift. Better to roll back and redo.

### Step 4: Re-align prd-checklist.md

Pull the checklist back in sync with the new PRD (the three tracking docs are in [§3.2](../03_implementation/02_tracking_docs.md)):

```markdown
| PRD § | Module | Status | Change |
|-------|------|------|------|
| 3.1   | Login | ✅   | —    |
| 3.2   | Pagination | 🔄   | v2: size cap 50→100, needs rework |   ← modified, reopen
| 3.5   | Export | ⬜   | v2 added |                             ← added, schedule it
| 3.7   | Anonymous comments | 🗑️ | v2 deleted, built, remove after user confirms | ← deleted, hands off
```

- 🆕 Added → add a new row, schedule it into the implementation order table.
- ✏️ Modified → mark that row 🔄, roll status back from ✅.
- 🗑️ Deleted → mark that row 🗑️, note "pending confirmation," **do not delete the row** (keep the audit trail).

### Step 5: Log it in the development log

Record the PRD version-bump event + the decision you made for each change:

```markdown
## [Date] PRD v1 → v2

| Change | Type | Impact | Decision |
|------|------|------|------|
| Pagination size 50→100 | ✏️ Modified | Completed module §3.2 | Reopen and rework |
| CSV export | 🆕 Added | Uncompleted | Scheduled as item 5 in order table |
| Anonymous comments | 🗑️ Deleted | Built §3.7 | Delete after user confirms |
```

This log is the only trustworthy source for "why does this code look the way it does" later — conversation memory forgets, the log doesn't.

---

## 2. Version discipline

- **Tag every commit with the PRD version**: put the version in the commit message, e.g. `[PRD v2 §3.2] Pagination: cap changed to 100`.
- **Never silently mix v1 and v2 assumptions**: within one PR / a run of consecutive commits, it's either all v1 or all v2. Half-new, half-old with no record is silent drift.
- **The change boundary needs one explicit commit** (the freeze commit from Step 1 is it). Later, `git log` shows at a glance "everything after this is v2."

---

## 3. Decision table: change type × module status → action

| Change type | Completed module | Uncompleted module |
|---|---|---|
| 🆕 Added | (usually N/A) → schedule as a new module in the order table | Add a checklist row, schedule into implementation order |
| ✏️ Modified | Roll back to 🔄, weigh rework cost, reopen and rework | Build straight to the new spec |
| 🗑️ Deleted | Mark 🗑️ pending confirmation, **ask the user** before deleting code | Just remove from checklist / order table |
| 💡 Clarified | Mostly no code change; compare, confirm, log it | Build to the clarified, explicit spec |

> The only cell that requires "ask the user" before acting: **Deleted × Completed.** The rest you can push forward on your own, but all of them must leave a trace in the development log.

---

## 4. Anti-patterns (any one appears → stop)

- ❌ "Casually" absorbing PRD changes while editing code, with no freeze, no diff.
- ❌ A completed module knowingly affected by v2, yet not rolled back from ✅, pretending it's still correct.
- ❌ Seeing a deletion and auto-`rm`-ing code without asking the user.
- ❌ Committing without tagging the version, mixing v1/v2 assumptions in the same working-tree blob.
- ❌ Misjudging a "modification" as a "clarification," skipping the rework.

---

## 🔗 Related Compass sections
- [§5.1 Vague / bug / gap](./01_vague_bug_gap.md) — the three conflict types of a static PRD; this file is the dynamic dual, "the PRD moves"
- [§3.4 Compare-fix loop](../03_implementation/04_compare_fix_loop.md) — the closed loop of comparing each slice against the PRD; once the PRD changes, the comparison baseline switches to the new version
- [§3.2 The three tracking docs](../03_implementation/02_tracking_docs.md) — the formats of prd-checklist / development-log / progress; steps 4 and 5 operate on them directly
- [§3.3 Implementation order](../03_implementation/03_implementation_order.md) — added modules must be scheduled into the order table
- [§4.1 DoD](../04_quality_gates/01_dod.md) — a reworked module still has to re-pass DoD before it counts as done
- [§5.4 Multi-PRD conflict](./04_multi_prd.md) — when the change comes from a different PRD rather than a version bump of the same one

## 📝 Status
v0.5.0 (Phase 2: original content).
