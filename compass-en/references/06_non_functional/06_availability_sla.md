# §6.6 Availability & SLA: What Happens When a Dependency Dies

> Part of [Compass](../../SKILL.md) §6 — Non-Functional Requirements (NFR).
> Turn "the system must be stable" into a measurable target (SLO / error budget), and define "what do I do when it dies" for **every external dependency** up front.

---

## 🎯 Positioning

Availability is the NFR category most easily punted to "we'll deal with it after launch" — until some third party goes down, your whole site dies with it, and you discover **nobody ever defined the degradation behavior**.

This file handles three things:
1. Write availability as an acceptance-testable target (SLA / SLO / error budget).
2. For **every external dependency**, ask "when it times out / dies / slows down, how does my system react?"
3. Catch all this back at [§2.1 DoR](../02_definition_of_ready/01_dor_checklist.md), not at a production incident.

---

## 1. SLA / SLO / Error Budget: Sort Them Out First

| Term | What it is | Who looks |
|---|---|---|
| **SLA** (agreement) | Availability promised externally; breaching it has penalties (refunds / compensation) | Customers / contracts |
| **SLO** (objective) | Your internal target, set a bit stricter than the SLA as a buffer | Engineering team |
| **SLI** (indicator) | The number actually measured (success rate / latency / uptime) | Monitoring |
| **Error Budget** | `1 − SLO`, the allowance for "being broken" | Decides whether you can still take release risks |

**How to use the error budget**: SLO 99.9% → ~43 minutes of allowed downtime per month. Budget left → ship boldly / run risky experiments; budget burned → freeze features, only stability fixes allowed. This turns "should we take this risk" from an argument into looking at a number.

### The "nines" of availability for reference (get a feel first)

| Availability | Allowed downtime per month | Fits |
|---|---|---|
| 99% (two nines) | ~7.2 hours | Internal tools |
| 99.9% (three nines) | ~43 minutes | General SaaS |
| 99.95% | ~22 minutes | Paid critical services |
| 99.99% (four nines) | ~4.4 minutes | Payments / infrastructure |

> ⚠️ Each extra nine raises cost and complexity **exponentially**. Don't default to chasing four nines — first ask the PRD / business "what does an hour of downtime actually cost," then work backward to how many nines you need. Not written → it's a gap in [§2.1 DoR](../02_definition_of_ready/01_dor_checklist.md).

---

## 2. Dependency Failure Behavior: Define It for Every External Dependency

**Iron rule: every additional external dependency you wire in (DB / third-party API / message queue / cache) adds one more "what do I do when it dies" to answer.** Can't answer = DoR gap.

For each dependency, define five behaviors:

| Mechanism | Question | Default approach |
|---|---|---|
| **Timeout** | It hangs and doesn't reply — how long do I wait? | **Always set a timeout.** No timeout = one slow dependency drags down all your threads |
| **Retry** | Should a failure be retried? | Only retry "transient failures," and with **exponential backoff + cap + jitter**. For non-idempotent operations, confirm idempotency before retrying |
| **Circuit Breaker** | It keeps dying — should I stop hitting it? | Consecutive failures hit a threshold → trip, fail fast for a while, don't let requests pile up |
| **Fallback** | When it's unavailable, what do I return? | A cached stale value / default / partial result / a clear degradation message — **not a 500** |
| **Graceful Degradation** | Which features can "be turned off while the main flow stays alive"? | Recommendations column dies → hide recommendations, don't 500 the whole homepage |

### Example (dependency failure decision, annotated per dependency)

```python
# Dependency: recommendations-api (non-critical)
# Timeout: 300ms (the homepage can't wait on recommendations)
# Retry: no retry (non-critical; retrying just drags it out longer)
# Circuit Breaker: 5 consecutive failures → trip for 30s
# Fallback: return empty list → frontend hides the recommendations block
# Degradation: the homepage's other blocks render as normal
async def get_homepage(user):
    try:
        recs = await rec_client.get(user.id, timeout=0.3)
    except (TimeoutError, CircuitOpen):
        recs = []                      # ← fallback, not blowing up the whole page
    return render(user, recommendations=recs)
```

> Contrast: when a **critical dependency** (e.g. payments, primary DB) fails, the right answer is usually NOT a fallback faking success, but **explicit fail closed + a clear error + alerting** (see secure-by-default in [§6.4 Security](04_security.md)). Degradation is only valid when "this block doesn't affect correctness."

---

## 3. Bulkhead: Don't Let One Dependency Drag Down Everything

The bulkhead principle: isolate resources (connection pools / threads) **per dependency**, so that when one dependency slows down it only drains its own pool, instead of exhausting the whole service's resources.

- Recommendations gets one pool, payments one pool, primary DB one pool — they don't fight each other.
- Without a bulkhead: one slow dependency → all threads stuck on it → even healthy dependencies have no threads available → cascade.

---

## 4. The Five Availability Questions to Plug into DoR

For every feature that touches an external dependency / has an availability requirement, [§2.1 DoR](../02_definition_of_ready/01_dor_checklist.md) adds:

- [ ] Which external services does this feature depend on? (List them)
- [ ] What's the timeout for each dependency? (None set = red flag)
- [ ] What's the fallback behavior when each dependency dies? (fail closed or degrade?)
- [ ] Does the PRD define an availability target (SLA/SLO)? No → mark the gap and ask the owner (see [§6.1](01_nfr_overview.md))
- [ ] Which features are "degradable," and which are "must be correct or fail closed"?

---

## 5. How to Verify (Write It into DoD)

Availability isn't "hope it's stable" — you have to be able to prove it:

- **Chaos testing**: in a test environment, **actively make the dependency time out / return 500 / slow down**, and see whether your fallback / circuit breaker actually kicks in. An untested fallback may as well not exist.
- **Timeout measured for real**: don't just set the timeout in code — actually simulate a slow dependency and confirm it really gives up at the configured time.
- **Degradation path visible**: every "dependency dies" path should be run manually at least once, with your eyes seeing the degradation behavior rather than a 500.

> Cautionary tale: locally the third party is always mocked to return 200 and its timeout was never tested — on launch, the first time the third party wobbles, the whole site goes down.

---

## 🔗 Related Compass sections
- [§6.1 NFR Overview](01_nfr_overview.md) — availability is one of the six NFR categories; this file is its dedicated chapter
- [§7.2 Rollback](../07_operations/02_rollback.md) — rollback for service-level failure; complements dependency-failure degradation
- [§6.3 Observability](03_observability.md) — SLIs depend on metrics to measure; the error budget depends on monitoring to compute
- [§6.4 Security](04_security.md) — critical dependency failure must fail closed (secure-by-default)
- [§2.1 DoR](../02_definition_of_ready/01_dor_checklist.md) — availability targets and dependency-failure behavior must be caught before work starts

## 📝 Status
v0.9.0 (Phase 4: completes the §6 NFR set — the SLA/availability chapter deferred from Phase 2).
