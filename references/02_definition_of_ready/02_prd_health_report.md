# §2.2 PRD Health Report and Failure Handling

> Part of [Compass](../../SKILL.md) §2 — Definition of Ready.
> After running the DoR checklist, produce a structured health report and make an explicit go / no-go ruling.

---

## 1. Why a report, not just checkboxes

The DoR checklist by itself only answers "which items passed, which didn't." But **not passing ≠ can't start**—almost no real PRD is 100% perfect. The value of the health report is sorting "failed items" into two piles:

- 🔴 **blocker**: a hole that means you'll be building on quicksand (starting = wasted work)
- 🟡 **minor**: a small hole you can mark with an assumption and fill in as you go

**DoR is not "blocking imperfect PRDs," it's "distinguishing which imperfections will block your path and which won't."** Confusing the two means either letting through what should be blocked (building on quicksand), or hard-blocking what shouldn't be (process paralysis). The report forces you to make this classification.

---

## 2. Health report format (Markdown template)

After running the DoR checklist, output the following structure:

```markdown
## PRD Health Report — <PRD name / §section>

**PRD size**: <S / M / L> (estimated file count, module count, contains security module?)
**Health pass rate**: <X / Y items passed> (XX%)

### 🔴 Blocker gaps (don't start without filling)
- [ ] <hole 1>: <why it's a blocker>
- [ ] <hole 2>: …

### 🟡 Minor ambiguities (mark assumption, can start)
- [ ] <ambiguity 1>: <the assumption I'll adopt>
- [ ] <ambiguity 2>: …

### Recommendation
<🟢 start / 🟡 mark assumptions and start / 🔴 return and await fill> — one-line reason
```

> Empty blocker section = no quicksand. Having items in the minor section is normal, not a failure signal.

---

## 3. Failure handling decision tree

Once the report is produced, rule per the table below. **Note: the vast majority of real PRDs land at 🟡.**

| Status | Criterion | Action |
|---|---|---|
| 🟢 healthy | pass rate > 90% and **no blocker** | start directly |
| 🟡 small holes | has minor ambiguities, but **no blocker** | **mark assumptions and start** (see §3.1) — don't get stuck on small holes |
| 🔴 has blocker | hits any blocker condition below | **return and await fill, don't start** (see §3.2) |

### 3.1 🟡 Mark assumptions and start

Minor ambiguities **should not block starting**. Handling:

1. In the report's 🟡 section, write down "the assumption I'll adopt" for each ambiguity (take the more concrete, more conservative side)
2. Route these ambiguities to [§5.1.1 PRD vague handling](../05_conflict_handling/01_vague_bug_gap.md), annotate per that process, then keep writing
3. Leave the assumption list in progress / development log, for later user ruling or correction
4. Start

> Key: minor holes are "converge as you write," not "stop and hold a meeting." The cost of stopping to hold a meeting is usually far higher than a well-annotated assumption.

### 3.2 🔴 Return and await fill

Hitting any of the following is a blocker—**stop, don't start**:

- Core endpoint / main data flow has **no schema** (request / response shape undefined)
- **Authentication or authorization ownership unclear**: who can call, verify identity vs verify it's the person (IDOR) undefined
- PRD **self-contradiction**: two places give conflicting specs for the same behavior
- Acceptance criteria (DoD / acceptance criteria) entirely missing, can't judge "done"

Handling:

1. In the report's 🔴 section, list the blockers and clearly write "why starting would blow up"
2. Return to the PRD author / user to fill in, record per the matching branch in [§5.1 conflict handling](../05_conflict_handling/01_vague_bug_gap.md)
3. **Don't fill in blockers from your own imagination**—guessing a core schema and then building on it all the way is the textbook case of building on quicksand

> **Starting on a blocker = building on quicksand.** The few minutes of awaiting a fill are far cheaper than the few hours of rewriting the whole block after the fill arrives.

---

## 4. The judgment boundary between blocker vs minor

Not sure which kind a hole is? Ask one question:

> **"If I don't fill this hole, is there any chance what I write will have to be torn down and redone wholesale?"**

- Yes → 🔴 blocker (schema, auth, self-contradiction all fall here: filling them later overturns what you've written)
- No, it's just guessing some branch behavior → 🟡 minor (mark assumption, a few lines changed at most)

| Example (language-neutral) | Classification |
|---|---|
| Example: `POST /orders` request body fields not listed at all | 🔴 blocker |
| Example: behavior when order amount is negative not written in PRD | 🟡 minor (assumption: reject and return 400) |
| Example: PRD §3 says "only the person can edit," §7 says "admins can also edit" | 🔴 blocker (self-contradiction) |
| Example: list default sort order not specified in PRD | 🟡 minor (assumption: by creation time desc) |
| Example: whether "user data" needs identity verification not written clearly | 🔴 blocker (auth ownership unclear) |

---

## 5. Anti-pattern: treating DoR as a bureaucratic gate

The purpose of DoR is to **save time**, not to manufacture ritual. The following symptoms mean it's gone off the rails:

- ❌ Stopping the whole task to hold a meeting over one minor ambiguity → should mark assumption and start
- ❌ A medium task's health check ran half an hour and wrote a three-page report → over-engineering
- ❌ Computing pass rate to two decimal places but not splitting blocker / minor → missing the point
- ❌ Treating "PRD imperfect" directly as "PRD failed" and returning it → no PRD passes this gate

> **Scale effort with task weight** (see [§1.2 three-tier](../01_foundations/02_three_tiers.md)): a medium task's health check should be a **few-minutes** affair—scan the list, list blockers, classify minors, make the ruling. Only L-level or security-module tasks are worth a full report.

---

## 6. Relationship to other gates

- **DoR is the dual of DoD**: DoR guards "is the PRD clear enough before starting," [§4.1 DoD](../04_quality_gates/01_dod.md) guards "is the implementation complete enough before finishing." Two gates, one in one out—miss either side and things leak through.
- **Holes found here feed §5**: minor ambiguities go to [§5.1.1](../05_conflict_handling/01_vague_bug_gap.md), blocker returns are also recorded per §5. The health check isn't the endpoint, it's the starting point that sorts holes into downstream flows.
- **If the PRD changes again after starting**: that's the domain of [§5.2 PRD change](../05_conflict_handling/02_prd_change.md), not within the DoR one-time health check.

---

## 🔗 Related Compass sections
- [§5.1 static three-track conflict](../05_conflict_handling/01_vague_bug_gap.md) — minor ambiguities / blockers found in the health check are sorted and handled here
- [§4.1 DoD](../04_quality_gates/01_dod.md) — DoR's dual gate: hard acceptance before finishing
- [§1.2 three-tier](../01_foundations/02_three_tiers.md) — the basis for scaling health-check effort with task weight
- [§3.1 PRD Intake](../03_implementation/01_prd_intake.md) — the PRD absorption step before the health check
- [§2 Definition of Ready](./_index.md) — the module this section belongs to and the DoR checklist entry point

## 📝 Status
v0.5.0 (Phase 2: original content).
