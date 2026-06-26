# §6.2 Landing Performance Specs

> Part of [Compass](../../SKILL.md) §6 — Non-Functional Requirements (NFR).
> Translate "make it fast" into "measurable numbers," then write the numbers into tests — otherwise performance is forever just talk.

---

## 🎯 Why "Make It Fast" Is Not a Spec

"The page should be fast," "the API can't lag" — these aren't requirements, they're complaints.
What can't be measured can't be accepted, and can't be checked off on the DoD.

Landing a performance spec has exactly one move: **replace adjectives with "metric + number + condition."**

| Vague phrasing | Measurable spec |
|---|---|
| "The API should be fast" | "`GET /orders` p95 < 200ms @ 50 req/s" |
| "Don't use too much memory" | "Single worker RSS < 512MB @ concurrency 100" |
| "Homepage should load instantly" | "LCP < 2.5s (4G/mid-range phone); JS bundle < 200KB gzip" |
| "Don't drag down the DB" | "≤ 3 DB queries per request, no N+1" |

Any performance description without a number, a load condition, or a measurement point is treated as a **DoR gap** (see [§2.1 DoR Checklist](../02_definition_of_ready/01_dor_checklist.md)).

---

## 📐 Three Metric Types: First Pick What to Measure

### 1. Latency — How Long One Request Takes

**Always use percentiles, never the average.** Averages hide things — a pretty p50 doesn't mean nobody's waiting.

| Percentile | Meaning | When you care |
|---|---|---|
| p50 | Half the users are faster than this | Perceived baseline |
| p95 | 95% of users are within this | **Primary acceptance line**, most SLOs use this |
| p99 | The slowest 1% | Tail latency; high-concurrency/paying customers care |

> ⚠️ Write the spec as p95/p99, **not avg**. One 10s request can be diluted by 99 10ms requests into an "average 110ms" — but that one user waiting 10s is your support ticket.

### 2. Throughput — How Much It Handles Per Unit Time

- Units: req/s, msg/s, rows/s.
- **Latency and throughput must be stated together**: "p95 < 200ms" must carry "@ X req/s," otherwise everyone's fast under zero load.

### 3. Resource Budget — What It Costs to Get There

| Resource | Typical metric | Landing point |
|---|---|---|
| Memory | RSS / heap peak | Container limit, OOM line |
| Frontend size | bundle KB (gzip/brotli) | CI bundle-size check |
| DB | query count / slow-query count | Prevent N+1, add indexes |
| Startup | cold start ms | serverless, container scheduling |

---

## 🚧 BUDGET vs GOAL: Separate "Ceiling" from "Wish"

This is the thing in performance specs most often conflated, yet most needing to be kept apart:

| | Performance BUDGET | Performance GOAL |
|---|---|---|
| Nature | **Hard ceiling**, not to be crossed | Wish value, strive toward |
| Consequence of violation | **Blocks the PR / blocks the release** (fail build) | Logged, tracked, queued into backlog |
| Example | bundle ≤ 200KB; p99 ≤ 1s | p95 target 100ms (currently 180ms) |
| Where it lives | CI gate, automated test assertion | tracking doc, dashboard |

**Rule**: only BUDGET counts as a checkbox on the DoD. GOAL goes into the tracking docs as an improvement direction, not as an acceptance gate (see [§3.2 Tracking Docs](../03_implementation/02_tracking_docs.md)).
Consequence of mixing them: either you never pass (using GOAL as the gate), or it's toothless (treating BUDGET as a wish).

---

## ✍️ Write Performance Goals into Tests (This Is What Landing Means)

A verbal goal = no goal. A performance spec's home is an assertion that goes **red**.

### Example: Load-test assertion on p95 (Python / locust-style)

```python
# Not "let's see how fast it runs" — it's "if not fast enough, fail"
def test_orders_p95_under_budget(load_result):
    P95_BUDGET_MS = 200
    TARGET_RPS = 50

    assert load_result.rps >= TARGET_RPS, \
        f"Load condition {TARGET_RPS} req/s not met; this result is invalid"
    assert load_result.p95_ms < P95_BUDGET_MS, \
        f"p95={load_result.p95_ms}ms exceeds budget {P95_BUDGET_MS}ms"
```

Key point: **verify the load condition is met first, then verify latency**. A "beautiful p95" that never hit the target RPS is fake data.

