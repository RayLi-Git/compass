# §5.1 PRD Vague / Bug / Gap: Three-Track Handling

> Part of [Compass](../../SKILL.md) §5 — Conflict Handling.
> When the PRD doesn't match reality, route the "solvable", the "unsolvable", and the "should-add" into three different handling tracks — so you don't stop where you shouldn't, or barrel ahead where you should stop.

---

## Why split PRD conflicts into three categories?

In practice "the PRD differs from what I expected" is actually three different things, and handling them mixed together is a disaster:

- **Vague**: PRD is unclear, but either reading lets you pick one and keep going → don't stop.
- **Bug**: PRD is self-contradictory, logically wrong, no reading works → must stop, await ruling from the user.
- **Gap + implementation adds something better**: PRD didn't write it, but while coding a small enhancement aligned with the design principles naturally surfaces → don't just YAGNI-cut it, and don't expand scope on your own authority either; record it and await ruling.

The three sections below are the SOPs for these three tracks. §5.1.4 at the end gives you a cheat sheet.

> 📍 **This file covers the three categories of "static PRD" conflict** (vague / bug / gap). "Dynamic conflicts" — mid-stream PRD changes, cross-document conflict (PRD vs ADR vs API contract), multi-PRD dependencies — see [§5.2](02_prd_change.md), [§5.3](03_cross_document.md), [§5.4](04_multi_prd.md) (all delivered).

---

## §5.1.1 PRD Vague (unclearly written)

**Symptom**: PRD is internally inconsistent, vaguely described, or the same thing is written two different ways in two places — but **either reading is workable, neither blows up**.

### 4-step handling

1. **Record both original passages**
   In the development log (see [§3.2 Tracking Docs](../03_implementation/02_tracking_docs.md)) under the "PRD Ambiguity" block, quote both original passages, noting their source sections.

2. **Decide which side to take, in this priority order**:
   1. **The more concrete, more verifiable side** (clear inputs/outputs, conditionals, boundary values)
   2. **The newer section** (what appears later in the PRD is usually the revision)
   3. **The side consistent with the "design principles / core philosophy" section**
   4. **The side consistent with the glossary / term definitions**

3. **Adopt it and continue, don't interrupt to ask the user**
   Vague is not a bug; making the call yourself is the judgment a sentinel should have.

4. **Annotate the matching PRD checklist row: "※ Took §X.Y reading"**
   So when the user reviews later they can see your decision points at a glance and quickly veto or confirm them.

### Key principle

> Vague doesn't stop work. Stopping is what §5.1.2 is for.
> Once you've picked, you leave a trace in the checklist, so the user can overturn it any time they look back — far cheaper than throwing a question at the user for every vague spot.

---

## §5.1.2 PRD Bug (written wrong)

**Symptom**: what you found isn't vagueness, it's a **logic error**. Typical examples:

- Permission matrix self-contradicts; either reading violates another rule
- API signature conflicts with schema; either way you write it, it fails
- A state machine transition doesn't exist, but the PRD requires it to run
- Math/business-logic formula is wrong, doesn't match the worked example

Criterion: **no reading works** — this is the mirror image of §5.1.1's "either reading is workable".

### 6-step handling (stop → record → await ruling)

1. **Stop immediately, don't keep writing that module**
   Don't force-write something you know is wrong.

2. **Don't "fix" the PRD yourself**
   The PRD is the contract; your job on finding a bug is to report it, not to amend the contract. Amending it means secretly swapping the user's intent for your guess.

3. **Record in the development log under the "PRD Issues" block** (tag `[SKIPPED-PRD]`):
   - Quote the original text (which paragraphs, which sections)
   - **Why you think it's wrong rather than vague** (this point matters most — you have to convince yourself and the user)
   - 2–3 suggested fixes, each with its cost

4. **Skip that module, continue with other unaffected modules**
   Don't let one PRD bug stall the whole sprint. Keep doing what can proceed in parallel.

5. **Mark the progress.md todo "⚠ Awaiting PRD ruling"**
   So the user knows where this line is stopped and why.

6. **Backfill after the user's ruling**
   Once the ruling comes down, move that module out of SKIPPED state, write it per the ruling, and mark that debug log entry resolved.

### Key principle

> You're not the author of the PRD, you're its executor.
> If your first reaction to a bug is "let me just fix it for you", that's overstepping; the correct reaction is "stop, log, wait".

---

## §5.1.3 PRD Gap + implementation adds something better

**Symptom**: while coding, a reasonable small enhancement that the PRD **didn't spell out** but that **aligns with the design principles** naturally surfaces.

E.g.: API response returns an extra `updated_at` field so the frontend can compute cache invalidation; middleware adds an extra `X-Content-Type-Options: nosniff`; a boundary input gets a reasonable fallback.

The trap in this situation: **straight YAGNI-cutting** loses a genuinely valuable enhancement; **silently keeping it** sneaks in scope expansion. So take a middle path — **keep + flag + await ruling**.

### 5-step handling

1. **Don't cut it back immediately**
   First acknowledge this small enhancement was thought through, not slapped on.

