# §5.4 Multi-PRD Dependencies

> Part of [Compass](../../SKILL.md) §5 — Conflict Handling.
> A product often splits into multiple sub-PRDs (auth, billing, notifications…) with dependencies and shared interfaces between them; this file governs how to order them and keep them consistent.

---

## 1. Nature of the Problem

Sub-PRDs aren't parallel — they're directed.

- auth-PRD defines `token` / `user_id`; billing-PRD consumes them.
- If you do billing first, you can only **guess** auth's interface → when auth actually gets written, the interfaces don't match → billing rework.
- The guessed interface also pollutes in reverse: billing's assumptions get treated as established fact, forcing auth to bend toward an interface it never should have looked like.

> Core: **What gets depended on goes first; what depends on others goes later.** The cost of violating this isn't delay — it's rework.

---

## 2. Dependency Inventory (mandatory pre-flight)

Draw the sub-PRD dependency graph before starting; don't order by gut feel.

### 2.1 Build the Dependency Graph

For each sub-PRD, ask two questions:

1. What does it **consume** that's defined by other PRDs? (→ who it depends on)
2. What does it **define** that other PRDs use? (→ who depends on it)

Connect the answers into a directed graph (A → B means B depends on A).

### 2.2 Mark Shared Contracts

Dependencies almost always flow through "shared contracts." List each one and name its **owner PRD**:

| Contract type | Example | owner (definer) | consumer |
|---|---|---|---|
| Identity token | `access_token` structure and signature | auth-PRD | billing / notifications |
| Entity ID | `user_id` type and lifecycle | auth-PRD | almost everyone |
| Event schema | `OrderPaid` event fields | checkout-PRD | notifications-PRD |
| Shared data model | `Product` field definition | catalog-PRD | cart / checkout |

> Each shared contract **can have only one owner PRD**. Two PRDs both claiming to define the same `user` → that's a conflict, go to §5.3.

---

## 3. Ordering Rules

Ordering = topological sort over the dependency graph, structurally identical to [§3.3 Implementation Order](../03_implementation/03_implementation_order.md), just at coarser granularity — from "file/module" up to "whole PRD."

```
foundation / shared PRDs first  →  leaf / feature PRDs later
(auth, core data model)            (individual features)
```

Decision rules:

- ✅ **Most-depended-on goes first**: auth, core data model, shared event bus.
- ✅ **Leaf nodes with no outbound dependencies go last**: pure feature PRDs that consume but are not consumed.
- ✅ **Same layer (mutually independent) can run in parallel**, but still must share the same contract definition.
- ❌ A cycle appears (A depends on B and B depends on A) → stop. A cycle means contract ownership wasn't cut cleanly; split the contract first, then order — don't force it.

> Write the ordering output into progress as a cross-PRD "implementation order table."

---

## 4. Contract Discipline

Once PRD-A defines an interface that PRD-B depends on, **that interface is a contract**, not A's private implementation detail.

Changing the contract = changing an agreement, not changing code. Process:

1. Any change to a shared contract first triggers [§5.2 PRD Change Protocol](./02_prd_change.md) (impact assessment + await ruling).
2. Because the change crosses documents, also go through [§5.3 Cross-Document Conflict](./03_cross_document.md): list **all** consumer PRDs and assess the impact on each.
3. Until all consumers are synced, the contract is considered undefined; PRDs depending on it cannot declare done ([§4.1 DoD](../04_quality_gates/01_dod.md) does not pass).

Red-line checks (any one → stop):

- [ ] Changed a shared field in the owner PRD but didn't re-check the consumer list
- [ ] A consumer forked its own contract definition to "tide it over"
- [ ] The contract fudges with `any` / loose types, kicking the mismatch down the road

---

## 5. Consistency Checks

The most insidious drift across sub-PRDs isn't interfaces failing to match — it's **vocabulary quietly diverging**.

| Check | Requirement | When inconsistent |
|---|---|---|
| Same name, same meaning | auth-PRD's `user` == billing-PRD's `user` | Flag → go to §5.3 to converge |
| Same meaning, same name | One calls it `account`, another `user`, but they mean the same thing | Unify naming, leave a mapping note |
| Boundary consistency | "Deactivated user" behavior is defined consistently across PRDs | Owner PRD is authoritative |
| State machine consistency | Order status value set is the same across PRDs | A mismatch is a contract conflict |

Practical approach: maintain a cross-PRD glossary, marking each shared term with its owner and definition. When a new sub-PRD comes in (see [§3.1 PRD Intake](../03_implementation/01_prd_intake.md)), compare against the glossary first; flag divergence the moment it's hit.

> Don't "reasonably infer which one is right" on vocabulary divergence yourself. Two PRDs giving different definitions for the same concept is a conflict between PRDs → go to [§5.3 Cross-Document Conflict](./03_cross_document.md) for the user to rule on.

---

## 6. Example: E-commerce Four Sub-PRDs

Suppose the product splits into four sub-PRDs: auth / catalog / cart / checkout.

Dependencies:

```
auth ──────────────┐
                   ▼
catalog ──► cart ──► checkout
```

- **auth**: defines `user_id`, `access_token`. Depended on by everyone, no outbound dependencies.
- **catalog**: defines `Product` (id / price / stock). Depended on by cart, checkout.
- **cart**: consumes auth(`user_id`) + catalog(`Product`); defines `Cart`. Depended on by checkout.
- **checkout**: consumes all of the above; defines `OrderPaid` event. Leaf node.

Topological sort yields the implementation order:

```
1. auth      (nail down token + user_id contract first)
2. catalog   (Product contract)
3. cart      (depends on 1+2)
4. checkout  (depends on 1+2+3, emits event for a future notifications-PRD)
```

Shared contract list:

| Contract | owner | consumers |
|---|---|---|
| `user_id` / `access_token` | auth | catalog?, cart, checkout |
| `Product` | catalog | cart, checkout |
| `Cart` | cart | checkout |
| `OrderPaid` event | checkout | (future) notifications |

Decision illustration: if while building checkout you find catalog's `Product` needs an extra `tax_rate` field — that's a change to catalog's shared contract, **don't sneak it into checkout**. Go through §5.2 + §5.3: assess whether cart is affected, update catalog-PRD, await ruling, then come back.

---

## 🔗 Related Compass sections
- [§5.3 Cross-Document Conflict](./03_cross_document.md) — convergence process for shared-contract changes / vocabulary divergence, referenced back repeatedly here
- [§5.2 PRD Change Protocol](./02_prd_change.md) — the change-impact assessment triggered whenever a shared contract changes
- [§3.3 Implementation Order](../03_implementation/03_implementation_order.md) — the isomorphic source of this file's ordering rules (granularity raised from module to PRD)
- [§3.1 PRD Intake](../03_implementation/01_prd_intake.md) — when to compare against the glossary as a new sub-PRD comes in
- [§4.1 DoD](../04_quality_gates/01_dod.md) — until contracts are synced and complete, dependents cannot declare done

## 📝 Status
v0.5.0 (Phase 2: original content).
