# §8.5 Minimal Discipline When There's No Formal PRD

> Part of [Compass](../../SKILL.md) §8 — Brownfield and existing projects.
> No formal PRD doesn't mean running naked: before you start, write down three lines — "goal / acceptance / out of scope" — so DoR, DoD, and compare-fix have an anchor to check against.

---

## 🎯 Reality: Most work has no PRD

A formal PRD is a luxury. Real requirements look like this:

- A one-liner on Slack: "add a CSV option to the export"
- A Jira ticket titled "fix login"
- The boss walks over: "just make it do X"
- Your own thought: "let me refactor this bit while I'm here"

Compass can't collapse just because "there's no PRD file." No contract ≠ no contract needed — it just means **the contract hasn't been written down yet**. An unwritten contract turns into he-said-she-said at acceptance time.

**Core claim**: with no formal PRD, your job isn't to skip discipline, but to **fill the gap with a three-line throwaway mini-PRD**, so the downstream gates have something to check against.

---

## 📝 Minimal Viable Spec (MVS): three lines before you start

Before writing code, put these three lines into a ticket comment, a draft commit message, or a scratch file in `.claude/`. Three lines is enough:

| Field | Question | Counter-example (fails) |
|---|---|---|
| **Goal** | After this is done, what goes from "can't" to "can"? | "Optimize export" (doesn't say what to optimize) |
| **Acceptance criteria** | How do you tell at a glance it's done? Observable, checkable | "Make it nicer" (unverifiable) |
| **Out of scope** | The scope boundary you explicitly **won't touch** this time | (left blank → scope creeps without bound) |

The third line (out of scope) is the one most often dropped, yet it's the most critical — it's the only wall stopping scope creep.

### Example: "add a CSV export" from Slack

```text
Goal: report page can export CSV (currently only JSON)
Acceptance:
  - report page shows an "Export CSV" button
  - clicking downloads a .csv, column order matches the on-screen table
  - empty data downloads a header-only file, no error
Out of scope:
  - no Excel / PDF
  - no column picker / sort settings
  - don't change existing JSON export behavior
```

These three lines are your "PRD" for this task. It's throwaway, but for as long as it lives, it **is the contract**.

---

## 🔁 How the three lines wire back into Compass gates

Once you've written the three lines, every gate that previously required a PRD can run:

| Gate | Equivalent without a PRD |
|---|---|
| **DoR** ([§2](../02_definition_of_ready/01_dor_checklist.md)) | The three lines you just wrote **are a mini DoR target** — clear goal, testable acceptance, explicit boundary; all three present before you start |
| **Compare-fix** ([§3.4](../03_implementation/04_compare_fix_loop.md)) | After each slice, go back and tick off "acceptance criteria" item by item, instead of going by gut feel and saying "close enough" |
| **DoD** ([§4](../04_quality_gates/01_dod.md)) | "Acceptance criteria" all green + lint/test/self-review before it counts as done |
| **YAGNI** ([§3.5](../03_implementation/05_yagni.md)) | "Out of scope" is your YAGNI list — before adding anything, check whether it's in "out of scope" |

In other words, **the three-line mini-PRD is the adapter that plugs a "spec-less task" back into the Compass mainline**.

---

## ⚖️ When three lines suffice, and when to insist on a real PRD

Not every task should be brushed off with three lines. Use this table to gauge the force needed:

| Signal | Three lines suffice ✅ | Insist on a formal PRD ⛔ |
|---|---|---|
| Blast radius | Single module, isolated change | Cross-module / cross-service |
| Data model | No schema change | Alter tables, columns, migrations |
| Security / permissions | Doesn't touch | Touches Auth / permissions / PII |
| People involved | You can handle it solo | Needs multi-person collaboration, has a handoff |
| Reversibility | Easy to roll back on error | Hard to roll back in prod / affects money flow |
| Ambiguity | Requirement clear, just unwritten | Requirement itself is in dispute |

### Decision procedure

```text
Does this change hit any "⛔" column?
├─ No  → write the three-line MVS, start work directly
└─ Yes → stop. Three lines aren't enough:
         1) list the ambiguous points as concrete questions (not "do it or not" but "A or B")
         2) go get a real PRD, or at least nail down and write down these points
         3) security cases mandatorily go test-first (see below)
```

**Iron rule**: when you hit the security column, three lines are no get-out-of-jail card. Auth / permissions / PII always go test-first, and the threat scenario goes into "acceptance criteria" (this is Sentinel's security-thinking floor, not a Compass option).

---

## 🕳️ The harm of zero spec (why you can't just start writing)

Skip the three lines, dive straight in, and you hit two inevitable traps:

### Trap 1: "Done" becomes undefined

With no acceptance criteria, "is it done" has no objective answer. The result:

- you think it's done, the requester thinks it isn't → back-and-forth rework
- with no "stop line," you keep adding detail until you're worn out
- the reviewer doesn't know what to verify, can only sign off on gut feel

### Trap 2: scope creeps silently

With no "out of scope," every "while I'm at it" looks reasonable:

```text
Original request: add a CSV export
  → "let's support Excel while we're at it"
    → "then let users pick columns too"
      → "if they can pick, may as well save it as a template"
        → two days later: you're writing an export-config system nobody asked for
```

Each step is "only a little more"; together they add up to a new feature no one approved. **The "out of scope" line is the lowest-cost moment to call stop — at step one.**

---

## ✅ Pre-flight self-check list

Run through this before you start; fill whatever's missing:

- [ ] Did I write down the **goal**? (one sentence: what goes from can't to can)
- [ ] Are the acceptance criteria **checkable**? (not "nicer," but yes/no items)
- [ ] Did I write down **out of scope**? (at least 2 scope boundaries)
- [ ] Does this change hit data model / security / cross-module / multi-person? → if so, escalate to demanding a real PRD
- [ ] With the three lines written, does it pass DoR's "clear goal, verifiable, explicit boundary" ([DoR](../02_definition_of_ready/01_dor_checklist.md))?
- [ ] When I want to add something from the "out of scope" list mid-way, will I go back and re-rule rather than sneak it in?

All checked → start. Any unchecked → fill the spec first, don't enter code mode.

---

## 🧭 Lifecycle of the three lines

The mini-PRD is throwaway, but don't throw it too early:

1. **Before you start**: write the three lines.
2. **During**: after each slice, compare back to "acceptance criteria" (compare-fix).
3. **When you want to expand**: check against "out of scope"; to expand, re-rule, update the three lines, don't sneak-add.
4. **On completion**: three lines all green → leave a trail alongside the commit message (`ticket: <goal> / N acceptance items all passed / scope excludes X`).
5. **After**: if this area will be touched repeatedly in future, or handed to multiple people → promote the three lines into a formal PRD section; don't let it sit in a comment forever.

---

## 🔗 Related Compass sections

- [§2.1 DoR Checklist](../02_definition_of_ready/01_dor_checklist.md) — the three-line MVS is you self-writing a mini DoR target
- [§3.4 Compare-Fix Loop](../03_implementation/04_compare_fix_loop.md) — compare back item by item against "acceptance criteria"
- [§3.5 YAGNI](../03_implementation/05_yagni.md) — "out of scope" is your YAGNI boundary
- [§8 Brownfield Overview](./01_overview.md) — shared discipline for changes to existing projects

---

## 📝 Status

v0.5.0 (Phase 2: original content)
