# §2.1 Definition of Ready: PRD Implementability Health Check Checklist

> Part of [Compass](../../SKILL.md) §2 — Definition of Ready.
> Before writing the first line of code, health-check whether the PRD itself is "implementable" — DoR is the dual of DoD.

---

## 0. Why DoR

DoD ([§4.1](../04_quality_gates/01_dod.md)) guards "**is it done**"; DoR guards "**can this spec even be started**". They're duals: DoD at the exit, DoR at the entrance.

A vague PRD **won't proactively pop up and warn you it's vague**. It blows up when you're on your third file, trying to assemble a return format you assumed was defined long ago — by then you've made a pile of assumptions and written a pile of code coupled to them. Fixing one ambiguity at the entrance is far cheaper than fixing half an implementation chain.

> Core spirit: **a bad PRD silently poisons everything downstream**. DoR = catch it before the first line of code, not midway.

DoR's product isn't "the spec looks prettier" — it's a **list of failed items**, where each failure = a PRD gap/ambiguity, all routed through [§5 Conflict Handling](../05_conflict_handling/_index.md) before work starts, not revisited halfway through.

---

## 1. Three-tier: quick check vs full check

DoR scales with task weight (aligned with [§1.2 three-tier](../01_foundations/02_three_tiers.md)):

| Tier | Trigger | Which blocks to run |
|---|---|---|
| 🟡 quick check (medium) | add a function / one endpoint / a piece of logic | §2 endpoints, §2 auth attribution, §2 acceptance criteria (the three musts) |
| 🔴 full check (heavy) | implement a whole PRD / span multiple endpoints / touch the data model / security module | all six blocks in §2, item by item |

> 🟢 light (typo fix, style tweak) doesn't run DoR.
> Same iron rule as the three-tier system: **escalate only, never downgrade**. Looks medium but touches the data model or auth → escalate to 🔴 full check.

---

## 2. Core health check checklist

Each item asks "did the PRD **explicitly write** this", not "can I fill it in from experience". What you *can* fill from experience is exactly the most dangerous — that's you making an unauthorized decision on the user's behalf.

### 🔌 Endpoint / API implementability (per endpoint)

- [ ] **method**? (GET / POST / PUT / PATCH / DELETE spelled out)
- [ ] **path**? (including path-param naming, e.g. `/orders/{order_id}`)
- [ ] **authn / authz requirements**? (public? login required? specific role required?)
- [ ] **request schema**? (fields, types, required / optional, validation rules)
- [ ] **response schema**? (shape and fields of the success return)
- [ ] **error codes**? (400 / 401 / 403 / 404 / 409 / 422 — which maps to which situation)
- [ ] **idempotency**? (does resending the same request create a duplicate order / double-charge)

> Example (FastAPI): the PRD only says "create-order API" but doesn't say "resending with the same idempotency key returns the existing order" — that's not a detail, it's a hole that becomes a double-charge in production. Not written → flag as a gap.

### 🗄️ Data model implementability (per table / per entity)