### Example: Frontend bundle budget (CI check)

```jsonc
// Size budget written as config, CI blocks automatically
{
  "budgets": [
    { "path": "dist/main.*.js", "maxSize": "200KB" },
    { "path": "dist/vendor.*.js", "maxSize": "150KB" }
  ]
}
```

### Landing Checklist

- [ ] Every performance BUDGET maps to an assertion that **fails** (not just prints a log)
- [ ] Latency assertions carry a **load condition** (@ N req/s) and verify the load is met first
- [ ] Uses p95/p99, not avg
- [ ] Test data volume close to production scale (100 rows running fast doesn't mean 1M rows will)
- [ ] BUDGET numbers written as named constants, no scattered magic numbers
- [ ] Budget violation blocks CI / PR, not just warns

---

## 🩹 What to Do When the PRD Gives No Performance Goals

Very common. The PRD specifies the feature but not the performance — this is a **DoR gap**, not a blank for you to freestyle.

Process:

1. **Mark it as a DoR gap**, write it into the PRD health report (see [§2.2 PRD Health Report](../02_definition_of_ready/02_prd_health_report.md)).
2. **Propose a default** rather than silently skipping — give a reasonable startable number, marked "to be confirmed."
3. Go through conflict handling: PRD gap + you have a better suggestion → keep it, mark it, await ruling — don't unilaterally treat it as the contract (see [§5.1 Vague/Gap/Bug](../05_conflict_handling/01_vague_bug_gap.md)).

### Defaults You Can Propose (starting points, not scripture)

| Scenario | Suggested default BUDGET |
|---|---|
| Interactive API (read) | p95 < 300ms @ estimated peak RPS |
| Interactive API (write) | p95 < 500ms |
| Background batch | Throughput first; no hard ceiling on per-item latency |
| Frontend first paint | LCP < 2.5s (mid-range phone/4G); initial JS < 200KB gzip |
| Memory | 70% of container limit as the alert line |

> When proposing a default you must also ask: "What's the estimated peak traffic?" Without a load magnitude, all latency numbers are hot air.

---

## 🚫 Anti-Pattern: Optimizing Before You Have a Goal

**The biggest performance anti-pattern: optimize first, define "fast enough" later (or never).**

Optimization without a goal produces:

- **Endless tuning**: always feeling "it could be faster," never able to stop — because there's no "this far and no further" line.
- **Optimizing the wrong place**: changing things by gut feel without measuring first. Touch code that isn't on the hot path and p95 doesn't budge (the symptom is not the root cause — Sentinel's diagnosis discipline: measure before you change).
- **Trading readability for a nonexistent requirement**: turning code into gibberish to save 2ms that nobody asked for. Violates [§3.5 YAGNI](../03_implementation/05_yagni.md).
- **Can't claim done**: with no BUDGET, there's no DoD to check off, and "is the optimization done" is forever unanswerable.

**Iron rule**:

```
measure → set goal (BUDGET) → only then optimize → prove it with an assertion
```

Any "let's just optimize first" urge → stop, fill in a measurable goal first.
Before claiming "optimization done," attach an evidence grade (Sentinel's evidence grading): 🟢 ran the load test, have numbers / 🟡 only read the logic, didn't actually test (say so and recommend running) / 🔴 speculation. **Without running a load test, you don't get to say "it's faster."**

---

## ✅ Landing Check for This Section

- [ ] Every performance requirement is "metric + number + load condition," no adjectives
- [ ] Latency uses p95/p99, throughput carries req/s, resources have a budget
- [ ] BUDGET and GOAL kept separate; only BUDGET enters the DoD
- [ ] Every BUDGET maps to a test assertion that fails
- [ ] PRD missing performance goals → mark DoR gap + propose default + await ruling, don't fill in unilaterally
- [ ] No optimization before there's a goal; back up optimization with measured numbers

---

## 🔗 Related Compass sections

- [§6.1 NFR Overview](./01_nfr_overview.md) — where performance sits in the full NFR picture
- [§6.3 Observability](./03_observability.md) — no metrics means you can't measure p95
- [§2.1 DoR Checklist](../02_definition_of_ready/01_dor_checklist.md) — missing performance goals means not ready
- [§4.1 DoD](../04_quality_gates/01_dod.md) — BUDGET assertions are part of the Definition of Done

---

## 📝 Status

v0.5.0 (Phase 2: original content).
