# §9.2 PRD → Effort Estimation

> Part of [Compass](../../SKILL.md) §9 — Collaboration & Handoff.
> Turn a PRD into a credible effort range: count the checklist, surface unknowns, separate "known work" from "research spikes."

---

## 🎯 Core stance

Estimation is a **planning aid**, not a **contract**.

- The contract is the PRD (the §3.2 checklist), not the number you give.
- The value of estimation is "exposing unknowns," not "guessing the right hours."
- An honest p50/p90 range > a confident single-point number.

> If you're asked to "give me an exact number," that's a demand to pretend there's no uncertainty. Refuse. Give a range + list assumptions.

---

## 📐 Estimation flow (five steps)

| Step | Action | Output |
|---|---|---|
| 1 | Count checklist items (§3.2 granularity) | N acceptance items |
| 2 | Tag each with a complexity weight | Weighted effort base |
| 3 | Surface unknowns → split into "known work" vs "research spikes" | Two lists |
| 4 | Apply real-world multipliers (NFR/migration/tests/review) | Adjusted base |
| 5 | Give a p50/p90 range, not a single point | Estimate delivery |

---

## 1️⃣ Count checklist × complexity weight

Start from the §3.2 checklist, apply a complexity weight to each item. Don't pull a total out of thin air.

| Weight | Traits | Baseline effort |
|---|---|---|
| XS | Pure UI copy, single field, config value | 0.5 day |
| S | Single function, one endpoint, clear CRUD | 1 day |
| M | Spans 2 modules, needs new data structure, stateful | 2–3 days |
| L | Cross-layer, new integration, has concurrency/consistency issues | Split! (see below) |

**Iron rule: L is not allowed into an estimate.** L = you haven't split enough. Split down to units of ≤ 1 day each, or that chunk is a hidden unknown.

> **Example**
> Checklist of 8 items: 5×S(1 day) + 2×M(2.5 days) + 1×L
> → L "support offline sync" splits into: conflict detection(M), merge strategy(M), retry queue(S) = 2.5+2.5+1 = 6 days
> Known work = 5×1 + 2×2.5 + 6 = 5 + 5 + 6 = 16 days (then apply multipliers)

---

## 2️⃣ Surface unknowns: the real risk lives here

Anyone can count happy-path effort. Estimates blow up because of **unknowns that never got counted**.

Ask three questions per item:

- [ ] Have I **done exactly this before**? (No → at least S→M)
- [ ] Is there a technical question I **can't answer right now**? (Yes → it's a research spike, not work)
- [ ] The external system / API I depend on — have I **verified its behavior**? (No → tag ⚠️ unverified assumption)

### Known work vs research spike

| | Known work | Research spike |
|---|---|---|
| Can you estimate it | Yes, apply weights | **Can't estimate hours** |
| How to handle | Goes into p50/p90 | Give a **timebox**, e.g. "figure out feasibility within 2 days" |
| Output | A feature | An answer + a re-estimate |

> Disguising a research spike as known work is the #1 root cause of bad estimates. A spike's output is "knowing how to do it," not "having done it." Timebox the spike first, then estimate the work that follows.

---

## 3️⃣ Estimation traps: what you forgot isn't code

Estimating only the happy path is the most common collapse. The items below **always** exist yet **always** get missed:

| Missed cost | Maps to Compass | Typical share |
|---|---|---|
| NFR (performance / observability / security / a11y) | §6 NFR | +20~40% |
| Data migration / rollback plan | §7 Operations | +10~30% |
| Tests (unit + integration) | §10 Testing | +30~50% |
| Code review + addressing review comments | §4 DoD | +15% |
| Deploy / canary / monitoring wiring | §7 Operations | +10% |

### Real-world multiplier

```
real effort = known-work base × (1 + NFR + migration + tests + review + deploy)
```

> **Example**
> Known work 15.5 days, apply: tests +40%, NFR +25%, review +15%, deploy +10%
> → 15.5 × 1.90 ≈ **29 days**
> If you report 15.5, you missed nearly half.

Don't bury multipliers in a "let me pad it a bit" gut feel — **list each one out** so whoever reviews your estimate can challenge each item.

---

## 4️⃣ Give a range, not a point: p50 / p90

A single-point estimate is lying. Give two numbers:

- **p50**: 50% chance you finish in this (median, if it goes smoothly).
- **p90**: 90% chance you don't exceed it (includes reasonable hiccups).

| Signal | p90 / p50 ratio | Reading |
|---|---|---|
| All known work, done similar before | ~1.3 | Healthy |
| 1~2 research spikes | ~2.0 | Run the spikes first, then re-estimate |
| PRD hasn't met DoR | > 3 or "can't estimate" | **Stop, fix the PRD first** |

> The p90/p50 ratio is your "uncertainty thermometer." Ratio blows up → the problem isn't estimation technique, it's that the input (PRD) is garbage.

---

## 5️⃣ DoR and "I can't estimate"

A garbage PRD pumps in huge uncertainty. A number produced before the PRD meets [DoR](../02_definition_of_ready/01_dor_checklist.md) disguises your guess as a commitment.

### When to just say "can't estimate"

If any of the following appear, reply "I can't estimate until the PRD meets DoR" and point out what's missing:

- [ ] Acceptance criteria vague / no checklist (§3.2 granularity insufficient)
- [ ] Core terms undefined ("real-time," "high-volume," "secure" not quantified)
- [ ] NFR not mentioned at all (→ no basis to apply multipliers, see §6)
- [ ] Migration / compatibility strategy blank (→ §7)
- [ ] More than half the items are actually research spikes

> This isn't slacking. Giving a number you know is wrong does more harm than saying "can't estimate" — it gets treated as a commitment and pinned to the schedule.

### **Re-estimate** after DoR

PRD fixed, spikes done → **re-estimate**. The first estimate was a snapshot taken when the input was garbage; once it's stale, throw it out.

---

## ✅ Estimate delivery checklist

Before reporting an estimate, run each item:

- [ ] Counted from the §3.2 checklist, not by feel
- [ ] Each item tagged with a complexity weight, no L mixed in
- [ ] Known work / research spikes **listed separately**
- [ ] Spikes given a timebox, not estimated as work
- [ ] Real-world multipliers **listed item by item** (tests/NFR/migration/review/deploy)
- [ ] Delivered a p50/p90 range, not a single point
- [ ] Listed the ⚠️ unverified assumptions
- [ ] Stated explicitly "this is a planning aid, not a commitment; re-estimate when the PRD changes"

---

## 🔗 Related Compass sections

- [§2.1 DoR Checklist](../02_definition_of_ready/01_dor_checklist.md) — the input gate for estimation; don't estimate before DoR
- [§3.3 Implementation Order](../03_implementation/03_implementation_order.md) — splitting and sequencing, the next step after estimating
- [§4.1 Definition of Done](../04_quality_gates/01_dod.md) — source of the review/test wrap-up cost
- [§9.1 Who Decides](./01_who_decides.md) — when you can't estimate, who rules on completing the PRD

---

## 📝 Status

v0.8.0 (Phase 3: original content).
