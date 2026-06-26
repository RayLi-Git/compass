# §4.2 Code Review: self / peer / AI

> Part of [Compass](../../SKILL.md) §4 — Quality Gates.
> What each of the three review modes covers, who reviews what, what a good review looks for, and the trust boundary on AI review.

Code review isn't one gate, it's three gates of **different nature**. Conflating them — assuming peer review is unnecessary once AI has run, assuming self-review is just "another glance" — is a common shortcut. This doc splits the three roles apart and gives executable checklists plus trust-calibration rules.

---

## 🧭 The three modes at a glance

| Mode | Who does it | When | Strength | Weakness |
|---|---|---|---|---|
| **SELF** | The author | Before every commit (DoD §4.1, mandatory) | Knows the change's intent best, catches debug residue | Too close to it, blind to own blind spots |
| **PEER** | Another person | High-risk / design decisions / knowledge sharing | Catches "intent, context, should-this-even-be-done" | Slow, costs people, not for every small diff |
| **AI** | A model | When you want a fast broad sweep | Fast, broad coverage, catches common bugs/traps | Low trust on intent and domain correctness, hallucinates problems |

**Core idea**: the three aren't substitutes, they're **complementary**. AI running doesn't mean you skip peer; peer reviewing doesn't mean self can be skipped.

---

## 1️⃣ SELF-review (every time, part of DoD)

The cheapest and most-often-skipped gate. One rule only: **read your own diff as if a stranger wrote it**.

Go line by line through `git diff` and ask yourself:

- [ ] If someone else wrote this line, would I understand why?
- [ ] Any debug residue? (`console.log` / `print` / commented-out old code / `TODO` / hardcoded test values)
- [ ] Do the names match what they do? (`data`, `tmp`, `handleStuff` need renaming)
- [ ] Any **scope creep**? Does this diff smuggle in "while I'm here" changes the PRD never asked for? (→ §3.5 YAGNI)
- [ ] Does the change scope match the commit message?
- [ ] Did anything that shouldn't be in git get pulled in? (keys, `.env`, local paths, large files)

> **Example**: you fix a null check, but the diff also has three lines turning some function `async`. Stop — that's not this commit's business. Either split it out or delete it. Self-review is the last gate that catches this kind of "slip of the hand".

SELF-review isn't about "does it run" (that's testing's job), it's about "**is this change clean and honest**".

---

## 2️⃣ PEER review (human, for risk / knowledge / design)

PEER review is expensive, so **not every diff needs it**. Its value is catching **what tools can't**:

| Tools catch | Only humans catch |
|---|---|
| Syntax errors, type errors | **Intent**: is the problem this code solves a real problem? |
| Style inconsistency | **Context**: this conflicts with that decision three months ago |
| Common bug patterns | **"Should this be done"**: does the PRD actually want this feature, or is it over-engineering? |
| Obvious security anti-patterns | **Domain correctness**: the discount algorithm is wrong in the refund case |

**When PEER review is mandatory:**

- 🔴 Security / auth / permissions / PII related (→ §6.4)
- 🔴 Architecture decisions, cross-module changes, hard-to-roll-back changes
- 🔴 Anywhere you're unsure, or got stuck more than once
- 🟡 A newcomer's code (knowledge transfer), or a module only you understand (eliminate bus factor)

**Good PEER review behavior:**

- Ask "why did you do it this way" rather than "change it to my way" — review intent, don't impose style
- **Clearly label** blocking (must change) vs nit (suggestion), don't make the author guess
- When unsure, ask; don't assume the author is dumb — most "obvious mistakes" have context you don't know

---

## 3️⃣ AI review (fast, broad, but discount the trust)

AI review works well as the **first broad sweep**: after self, before peer, quickly scoop up common issues and save the peer's eyeballs.

**AI is good at:**

- Finding off-by-one, null/undefined, unhandled error paths
- Pointing out uncovered edge cases, missing tests
- Catching common security traps (injection, unvalidated input) and style inconsistency
- Quickly locating "worth a human glance" blocks in a large diff

**AI is bad at (discount the trust):**

- ⚠️ **Intent**: it doesn't know what the PRD wants, can't judge "should this be done"
- ⚠️ **Domain correctness**: for finance, billing, permissions, its "looks right" can't be trusted
- ⚠️ **Hallucination**: it will confidently report problems that **don't exist at all**, or cite nonexistent APIs

> **Example**: AI reporting "there's a race condition here" sounds scary. Until you can **concretely point to the two interleaving paths**, treat it as "to investigate", not "confirmed". Every non-mechanical AI-review finding needs a human to verify — this is exactly Sentinel's evidence-grading principle: anything unverified gets marked ⚠️speculation.

