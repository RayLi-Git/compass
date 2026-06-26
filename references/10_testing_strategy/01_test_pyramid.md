# §10.1 The Test Pyramid and Per-Layer Division of Labor
> Part of [Compass](../../SKILL.md) §10 — Testing Strategy.
> Decides "which layer tests what, and how many" — so you don't push acceptance cost onto the slowest, most fragile layer.

More tests isn't better — **putting them in the right layer** is. The same acceptance criterion, placed in the wrong layer, costs you ten times as much for half the confidence. This chapter gives you the layering rules and the "PRD acceptance criterion → test layer" mapping procedure.

---

## 🔺 The Classic Pyramid

```
        ╱ E2E ╲          few (critical money paths) — slow, fragile, expensive
      ╱─────────╲
    ╱ Integration ╲      medium (module contracts, DB, external)
  ╱─────────────────╲
 ╱       Unit        ╲   many (pure logic, boundaries) — fast, stable, cheap
╱─────────────────────╲
```

Bottom layer is fast, stable, cheap → write the most; top layer is slow, fragile, expensive → write the fewest but test the most critical paths. **The ratio isn't dogma — it's the result of the cost curve.**

---

## 📊 Per-Layer Division of Labor

| Layer | Catches what bug | Cost / speed | Order of magnitude | Should NOT catch |
|---|---|---|---|---|
| **Unit** | Pure-function logic, boundary values, branches, error classification | Millisecond, isolated, zero I/O | Most (hundreds–thousands) | Whether modules connect |
| **Integration** | Module contracts, SQL/ORM, external API shape, serialization, transaction boundaries | Second-scale, needs DB/container | Medium (tens–hundreds) | Whether UI flow works end-to-end |
| **E2E** | Real user journeys work, end-to-end assembly is correct | Minute-scale, fragile, will be flaky | Very few (single digits–teens) | Individual logic branches |

One-line test for placement: **can this bug be reproduced without crossing process boundaries?** If yes → push it down a layer.

---

## 🍦 Anti-Patterns

**Ice-cream cone (inverted pyramid) — the most common way to die:**
- Too many E2E → CI runs 40 minutes, goes red constantly, nobody trusts it, eventually gets `skip`ped
- A button-logic bug that can only be tested by opening a browser → feedback loop measured in minutes
- Symptom: "the tests broke again, just rerun it" becomes the team's catchphrase → equivalent to having no tests

**Testing implementation instead of behavior:**
```js
// ❌ Testing implementation: rename the method and it goes red, refactoring grinds to a halt
expect(svc._buildQuery).toHaveBeenCalledWith('SELECT ...')

// ✅ Testing behavior: input→output contract, internals can change freely
expect(await repo.findActiveUsers()).toEqual([{ id: 1, status: 'active' }])
```
> Iron rule: assert "externally observable behavior" (return values, state changes, calls to collaborators), not private steps. Private methods, call order, and internal fields should never enter assertions.

Other red flags: mocking down to where only mocks talk to mocks; a test named `test1`; one test asserting 10 things.

---

## 🔄 When To Flip It

The pyramid is the **default**, not law. The following situations reasonably shift the center of gravity upward:

| Situation | Adjustment | Reason |
|---|---|---|
| Thin CRUD / BFF (almost no logic, all assembly) | Lean into integration; unit has nothing to test anyway | Logic lives at the boundaries; testing pure functions is fake coverage |
| Glue / orchestration layer (chains multiple services) | Integration-centric | Risk is "does it connect," not "does it compute correctly" |
| Heavy algorithm / billing / rules engine | Unit explodes, one E2E | Risk is branch correctness; only unit can handle combinatorial explosion |
| Legacy with no tests, about to cut into it | First add E2E/characterization tests as a safety net, then fill downward | Before you understand the internals, end-to-end is the only trustworthy net (see ../08_brownfield/03_refactor.md) |

Criterion: **wherever the risk concentrates, that's where the test center of gravity moves**. Don't force fake units onto a layer with no logic.

