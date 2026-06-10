# §4.1 Definition of Done (DoD)

> Part of [Compass](../../SKILL.md) §4 — Quality Gates.
> Defines the hard gate for when a slice of work is "truly done": which checks must pass, which are recommended, and the iron rule when violated.

---

## 🔒 Iron Rule

> **Any one Required item not passing = not done. Not done means you may not start the next slice.**

You can't dodge it with "I'll come back and fill it in later," "let me commit first," or "I'll run it all next round." DoD is a gate, not a wish list. Half-finished work may not hit the mainline, may not be marked done, may not unlock the next slice of work.

Echoing the core principle: **"Done means done, no half-finished work; ship in small slices, but no half-finished staging."**

---

## ✅ Required (always applies)

Precondition: **code is written** (covering the scope this slice committed to, no TODO placeholders left). On top of that, the following **eight items** must all pass:

- [ ] **1. Lint passes** (using your language's lint tool)
- [ ] **2. Typecheck passes** (if your language has a static type checker)
- [ ] **3. Relevant unit tests pass** (existing tests must not go red because of this slice's change)
- [ ] **4. Manual smoke test**: run the minimum viable path once in a real environment (not test doubles), eyeball it to confirm nothing blew up　⚠️ **library / CLI and other projects with no runnable entry point are exempt from this item**, but must note the exemption reason in the DoD record
- [ ] **5. PRD checklist ticked off** (every line this slice touches must come with a "verified with my own eyes in the codebase" confirmation — no ticking from memory)
- [ ] **6. Self-review done** (read your own diff as if a stranger wrote it; full checklist in [§4.2 Code Review](02_code_review.md))
- [ ] **7. Git commit done** (message format in [§3 Implementation](../03_implementation/_index.md) or your project's existing commit convention)
- [ ] **8. progress.md updated** (write this slice's done status, decisions, and open items into cross-session persistent memory; the mechanism varies by your setup)

These eight are the floor. Missing one (except the smoke library exemption) means not done, no room for debate.

> 📌 **Conditional item #9**: once your project sets up a reverse-audit script (see the reverse-audit script in [§11 Tooling audit](../11_tooling/01_m007_to_m010.md)), **"reverse audit exit code 0" is promoted to Required** — having a mechanized check and not running it is the same as not building it.

---

## 🟡 Recommended additions (strongly advised)

The following aren't mandatory for every project, but the moment your project's scale or risk rises above toy level, almost all of them should be included:

- [ ] **Broader integration / e2e tests** (see [§10.1 Test pyramid](../10_testing_strategy/01_test_pyramid.md))
- [ ] **Observability in place** (log / metrics, see [§6.3 Observability](../06_non_functional/03_observability.md)) — the implicit done condition for production services

The value of these items: when you come back, switch sessions, or hand off to the next agent, **future you / someone else** can pick it up immediately without re-excavating.

---

## 📐 Project-level extensions

> **DoD is a project-level decision.**

Different projects stack their own gates on top of Required and Recommended, for example:

- Accessibility check (a11y audit)
- Performance budget (performance budget / bundle size cap)
- Security scan (SAST, dependency CVE check)
- i18n string coverage
- Synced doc updates (API reference, CHANGELOG)
- Visual regression test (visual regression snapshot)

Which ones to pick, and whether they go in Required or Recommended, is decided by the project team and written into the DoD definition at the project root. What Compass provides is the **common minimum set**, not the ceiling.

---

## 🧭 How to use this DoD

1. **Pre-flight**: map this checklist onto the current slice of work, so you know which gates this slice's wrap-up must clear.
2. **During**: run lint / typecheck as soon as you finish a chunk, don't accumulate to one big run at the end (smaller blast radius when something breaks).
3. **Before wrap-up**: tick off item by item. An item you can't tick = not done yet, go back and do it.
4. **Once ticked**: only then may you commit, declare done, and start the next slice.

> If you catch yourself mentally calculating "skip this one, fill it in next slice" — that's a red flag. Stop, finish it, then move on.

---

## 🚫 Common sneak-by moves (not accepted)

- "lint is only a warning, doesn't affect functionality" → not accepted. Warnings get dealt with in this slice too, or explicitly recorded as a known exception.
- "the red test is pre-existing, I didn't break it" → after confirming, if true, open a separate slice to fix it. But **this** slice can't be declared done under a red light.
- "smoke test waits till the whole feature is done, run it all together" → not accepted. Every slice must at least run its own minimum path.
- "commit later, do the next slice first" → not accepted. Uncommitted = not done (see [§3 Implementation discipline](../03_implementation/_index.md)).

---

## 🔗 Related Compass sections
- [§3 Implementation](../03_implementation/_index.md) — DoD is the wrap-up gate of implementation discipline; commit conventions and slicing rhythm live here.
- [§2 Definition of Ready](../02_definition_of_ready/_index.md) — the dual gate before you start: what to confirm before kicking off.
- [§5 Conflict Handling](../05_conflict_handling/_index.md) — escalation and ruling flow when DoD blocks but there's a legitimate reason.
- [§11 Tooling](../11_tooling/01_m007_to_m010.md) — details of automated audit tools like the reverse-audit script.

## 📝 Status
v0.2.0 (Phase 1: ported from prior SOP, generalized and de-privatized).
