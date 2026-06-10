# §6.1 Non-Functional Requirements (NFR) Overview: Why PRDs Keep Dropping Them

> Part of [Compass](../../SKILL.md) §6 — Non-Functional Requirements
> Why a PRD's feature list is packed while the NFR section is blank, and how to force NFRs out at the DoR stage.

---

## 🎯 Core problem: PRDs structurally over-specify features and under-specify NFRs

Most PRDs look like this:

- "Users can create an order" → three paragraphs, plus schema, plus wireframe
- "The order list should be fast" → **nothing written**. How fast? P95 at how many ms? Tested under how much data? Nobody says.

A feature is "will it work" — visible, demoable, something a PM can write.
An NFR is "is it good enough" — invisible, only surfaces under load testing, and the PM usually **doesn't realize it needs writing**.

Result: the feature spec is detailed down to the field, and the entire NFR category is absent. By the time production load hits, you discover "nobody ever defined the target" — and now what you're changing is architecture, not a one-line if.

---

## 🚨 Why the reverse audit (§11) can't save you

The §11 reverse audit mechanism (M007–M010) takes the PRD's **feature list** and checks it back against the implementation: are the endpoints listed, do the schema fields match, are any pages missing.

> What it checks item by item is "PRD wrote it → did the implementation do it".
> **NFRs were never written into the PRD, so the reverse audit has nothing to compare.** The whole category slips through the gap, zero alerts.

This is the most dangerous thing about NFRs: **the automated defenses are blind to them**. A missing feature implementation gets caught by M008; a missing NFR definition trips no gate at all. The only interception point is further upstream — DoR.

See [§11 reverse audit toolchain](../11_tooling/01_m007_to_m010.md).

---

## 📋 NFR categories Compass tracks

| Category | One line | What breaks if you drop it |
|---|---|---|
| ⚡ Performance | P95/P99 latency, throughput, targets at a given data scale | No target means nobody optimizes; you find out in production that the list takes 8s and the query full-table scans |
| 🔭 Observability | log / metric / trace / alerting | When things break you're flying blind, just guessing; MTTR runs away |
| 🔒 Security | authN/authZ, input validation, secret management, PII | One IDOR or injection point leaks the whole table; the fix is the trust boundary, not a patch |
| 🟢 Availability (SLA) | target availability, degradation strategy, dependency-failure behavior | One third party goes down and your whole site goes with it, because nobody defined "what do I do when it dies" |
| ♿ a11y | keyboard, contrast, ARIA, screen reader | You find out after the fact the whole component set is unusable; retrofitting a11y is a rewrite, not a tweak |
| 🌐 i18n | string externalization, date/number/currency, RTL, plural rules | Hardcoded strings scattered across the whole codebase; adding a second language means redoing the UI layer |

Each of the six has its own chapter: performance ([§6.2](02_performance.md)), observability ([§6.3](03_observability.md)), security ([§6.4](04_security.md)), a11y+i18n ([§6.5](05_accessibility_i18n.md)), availability/SLA ([§6.6](06_availability_sla.md)).

---

## 🔑 KEY: NFRs must be caught at DoR (§2.1)

This is the single most important rule in this chapter:

> **"The PRD didn't write a performance target" is a gap to flag before you write code, not a surprise on load-test day.**

The path for handling a missing NFR is the same Sentinel "pre-flight" as a feature gap — ask inward to get clarity, push outward to map the blast radius. The only difference: for a feature gap you know it's missing just by reading the PRD; for an NFR gap **the PRD is blank, so you have to proactively ask "shouldn't there be a target here"**.

Wire it into the [DoR checklist](../02_definition_of_ready/01_dor_checklist.md): DoR isn't only "are the features fully written", it's also "is each NFR explicitly defined or explicitly marked N/A".

"Not written" and "not needed" are two different things —
- ✅ Passes: "This feature has no performance requirement (internal admin tool, single admin, data volume < 100 rows)" ← explicitly marked N/A
- ❌ Fails: the performance row is entirely blank ← this is a gap, not N/A

A blank must turn into a red line on the [PRD health report](../02_definition_of_ready/02_prd_health_report.md) at DoR.