2. **Record in the development log under the "PRD Gaps" block**:
   - What you implemented (specific field / header / behavior)
   - Where the PRD gap is (§X.Y should have written it but didn't)
   - Why it's better (which design principle / security iron rule / UX consideration it aligns with)
   - What's missing if you don't do it (consequences of the gap)

3. **Mark the progress.md todo "⚠ Awaiting PRD enhancement ruling"**

4. **Keep the implementation for now, continue other modules**
   Don't stall over this small enhancement, but don't pretend it doesn't exist either.

5. **Await the user's ruling**:
   - **Adopt** → **the user amends the PRD** (you don't amend it yourself) → add a row to the PRD checklist → keep the implementation
   - **Reject** → cut back to the PRD spec → record the reason for the cut in the debug log (this helps the next similar judgment)

### Decision gates (any one fails → scope creep, cut directly, don't use §5.1.3)

Before entering this track, run these 6 gates. **Any one fails → §5.1.3 doesn't apply, cut back to the PRD spec**:

- [ ] Aligns with the PRD's "design principles / core philosophy" section
- [ ] Doesn't violate the PRD's "security" iron rules (especially PII isolation, permission boundaries)
- [ ] Introduces no new dependency outside the PRD's "tech stack" section
- [ ] Doesn't expand the data model (no new tables, no new fields)
- [ ] Doesn't affect other modules' API contract (path / method / return structure)
- [ ] New logic ≤ ~20 lines (over that means it's already a new feature — not a bug, not a small enhancement; stop and report it to the user as a "large enhancement to a PRD gap", await a ruling on whether to fold it into the PRD, rather than writing it on your own)

### 9 typical scenarios

| Scenario | Handling |
|---|---|
| API returns a field the PRD didn't write but obviously should (e.g. `updated_at`) | Use §5.1.3, may keep for now |
| Middleware adds a security header (e.g. `nosniff` / basic CSP defense) | Use §5.1.3, may keep for now |
| Boundary input fallback (e.g. empty string→400, avoid downstream NPE) | Use §5.1.3, may keep for now |
| Error-case log enhancement (so future debug isn't blind) | Use §5.1.3, may keep for now |
| Adding an endpoint / module the PRD didn't list | **Must cut** (this is a new feature, not an enhancement) |
| Adding a table / field | **Must cut** (data model expansion, needs a ruling) |
| Introducing a new package | **Must cut** (tech-stack expansion) |
| Changing an existing API shape | **Must cut** (breaks contract) |
| Over-abstraction (writing a strategy / factory after seeing two cases) | **Must cut** (YAGNI territory) |

### Key principle

> §5.1.3 is for small things you still feel should be added *after* restraint — not a get-out-of-jail card for "my hands itch to write more".
> 6 gates don't pass → that's not an enhancement, it's scope creep; go YAGNI and cut directly.

---

## §5.1.4 Three-track handling cheat sheet

When the PRD doesn't match your expectation, route it with this table first:

| Scenario | Which section | Stop work? | Action keywords |
|---|---|---|---|
| Vague / internally inconsistent, but **either reading lets you continue** | §5.1.1 | **Don't stop** | Decision criteria → adopt → annotate checklist |
| Logic error, self-contradictory, **no reading produces a result** | §5.1.2 | **Stop, await ruling** | log `[SKIPPED-PRD]` → skip module → wait |
| PRD didn't write it, but implementation naturally adds a **principle-aligned small enhancement** | §5.1.3 | **Don't stop, but keep and await ruling** | 6-gate check → log Gap → wait |
| PRD didn't write it, **and there's no implementation need** | YAGNI (see [§1 Core Principles](../01_foundations/01_principles.md) rule #8) | — | Don't write it |

### Recording habits common to all three tracks

Whichever section you take, three things are mandatory:

1. **Leave a trace in the development log** (PRD Issues / PRD Gaps / PRD Ambiguity, each in its own block)
2. **Mark the progress.md todo** (⚠ awaiting ruling / ※ took §X.Y reading / ⚠ awaiting enhancement ruling)
3. **After the ruling comes down**, resolve the matching entry out of pending state and sync the PRD checklist

Skip any one and at the start of the next session you'll lose track of what's decided versus still pending — more trouble than the PRD problem itself.

---

## Links to other sections

- §5.1.1 (Vague) maps to [§1 Core Principles rule #5](../01_foundations/01_principles.md)
- §5.1.2 (Bug) maps to rule #6
- §5.1.3 (Gap + implementation better) maps to rule #7 — the one most easily mis-applied with a YAGNI cut, which is why it gets a dedicated middle path
- If §5.1.3's 6-gate check fails → apply YAGNI directly (rule #8)

---

## 🔗 Related Compass sections
- [§1 Core Principles](../01_foundations/01_principles.md) — rules #5, #6, #7, #8 map respectively to this section's three tracks and the YAGNI backstop
- [§5 Conflict Handling index](./_index.md) — the entry point for the category this section lives in
- [§1 Three-Tier Discipline](../01_foundations/02_three_tiers.md) — PRD implementation tasks always run 🔴heavy; this section is a core sub-flow under that mode
- Sentinel's safety nets ("don't stack patches on errors", "re-anchor", etc.) match the spirit of §5.1.2's stop-and-await-ruling

## 📝 Status
v0.2.0 (Phase 1: ported from prior SOP, generalized and de-privatized).
