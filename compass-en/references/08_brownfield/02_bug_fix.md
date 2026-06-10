# §8.2 Bug Fix Workflow

> Part of [Compass](../../SKILL.md) §8 — Brownfield.
> Fixing a bug in existing code: reproduce first, chase the root cause, lock the behavior, make a minimal change, leave a regression test.

Fixing a bug is not "making the error message disappear." There are two ways an error message can disappear: the bug got fixed, or the bug got hidden.
This workflow exists to force you into the first one.

---

## 🚦 Before you start: confirm this is actually a bug

"The user thinks it's wrong" ≠ "the program has a bug." Classify before you touch anything:

| Situation | Criterion | Where to go |
|---|---|---|
| Code bug | spec says X, code does Y, X is correct | Continue this workflow |
| PRD / spec mismatch | spec says X, code does Y, but **unsure which is right** | Go rule via [§5.3 Cross-document conflict](../05_conflict_handling/03_cross_document.md) |
| Spec is silent | spec says nothing about this scenario | Go to [§5.1 Vague/gap](../05_conflict_handling/01_vague_bug_gap.md) |
| New behavior the user wants | spec doesn't cover it and it doesn't error today, it's just insufficient | This is a feature — go to [§8.4 Add Feature](./04_add_feature.md) |

**The most common trap**: spec says X, code does Y, you change code straight to X — and it turns out X is the stale spec, Y was last time's correct fix.
→ When spec and code disagree, first ask "which one is right," don't assume the code must be wrong. This step goes through §5.3 — don't rule on it yourself inside the bug workflow.

---

## 1️⃣ Reproduce first: No repro, no fix

**No touching production code until you have stable reproduction steps.**

Fixing a bug you can't reproduce means you can't prove you fixed it — you just changed some code and prayed.

Reproduction checklist:

- [ ] Write down **precise** reproduction steps (input, preconditions, order of operations)
- [ ] Run it **at least twice** to confirm stable repro, not a fluke
- [ ] Note the "expected vs actual" two-line comparison
- [ ] Confirm the repro environment (version, data, config) matches the reporter's

If you **can't reproduce reliably**:

| Situation | Action |
|---|---|
| Intermittent, comes and goes | Find the trigger condition first (concurrency? timing? specific data?), don't flail |
| Only happens in prod | Add log / trace to narrow the range — this is the "instrument" move of Sentinel's diagnosis phase, not buckshot |
| Can't reproduce at all | Mark as "repro pending," **don't fix** — downgrade to an observation task |

> ⚠️ "Adding piles of logs with no direction" is a Sentinel shallow red flag. Have a hypothesis before adding logs; the log exists to falsify a hypothesis, not to cast a net.

---

## 2️⃣ Root cause, not symptom

Where the error surfaces is often not where the error originates. Always chase one layer upstream.

This is the core of Sentinel's diagnosis phase. Before fixing the bug, ask:

1. **Is this error a symptom or the source?** E.g. the `null pointer` is at A, but the null was stuffed in by B — the root cause is at B.
2. **Why did this bad value/bad state get here?** Trace all the way back to "the first thing that shouldn't have happened."
3. **Where else can this same root cause surface?** If you only patch the current point, the other entry points will still blow up.

### Bypassing ≠ solving (red flag)

The following all "turn off the alarm" rather than "put out the fire" — stop the moment you see them:

```text
✗ try { risky() } catch { /* swallow it, let it pass */ }
✗ if (x == null) return;        // special-case blocks the symptom, never asks why x is null
✗ value as any                  // press the type error down
✗ adding a 3rd special-case if as a patch
```

> Wanting to cover an error with try/except, adding a 3rd special-case if, casting to `any` — if any of the three shows up, exit code-changing mode and enter Sentinel's diagnosis mode.

---

## 3️⃣ Characterization test: lock first, fix second

The biggest risk in changing existing code is **fixing A breaks B**. The defense: before changing any logic, pin "the current behavior" with a test.

Order matters:

