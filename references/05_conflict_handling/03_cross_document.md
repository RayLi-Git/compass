# §5.3 Cross-Document Conflict

> Part of [Compass](../../SKILL.md) §5 — Conflict Handling.
> The PRD is rarely the only spec. ADRs, API contracts (OpenAPI), ERDs, and design mockups may all exist at once — and contradict each other, or contradict the PRD. This section gives you the "who decides what" procedure.

---

## 1. What the problem looks like

Mid-implementation, you discover you're holding more than one spec, and they don't line up:

- PRD §4 says the response carries a `risk_score` field, but the OpenAPI contract's schema doesn't list it at all.
- `ADR-007` rules "use Postgres," but PRD §3 "tech selection" says "MongoDB."
- The ERD has an `audit_log` table; the PRD never mentions it anywhere.
- The design mockup (Figma) shows an "Export CSV" button; the PRD's scope section has no such feature.

**The most dangerous reaction here is "pick whichever is convenient and go."** You write that field per the PRD, then another team that consumes your API wires up against the OpenAPI, the fields don't match, and prod blows up. You use Postgres per the ADR, but that MongoDB line in the PRD was the latest intent, changed last week — and you've done throwaway work.

The essence of a cross-document conflict: **each document is authoritative within its own domain; none unconditionally overrides another.** First ask "whose domain is this?" then ask "which is newer?"

---

## 2. Each document's domain of authority (split by domain first, then talk priority)

The first cut on a conflict isn't comparing priority — it's **splitting by domain**. Different documents decide different things:

| Document type | Domain of authority (it decides) | What it shouldn't overreach into |
|---|---|---|
| API contract (OpenAPI / Protobuf / a signed interface) | **Wire format**: field names, types, required-ness, HTTP status codes, paths | Business logic, why a field exists |
| ADR | **Architecture decisions**: selection, layering, boundaries, rationale for tradeoffs | Product behavior, UI copy, field details |
| PRD | **Behavior and scope**: what to do, what not to do, rules, boundary conditions | How to implement, which DB to use (unless it explicitly names it as a decision) |
| ERD / schema migration | **Data shape**: tables, fields, relations, indexes, constraints | External API surface, business rules |
| Design mockup (Figma etc.) | **Visual and interaction**: layout, flow, copy | Backend contracts, data models |

**Decision question #1: "Whose domain is this?"**

- Whether a response field exists → **the API contract's domain** (PRD says yes, contract doesn't list it — most likely the PRD lags or the contract missed an update, but the external promise is governed by the contract).
- Postgres or MongoDB → **the ADR's domain** (the ADR is a weighed decision; that tech-selection line in PRD §3, if it carries no rationale, is usually something the PRD author jotted down, not a contract).
- An extra `audit_log` table → **the ERD's domain**, but the PRD doesn't mention this feature → simultaneously a scope problem, see §3's "cross-domain genuine contradiction."

> Seventy percent of cross-document conflicts vanish once you split by domain — because the two documents were talking about different layers, there's no real conflict, just one of them being stale and out of sync.

---

## 3. Priority on a genuine conflict (a clash within the same domain)

When two documents **truly give contradictory answers within the same domain**, apply this default priority (**a project can override it in its own CLAUDE.md / spec master doc**):

1. **A document explicitly marked "contract" and consumed by other teams**
   A signed API contract, a schema depended on by downstream services. **Break it and you break others** — this is top priority, because the cost spills out into systems you don't control.

2. **The newest and most specific document** (recency + specificity)
   What appears later is usually a revision; one with explicit inputs/outputs / conditions / boundary values beats a vague one-liner. Having both is strongest.

3. **PRD** — when the dispute is about **behavior / scope** (what to do, what not to do).
   The PRD represents product intent; on the behavioral layer it decides.

4. **ADR** — when the dispute is about a **deliberate architecture decision**.
   An ADR is a "decision," not a "suggestion." An ADR with weighed rationale and status Accepted overrides a tech-selection line jotted into the PRD.

> Note rule #1 overrides everything: even if the PRD is the latest intent changed last week, if following it would break a contract already consumed by another team, **you cannot silently change the contract to match the PRD** — this becomes a §3.2 genuine contradiction: stop and await ruling (see §4).

### Applied examples

| Conflict | Domain | Verdict |
|---|---|---|
| PRD says response has `risk_score`, OpenAPI doesn't list it, and the API is already wired up by the frontend team | Wire format | Contract wins (already consumed). PRD wants to add the field → go through the add-field flow to change the contract, not silently return it |
| ADR-007 "use Postgres" vs PRD §3 "MongoDB", ADR carries weighed rationale and is Accepted | Architecture | ADR wins. That PRD §3 line is suspected stale → report and ask the user to sync the PRD |
| PRD changed last week "list default sort to newest-first" vs design mockup still drawing old sort | Behavior | PRD wins (newer, and sort is behavior not visual) |
| ERD has `audit_log` table, PRD never mentions this feature | Cross-domain | Genuine contradiction → §3.2 |

