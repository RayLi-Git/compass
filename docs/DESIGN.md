**English** | [繁體中文](../compass-zh/docs/DESIGN.md)

# Design

> The value of a portfolio piece isn't *what* was built — it's *why it was built this way*. This document records the design philosophy and key decisions behind Compass's journey from a private development SOP into a reusable skill.
> Coverage boundaries and future directions live in [SCOPE](./SCOPE.md); this doc is only about the *why*.

---

## Design philosophy

Compass's raw material wasn't conjured from nothing — it was a "PRD-driven development SOP" used privately for a long time, plus a "PRD Twelve Commandments" list. The first key insight set the tone for the whole project:

> Turning an SOP **tailored to one person** into a skill **anyone can use** isn't a copy-paste problem — it's a **de-privatization** problem.

The original SOP was packed with things that only held for its author: a hardcoded FastAPI structure, one project's PII module ordering, a private skills path, a custom audit script. Useful to the author, but to a stranger receiving the skill they're noise — or dead links.

**So one of Compass's core jobs is translating "holds for me" into "holds for any engineer" — keep the skeleton of discipline, strip out the personal flesh.** Three principles fall out of that:

1. **PRD is a contract, not a suggestion** — every deviation is logged, aligned, and ruled on.
2. **Done means done** — ship in small slices if you like, but never half-finished phases.
3. **Rely on exit codes, not discipline** — mechanical checks beat stated rules, by a lot.
4. **Brownfield needs discipline too** — PRD discipline isn't only for greenfield.

The architecture mirrors that of its companions: **pointers always on, detail on demand.** `SKILL.md` stays lean (its description is also bound by a ~1024-character limit) to guarantee triggering, while the real discipline detail loads on demand from `references/` per module — never blowing up the context.

| Layer | Role | Analogy |
|---|---|---|
| `SKILL.md` | always-on pointers + trigger protocol | doorpost sign (lean, loads references on demand) |
| `references/` | detailed discipline across 11 topic modules | library stacks (visited when needed) |
| `scripts/` + `templates/` | runnable tool enforcement + tracking-doc templates | toolbox (the physical form of mechanical enforcement) |

---

## Key decisions

### Decision 1: A separate skill, not merged into one

- **Problem**: Should PRD discipline be crammed into one mega-skill alongside the thinking layer, or split out?
- **Choice**: Split it out. The thinking layer governs *how you think* (surface vs. deep, root cause vs. symptom) — it applies to any engineering task. Compass governs *how you execute to spec* — applicable only when there's a PRD/spec. The two have **different triggers and different scopes**.
- **Trade-off**: Two skills to install instead of one, and they must share state (the `.claude/` case files; Compass entries get a `[COMPASS]` prefix for retrieval). In exchange, a typo fix is never dragged into PRD discipline. This same "separate skill, each watches one thing, triggered on demand" principle later extended into the full four-skill toolchain.

### Decision 2: DoR is the dual of DoD — adding an entry gate

- **Problem**: The original SOP had only a DoD (the exit gate). But the most painful real failure isn't "finished without acceptance" — it's "**the PRD itself was incomplete, yet you coded against it for three days**." A vague PRD doesn't announce itself; it bites when you reach the third file and try to assemble a return format you assumed was defined.
- **Choice**: Add §2 Definition of Ready — before writing the first line, health-check whether the PRD *can be implemented* (per-endpoint method/path/auth/schema/error codes/idempotency, per-table constraints, auth ownership…). DoR at the entrance, DoD at the exit — dual gates.
- **Trade-off**: An up-front cost before any code is written. But DoR is explicitly *not* "reject imperfect PRDs" — real PRDs are almost never perfect. It only "tells which imperfections block and which don't": send blockers back, annotate minor gaps as assumptions and continue.

### Decision 3: Enforce with tools, not discipline

- **Problem**: No amount of "discipline," "rules," or "be careful next time" stops the self-rationalization that kicks in under deadline pressure. "Finished 9 of 12 endpoints, check it off"; "commit message says 'all done' but half is missing." These aren't from not knowing the rules — they're because **rules depend on a human to remember and self-enforce**.
- **Choice**: Turn judgment from "rely on memory" into **mechanical enforcement** — M-007 anti-aggregation (checklists forbid "12 ⬜"; one checkbox per item), M-008 reverse audit (a script comparing PRD vs. code; **non-zero exit code = failure**), M-010 banning subjective commit words (a git hook blocks "complete/done/all," forcing "12/12 endpoints").
- **Trade-off**: You have to actually build and run the checks — a check that exists but isn't run is wasted. But once built, it catches every time and never slacks because you're tired. This is Compass's most original contribution and runs through all its tooling.

### Decision 4: Scripts are config-driven, not hardcoded

