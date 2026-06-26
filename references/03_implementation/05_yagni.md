# §3.5 YAGNI: An Explicit "Don't Write" List

> Part of [Compass](../../SKILL.md) §3 — Implementation.
> Self-discipline at implementation time: anything the PRD doesn't require and that isn't necessary to implement, don't write. Treat "writing less" as a discipline, not laziness.

---

## Applicability (read first, so you don't over-cut)

This list targets things the **PRD didn't specify AND aren't necessary to implement**.

⚠️ **Important exception**: if something the PRD didn't list naturally emerges during implementation but is a **reasonable enhancement aligned with design principles**, **do not just cut it with this list** — route it through the "PRD gap + implementation is better" track in [§5 Conflict Handling](../05_conflict_handling/01_vague_bug_gap.md) (record, hold, await ruling).

YAGNI and "PRD gap enhancement" are two sides of the same coin:
- Pure extra writing, no design rationale → cut via YAGNI (this file)
- Has design rationale, aligned with principles → route to the §5 gap track, don't cut

---

## Code level

- ❌ Endpoints / fields / params the PRD never mentioned
- ❌ "Just in case" try/except (let it throw; only catch if the PRD specifies an error code)
- ❌ Params reserved for future features (e.g. `def foo(x, future_y=None)`)
- ❌ Generalized abstractions (if the PRD only needs two cases, write two; don't pre-build a strategy pattern)
- ❌ Inline comments longer than one line (unless the PRD explicitly requires it)
- ❌ Module docstrings saying "this module does X" (the filename / class name already says so)
- ❌ Wrapping the same logic into a helper (wait until it shows up a third time)
- ❌ Homegrown logger / config loader (use the standard library or the PRD-specified package)

## File level

- ❌ `utils.py` / `helpers.py` (don't create them without a clear home)
- ❌ `TODO.md` / `NOTES.md` (put info in `progress.md` / `development-log.md`, see [§3.2 Tracking Docs](02_tracking_docs.md))
- ❌ Any file not listed in the PRD's directory structure

## Dependency level

- ❌ Packages not listed in the PRD's tech-stack choices
- ❌ "Convenient" quality-of-life packages (syntactic sugar, output prettifiers, etc.; don't install anything not specified by the PRD)

---

## The only exception

PRD blanks (explicitly written "TBD", "your choice", "implementer decides") are the only place you may decide for yourself, and you **must write it into `development-log.md`** to leave a decision trail.

---

## Why YAGNI is discipline, not laziness

Every extra line of code the PRD didn't ask for adds:
- More surface area to maintain
- A guess that may conflict with a future PRD
- The cost of making a reviewer wonder "is this PRD-required or did you add it?"

The spirit of YAGNI is "**prove you need it, then write it**" — the same discipline as "PRD gaps must await a ruling" in [§5 Conflict Handling](../05_conflict_handling/01_vague_bug_gap.md): **don't unilaterally expand the contract**.

---

## 🔗 Related Compass sections
- [§5.1 PRD Vague / Bug / Gap](../05_conflict_handling/01_vague_bug_gap.md) — the flip side of YAGNI: gap enhancements with design rationale go here, don't cut
- [§3.2 The Three Tracking Docs](02_tracking_docs.md) — exception decisions go into development-log.md
- [§3.3 Implementation Order and Dependencies](03_implementation_order.md) — don't introduce dependencies outside the PRD

## 📝 Status
v0.2.0 (Phase 1: ported from prior SOP §11, generalized and de-privatized).
