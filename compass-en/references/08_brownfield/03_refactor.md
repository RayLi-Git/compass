# §8.3 Refactor Workflow

> Part of [Compass](../../SKILL.md) §8 — Brownfield.
> Refactoring changes structure, not behavior; green in, green out, behavior identical to the byte.

---

## 🎯 Defining refactor (draw the line first)

> **Refactor = change internal structure, do not change externally observable behavior.**

Any change that makes "same input → different output" is **not a refactor**; it's a behavior change — it must go through the PRD flow or §8.4 add-a-feature.

| What you're doing | Category | Which path |
|---|---|---|
| Extract function, rename, split file, reorder, dedupe | ✅ Refactor | This document |
| Swap implementation but I/O unchanged (e.g. swap JSON parser) | ✅ Refactor | This document |
| Change return format, add field, change error code | ❌ Behavior change | PRD / [§8.4](./04_add_feature.md) |
| "While I'm at it" fix a bug | ❌ Behavior change | [§8.2](./02_bug_fix.md) (separate commit) |
| Rip out and rewrite a whole module | ❌ Rewrite | See "Refactor vs Rewrite" below |

🚩 **Red flag**: mid-refactor you notice "wait, this logic was wrong all along" → **stop**. Don't sneak a fix into the refactor commit. Note it down, and after the refactor is green open a separate bug-fix. Mixing them makes "was behavior preserved" impossible to verify.

---

## ⚖️ Iron rule: green in, green out

```
[all tests green] → one small refactor step → [all tests green] → commit → next step
     ↑                                                                  │
     └──────────── any step turns red → immediately revert that step ───┘
```

- **Before entering**: relevant tests must be all green. Red or no tests → backfill first (see characterization below).
- **After each small step**: rerun tests. Red means this step broke the structure — **revert this step**, don't pile on.
- **Never simultaneously** change structure and behavior. One commit does one thing.

> Why so strict? Because the only safety guarantee in refactoring comes from "behavior didn't change," and the only evidence that "behavior didn't change" is **tests green before and after the change**. Without that evidence, you're just gambling.

---

## 🧪 No tests means you can't refactor safely → write a Characterization Test first

When coverage is too thin, **don't dive in**. First write "characterization tests" to pin down **current behavior** — regardless of whether the current behavior is correct, first make it verifiable.

Characterization test ≠ spec test: it doesn't assert "what it should be," it only records "what it is now."

**How to write it (golden master method):**

1. Find the unit you want to refactor, call it, and **deliberately assert an obviously wrong value**.
2. Run the test, let it fail, and copy back the **actual output** from the failure message.
3. Fill the actual output back into the assertion → green. This locks down the current state.
4. Repeat for the key branches until you cover the part you're about to touch.

**Example (TypeScript / Vitest):**

```ts
// Don't yet know what formatPrice returns for negatives, force it to spit it out
it('characterizes formatPrice(-5)', () => {
  expect(formatPrice(-5)).toBe('__FILL_ME__'); // run once → get '-$5.00'
});
// Copy back the real value, lock the current state; if a later refactor changes it, this line turns red
```

✅ Characterization done means: **every branch you're going to change has a test that turns red when behavior changes.**

---

## 🪜 Small steps + commit per step

Each step must be small enough that "if it breaks, you can spot which step at a glance." One step, one green, one commit, echoing [§3 commit per slice](../03_implementation/02_tracking_docs.md).

| Refactor action | Granularity of one step |
|---|---|
| Rename | One symbol renamed all the way through (use IDE/tooling, not by hand) |
| Extract function | Extract one, run tests, commit |
| Split file | Move one unit + fix imports, run tests, commit |
| Dedupe | Collapse one duplication, run tests, commit |

Suggested commit message: `refactor(<scope>): <what structural change>`, and note in the body "behavior unchanged, test X all green."

🚩 **Red flag**: the working tree has accumulated 5 uncommitted refactor actions → stop. Once some middle step breaks, you won't be able to tell which one. Go back to the last green point.

---

## 🎯 A refactor needs a "goal" — state it, scope it small, YAGNI the rest

Aimless "tidying while I'm here" is the number-one cause of refactors spiraling out of control. Before starting, answer:

