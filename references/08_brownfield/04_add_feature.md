# §8.4 Adding a Feature to an Existing Codebase
> Part of [Compass](../../SKILL.md) §8 — Brownfield (existing projects).
> Adding a room to a house someone else built: read the load-bearing walls first, then decide where the door goes.

Adding a feature isn't as clean as writing a new module — you're splicing something new into a system that's **already running, already has users, already has established conventions**. The worst failure isn't that the new feature doesn't work; it's that the new feature works, but **breaks three existing behaviors next to it**. This page specifies: reverse-understand the area before you touch it, a DoR add-on check for conflicts, blast-radius analysis, integration points and backward compat, and the double acceptance of "test the new feature + test you didn't break the neighbors."

---

## 🧭 Step one: reverse-understand the area you're about to touch (reverse-understand)

Before writing the new feature, spend time reverse-understanding **the patch you're about to touch**. The goal isn't to read the whole codebase — it's to read what's **inside the blast radius**. This maps to Sentinel's pre-flight protocol "ask inward."

| What to reverse-understand | How to look | Why |
|---|---|---|
| Existing patterns / conventions | How 3-5 neighbor files in the same directory are written | Your new code should look like the neighbors, not like you |
| Data flow | From request in to DB / response out | Know which layer the new feature plugs into |
| Naming / layering conventions | How service / repo / handler are split | Don't invent your own new layering |
| Existing error-handling style | Throw exceptions? Return Result? Return error codes? | New code follows the same scheme |
| Existing test style | How fixtures / mocks / factories are used | Your tests must run alongside theirs |

> **Iron rule: match surrounding code, don't impose a new style.**
> If you think the existing style is ugly, now is not the time to rewrite it → that's refactoring (see [§8.3](./03_refactor.md)), done **separately, committed separately** from adding the feature. Slipping a style change into a feature PR = blowing up the blast radius without limit.

**Reverse-understand checklist:**

- [ ] Found at least 1 existing feature that's "most like what I'm about to do" and read it end to end
- [ ] Drew (even just in your head) the data flow for this patch: who calls the thing I'm changing, what the thing I'm changing calls
- [ ] Confirmed existing naming / layering / error-handling / test conventions and noted them down to copy
- [ ] Found the **seam** where the new feature should plug in — an existing extension point, not a hard cut

---

## 📋 Run DoR as usual, but add one item: new feature vs existing behavior conflict

Run all of [§2 DoR](../02_definition_of_ready/01_dor_checklist.md) as usual. But brownfield feature-adding gets one more **fatal check**:

> **Does the new feature the PRD describes conflict with already-implemented existing behavior?**

PRDs are usually written "standing in an ideal new world"; the author **may not know how the existing code actually runs today**. Common conflicts:

- PRD says "clicking this button exports CSV," but the existing same button currently exports Excel → changing it hits current users
- PRD says "user default role is viewer," but an existing migration defaults to editor → two facts clash
- PRD says "new field X is required," but the existing table already has a million rows where X is null → adding NOT NULL directly blows up

**The existing code is itself a "document."** When the PRD conflicts with existing code, this is a **cross-document conflict** — handle it per [§5.3 Cross-document conflict](../05_conflict_handling/03_cross_document.md). Don't guess which one is right.

```text
Detection flow:
  Read this requirement in the PRD
    → How does the existing code run this patch today? (the fruit of reverse-understanding)
      → Consistent? → keep going
      → Conflict? → this is a §5.3 cross-document conflict
                  The PRD is one document, the existing behavior is another
                  → stop, record both sides' facts, await ruling (change the PRD? or is the new feature overwriting old behavior intentional?)
```

> ⚠️ "New feature overwrites old behavior" may be **intentional** (the PRD wants to change it), or the PRD author **didn't notice the old behavior exists**. The handling for these two is worlds apart, so you can't decide yourself — throw it back for a ruling.

---

## 💥 Blast-radius analysis (blast-radius)

This maps to Sentinel's pre-flight protocol "project the blast radius outward." When adding a feature requires changing existing code, first ask: **who gets hit by my change?**

### Three rings of blast radius

| Ring | Scope | What to do |
|---|---|---|
| 🎯 Direct ring | The function / file I directly change | Change it itself + its unit tests |
| 🔗 Caller ring | Everywhere that calls what I change | Find them all, confirm one by one that my signature / behavior change didn't break them |
| 🌊 Ripple ring | Consumers of shared DB schema / global state / events / cache | Confirm the data shape / event contract didn't change, or if it did, there's compat handling |

**How to find the caller ring (concrete actions, not from memory):**

- [ ] Full-text search the **function / method / endpoint** you're changing (find all callers)
- [ ] Full-text search the **table / column** you're changing (find everywhere that reads or writes it)
- [ ] Full-text search the **shared type / interface / DTO** you're changing (find everything that depends on it)
- [ ] List them out. **List not finished = blast radius not computed = not allowed to start**