---

## 🎯 How Many E2E Is "Enough"

It's not "cover everything," it's **cover the money paths**.

E2E inclusion checklist (must satisfy ALL to qualify for E2E):
- [ ] Breaking it directly loses revenue / violates compliance / locks out users (login, checkout, payment, order submission)
- [ ] Real assembly crossing ≥3 systems, where lower layers can't prove the whole path works
- [ ] It's the "happy path" trunk, not the 7th error branch

**Example (e-commerce):**

| Journey | E2E? | Goes where |
|---|---|---|
| Register → login → place order → payment success | ✅ Yes | E2E (core money path) |
| Discount-code calculation rules (spend-1000-save-100, stacking caps) | ❌ | unit (pure logic, many branches) |
| API returns 409 when stock insufficient | ❌ | integration (contract) |
| Retry on payment gateway timeout | ❌ | integration (with a fake gateway) |
| Forgot-password email flow | ⚠️ Depends on revenue impact | mostly integration suffices |

A healthy E2E count for a mid-size product is typically **5–15**, not 50. Every E2E you add adds CI time and flaky probability — only add it if you can afford it.

---

## 🗺️ PRD Acceptance Criteria → Test Layer (Mapping Procedure)

Read the PRD's acceptance criteria one by one and apply this decision:

1. **Is this pure computation / a rule / a boundary?** → Unit
2. **Does this describe a contract between modules or to the outside (DB, API, message format, transaction)?** → Integration
3. **Does this describe a complete user journey that is a money path?** → E2E
4. **Does this talk about performance / security / availability?** → Not in the functional pyramid; goes to its dedicated test type (see next section)

**Example (PRD acceptance criteria mapping):**

| PRD acceptance criterion | Layer |
|---|---|
| "Accept only if amount > 0 and ≤ cap" | Unit |
| "Submitting the same order twice should not create two rows" (idempotency) | Integration (hit DB, verify uniqueness / upsert) |
| "User receives confirmation page after completing checkout" | E2E |
| "List query p95 < 200ms" | Performance test (§6.2, not unit/e2e) |
| "Unauthorized user cannot read another's orders" | Security test + integration (§6.4, test-first) |

> Every acceptance criterion must point to **at least one** test. A criterion that points to nothing = not accepted = DoD does not pass (../04_quality_gates/01_dod.md).

---

## 🚧 NFRs Are Not In This Pyramid

Performance, security, observability, and accessibility have **their own test types** — don't cram them into unit/integration/e2e:

- Performance → load / stress / p95-threshold tests (../06_non_functional/02_performance.md)
- Security → authz/IDOR tests, injection tests, and **write the test before the implementation** (../06_non_functional/04_security.md)
- Boundary and test-first rules → ./02_test_first_boundary.md

Writing a performance SLA as one e2e assertion is the classic misplacement: e2e environments jitter heavily, so it measures inaccurately and can't block regressions either.

---

## ✅ Self-Check Checklist

- [ ] Every PRD acceptance criterion maps to a test at a clearly defined layer
- [ ] E2E covers only money paths, count in the single digits to teens, every one affordable
- [ ] No pure-logic bug pushed up to e2e to catch
- [ ] Assertions are on behavior (input→output / state), not private implementation steps
- [ ] No fake units forced onto thin assembly layers; tests are heavier at the risk-concentrated layer
- [ ] NFRs go to their dedicated test types, not crammed into the functional pyramid
- [ ] CI is all-green and stable, no flaky e2e papered over by reruns

---

## 🔗 Related Compass sections

- [§10 Testing Strategy (this module)](./_index.md)
- [§10.2 The Test-First Boundary](./02_test_first_boundary.md)
- [§4.1 Definition of Done](../04_quality_gates/01_dod.md)
- [§6.1 NFR Overview](../06_non_functional/01_nfr_overview.md)

## 📝 Status
v0.8.0 (Phase 3: original content)