```text
① Write characterization test → lock the currently 'correct' adjacent behavior (goes green)
② Write failing test          → express the correct behavior the bug should have (goes red now)
③ Change production code       → make ② go green, and ① must not go red
```

- **①** is not testing the bug, it's testing "the thing this change absolutely must not break." It's green from the start — if it's red first, you misunderstood the current state, go back to step 2.
- **②** is the bug's red test: precisely matching the reproduction steps you wrote in step 1. It being red proves you actually reproduced the bug.
- Bugs in security modules (Auth / permissions / PII) are **mandatorily test-first**, see [§4.1 DoD](../04_quality_gates/01_dod.md).

> **Example** (FastAPI, illustrative only, not required)
> bug: an expired discount code still works.
> ① `test_valid_code_still_applies()` — locks "an unexpired code applies as usual" (green)
> ② `test_expired_code_rejected()` — an expired code should return 400 (red now, because of the bug)
> ③ fix `apply_discount()` to add the expiry check → ② goes green, ① stays green

---

## 4️⃣ Minimal diff discipline

**A bug-fix commit does one thing: fix this bug.**

You'll see ugly code nearby and itch to refactor it on the side — resist. Reasons:

- A refactor mixed into a bug fix means review can't tell "which line is the fix, which line is the itch."
- On a real regression, `git bisect` / revert will sweep away your fix and the refactor together.
- Widening the diff = widening the "fixing A breaks B" surface, exactly violating step 3's defense.

| Do | Don't |
|---|---|
| Change the fewest lines to make ② go green | Rename variables, tweak formatting, extract functions on the side |
| Record the refactor urge as a separate task | Refactor in the same commit |
| commit: `[fix] module: root cause in one line` | One commit mixing fix + refactor + formatting |

The urge to refactor is reasonable — but it's **another PR**, go through [§8.3 Refactor](./03_refactor.md).

---

## 5️⃣ The regression test is DoD, not bonus

After step 3's failing test (②) goes green, **leave it in the codebase** — it is the regression test, guaranteeing this bug won't come back to life.

Before wrapping up, align with [§4.1 DoD](../04_quality_gates/01_dod.md):

- [ ] **Reproduction steps reproduce** → after the fix, follow the original steps, the bug no longer appears (🟢 verified, with actual run results attached)
- [ ] **Failing test is now green** → and keep it as a regression test
- [ ] **Characterization test still green** → proves adjacent behavior isn't broken
- [ ] **lint / typecheck / full test suite** pass
- [ ] **Diff is minimal** → self-review confirms no smuggled-in refactor
- [ ] **commit** message names the root cause, not just "fix bug"
- [ ] If it's a "painful enough" case (misjudged the root cause / ≥2 hypotheses falsified / root cause spans layers) → write it into the Sentinel log `.claude/debug-log.md`

> 🔬 Before claiming "fixed," grade the evidence strength: 🟢 verified (ran it, evidence attached) / 🟡 reviewed (read the logic, didn't run) / 🔴 speculation. Never say "I ran it" without having run it.

---

## ✅ Bug fix full-workflow quick reference

```text
1. Classify: code bug? or spec mismatch? (mismatch → §5.3)
2. Reproduce: stable repro, otherwise don't fix
3. Root cause: chase upstream, don't stop at the symptom
4. Lock behavior: characterization test (green)
5. red test: express the correct behavior (red)
6. Minimal change: make red go green, characterization stays green
7. DoD: leave the regression test, clean diff, commit names the root cause
```

---

## 🔗 Related Compass sections

- [§5.3 Cross-document conflict](../05_conflict_handling/03_cross_document.md) — who's right when spec says X, code does Y
- [§4.1 Definition of Done](../04_quality_gates/01_dod.md) — regression tests and the wrap-up gate
- [§8.3 Refactor Workflow](./03_refactor.md) — move the "refactor on the side" urge here
- [§8 Brownfield overview](./_index.md) — the map for modifying existing code

---

## 📝 Status

v0.5.0 (Phase 2: original content)
