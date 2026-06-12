# §3.4 Compare-Fix Loop

> Part of [Compass](../../SKILL.md) §3 — Implementation.
> After completing each file/feature block, immediately run the "complete → compare against PRD → fix → accept" loop to prevent drift from accumulating.

---

## 1. The 12-Step Loop

After completing each file / feature block:

```
1. Finish implementation
2. Pass DoD (see §4.1)
3. Re-read the corresponding PRD section
4. Compare item by item: naming / behavior / boundary conditions / return values and error codes
5. Drift found → fix, PRD wins
   Exception: implementation beats PRD and meets the "implementation beats PRD" threshold →
              go to the corresponding flow in §5 Conflict Handling
6. Self-review
7. Check off or mark 🟡 in the PRD checklist
8. Record in the development log
9. Update the progress record
10. git commit
11. List test steps, ask the user to accept (see §3 User Acceptance Gate below)
12. Pass → next block; fail → fix and retest
```

> **DoD details are not repeated here**: for the eight hard gates and tooling-based verification, see [§4.1 DoD](../04_quality_gates/01_dod.md).

---

## 2. Forbidden Actions

If any of the following occurs, it counts as violating the compare-fix loop and you must stop immediately:

- ❌ Skipping the comparison and moving ahead
- ❌ Skipping any DoD item
- ❌ Accumulating tech debt via "I'll check back later"
- ❌ Implementing from memory without reading the PRD
- ❌ Multiple modules left uncommitted, piling up in the working tree
- ❌ Moving to the next stage without user test acceptance

> Core spirit: **done means done, no half-finished work; ship in small slices, but no half-finished staging**.

---

## 3. Stage Acceptance: User Test Gate (User Acceptance Gate)

> 📌 Terminology: "stage" here = one independently-acceptable "block / unit". Ship in small slices (encouraged),
> but every block passes full acceptance with no half-finished work (echoing "done means done"). Smaller block, lighter test guide.

After completing each stage (= one item in the "implementation order table") and passing DoD:

1. **Stop**, do not proactively move to the next stage
2. List a "## Stage N Test Guide" (covering: test preconditions, test steps, expected results, boundary and exception cases)
3. **Run it yourself first** (automated self-check loop, max 3 rounds — see §3.1 below)
4. All green within 3 rounds → ask the user to accept
5. Still failing after 3 rounds → stop and notify the user to rule
6. User passes → mark ✅ in the progress record + commit + move to next stage
7. User fails → enter the fix loop

### 3.1 Automated Self-Check Loop Rules

- "All Tests" means **all** Tests listed in this stage's test guide (including boundary / exception)
- After a fix you must rerun **all** Tests (to prevent fixing one and breaking two)
- Leave a record in the development log each round: failure point + fix taken
- **3 failures and still failing → stop, do not attempt a 4th time**
- Only applies to "automatically verifiable" Tests; parts needing human judgment like UI experience go straight to the user to test

### 3.2 Exceptions That May Skip the User Acceptance Gate

The following cases may skip the Gate and go straight to the next block:

- Pure documentation changes (e.g. CLAUDE.md / CHANGELOG.md and other docs)
- Pure comment / typo fixes
- Intermediate refactors already covered by later-stage verification

> When skipping, note in the development log: "Skipped user test — reason: …".

### 3.3 Test Guide Writing — 4 Norms (template: [templates/test-guide.md.template](../../templates/test-guide.md.template))

1. **Independently runnable**: each step depends on no memory of the prior step; the user can paste and run.
2. **Explicit commands**: give the full pasteable command, not "run some script".
3. **Concrete expected results**: "returns 200 + contains field X" rather than "succeeds".
4. **Clear failure criteria**: "if Y appears → it means Z", so the user can judge what went wrong themselves.

> When the 3 self-check rounds are exhausted or you hit a blocker mid-way, use [templates/selfcheck-fail.md.template](../../templates/selfcheck-fail.md.template) to summarize for ruling — round 3 must invoke Sentinel's diagnostic mode to list 2-3 hypotheses, not just report "can't fix it".

---

## 4. Decision Tree When the Loop Fails

| State | Action |
|---|---|
| Self-check fails round 1–2 | Fix and rerun all Tests |
| Self-check still failing round 3 | Stop, list failure points + directions tried, ask the user to rule |
| User acceptance fails | Enter the fix loop (back to step 1), does not count as moving to the next block |
| Comparison finds PRD vague | Go to the "PRD vague" flow in [§5 Conflict Handling](../05_conflict_handling/_index.md) |
| Comparison finds the PRD itself has a bug | Go to the "PRD bug" flow in [§5 Conflict Handling](../05_conflict_handling/_index.md), await ruling |
| Implementation beats PRD | Go to the "implementation beats PRD" flow in [§5 Conflict Handling](../05_conflict_handling/_index.md), keep implementation + record + await ruling |

---

## 🔗 Related Compass sections
- [§4.1 DoD](../04_quality_gates/01_dod.md) — details of the hard gates referenced by step 2 of this loop
- [§3.3 Implementation Order](./03_implementation_order.md) — basis for stage splitting, decides when this loop fires
- [§5 Conflict Handling](../05_conflict_handling/_index.md) — handling flow when comparison finds the PRD vague / buggy / worse than the implementation
- [§3 Implementation](../03_implementation/_index.md) — message format and granularity for the step 10 git commit (commit convention)

## 📝 Status
v0.3.0 (+ §3.3 test-guide 4 norms + test-guide / selfcheck-fail templates + block vs stage terminology).