---

## ✅ NFR present? Checklist (insert into DoR)

For every PRD feature, run the six questions below. **Any one you can't answer = gap, go back and ask the PRD owner.** You may propose a reasonable starting value flagged "to confirm" ([§6.2](02_performance.md) does exactly this for performance targets), but **do not silently pass off a made-up value as an established target** — the final value still needs the owner's ruling.

```text
[ ] ⚡ Performance: is there a measurable target?
      P95/P99 latency? Throughput? Tested at what data scale?
      (Can't answer → not "ignore for now", it's flag to owner)

[ ] 🔭 Observability: what do you look at when things break?
      Does the critical path have logs? Metrics? Are alert thresholds set?

[ ] 🔒 Security: where is the trust boundary?
      Who can call it? Do you verify "logged in" or "is this person" (IDOR)?
      Is input validated? Does it touch PII / secrets?

[ ] 🟢 Availability (SLA): what happens when a dependency dies?
      Target availability? Degradation strategy? Is third-party timeout / failure behavior defined?

[ ] ♿ a11y: (applies only if there's UI)
      Keyboard reachable? Contrast meets standard? Do interactive elements have semantics/ARIA?

[ ] 🌐 i18n: (applies only if there's user-facing copy)
      Are strings externalized? Do date/currency/plurals have locale handling? Do you need RTL?
```

**Interpretation rule**: each cell has only three legal states —

| State | Meaning | DoR pass? |
|---|---|---|
| 🟢 has target | a measurable value is written | ✅ pass |
| ⚪ marked N/A + reason | explicitly says "this feature doesn't need it, because ___" | ✅ pass |
| 🔴 blank | nobody thought about it | ❌ block, flag as gap |

---

## 🪤 Trap: NFRs are invisible until production

A missing feature breaks the first time you run it — feedback is immediate.
A missing NFR is **green all the way through dev, test, and demo**, because:

- Performance: 50 rows on the dev box, of course it's fast. 500k rows in production is where it surfaces.
- Availability: the local third-party mock always returns 200; nobody tested its timeout.
- Observability: a feature you can demo doesn't need logs; what needs logs is production at 3 a.m.
- a11y / i18n: the developer uses a mouse and reads English, so they'll never hit it themselves.

> Invisible ≠ nonexistent. It just puts the bill on the production day, with interest.

**Example** (FastAPI, not mandatory, just illustrating how an NFR hides in dev):

```python
# Looks perfect in dev. Full-table scan in production, P95 spikes to seconds.
@app.get("/orders")
def list_orders(db: Session):
    return db.query(Order).all()   # no pagination, no index hint, no limit
```

If the PRD had a line "list P95 < 200ms @ 100k rows", this snippet would get challenged at DoR / code review. Without that line, it's green all the way to launch.

This is why the NFR interception point has to move upstream to **DoR**, instead of hoping some downstream gate will catch it — there is no downstream gate that catches something invisible.

---

## 🧭 Where to go next

| Section | Content |
|---|---|
| [§6.2 Performance](./02_performance.md) | how to set measurable performance targets and wire them into DoD |
| [§6.3 Observability](./03_observability.md) | the minimal set of log / metric / trace / alerting |
| [§6.4 Security](./04_security.md) | trust boundaries, input validation, test-first security modules |
| [§6.5 a11y / i18n](./05_accessibility_i18n.md) | why retrofitting is a rewrite, and how to build it in from the start |
| [§6 module index](./_index.md) | full overview of this folder |

---

## 🔗 Related Compass sections

- [§2.1 DoR checklist](../02_definition_of_ready/01_dor_checklist.md) — the mount point for the NFR present? checklist
- [§2.2 PRD health report](../02_definition_of_ready/02_prd_health_report.md) — how a blank NFR shows up as a red line
- [§5.1 Vague / bug / gap handling](../05_conflict_handling/01_vague_bug_gap.md) — the same gap path a missing NFR takes
- [§11 reverse audit toolchain](../11_tooling/01_m007_to_m010.md) — why it can't catch NFRs

---

## 📝 Status

`v0.5.0` (Phase 2: original content)
