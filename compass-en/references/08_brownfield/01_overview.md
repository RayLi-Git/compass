# §8.1 Brownfield Overview: Discipline for Existing Codebases

> Part of [Compass](../../SKILL.md) §8 — Brownfield.
> Understand it before you touch it: existing code stands alongside the PRD as a second source of truth.

---

## 🧭 Why §8 Exists

SOP §9 explicitly puts brownfield / bugfix OUT of scope.
But the reality is: **the vast majority of work is brownfield**—you're not starting a fresh project on a blank page, you're cutting into a pile of code already running in prod. The SOP gap lands exactly on 90% of your time.

Compass §8 fills that gap. It's not "a discount version of the greenfield flow," it's a **different discipline**: the greenfield risk is "not writing it," the brownfield risk is "breaking something that already works."

---

## 🎯 Core Mindset: Existing Code Is a Second Truth

A greenfield project has one contract—the PRD. Brownfield has two:

| Source of truth | What it is | Can you change it |
|---|---|---|
| **PRD / spec** | What you "should" do | No, the PRD is a contract (see §3) |
| **Existing code's current behavior** | What the system "actually does right now" | Yes, but you must understand why first |

When the two conflict, the PRD does NOT automatically win—the existing behavior may be an implicit requirement never written into the PRD, an edge-case patch, or a downstream dependency. Since existing code is the "second source of truth," a PRD fighting with it is a **cross-document conflict**—handle it per [§5.3 Cross-Document Conflict](../05_conflict_handling/03_cross_document.md) (split by domain first; if you can't, stop and await ruling)—do not just overwrite.

> **Reverse-understand before you modify**—this is exactly Sentinel's pre-flight protocol: before touching existing code, ask inward (why is this written this way) + push outward on the blast radius (who depends on it). Brownfield upgrades this from "advice" to "iron rule."

### Pre-flight Protocol (brownfield edition)

Every time you're about to change a piece of existing code, first answer:

- [ ] **What does this do right now?** Restate its actual behavior in one sentence (not what it "should" do)
- [ ] **Why is it written this way?** Find the commit / PR / issue; if you can't see the history, mark ⚠️speculation
- [ ] **Who depends on it?** Upstream callers, downstream consumers, tests, external API contracts
- [ ] **Who gets hit if you change it?** List the blast radius
- [ ] **Do existing tests cover it?** If not, add a test that "locks in current behavior" before you touch anything

If you can't answer any one of these → you're not ready to change it, keep reverse-understanding.

---

## ⚖️ Asymmetric Risk: Breaking > Omitting

This is the most critical difference in value ordering between brownfield and greenfield:

```
Greenfield: omitting a feature   ≈  breaking a (not-yet-existing) feature   → symmetric
Brownfield: breaking existing behavior  >>  omitting a new feature          → severely asymmetric
```

**Why asymmetric**: omit a new feature and the user at worst "didn't get the new thing"; break existing behavior and "something that used to work now blows up"—the latter is a regression, hits people actively using it, and often explodes in the corner you least expected.

Practical implications:

- **Default conservative**: if you're unsure whether a piece of code can be deleted / changed, default to "leave it," flag it, and ask.
- **YAGNI still holds but tread carefully**: don't add what the PRD doesn't specify ([§3.5 YAGNI](../03_implementation/05_yagni.md)); but "existing code that looks unused" **does not equal** "safe to delete"—it may be a dependency you haven't understood yet. Deletion is a kind of modification, so it runs the pre-flight protocol too.
- **Changes must be reversible**: ensure git is clean before you start; small commit per slice ([§3.2 Tracking Docs](../03_implementation/02_tracking_docs.md)). This is Sentinel's "retreat route" safety net.
- **Regression tests are part of DoD**: before claiming done, all existing tests green + the "lock-in-behavior" tests you added are also green ([§4.1 DoD](../04_quality_gates/01_dod.md)).

---

## 🗺️ §8 Sub-file Map: Pick the Right Flow

Brownfield isn't a single flow. First decide which kind of task you have, then go to the matching sub-file:

| Sub-file | Task type | When to use |
|---|---|---|
| [§8.2 Bug fix](./02_bug_fix.md) | Fix a broken existing behavior | Someone reports "it used to do X, now it does Y"; behavior deviates from expectation |
| [§8.3 Refactor](./03_refactor.md) | Change structure, **not external behavior** | Want to clean up, rename, extract functions, split modules; behavior must be identical before and after |
| [§8.4 Add feature](./04_add_feature.md) | **Add new behavior** to an existing system | You have a PRD, but it must grow on existing code, not a blank page |
| [§8.5 No PRD](./05_no_prd.md) | Existing-code work with no PRD | Only a verbal request / a screenshot / a "just add a button for me" |

### Quick Decision

```
Do you need to change "externally observable behavior"?
├─ No behavior change, structure only ......... §8.3 Refactor
└─ Change / add behavior
    ├─ "Fixing" an existing deviation ......... §8.2 Bug fix
    ├─ "Adding" a capability
    │   ├─ Have a PRD ....................... §8.4 Add feature
    │   └─ No PRD ........................... §8.5 No PRD (first pin the requirement into something acceptance-testable)
```

> **Example**: user says "the checkout page is too slow, and while you're at it rewrite that discount calc"—that's actually **two things**: performance is a bug fix (§8.2) + the rewrite is a refactor (§8.3). Don't mix them in one commit. Decompose mixed tasks first, run each through its own flow, commit separately, accept separately.

---

## 🚩 Brownfield-Specific Red Flags

Any one of these → stop, fall back to reverse-understanding:

- "This code looks unused, I'll just delete it"—are you sure you understand it? Deletion runs the pre-flight protocol too.
- "The existing test is in my way, I'll comment it out"—the test is protecting a contract you haven't understood yet. **Never turn off a test just to make code pass.**
- "I'll change this type to any / slap a `// @ts-ignore` to get past it"—that's a Sentinel red flag, silencing the alarm isn't putting out the fire.
- "Existing behavior differs from the PRD, I'll just change it to match the PRD"—you may be stepping on an implicit requirement, run the cross-document conflict ruling first ([§5.3](../05_conflict_handling/03_cross_document.md)).
- "Copy a similar existing function and tweak it"—copying is debt; first ask whether you can extract a shared piece.
- Changing the same piece a 3rd time and still not right → escalate to 🔴, enter Sentinel's diagnosis mode, chase the root cause upstream.

---

## 🔗 Related Compass sections

- [§3.5 YAGNI](../03_implementation/05_yagni.md) — existing code that "looks unused" ≠ "safe to delete"
- [§4.1 Definition of Done](../04_quality_gates/01_dod.md) — done only when regression tests are all green
- [§5.3 Cross-Document Conflict](../05_conflict_handling/03_cross_document.md) — ruling when existing code (the second document) conflicts with the PRD
- [§5.1 Vague / bug / gap handling](../05_conflict_handling/01_vague_bug_gap.md) — vagueness/bug/gap in the spec itself
- [§8 Brownfield module overview](./_index.md) — all sub-files in this chapter

---

## 📝 Status

v0.5.0 (Phase 2: original content)
