# §10.2 The Real Boundary of test-first + coverage Targets

> Part of [Compass](../../SKILL.md) §10 — Testing Strategy.
> Where test-first actually pays off vs. where it's just ritual; coverage is a floor detector, not a proof of quality.

[§4.1 DoD](../04_quality_gates/01_dod.md) and DoR **mandate** test-first for Auth / permissions / PII.
This file handles the rest of the gray zone: beyond security modules, **where else should you test-first**, where is test-first pure overhead, and what the coverage number actually proves vs. doesn't.

Two common inverse mistakes:
- Misreading "mandatory test-first" as "test-first everything" → writing tests on throwaway prototypes, wasted effort.
- Treating "80% coverage" as a pass certificate → pretty number but not a single assert, equals no test.

---

## 1️⃣ Where test-first pays off (beyond security modules)

The value of test-first isn't "tests" — it's that it **forces you to spell out behavior before you write**. Worth it or not depends on how hard the behavior is to define.

| Scenario | test-first? | Why |
|---|---|---|
| Auth / permissions / PII | ✅ Mandatory ([§4.1](../04_quality_gates/01_dod.md)) | Highest cost of error; holes invisible to the naked eye |
| Complex business logic (billing, discounts, tax, scheduling) | ✅ Strongly recommended | Many rules, many boundaries, one change ripples to many |
| Tricky edge cases (off-by-one, time zones, empty sets, overflow) | ✅ Strongly recommended | Boundaries are bug breeding grounds; write the case first or you'll miss it |
| Bug fixes | ✅ red test first | See [§8.2](../08_brownfield/02_bug_fix.md); a red test proves you actually reproduced it |
| Algorithms / pure functions (input→output well-defined) | ✅ Worth it | No side effects, easy to assert, test-first has near-zero friction |

> **One-line criterion**: if you **can't articulate what "correct" looks like before writing it**, test-first — writing the test forces you to think it through.

---

## 2️⃣ Where test-first is overhead

Not laziness — these are scenarios where "behavior definition" is so cheap that writing the test first slows you down, or the test itself offers no protection.

| Scenario | test-first? | Use instead |
|---|---|---|
| Throwaway prototype / spike | ❌ | Just make it run, discard once validated (see [§3.5 YAGNI](../03_implementation/05_yagni.md)) |
| Pure glue (wire A's output into B, reformat) | ❌ | One integration / smoke test on the wiring point is enough |
| Trivial CRUD (no business rules, framework passthrough) | ⚠️ Low priority | Test "is the wiring right," don't test the ORM itself |
| Config / constants / DTO declarations | ❌ | No logic means nothing to assert |
| Behavior of a third-party library | ❌ | That's its test, not yours |

⚠️ Red flag: you find yourself writing a test for "does the framework behave per its docs" — stop. That's not your responsibility boundary.

> The prototype exception **does not apply** to Auth/PII: the moment a prototype touches real user credentials or PII, it escalates back to mandatory test-first and is no longer throwaway.

---

## 3️⃣ Coverage targets: 80% is a heuristic, not law

"80% coverage across the project" is a **convenient default**, not a hard line every file must hit. Tune it per zone:

| Zone | Reasonable target | Rationale |
|---|---|---|
| Payments / amounts / permission decisions | Near 100% (incl. branches) | One wrong branch is real money or privilege escalation |
| Core business logic | 85–95% | Wide ripple, high regression cost |
| General application layer | 70–80% | The source range of the 80% heuristic |
| Generated code / boilerplate / DTO | Low or excluded | Testing it = testing the generator, zero information |
| UI glue / framework scaffolding | Low | Poor ROI, smoke tests cover the floor |

**Anti-pattern**: to push the global number from 78% to 80%, you backfill a pile of assertion-free tests for getters/DTOs. The number hits target, the untested branch in payment logic is still there. **You optimized the metric, not safety.**

---

## 4️⃣ Why high coverage ≠ safe

line/branch coverage measures "this line **was executed**," not "this line's result **was asserted**." Those are very different things.

```text
Example: 100% line coverage, zero protection

def apply_discount(price, code):
    rate = lookup_rate(code)      # executed ✓
    return price * (1 - rate)     # executed ✓

# Test:
def test_discount():
    apply_discount(100, "SAVE10")   # no assert!
```

Both lines of `apply_discount` are "covered," and the coverage tool reports 100%. But this test **asserts nothing** — it stays green even if `rate` is computed as double.

> Coverage only tells you "**where nothing was ever touched**" (floor detector). It does **not** tell you "is the touched code correct." High coverage + weak asserts = false sense of safety.

Correct use of the floor detector:

- [ ] Read the coverage report for **0% / red** blocks — those are "not even executed" blind spots; backfill them first.
- [ ] For high-risk files look at **branch** coverage, not just line coverage (error branches are often 0%).
- [ ] Do **not** chase the global percentage as a quality KPI; the cheapest way to raise it is padding.

---

## 5️⃣ mutation testing: the harder signal (brief)

To know "will the tests actually catch a mistake," coverage can't answer; mutation testing can.

Mechanism: the tool automatically mutates production code (change `>` to `>=`, `+` to `-`, delete a line…) to create "mutants," then reruns your tests.

- Test goes **red** → the mutant is "killed," meaning the test really guards that logic.
- Test stays **green** → the mutant "survives," meaning even if this code were wrong, your tests wouldn't notice — missing or too-weak assert.

That assert-free `apply_discount` test from the start of §4 lets almost every mutant survive: mutation score near 0, even with 100% coverage. This is exactly the hole coverage can't see.

> Pragmatic use: don't run it project-wide (slow). Run it once over the high-risk modules — **payments / permissions / core business** — see which mutants survive, and backfill asserts. Treat it as a closing health check, not a daily gate.

---

## ✅ Decision cheat sheet

```text
Should I test-first?
  Touches Auth/permissions/PII ... always YES (mandatory, §4.1)
  Can't articulate "correct" ...... YES (the test forces you to think it through)
  Complex business / tricky edge .. YES
  Bug fix ......................... red test first (§8.2)
  Throwaway prototype / pure glue / trivial CRUD  NO (or one smoke test as floor)

How to use coverage?
  As a floor detector → find 0%/red blind spots, backfill first
  Not a quality certificate → don't chase the global percentage, don't pad assert-free tests
  For high-risk files look at branch coverage, not just line coverage
  Want to verify tests really work → run mutation testing on high-risk modules
```

When **not** to write tests: prototypes, pure config/constants, third-party behavior, generated code, and "to push the number past the threshold" — beware of the last one especially, that's optimizing the metric, not safety.

---

## 🔗 Related Compass sections

- [§10.1 Test Pyramid](./01_test_pyramid.md) — which layer of test to write (unit/integration/E2E ratios)
- [§4.1 Definition of Done](../04_quality_gates/01_dod.md) — source of mandatory test-first for Auth/PII and the wrap-up gate
- [§8.2 Bug Fix Workflow](../08_brownfield/02_bug_fix.md) — red test / characterization test ordering for bug fixes
- [§3.5 YAGNI](../03_implementation/05_yagni.md) — the boundary of prototypes and things you shouldn't write

---

## 📝 Status

v0.8.0 (Phase 3: original content)
