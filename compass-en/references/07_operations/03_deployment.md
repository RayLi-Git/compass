# §7.3 Deployment Checklist
> Part of [Compass](../../SKILL.md) §7 — Operations.
> A gate before going live: confirm item by item that everything that should pass has passed, then let the code into production.

---

This is a **discipline checklist**, not a CI/CD tutorial.
It does not teach you how to design a pipeline, choose between GitHub Actions and ArgoCD, or write a Dockerfile.
It answers exactly one question: **"Can this build ship right now?"**

Treat it like a pre-flight checklist — no matter how senior the pilot, every takeoff still gets read item by item.

---

## ✅ Pre-deploy gate

Every item below must get an explicit **yes / no / N/A**. Any "no" → **don't ship**.

| # | Check | Pass criteria | Source |
|---|---|---|---|
| 1 | **DoD all green** | lint / typecheck / unit / smoke all pass, no skip masking | [§4.1](../04_quality_gates/01_dod.md) |
| 2 | **Migration plan ready** | schema changes have forward/backward scripts, rehearsed, can roll back | [§7.1](./01_migration.md) |
| 3 | **Rollback plan ready** | you know how to roll back, to which version, and how long it takes | [§7.2](./02_rollback.md) |
| 4 | **Observability in place** | new paths have log / metric / trace, alerts configured | [§6.3](../06_non_functional/03_observability.md) |
| 5 | **Secrets not hardcoded** | keys/tokens via env vars or secret store, not in code, not in log, not in git | [§6.4](../06_non_functional/04_security.md) |
| 6 | **Feature flag config confirmed** | new feature default value correct; rollout scope clear | This doc |
| 7 | **Staging smoke passed** | critical paths run in a prod-like env, not just locally | This doc |

> Iron rule: **an unrehearsed rollback is not a rollback**. Before ticking item 3, ask yourself: "Have I actually rolled back once?"

---

## 🔍 Item details

### 1 · DoD green
Not "I think I'm done" — it's all eight items of [§4.1 DoD](../04_quality_gates/01_dod.md) checked one by one.
Watch especially: did you `skip` / `xfail` / comment out a test just to make CI pass? That's silencing the alarm, not fixing it.

### 5 · Secrets configured, not hardcoded
This is a security red flag, broken out as its own gate. Sweep once before shipping:

```bash
# Example: rough pre-deploy scan (a hit means stop and verify by hand, not auto life-or-death)
git grep -nE "(api[_-]?key|secret|password|token)\s*=\s*['\"]" -- '*.py' '*.ts'
```

A hit isn't necessarily a leak, but **every one must be eyeballed by a human**. See [§6.4 Security](../06_non_functional/04_security.md).

### 6 · Feature flags
- When a new feature ships, the flag is **default off** and opened gradually via rollout — unless the PRD explicitly demands full rollout.
- Decouple flag "on" from "code deploy": deploy first (flag off), confirm stable, then flip the flag.
- Record a "remove-by date" for every flag. A flag that lingers long-term is technical debt.

### 7 · Staging smoke test
Run critical paths in an environment **as close to production as possible** (login → core transaction → logout, etc.).
Passing locally doesn't count — local has no real DNS, certs, network latency, or data volume.

```text
# Example smoke list (adjust per project, not mandatory)
[ ] Health check endpoint returns 200
[ ] One core happy path works end to end
[ ] One known error path returns the correct error code (not 500)
[ ] External dependencies (DB / third-party API) are reachable
```

---

## 🚀 At deploy time

- Ship during a **low-traffic window** — not at peak, not right before Friday close-of-business.
- Have **someone watching** during the deploy — not hit deploy and walk away.
- Order migration vs code per [§7.1](./01_migration.md) (usually expand → deploy → contract).

---

## 📡 Post-deploy verification

Deploy succeeded ≠ launch succeeded. Watch the **4 golden signals** for at least **N minutes**
(N depends on traffic; recommend ≥15 minutes or one full traffic cycle):

| Golden signal | What to watch | Anomaly sign |
|---|---|---|
| **Latency** | p95 / p99 response time | noticeably slower than before deploy |
| **Traffic** | QPS / RPS | suddenly drops near 0 (whole thing may be down) |
| **Errors** | 5xx / exception ratio | higher than baseline |
| **Saturation** | CPU / memory / connection pool | approaching the limit |

> Definitions sourced from [§6.3 Observability](../06_non_functional/03_observability.md).
> **Any signal worsens and can't be quickly stopped → immediately trigger [§7.2 Rollback](./02_rollback.md), don't fight it.**
> Don't stack patches on the error to save it (Sentinel's sunk-cost guard) — roll back first, then find the root cause in a clean environment.

---

## 📣 Who to notify

| When | Notify whom | Content |
|---|---|---|
| Before deploy | team channel | "Preparing to ship X, ETA Y minutes" |
| After deploy | team channel | version number, change summary, monitoring |
| Watch passed | team channel | "X is stable in production" |
| Anomaly / rollback | team channel + on-call + affected downstream | symptom, blast radius, rolled back |

Notification isn't ritual — it's letting **others know what state the system is in**, so when something breaks they don't have to figure it out from scratch.

---

## 🚩 Don't-ship red flags

Any one of these → stop, don't ship:

- DoD has items forced through via skip / any / commented-out tests.
- Rollback "should work in theory" but **has never been rolled back once**.
- Secrets scan has hits no one has confirmed.
- Only local smoke passed, staging not run.
- "Just ship it and fix later if there's a problem" — that sentence itself is a red flag.

---

## 🔗 Related Compass sections
- [§7.1 Migration Plan](./01_migration.md) — schema changes and forward/backward scripts
- [§7.2 Rollback Plan](./02_rollback.md) — rollback triggers, steps, and rehearsal
- [§6.3 Observability](../06_non_functional/03_observability.md) — golden signals and alerts
- [§4.1 Definition of Done](../04_quality_gates/01_dod.md) — the done definition that must pass before shipping

## 📝 Status
v0.5.0 (Phase 2: original content)