- [ ] **primary key (PK)**? (what serves as PK — UUID / auto-increment / composite)
- [ ] **foreign key (FK)**? (points to whom, delete behavior cascade / restrict / set null)
- [ ] **unique / check constraints**? (which field combos can't repeat, value-range limits)
- [ ] **nullable**? (can each field be null — spell it out, don't guess)
- [ ] **default**? (what to fill when no value is given on create)
- [ ] **indexes**? (does any hot query path mention building an index)

> "nullable not written" is the most common silent poison: you guess `nullable=True`, half a year later someone builds required-field logic on it, and the data is already dirty.

### 🔐 Authn/authz attribution

- [ ] **who can call what**? (caller identity requirement for each protected endpoint)
- [ ] **is "logged in" enough, or must you verify "is it really them"**? (IDOR: `GET /orders/{id}` checking only login lets A see B's order)
- [ ] **roles clearly defined**? (what admin / user / guest can each do, where the boundaries are)

> This block also runs in 🟡 quick check. Authz attribution is the easiest hole to skip with "just make it work" and the most expensive.
> For security modules (Auth / permissions / PII), if the PRD has no explicit authz rules → treat directly as a gap, **do not fill in rules from intuition**.

### 📐 Non-functional requirements mentioned? (links §6 NFR)

- [ ] **performance targets**? (latency / throughput / data scale — are numbers given)
- [ ] **observability**? (need log / metric / trace, recording what)
- [ ] **security baseline**? (transport encryption, input validation, sensitive-data handling — any requirement)

> Rule: **if an NFR is absent, flag it — don't silently assume**. PRD not writing a performance target ≠ there's no performance target — it may be an omission. Treat "not mentioned" as an item to await ruling and throw it back to §5; don't slip in an SLA yourself, and don't assume "doesn't matter". NFR details in [§6 Non-Functional](../06_non_functional/_index.md).

### 🧨 Boundary and error behavior

- [ ] **bad input**? (what to return on wrong type, wrong format, out of value range)
- [ ] **empty values**? (behavior for empty string / empty array / missing field)
- [ ] **oversized input**? (pagination cap, file size, string length)
- [ ] **concurrency**? (two requests modifying the same record — who wins / lock / optimistic concurrency)

> A PRD usually writes only the happy path. Boundary behavior being "not written" is nearly the norm — so this block's product is often a string of §5 await-ruling items, and that's normal.

### ✅ Acceptance criteria

- [ ] **does every feature have one testable acceptance criterion**?

This is the most direct expression of the DoR/DoD duality: **with no testable acceptance criterion, you can't DoD it**. If a feature's "done" can't be written as a pass/fail assertion, it simply isn't ready.

> Example: PRD says "search must be fast" → not testable. Demand a rewrite to "p95 < 200ms / 10k rows" → testable, can DoD. The former is a gap, route to §5.

---

## 3. One failed item = one conflict, handle before work starts

DoR isn't a "fill it in and you're fine" formality. Every unchecked box maps to a class of static conflict in [§5 Conflict Handling](../05_conflict_handling/_index.md):

| DoR failure shape | Class | Where to go |
|---|---|---|
| PRD wrote it but there are two readings | vague | [§5.1 vague](../05_conflict_handling/01_vague_bug_gap.md) vague flow |
| What the PRD wrote is logically impossible / self-contradictory | PRD bug | [§5.1](../05_conflict_handling/01_vague_bug_gap.md) bug flow, await ruling |
| PRD never mentions it, but implementation must have it | gap | [§5.1](../05_conflict_handling/01_vague_bug_gap.md) gap flow; **don't just cut it with YAGNI** (see [§3.5](../03_implementation/05_yagni.md)) |

**Iron rule: handle before coding, not during coding.**

DoR sits at the entrance precisely because the "discover mid-write that the PRD is vague" cost from [§3.4 compare-fix loop](../03_implementation/04_compare_fix_loop.md) is exactly what DoR is meant to eliminate. The compare-fix loop is the safety net for re-comparing **while doing**; DoR is the gate that stops the spec itself **before doing**. With both passed, deviation has nowhere left to hide.

> Exception (gaps aren't always fully blocked): if it's a pure gap that's "not in the PRD but clearly doesn't affect this block", you may record it and push on later. But the moment a gap would change the schema / authz / return shape of **this current block**, you must get a ruling first — otherwise you're stacking code on a known ambiguity, the classic Sentinel "patching on top of an error" anti-pattern.

---

## 4. Minimize the ceremony

DoR shouldn't become an obstacle. Practical rhythm:

1. Before work, run the matching blocks against the endpoints / tables this block touches (🟡 the three musts / 🔴 all six).
2. List failed items as a list at once and **throw them back to the user for ruling at once** (don't ask one by one, don't ask while writing).
3. Write the returned decisions into the tracking docs (see [§3.2 tracking docs](../03_implementation/02_tracking_docs.md)), not relying on conversation memory.
4. All ready → only then enter [§3.3 implementation order](../03_implementation/03_implementation_order.md) and start sequencing the work.

> One-line closer: **if DoR doesn't pass, don't start**. Implementing a vague PRD as-is means smuggling the user's decision rights into your guesses — and the bill comes due in production.

---

## 🔗 Related Compass sections
- [§4.1 DoD](../04_quality_gates/01_dod.md) — DoR's dual; the exit Gate, DoR is the entrance Gate
- [§5.1 vague / bug / gap](../05_conflict_handling/01_vague_bug_gap.md) — where any failed DoR item gets ruled
- [§3.4 compare-fix loop](../03_implementation/04_compare_fix_loop.md) — the compare safety net while doing, complements DoR
- [§3.5 YAGNI](../03_implementation/05_yagni.md) — a "gap" flagged by DoR can't be cut directly with YAGNI
- [§3.1 PRD intake](../03_implementation/01_prd_intake.md) — absorb the matching PRD section before the DoR health check
- [§6 Non-Functional](../06_non_functional/_index.md) — extension for not-mentioned items in the NFR block
- [§1.2 three-tier](../01_foundations/02_three_tiers.md) — the scaling basis for quick check / full check

## 📝 Status
v0.5.0 (Phase 2: original content).