```
Refactor goal: ______ (testability / readability / performance / dependency removal, pick one main axis)
Scope boundary: only touch ______, do not touch ______
Definition of done: when ______ holds, stop
```

| Goal | Measurable done signal |
|---|---|
| Testability | Target unit can be tested in isolation (dependencies injectable/mockable) |
| Readability | Function length/nesting depth/duplication dropped below a set line |
| Performance | A benchmark proves improvement (measure first, then change, see [§6.2](../06_non_functional/02_performance.md)) |
| Dependency removal | Target module no longer imports some package/layer |

**Once scope is set, any other grime you spot along the way is YAGNI** ([§3.5](../03_implementation/05_yagni.md)): don't "while I'm at it" change other modules, add abstraction layers, or pull in new dependencies in this refactor. See something worth doing, log it to the backlog, open a separate pass.

> Performance refactor exception: **no before/after measurement, no starting**. Otherwise you can't prove "the structure changed and it's actually faster," you're just rewording it and feeling good about yourself.

---

## 📜 With no PRD, the "spec" is "existing behavior must be preserved"

Brownfield refactors usually have no PRD. That doesn't mean there's no contract — **the contract is the current state itself**.

- Contract source = characterization tests + existing passing tests.
- "PRD is the contract" becomes here: **existing observable behavior is the contract**, you can't unilaterally change it.
- If you really must change behavior → escalate to a requirements change, go through PRD / [§5.2 PRD Change](../05_conflict_handling/02_prd_change.md), don't smuggle it into the refactor.

When there's no PRD at all and you need a larger change, first read [§8.5 No-PRD Workflow](./05_no_prd.md) to backfill a minimal contract.

---

## 🔀 Refactor vs Rewrite (don't call a rewrite a refactor)

| | Refactor | Rewrite |
|---|---|---|
| Behavior | Must stay unchanged | May change / be redefined |
| Safety net | Existing tests + characterization tests | **Needs a PRD** (contract for the new behavior) |
| Pace | Small steps, stoppable anytime, green anytime | Large chunks, unusable mid-way |
| Risk | Low (each step revertible) | High (needs §7 migration/rollback plan) |
| Trigger | Structure bad but behavior correct | Behavior itself needs redesign |

🚩 When a "refactor" starts needing to **temporarily make a feature unusable**, or you find yourself **redeciding behavior** — that's already a rewrite. Stop, go write a PRD, and prepare a [§7 Migration & Rollback](../07_operations/_index.md) plan. A rewrite is not a scaled-up refactor; it's engineering of a different risk class.

---

## ✅ Refactor pre-flight / wrap-up checklist

**Pre-flight:**
- [ ] git working tree clean (retreat route, see Sentinel's safety nets)
- [ ] target unit's relevant tests **all green**; thin spots have characterization tests backfilled
- [ ] written down: goal / scope boundary / done signal
- [ ] confirmed it's a refactor not a behavior change (passed the table above)

**Each step:**
- [ ] only changed structure, didn't touch behavior
- [ ] tests all green → commit; red → revert this step

**Wrap-up (aligned with [§4 DoD](../04_quality_gates/01_dod.md)):**
- [ ] lint / typecheck / all tests green
- [ ] no smuggled-in bug fixes or new features
- [ ] performance refactor: before/after numbers attached
- [ ] every step committed, working tree clean

> Evidence grading (Sentinel): before claiming "refactor done, behavior unchanged," it must be 🟢 verified — tests actually run and all green. Not run means you can only say 🟡 reviewed, and ask the user to run them.

---

## 🔗 Related Compass sections

- [§8.2 Bug-Fix Workflow](./02_bug_fix.md) — a bug found mid-refactor goes here instead
- [§8.4 Add-a-Feature Workflow](./04_add_feature.md) — changing behavior/adding features is not refactoring
- [§3.5 YAGNI](../03_implementation/05_yagni.md) — pin the refactor scope, no opportunistic expansion
- [§4.1 Definition of Done](../04_quality_gates/01_dod.md) — a refactor must pass DoD too

---

## 📝 Status

v0.5.0 (Phase 2: original content).
