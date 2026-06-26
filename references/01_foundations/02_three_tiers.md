# §1.2 Three-Tier Discipline Scaling

> Part of [Compass](../../SKILL.md) §1 — Foundations.
> Compass is not a heavyweight process you apply to every task. It scales across three tiers so discipline strength is proportional to risk — avoiding an eleven-section process for a typo fix, and avoiding a sloppy pass on a migration.

---

## Why tiers are needed

If every task ran the full Compass process, the user would abandon it by the second time; if every task skipped discipline, the brownfield big feature would blow up in week three.
The point of tiering: **discipline strength = task risk × irreversibility**.

| Tier | Trigger | Compass discipline applied | What can be skipped | Stage marker example |
|---|---|---|---|---|
| 🟢 light | typo fix, style tweak, copy change, adding a comment, single-line obvious fix | almost none; keep the "evidence grading" only | DoR, compare-fix, checklist, commit message format | no stage marker needed |
| 🟡 medium | add an endpoint, write a function/component, change a piece of logic, integrate an API | run DoR quick check pre-flight; run compare-fix loop after each slice; commit cites PRD section | full 11-section process; reverse-audit; root-cause tree | `[PRD §X.Y] module: brief` |
| 🔴 heavy | implement a whole PRD section, schema migration, rollback mechanism, brownfield big feature, security-related module, multi-file refactor | full 11-section process (DoR → plan → implement → compare-fix → DoD → commit → progress → retro); reverse-audit; root-cause tree if stuck | nothing skippable; use the "emergency valve" only if time truly runs out | `[PRD §X.Y] module: brief` |

---

## 🟢 Light

**Triggers** (any one):
- typo, copy, or comment fix
- single-file single-line obvious fix (e.g. removing a `console.log`)
- pure style tweak (color, spacing)
- behavior-preserving rename / formatting