---

## §3.2 Cross-domain genuine contradiction: can't split by domain, or top authorities of the same domain clash

Some conflicts **don't resolve even after splitting by domain**:

- The ERD has a table / field whose corresponding feature the PRD never mentions — this is simultaneously a "data shape" and a "scope" matter; the authorities of two domains clash.
- A behavior required by the API contract (already consumed by another team) is **directly opposite** to the PRD's latest intent.
- Two documents both marked "contract" contradict each other.

These — **un-resolvable by domain attribution** — get handled as a **PRD bug** (see [§5.1.2](./01_vague_bug_gap.md)):

1. **Stop immediately.** Don't force-pick a side and keep writing on top of the contradiction.
2. **Don't change any spec document yourself** (don't touch the PRD, the contract, or the ADR) — your job is to report, not to arbitrate.
3. **Record in the development log** (tag `[SKIPPED-PRD]`):
   - Quote the **two conflicting passages verbatim + their document names and section / version**
   - The **domain-attribution analysis you already attempted**, and why it won't split (this is the most critical part — you have to convince the user this is a genuine contradiction, not you not reading carefully).
   - 2–3 suggested resolutions with their respective costs (e.g.: change the PRD? change the contract and notify downstream? drop that table?)
4. **Mark "⚠ awaiting cross-document ruling" in progress.md**, skip the affected module, continue with others that aren't affected.
5. **Only after the user rules** do you fill it back in, and the **user** changes the corresponding document — not you.

> You're the executor, not the arbiter. When you see two contracts clashing, if your first reaction is "I'll decide which one for you," that's overstepping; the correct reaction is stop, log, list the costs, await ruling.

---

## 4. Full decision flow (one decision tree)

For any cross-document mismatch, walk this order:

```
1. Confirm it's a real conflict, not one of them being stale and out of sync
   (stale → report and ask the user to sync that one, continue with the latest intent)
2. Ask "whose domain is this?" (§2 table)
   → splits by domain → that domain's authoritative document decides, keep implementing
3. Two documents clash within the same domain → apply priority (§3)
   → rule #1: would it break a contract consumed by another team? yes → §3.2 stop
   → no → newer + more specific > PRD (behavior) > ADR (architecture)
4. Can't split by domain / top authorities of same domain clash → genuine contradiction → §3.2 (handle as PRD bug: stop, log, await ruling)
```

### Minimal pre-flight checklist

Before implementing a module that touches multiple specs, run through these:

- [ ] List **all** spec documents this module touches (PRD sections, relevant ADRs, corresponding OpenAPI paths, relevant tables)
- [ ] Compare item by item: are any field names / types / behaviors / status codes mismatched
- [ ] For mismatches, first judge **whether it's stale-out-of-sync or a real conflict**
- [ ] For real conflicts, **split by domain** before talking priority
- [ ] For the un-splittable ones, **stop and log, don't arbitrate yourself**

---

## 5. Key principles

> **Split by domain first; if it won't split, stop and await ruling.** Skipping the domain split and stopping outright misjudges a pile of "actually no conflict, just one being stale" things as needing a ruling, dragging down progress; skipping the domain split and force-picking a side makes unilateral calls in someone else's domain, breaking downstream you can't see. (Note: stopping isn't always at the end — the moment you hit the "would break a contract consumed by another team" red line, stop right at the priority step, see the decision tree.)

> **"A contract consumed by others" is top priority, because its cost spills out.** You can change the code on your side, but you can't change the team wiring up to your API against the old contract.

> **You're not the arbiter.** Two contracts clash → stop, log, list the costs, await ruling; the spec's owner changes the document, not you.

---

## 🔗 Related Compass sections
- [§5.1 PRD Vague / Bug / Gap](./01_vague_bug_gap.md) — §3.2 cross-domain genuine contradiction reuses §5.1.2's "stop → log `[SKIPPED-PRD]` → await ruling" track
- [§5.2 PRD Mid-Course Change](./02_prd_change.md) — "one document is newer" often stems from a mid-course spec change, sharing this section's recency criterion
- [§5.4 Multi-PRD Dependency](./04_multi_prd.md) — another form of multiple specs coexisting: cross-PRD dependency and override
- [§3.4 Compare-Fix Loop](../03_implementation/04_compare_fix_loop.md) — when the compare step finds a cross-document mismatch, route it here
- [§3.1 PRD Intake](../03_implementation/01_prd_intake.md) — the intake stage should already inventory which ADRs / contracts / ERDs are involved; the earlier you spot a conflict, the cheaper
- Sentinel's safety nets ("don't patch on top of an error," stop and await ruling) align with the §3.2 genuine-contradiction handling spirit

## 📝 Status
v0.5.0 (Phase 2: original content).
