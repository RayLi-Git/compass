# §9.1 Who Decides What

> Part of [Compass](../../SKILL.md) §9 — Collaboration.
> §5 conflict handling always says "await the user's ruling" — but in a real org "the user" splits into multiple roles. This file routes conflict types to the right decision-maker.

The §5 files keep saying "stop, log, await the user's ruling." The problem: **"the user" is not one person.**
An eng lead can't rule on a product-behavior conflict; a PM shouldn't call the shot on architecture selection; nobody overrides what security says on a security/compliance conflict.
Throwing every conflict at the same "user" outsources the ruling to "whoever's loudest in the room." This file's job: **decide who has the authority to rule first, then go ask.**

---

## 🧭 Ruling Routing Table

| Conflict type | Who decides | Why them | Info you must have ready before asking |
|---|---|---|---|
| Product behavior / scope (whether to build it, what it looks like) | PM / product owner | Owns "user value / prioritization" | Each option's user impact, cost estimate, whether it touches already-committed scope |
| Architecture / tech selection (which approach, whether to add a dependency) | Architect / tech lead | Owns "long-term maintainability / consistency" | Trade-off table per option, compatibility with existing architecture, rollback cost |
| Security / compliance (PII, auth, permissions, regulation) | Security / legal | Owns "org risk / legal liability" | Data classification, attack surface, compliance clause citation, least-privilege option |
| Bug in the PRD itself (spec self-contradicts / is wrong) | PRD author | Only they know which was the "intent" | Source quotes of both contradicting passages, your two guessed readings, downstream impact of each |
| Release timing (when to ship, whether to roll back) | Release manager | Owns "release cadence / risk window" | Change risk level, rollback plan, other dependent releases, monitoring readiness |

> **Iron rule**: you can only "prepare the info and go ask," you cannot "decide for the decision-maker." Showing up underprepared forces them to call the shot on incomplete info — they call it wrong, the blame is still on you.

---

## 🔀 How to Route a Conflict to the Right Person

```text
Got a conflict →
  1. Does it change "behavior the user sees / experiences"?      → product behavior → PM
  2. Does it change "code structure / tech dependencies"?         → architecture → tech lead
  3. Does it touch "user data / auth / permissions / regulation"? → security → security/legal (highest veto)
  4. Is the root cause "the PRD itself is wrong / contradicts"?   → PRD bug → PRD author
  5. Is it "when to ship / whether to roll back"?                 → release timing → release manager
```

**One conflict can hit multiple branches** — e.g. "to make the ship date, downgrade PII encryption to plaintext storage" is both #3 and #5.
Rule: **security (#3) is a gate, not a vote.** The moment #3 is hit, security's veto takes precedence over every other role's "want." Clear security first, then talk timing.

---

## 🎩 Solo Mode: You Wear Every Hat

With no org, just you and Claude, all five roles above are you.
**The danger isn't that you play multiple roles — it's that you let the "strong hat" eat the "weak hat"** — usually "product wants to ship now" steamrolling "security says not yet."

The solo discipline is to **wear the hats separately and record them separately:**

- [ ] Before ruling, explicitly write "which hat I'm wearing now" — `[PM view]` / `[Security view]`, don't blend them into one paragraph
- [ ] **The security hat has veto power and must speak separately** — you can't silence security just because "I'm also the PM and really want to ship"
- [ ] When hats conflict, **write it down, then rule** — don't "just feel it through" in your head
- [ ] Record the ruling conclusion in `.claude/progress.md` (decisions don't rely on conversation memory — this is Sentinel's re-anchor principle)

> **Example (solo, anti-pattern)**
> You're rushing a demo, the PRD doesn't say the password must be hashed.
> ✗ "I'm the user, I call it — store plaintext for now, fix after the demo" — the product hat ate the security hat.
> ✓ `[Security view]` plaintext password = fail, this isn't open to ruling, hashing is the secure-by-default floor; `[PM view]` the demo scope can drop other features to buy time.
> The security hat keeps its veto in solo mode too — this is exactly the "await ruling" §5 talks about, just that the decision-maker is "you wearing the security hat."

---

## ⬆️ Escalation: When Decision-Makers Disagree With Each Other

When two roles are each within their own authority but reach opposite conclusions (classic: tech lead wants a rewrite, release manager wants to ship on schedule), **don't pick a side yourself and make the other swallow it.**

Escalation flow:

| Step | Action |
|---|---|
| 1. Freeze | Stop, don't implement either side first — avoid creating a fait accompli |
| 2. Write shared facts | List the facts both sides agree on + each side's trade-offs, lay the disagreement flat on one page |
| 3. Find common superior | Escalate to both parties' common superior (e.g. eng manager / product head) to rule |
| 4. Record ruling + rationale | Write the conclusion **and its rationale** into the tracking doc, reusable for the next conflict of the same type |

> Solo-mode "escalation" = escalate to Sentinel 🔴 heavy: load the skill, run the disagreement as a decision needing evidence grading, not an intuition coin-flip.

---

## 🔗 Tying Back to §5 Conflict Handling

Those "await the user's ruling" in §5 can now resolve to "await the **right** decision-maker":

- The **PRD bug (§5.1.2)** in [§5.1 vague / bug / gap](../05_conflict_handling/01_vague_bug_gap.md) → decision-maker is the **PRD author**, not just any reviewer
- The scope change in [§5.2 PRD change](../05_conflict_handling/02_prd_change.md) → decision-maker is the **PM / product owner**
- [§5.3 cross-document conflict](../05_conflict_handling/03_cross_document.md) → decision-maker is the **domain owner** of that document / domain (architecture doc → tech lead, security spec → security)
- [§5.4 multi-PRD conflict](../05_conflict_handling/04_multi_prd.md) → cross-PRD prioritization → escalate to common superior

**Judgment shortcut**: before saying "await ruling," ask yourself one thing — "does the person I'm about to ask have authority that covers this conflict?" If not, you've routed it wrong.

---

## ✅ Pre-Wrap Self-Check

- [ ] Every parked conflict is tagged with "who the decision-maker is," not just "await the user"
- [ ] For security / compliance conflicts, confirm security's veto wasn't overridden by another role
- [ ] In solo mode, conflicting hats spoke separately and were written into progress.md
- [ ] Where decision-makers disagree, it's frozen + escalated, no sneaking a side-pick
- [ ] Ruling conclusion plus rationale recorded in the tracking doc, reusable next time

---

## 🔗 Related Compass sections

- [§5.1 vague / bug / gap](../05_conflict_handling/01_vague_bug_gap.md) — the PRD bug (§5.1.2) decision-maker is the PRD author
- [§5.3 cross-document conflict](../05_conflict_handling/03_cross_document.md) — cross-document conflicts are ruled by the domain owner
- [§3.2 Tracking Docs](../03_implementation/02_tracking_docs.md) — where the ruling conclusion and rationale are recorded
- [§9 Collaboration overview](./_index.md) — cross-person / cross-AI collaboration map

---

## 📝 Status

v0.8.0 (Phase 3: original content)