- **Problem**: The original audit script hardcoded FastAPI's `@app.get` pattern and specific PRD section numbers. Runs for one project, wrong for everyone else.
- **Choice**: Make the scripts **config-driven** — read a `compass-audit.json` describing "where your PRD is, what regex extracts items, which code files to scan." The script itself is project-agnostic; each project writes its own config. When no config is found, print an example and exit 2 (by design, not a failure).
- **Trade-off**: Each project pays a one-time config-writing cost. A derived lesson: these emoji-printing scripts crash with `UnicodeEncodeError` on a Traditional-Chinese Windows console, and that crash's exit 1 collides with the "PRD has gaps" business code — a silent misjudgment. The fix is `sys.stdout.reconfigure(encoding="utf-8")` everywhere. Generalization isn't just stripping paths — it's surviving different environments.

### Decision 5: "Done means done" — reconciling with Agile

- **Problem**: The original SOP said "write it all at once, no phasing, no V1/V2/V3." That directly conflicts with mainstream practice (Agile / MVP / incremental delivery) — incremental delivery isn't laziness, it's a legitimate way to cut risk and get real feedback.
- **Choice**: What the SOP really meant wasn't "no phasing," but "**no half-finished work**." So soften the rule to "done means done, no half-finished work; you can ship in small slices, but no half-finished phasing." The keyword shifts from "phase" to "**half-finished**."
- **Trade-off**: A softer rule is easier to wriggle out of, so the anti-half-finished spirit has to be enforced elsewhere (the tooling in Decision 3). The general lesson: when turning "holds for me" into "holds for others," separate a rule's **spirit** from its **literal wording** — the literal may clash with how others work, but the spirit is usually shared.

### Decision 6: Conflict handling by track — static three + dynamic three

- **Problem**: "The PRD differs from what I expected" is actually several different things; handling them together is a disaster.
- **Choice**: Route them. **Static three** (PRD doesn't move, you find it reading): *vague* → take the more specific reading, don't stop; *bug* → self-contradictory, stop and await a ruling; *gap + better implementation* → 6-gate check, keep and await a ruling. **Dynamic three** (highest-frequency real conflicts the SOP never covered): *mid-flight PRD change*, *cross-document conflict* (decide authority by domain), *multi-PRD dependencies*.
- **Trade-off**: More branches to learn than a single "ask when unsure" rule. But the precise routing means you don't waste time asking about vague points, nor barrel ahead on a real bug.

### Decision 7: Existing code is a "second document"

- **Problem**: The original SOP listed brownfield / pure bug fixes as "not applicable." But most real work IS brownfield — that's a gap.
- **Choice**: Frame existing code as **a second source of truth alongside the PRD** — it records "how the system actually runs now," and may hide implicit requirements, edge-case patches, and downstream dependencies the PRD never mentioned. So a PRD-vs-code conflict is a *cross-document conflict* (§5.3), not a "PRD bug": decide authority by domain, don't blindly overwrite to match the PRD.
- **Trade-off**: Brownfield work gets slower and more cautious. But the risk is asymmetric — in an existing codebase, breaking existing behavior costs far more than missing a new feature.

### Decision 8: A dedicated SCOPE — saying "no" is also design

- **Problem**: Compass's scope blurs easily — the boundary between "PRD discipline" and "not PRD discipline" is fuzzy (PRD writing? product discovery? PM tooling? architecture decisions?).
- **Choice**: Write a dedicated [SCOPE](./SCOPE.md) that spells out what's covered and what isn't, and declares the division of labor across the toolchain.
- **Trade-off**: Maintenance overhead, and it narrows the perceived audience. But a tool that tries to "do everything" ends up doing nothing precisely — the explicit "no" prevents misuse and mismatched expectations.

---

## What it deliberately doesn't do

These are boundaries drawn on purpose, not gaps. The full reasoning lives in [SCOPE](./SCOPE.md); the short version:

- **It is not a lightweight reminder.** Compass assumes you're willing to spend time building tracking docs, running audits, and writing checklists. If you want lightweight, use [Sentinel](https://github.com/RayLi-Git/sentinel).
- **It does not write the PRD.** Compass starts from a PRD that already exists; turning a fuzzy idea into a solid spec is [Cartographer](https://github.com/RayLi-Git/cartographer)'s job.
- **It does not assume a perfect PRD.** DoR is precisely the acknowledgment that real PRDs are often imperfect — so before kickoff you check the PRD itself rather than blindly trusting it.
- **It has tension with rapid-MVP culture, on purpose.** Not opposed to Lean Startup — the stance is simply "once you decide to follow the PRD, follow it all the way through." In one line: *the PRD is not Compass's enemy; changing the PRD mid-flight is.*

---

> Compass isn't a silver bullet — it's a **precise tool for a specific situation**. It explores "how to encode the discipline of PRD-driven development into an AI coding partner's execution discipline." Its companions explore the rest: [Cartographer](https://github.com/RayLi-Git/cartographer) draws the map, [Sentinel](https://github.com/RayLi-Git/sentinel) governs how you think, [Lookout](https://github.com/RayLi-Git/lookout) watches from the mast.
