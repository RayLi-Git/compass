# §9.3 Cross-session / cross-AI handoff

> Part of [Compass](../../SKILL.md) §9 — Collaboration.
> One PRD spans multiple Claude Code sessions / multiple agents: zero-friction handoff, the next in line doesn't re-excavate from scratch.

A long PRD won't get finished in one session. Context fills up, work spans days, agents get swapped.
Botch the handoff and the next in line spends half an hour rebuilding context — and often rebuilds it wrong, re-editing something that was already changed.
The goal of this flow: **let the incoming session know within 5 minutes "where we are, what to touch next, what not to touch" — from files, not memory.**

A handoff is not a new document. It's leaving the [§3.2 three tracking docs](../03_implementation/02_tracking_docs.md) in a "cold-readable" state, plus a git snapshot.

---

## 🧠 Core principle: handoff via files, not conversation

The incoming session has **no** memory of the previous turn's conversation. All it can see:

- What you committed to git
- What you wrote into `progress.md` / `development-log.md` / `prd-checklist.md`

→ Any decision, progress, or half-finished work that "lives only in the conversation" doesn't exist for the next in line.

This is Sentinel's re-anchor — but written as plain text, left in a file, not dropped in chat history waiting for compaction to eat it.

---

## 📤 OUTGOING: five things to leave before you exit

Before exiting, the next in line must be able to cold-start from these five alone. Miss one and the handoff has a hole.

| # | Leave what | State requirement |
|---|---|---|
| 1 | `progress.md` | "In progress" points at the current slice + **next action in one sentence** |
| 2 | `development-log.md` | Last entry says "what decision I made / where I'm stuck this stretch", with date + PRD anchor |
| 3 | `prd-checklist.md` | Touched items have correct state (⬜ / 🟡 / 🟢), no "did it but forgot to update state" |
| 4 | **"RESUME HERE" pointer** | One line at the top of `progress.md`: what the next in line's first action is, in which file |
| 5 | **Clean git** | Commit WIP too; don't leave a dirty working tree for the next in line |

### "RESUME HERE" pointer (example)

Put it at the very top of `progress.md` so the next in line sees it first:

```markdown
## ▶ RESUME HERE
- In progress: PRD §4.3 refund webhook signature verification (slice 5 / 9)
- Next action: add timestamp tolerance window (±5 min) in src/webhooks/refund.py; red test
  already written at tests/test_refund_sig.py::test_stale_timestamp_rejected (currently red)
- Don't touch: src/webhooks/charge.py is already accepted, don't casually refactor
```

> Write the pointer as an **action** ("add X / turn some test green"), not a state ("webhook half done").
> A state forces the next in line to derive the next step themselves; an action is directly executable.

### WIP commit discipline

When context is nearly full and you have to hand off mid-slice — git can't be clean. Do this:

```bash
git add -A
git commit -m "WIP [PRD §4.3] refund webhook: signature verification half-done, red test is red, see progress.md RESUME HERE"
```

- The WIP commit message must name "where it stopped, what's red", echoing the `progress.md` pointer.
- Don't use `git stash` to hand off — the next in line won't proactively see a stash, so it's effectively hidden.
- After the next in line finishes the first slice, they can choose to `git commit --amend` or squash out the WIP (see §3.2 commit discipline).

---

## 📥 INCOMING: read first, in fixed order

The incoming session's **first job is not writing code, it's cold-reading**. Follow this order, converging from "where am I" to "can I start":

| Seq | Read what | Question answered |
|---|---|---|
| 1 | `progress.md` **RESUME HERE + In progress** | Where are we? What's the next action? |
| 2 | `development-log.md` **last 3 entries** | Why did the previous turn do it this way? Any blocker / awaiting ruling? |
| 3 | `prd-checklist.md` **next ⬜/🟡 item** | What's left? What's the acceptance condition for this slice? |
| 4 | `git log --oneline -10` + `git status` | Does physical state match the docs? Any WIP / dirty tree? |
| 5 | Confirm **DoD environment runs** (lint / typecheck / test commands start up) | Can I verify "it's fixed"? |

After reading 1–4, output a **re-anchor** confirming you're aligned (plain text, for the user to review):

```text
📍Re-anchor (taking over PRD §4.3)
- Original goal: full refund webhook chain, incl. signature verification (§4, 9 slices)
- Progress: 8 slices committed, slice 5 signature verification in progress
- Todo: add timestamp tolerance window → turn test_stale_timestamp_rejected green
- Drift check: dev-log has no awaiting-ruling items; charge.py marked do-not-touch, respected
```

> Step 5 often gets skipped — then the incoming party finishes editing and discovers the tests won't even run, with no way to tell whether they broke it or it was already broken.
> **Confirm the environment is green before touching production code.** When things don't match, first check the gap between git and the docs; don't assume the docs are right.

### When docs and git don't match

If cold-read step 4 finds a contradiction (e.g. `progress.md` says a slice is done, but git has no matching commit):

| Contradiction | Handling |
|---|---|
| Doc says done, git doesn't have it | Treat **git (the physical snapshot written down) as the source of truth**; the doc may have been cut off before the commit |
| git has the commit, checklist not ticked | Tick it + fill the evidence column, don't redo that slice |
| Neither side matches, state unclear | **Stop**, re-anchor listing the gaps and ask the user; don't guess your way forward |

---

## ⏳ Proactive handoff triggers: don't wait for context to blow up

Handoffs most often break from "dragging it to the last second" — context fills until the model starts forgetting, then you scramble to leave records, so `progress.md` ends up vague.

**Proactive handoff trigger conditions (any one → enter the handoff flow immediately, don't open a new slice):**

- Context usage near the limit (it feels like you're starting to lose earlier decisions)
- A slice just committed, right as you're about to open the next one (a natural clean cut point)
- About to switch agent / hand off to another person
- The user says "stop here for now / continue next time"

> The golden cut point is **"a slice just committed, next slice not yet opened"**: git is clean, checklist state just aligned, the pointer is easy to write.
> Being forced to hand off mid-slice is the costliest case (you have to write a WIP commit + explain what's red) — hold out for a slice boundary if you can.

---

## ✅ Handoff checklist (confirm each item before exiting)

```text
OUTGOING
[ ] progress.md "In progress" points at the current slice, top has RESUME HERE (next action = executable)
[ ] development-log.md last entry clearly states "what decision / where stuck" + date + PRD anchor
[ ] prd-checklist.md touched items have correct state (⬜/🟡/🟢), none done-but-forgotten
[ ] git committed (commit WIP too, message names where it stopped / what's red), working tree clean
[ ] awaiting-ruling / blocker marked in dev-log ([SKIPPED-PRD] etc.), visible to next in line

INCOMING
[ ] Read progress RESUME HERE → dev-log last 3 entries → checklist next item → git log/status
[ ] Confirmed DoD environment runs (lint / typecheck / test start up)
[ ] Output re-anchor, confirmed alignment with the user, no unresolved doc-vs-git contradiction
[ ] Only then start touching production code
```

---

## 🔗 Related Compass sections

- [§3.2 three tracking docs](../03_implementation/02_tracking_docs.md) — the physical carrier of the handoff; here it's just kept cold-readable
- [§4.1 Definition of Done](../04_quality_gates/01_dod.md) — the DoD environment to confirm at incoming step 5
- [§9.1 Who decides](./01_who_decides.md) — responsibility ownership when an awaiting-ruling item crosses turns
- [§9 Collaboration index](./_index.md) — multi-person / multi-agent collaboration map

---

## 📝 Status

v0.8.0 (Phase 3: original content)
