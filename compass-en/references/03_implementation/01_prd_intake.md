# §3.1 PRD Intake

> Part of [Compass](../../SKILL.md) §3 — Implementation.
> Before writing any code, build a complete mental model of the PRD so you don't drop items mid-implementation.

---

## Purpose

Before any implementation action, **fully absorb the PRD** — turn the spec from an "external document" into a "navigable map in your head". The PRD is a contract, but starting work without finishing the read is like signing with your eyes closed. The output of this stage isn't code — it's a **checklist + skeleton**: knowing which features need to be written, and knowing where files go.

> Core principle: **done means done, no half-finished work**; you may ship in small slices, but no half-finished phasing. Once PRD intake is done, every later slice should be independently completable, committable, and verifiable.

---

## Steps

### 1. Measure the PRD's size

First know what you're dealing with:

- **Line count**: how many lines is the whole PRD?
- **Token volume**: estimate whether it fits into context in one pass.
- **Section count**: how many top-level sections, how many sub-sections?
- **Appendices/diagrams**: any ER diagrams, API schemas, flowcharts, etc. that need extra absorption?

The measurement decides how you read next:

| Size | Approach |
|---|---|
| Small (< 300 lines) | Read in one pass, take notes |
| Medium (300–800 lines) | Read in 2–3 segments; after each, organize that segment's feature checklist |
| Large (> 800 lines) | Read in segments of ~500 lines each; after each, write a summary + that segment's feature checklist, so later segments don't push earlier ones out of context |

### 2. Read the entire PRD in segments

- Don't skim. Don't read only the sections "related to my slice" — PRD sections often have implicit dependencies (schema affects API, API affects UI, permissions affect everything).
- After each segment, **immediately output that segment's mini feature checklist and open questions**. Don't wait until you've read everything to organize — by then the details are blurry.
- While reading, mark three categories:
  - ✅ **Clear spec**: can implement directly
  - ⚠️ **Ambiguity**: needs the conflict-handling flow (see [§5 Conflict Handling](../05_conflict_handling/_index.md))
  - ‼️ **Gap**: details the PRD doesn't write but implementation will definitely hit

### 3. Build the feature checklist

Break the PRD into individual **independently-shippable** feature items, as seeds for the later checklist:

- Each item should be small enough to write in one pass, commit in one pass, verify in one pass
- Each item is tagged with its corresponding PRD section (contract mapping)
- Security-sensitive modules (authn / authz / PII / payments / key handling) are tagged **test-first**

This checklist becomes the input to the PRD checklist in [§3.2 The three tracking docs](./02_tracking_docs.md). Compass recommends a **PRD-table expansion script** (behavior varies by config) to turn the PRD's feature/field/endpoint tables into checklist entries; whatever tool you use, the checklist must map back to PRD sections in reverse.

> **🤝 Ingesting a Cartographer handoff**
> If the PRD was produced by [Cartographer](https://github.com/RayLi-Git/cartographer), its §14 handoff ships a checklist bullet list, e.g.:
> `- [ ] FR-PAY-01 create payment intent ｜P0｜AC: 200 with paymentId｜verify-by: integration test`
> Map it directly onto the columns of `templates/prd-checklist.md.template` — **don't drop columns**:
>
> | Handoff bullet field | → checklist column |
> |---|---|
> | ID + description (`FR-PAY-01 create payment intent`) | Item (smallest unit) |
> | the PRD section that ID maps to | PRD §ref |
> | `P0` | Priority |
> | `AC: …` + `verify-by: …` | AC / verify-by |
> | (backfill after implementing) | Status / verified-in-codebase? |
>
> This way Cartographer's priority / AC / verify-by are not lost at the handoff (the old four-column compass table had no such columns and dropped this data at the seam).

### 4. Build an empty skeleton from the "directory structure" section first

If the PRD defines a project directory structure or file-layout section:

- **Build the whole directory tree first** — folders + empty files (or placeholder comments)
- Don't write any logic
- The point: so every later feature slice has a clear answer to "where does this go", avoiding placing things ad hoc while writing, and drifting from the PRD while placing things ad hoc

If the PRD has no directory-structure section:
- Mark it as a ‼️ gap, draft a directory per project convention, then handle it via the "PRD gap" flow in [§5 Conflict Handling](../05_conflict_handling/_index.md)

### 5. Sequence the implementation order

After absorbing the PRD, lay out the **implementation order** — not phased half-finished work, but **which slice finishes first, which finishes later**:

- **Security-critical modules first, and mandatory test-first**
- Foundations depended on by many places (schema, shared types, config loading) first
- UI/cosmetic last

> **Example: a typical Web App stack**
> A typical order might be: schema → config/key loading → authn/authz (test-first) → core domain logic → API endpoints → UI. **This is just an example, not a mandatory list** — the actual order depends on your PRD and stack.

---

## Done criteria

Once PRD intake is done, you should be able to answer:

- [ ] How many feature items does the PRD have in total? (have a checklist)
- [ ] Which PRD section does each feature map to? (have a mapping)
- [ ] Is the project skeleton directory built? (have a file tree)
- [ ] Which are security-critical modules needing test-first? (tagged)
- [ ] What's the implementation order? (sequenced)
- [ ] Checklist of ambiguities / gaps in the PRD? (recorded, pending conflict handling)

Can't answer any one of these — go back and fill it in, don't force the next step.

---

## 🔗 Related Compass sections
- [§3.2 The three tracking docs](./02_tracking_docs.md) — the next step: turning the feature checklist into a trackable checklist
- [§3.3 Implementation order and dependencies](./03_implementation_order.md) — sequencing implementation after the skeleton is built
- [§3.4 The compare-fix loop](./04_compare_fix_loop.md) — the wrap-up loop for each implementation slice
- [§5 Conflict Handling](../05_conflict_handling/_index.md) — the flow for handling PRD ambiguity / bug / gap
- Sentinel's pre-flight protocol — the general pre-flight check protocol (a Sentinel thinking-OS concept, not a Compass section)

## 📝 Status
v0.2.0 (Phase 1: ported from prior SOP, generalized and de-privatized).
