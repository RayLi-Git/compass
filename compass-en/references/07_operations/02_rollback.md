# §7.2 Rollback: safe retreat after things break

> Part of [Compass](../../SKILL.md) §7 — Operations.
> Have your rollback plan ready before every deploy ships — not improvised at 3 a.m.

---

## 🎯 Core iron rule

**The rollback plan must exist before you ship.** Starting to think about "how do we roll back" only after going live is already too late — by then you're under pressure, sleep-deprived, monitoring is all red, and every decision you make is more error-prone.

> If you can't answer "how does this deploy roll back, how many minutes does it take, who pushes the button," this deploy isn't ready to ship.

This maps to Sentinel's safety net "retreat route": before touching existing production, ensure there's a clean, verified escape path executable within minutes. No escape path, don't go forward.

---

## 🔀 Deploy ≠ Release: decouple with feature flags

The strongest rollback lever is making "ship code" and "enable feature" two separate things.

| Concept | Meaning | Rollback method |
|---|---|---|
| **Deploy** | Code enters the production environment | Need to redeploy the old version (slow) |
| **Release** | Feature actually takes effect for users | Turn off the flag (seconds, no redeploy) |

Wrap the new feature behind a feature flag, and when things break you don't have to roll back the whole version — just turn the flag off. This is the **kill-switch**.

```python
# Example (FastAPI): feature hidden behind a flag, flip it off when things break
if flags.is_enabled("new_checkout_flow", user=user):
    return new_checkout(cart)
return legacy_checkout(cart)   # flag off → back to old path in seconds
```

**Flag usage rules:**
- A kill-switch flag's default must be "off" or "the safe old behavior" (echoes Sentinel security "secure by default")
- The person flipping the flag off shouldn't need to be an engineer, redeploy, or touch git
- Flag flips go into an audit log (who, when, why)
- Once stable in production, schedule a **cleanup of old flags** — otherwise the flag graveyard becomes the next tech debt (reverse YAGNI: keeping unused flags is debt too)

---

## 🟦🟩 Blue-green and canary basics

Two deploy strategies that shrink a deploy's blast radius, with different rollback logic:

| Strategy | How it works | Rollback action | Good for |
|---|---|---|---|
| **Blue-green** | Two full environments, traffic switched all at once | Switch the router back to the old environment (blue) | Rollback needs to be fast and clean |
| **Canary** | New version takes 1% → 5% → 25% of traffic first | Dial the traffic ratio back to 0% | Want to validate with small traffic first |
| **Rolling** | Replace instances one at a time | Reverse-rolling back to the old version (slower) | Resource-constrained |

- **Blue-green** has the cleanest rollback: the old environment is still alive, just switch back — near-zero latency. But you pay for two environments.
- **Canary**'s value is "early detection": when the bad thing only hits 1% of users, that's when you should catch it — not wait until 100% to find out. The canary stage must **watch the metrics**, otherwise you've just delayed the full-fleet explosion by a few minutes.

---

## ⚠️ Migration-rollback trap: code can revert, data may not

**This is the most lethal blind spot in rollback.** You can switch the code back to the old version, but the database's schema changes and already-written data **won't automatically follow it back**.

Classic way to die:

```
1. Deploy v2, migration splits column full_name into first_name / last_name and DROPs full_name
2. v2 breaks, roll code back to v1
3. v1 code reads full_name → column no longer exists → site-wide 500
   (and the first/last data written during those minutes can't go back to full_name either)
```

**Root cause**: a destructive schema change (DROP / RENAME / NOT NULL) is coupled with the code rollback, so when you revert code there's no matching escape path at the data layer.

**Fix**: use §7.1's **expand / contract**. First ship only compatible expand changes; once the code is stable, a later deploy does the contract (drop the old column). This way "rolling back code" never requires "rolling back data."

> Iron rule: **a destructive migration never goes in the same deploy as the code that enables that change.** The contract step is a separate follow-up deploy. See [§7.1 Migration](./01_migration.md).

---

## 📊 Rollback decision criteria: when to push the button

Rollback can't ride on "something feels off." Hard-code the trigger thresholds before shipping, then execute by the book on the spot — no live debate.

| Signal | Threshold to trigger rollback (example, tune per service) |
|---|---|
| Error rate | 5xx ratio > baseline + 1%, sustained > 2 min |
| Latency | p99 > SLO ceiling, sustained > 5 min |
| Key business metric | Checkout success rate / login success rate drops > X% |
| Saturation | DB connection pool / queue keeps approaching the ceiling and still worsening |
| Data correctness | Any data corruption or write error → **roll back immediately, don't wait for the threshold** |

**Decision principles:**
- **Rollback before debug**: when production breaks, restore service first, then chase the root cause slowly. Don't trace wiring inside a burning house (echoes Sentinel: stop the bleeding first, do the root-cause retrospective afterward).
- Agree the thresholds before deploy; don't re-litigate "is this severe enough" on the spot.
- Designate one person with authority to call it (roll-back owner) — no all-hands vote.
- Set an **observation window**: after deploy, actively watch metrics for a stretch (e.g. 30 min) — don't walk away the moment the deploy finishes.

---

## 🛡️ The rollback itself must be verified first

The most dangerous rollback is the one **nobody ever rehearsed — and you find out it's broken too only after pushing the button**.

- Run the rollback procedure once for real in staging and measure how long it takes.
- Confirm the old version's artifact / image still exists and is still deployable (don't let auto-cleanup delete it).
- Confirm that after rollback the old code can read the current data correctly (this is exactly the migration-trap checkpoint).

---

## ✅ Pre-deploy rollback checklist

Tick each item before deploy; if any item can't be ticked → this deploy isn't ready:

- [ ] Rollback method written down (flip a flag? switch blue-green? redeploy old version?)
- [ ] Estimated rollback time known (seconds / minutes / hours) and acceptable
- [ ] Old-version artifact still available, and the rollback procedure rehearsed in staging
- [ ] Any destructive schema changes this time? → if so, confirm they're split into expand/contract so rolling back code doesn't require rolling back data
- [ ] Is the new feature wrapped behind a feature flag / kill-switch
- [ ] Rollback trigger thresholds defined (concrete numbers for error rate / latency / business metric)
- [ ] Roll-back owner designated (who has authority to push, who knows how)
- [ ] Monitoring and alerting in place, able to actively notify when a threshold is hit
- [ ] Post-deploy observation window scheduled, with someone watching
- [ ] Post-rollback verification method known (how to confirm "we're back to a safe state")

---

## 🔗 Related Compass sections

- [§7.1 Migration](./01_migration.md) — expand/contract, give the data layer an escape path too
- [§7.3 Deployment](./03_deployment.md) — the deploy process itself
- [§7 Operations](./_index.md) — module overview
- [§6.3 Observability](../06_non_functional/03_observability.md) — without monitoring you can't measure the rollback thresholds

---

## 📝 Status

v0.5.0 (Phase 2: original content)