**Discipline applied**:
- Just do it.
- Keep the "evidence grading": before claiming done, still mark 🟢verified / 🟡reviewed / 🔴speculative (this is one of Sentinel's three safety nets, "evidence grading", which Compass reuses).

**Can be skipped**:
- DoR (Definition of Ready) check
- compare-fix loop
- DoD checklist
- stage marker
- progress update (unless the file is collaborated on by multiple people)

**Anti-pattern**: escalating "fix one typo" into the full 11-section process — this is over-discipline and makes people resent Compass.

---

## 🟡 Medium

**Triggers** (any one):
- add an endpoint / route
- write a new function or component
- change a piece of existing logic (< 100 lines blast radius)
- integrate an external API
- add a field, change part of a schema (non-breaking)

**Discipline applied**:
1. **Pre-flight**: run a DoR quick check — "Do I know the acceptance criteria? Which files are affected? Is there a matching PRD section?" (see [§2 Definition of Ready](../02_definition_of_ready/_index.md)).
2. **During implementation**: done means done, no half-finished work; ship in small slices, but no half-finished staging.
3. **After each slice**: immediately run the compare-fix loop — check against the PRD original for drift, fix it immediately if it drifted, no batching up (see [§4 Compare-Fix Loop](../03_implementation/04_compare_fix_loop.md)).
4. **commit**: message cites the PRD section, e.g. `[PRD §X.Y] module: brief` (use `feat: brief` when there's no PRD number).

**Can be skipped**:
- "§6 reverse-audit" of the full 11-section process (unless the module is already a brownfield pain point)
- root-cause tree (unless ≥ 2 hypothesis directions are falsified during development)
- full progress.md update (the commit message records enough)

---

## 🔴 Heavy

**Triggers** (any one):
- implement a whole PRD section
- schema migration / data migration
- rollback / recovery mechanism
- adding a big feature to or refactoring an existing brownfield system
- security-related module (authentication, authorization, PII, key handling)
- multi-file / cross-module bug or refactor
- stuck more than once, wanting to add a 3rd special-case if, wanting to use try/except to cover up an error

**Discipline applied**:
1. **Full 11-section process**: from DoR → plan → implement → compare-fix → DoD → commit → progress → retro, skip not one section.
2. **Reverse-audit**: against your backend framework's route definitions / schema definitions / config, run a reverse-audit pass — anything in the code that isn't in the PRD, or vice versa (see [§6 Reverse Audit](../11_tooling/01_m007_to_m010.md)).
3. **Security module test-first**: authentication, authorization, PII handling always get tests written before implementation.
   - **Example: typical web app stack** — Auth flow / token issuance / password hashing / 2FA / PII redaction; these examples are for reference only, the actual list depends on your tech stack.
4. **Produce a root-cause tree when stuck**: ≥ 2 hypothesis directions falsified → stop and draw a root-cause tree, don't keep stacking patches (the root-cause tree is a Sentinel thinking concept).
5. **commit message format**: `[PRD §X.Y] module: brief`, where §X.Y points to the PRD section.
6. **progress update**: update the progress file after each slice (cross-session persistent memory, mechanism varies by setup).

**Can be skipped**: nothing. Use the "emergency valve" (below) only if time truly runs out.

---

## 🧷 Escalate-only, no graceful degradation (Iron Rule)

**Rule**: tiers can only move from low to high, never high to low.

- User says "go deeper / think harder / plan this for me / why / what's the root cause" → escalate 🟡 to 🔴.
- User says "hurry up / simple change / minor fix" → if the task actually meets 🔴 triggers, **refuse to degrade**.
  - Say it directly: "This change actually meets the heavy-tier triggers (reason X), it can't go light; if you're truly rushed, we use the emergency valve."
- Compass judges by itself that 🔴 triggers are met but the user didn't say so → escalate 🔴 directly, and explain why.

**Why**: degradation tends to happen at exactly the moment you should be most careful (migration deadline, demo eve, production on fire). These are precisely when discipline is most needed. Allowing degradation = Compass is useless.

---

## 🚨 Emergency Override Valve

**Purpose**: when it's "truly, genuinely, no-lie" urgent (e.g. production down, demo starts in 30 minutes), allow skipping some discipline to stop the bleeding first.

**Rules**:
1. **You can only skip the process, not the record**. Mark `🔴[SKIPPED]` in the debug or change log, recording:
   - which sections were skipped (e.g. skipped DoR, skipped reverse-audit)
   - why it was urgent (one sentence)
   - when it must be paid back (e.g. "run the full process within 24 hours afterward")
2. **You must retro and pay it back afterward**. The emergency valve is not a get-out-of-jail-free card, it's deferred payment. No payback = technical debt + discipline debt accumulating together.
3. **You cannot use the emergency valve on "security-related modules"**. Authentication, authorization, key handling are test-first even under time pressure. Using the emergency valve here = manufacturing the next incident.
4. **You cannot use it twice in a row**. A second attempt to open the emergency valve in the same project, same week → forced stop to examine why you keep firefighting, which is a signal of an upstream problem.

**Anti-pattern**: using the emergency valve every time to skip the compare-fix loop, then three months later finding the code and PRD have completely diverged — at which point the thing to do is not open the emergency valve again, but stop and run a reverse-audit.

---

## 🔗 Related Compass sections
- [§1.1 Core principles + five-stage overview](./01_principles.md) — Compass's positioning and why discipline strength is tiered
- [§2 Definition of Ready](../02_definition_of_ready/_index.md) — 🟡 / 🔴 pre-flight entry check
- [§3.4 Compare-Fix Loop](../03_implementation/04_compare_fix_loop.md) — 🟡 / 🔴 compare-and-fix after each slice
- [§11.1 Reverse Audit (M-008)](../11_tooling/01_m007_to_m010.md) — 🔴 mandatory reverse-audit
- Evidence grading and root-cause tree are both Sentinel concepts, reused by Compass in 🔴 heavy-tier tasks

## 📝 Status
v0.2.0 (Phase 1: ported from prior SOP, generalized and de-privatized).