> 🚩 **Red flag**: you're about to change a function called from 20 places but just figure "it's probably fine" and start → stop. This triggers Sentinel heavy tier. Either change all callers, or add a coexisting new function (see backward compat below).

---

## 🔌 Integration points and backward compat (integration & backward compat)

The safest posture for adding a feature: **add, don't change**. Where you can "add a coexisting one," don't "modify in place."

### Compat strategies when changing an existing contract

| What you want to do | Risk to existing consumers | Safe approach |
|---|---|---|
| Change function signature (add a param) | All callers fail to compile/call | Give the new param a **default value**, old callers don't change |
| Change API response shape | Existing frontend / third parties fail to parse | **Add fields only, never remove**; to remove, go versioned |
| Change API behavior | Existing clients' assumptions broken | New behavior goes through a new endpoint / feature flag |
| Change DB column semantics | Existing data + existing queries all wrong | Add a new column, dual-write transition, see [§7.1 Migration](../07_operations/01_migration.md) |
| Change enum / state machine | Existing data lands in an unknown state | Add states only, never remove; before removing, confirm no data references it |

> **Example (extending backward-compatibly, not a mandated approach)**
> ```python
> # Existing: def create_order(items): ...  —— called from 12 places
> # Adding: support discount codes. Don't change it to def create_order(items, coupon)
> #         that would hit all 12 callers. Give a default value:
> def create_order(items, coupon: str | None = None):
>     ...  # when coupon=None behavior is identical to before → 12 old callers untouched
> ```

**Integration-point checklist:**

- [ ] At **the point** where the new feature plugs into the existing flow, did I reuse the existing extension mechanism (hook / event / middleware / DI)?
- [ ] The outward contract I changed (function signature / API / event / DB) — will existing consumers **break silently**?
- [ ] When breaking compat is unavoidable, did I go through versioning / feature flag / a transition period, instead of a hard cut?
- [ ] Does the feature flag or toggle default to the **safe old behavior** (secure by default, maps to Sentinel security thinking)?

---

## ✅ Double acceptance: test the new feature + test you didn't break the neighbors

Run the full [§4 DoD](../04_quality_gates/01_dod.md). Brownfield feature-adding tests are **always two sets**; missing either means not done:

### A. The new feature itself works

- [ ] The new feature's happy path has tests and they pass
- [ ] The new feature's boundary / error paths have tests
- [ ] The new feature matches the PRD description ([§3.4 Compare-fix loop](../03_implementation/04_compare_fix_loop.md))

### B. You didn't break the neighbors (regression)

- [ ] **The existing tests inside the blast-radius caller ring all re-run and pass** (not just the ones you newly wrote)
- [ ] For every signature / contract you changed, verified each caller's behavior is unchanged
- [ ] For existing consumers of shared DB / state / event, behavior is unchanged
- [ ] If existing test coverage is insufficient and happens not to guard the patch you touched → **add a characterization test** to pin down the old behavior, then start

> 🔬 **Evidence grading (maps to Sentinel)**: before claiming "didn't break existing features," you must **actually run the relevant existing tests**. If you haven't run them, you can only say "🟡 reviewed the logic, suggest you run the full suite," never "🟢 no impact." The most common brownfield wreck is this sentence going uncashed.

### Definition of done for feature-adding (on top of §4 DoD)

```text
☐ Reverse-understood the area, new code style matches the neighbors
☐ DoR + "new feature vs existing behavior conflict" check passes (conflicts go §5.3)
☐ All three rings of blast radius listed, caller ring handled one by one
☐ Outward contract changes have a backward-compat strategy (or already went versioned/flag)
☐ Set A tests (new feature) pass
☐ Set B tests (existing regression) pass — actually run, with evidence
☐ Feature-add and refactor/style-tweak committed separately (YAGNI, see §3.5)
```

---

## 🚩 Red flags when adding a feature (any one lit → Sentinel heavy tier)

- "While I'm at it, let me also tidy up this patch's style" → blast radius out of control, split it out
- Changing a multi-caller function without listing the callers → blast radius not computed
- PRD clashes with existing behavior and you picked a side and kept going → should go [§5.3](../05_conflict_handling/03_cross_document.md)
- Ran only the new tests, not the existing ones, and said "done" → Set B acceptance not done
- To cram the new feature in, changed an existing shared type to `any` / loosened the contract to make it pass → silencing the alarm, not putting out the fire

---

## 🔗 Related Compass sections
- [§8 Brownfield overview](./01_overview.md) — the shared mindset for working in existing projects
- [§8.3 Refactor](./03_refactor.md) — style tweaks / structural changes belong here, don't mix them into feature-adding
- [§5.3 Cross-document conflict](../05_conflict_handling/03_cross_document.md) — the ruling process when PRD vs existing behavior clash
- [§4 DoD](../04_quality_gates/01_dod.md) — double acceptance hangs on top of DoD

## 📝 Status
v0.5.0 (Phase 2: original content).