---

## 🧮 Who reviews what: the division-of-labor matrix

| Review item | SELF | AI | PEER |
|---|:---:|:---:|:---:|
| debug residue / naming / scope creep | ✅ primary | ✅ | — |
| syntax / type / lint | linter primary | ✅ | ❌ humans shouldn't |
| common bug patterns (null, edges) | ✅ | ✅ primary | ✅ |
| test sufficiency | ✅ | ✅ | ✅ |
| **security correctness** (→ §6.4) | ✅ | broad sweep | ✅ **primary** |
| **PRD alignment** (→ §3.4) | ✅ | ❌ untrustworthy | ✅ **primary** |
| **simplicity / YAGNI** (→ §3.5) | ✅ | suggests | ✅ **primary** |
| **domain / business correctness** | ✅ | ❌ untrustworthy | ✅ **primary** |
| **architecture / should-this-be-done** | — | ❌ | ✅ **primary** |

How to read: a ❌ cell means "this mode can't be trusted on this item, don't rely on it".

---

## 🔍 What a good review looks for (applies to all modes)

In priority order, **from high to low**, don't spend time on low-level nits:

1. **Correctness** — does it actually do the right thing? edges, error paths, concurrency, data consistency
2. **Security** — distrust input, authn/authz, least privilege, sensitive data (→ §6.4)
3. **PRD alignment** — does what it does match what the contract wants? under-doing? over-doing? (→ §3.4)
4. **Simplicity / YAGNI** — any over-engineering, flexibility nobody asked for, speculative abstraction? (→ §3.5)
5. **Tests** — does the change have matching tests? do they test behavior or implementation detail?

```text
Review-order mindset:
  First ask "is this correct, secure, what the PRD wants"
  Then ask "could it be simpler"
  Only last touch "naming/formatting" — and formatting belongs to the linter, shouldn't occupy human brains
```

---

## 🚫 What review should NOT do

- ❌ **Nitpick formatting the linter should catch**: indentation, semicolons, quotes, import ordering — automate these with proper tooling, humans shouldn't argue them in review
- ❌ **Treat style preference as blocking**: "I'd write it this way" isn't "you wrote it wrong"
- ❌ **Praise/trash the whole code with no direction**: review must land on specific lines, specific reasons
- ❌ **Change whatever the AI reports**: see trust calibration below

> If half your PEER review comments are formatting nits, the problem isn't the author, it's your lint/format setup not being wired up. Fix the tooling first.

---

## ⚖️ Trust calibration: how to handle AI findings

AI-review findings **split into mechanical and non-mechanical**, with different trust levels:

| Finding type | Example | Handling |
|---|---|---|
| **Mechanical** | missing null check, un-awaited, obvious typo | 🟡 can trust faster, but still glance yourself |
| **Non-mechanical** | "there's a race condition", "logic error", "insecure" | 🔴 must be human-verified, only counts if reproducible / a concrete path can be pointed to |
| **Domain / business** | "this discount algorithm is wrong" | 🔴 AI untrustworthy, go back to PRD / find someone who knows the business |

Iron rule:

- **AI saying "no problem" doesn't mean no problem** — what it didn't see doesn't mean it doesn't exist; security/domain items still need a human or tests as gatekeeper
- **AI saying "there's a problem" doesn't mean there's a problem** — it may be hallucination; mark ⚠️speculation before verifying, don't rush to change code to appease a nonexistent bug
- Any AI finding that touches security / auth / billing / permissions code escalates to PEER, no exceptions (→ §6.4)

---

## ✅ Minimum pre-commit check (continues from DoD §4.1)

- [ ] SELF-review: diff read line by line, no debug residue / no scope creep
- [ ] linter / typecheck green (formatting issues handed to tooling, not left for humans)
- [ ] AI broad sweep run, non-mechanical findings human-classified (trusted / to-investigate / hallucination)
- [ ] Touches security / architecture / cross-module → PEER review arranged
- [ ] Review comments responded to, all blocking handled, nits decided in or out

---

## 🔗 Related Compass sections

- [§4.1 Definition of Done](./01_dod.md) — self-review is one of the eight DoD items
- [§3.4 Compare-Fix Loop](../03_implementation/04_compare_fix_loop.md) — how to check PRD alignment
- [§3.5 YAGNI](../03_implementation/05_yagni.md) — the simplicity criterion in review
- [§6.4 Security](../06_non_functional/04_security.md) — security review is peer's primary responsibility
- [§9 Collaboration](../09_collaboration/_index.md) — peer review belongs to the collaboration side

## 📝 Status

v0.8.0 (Phase 3: original content)
