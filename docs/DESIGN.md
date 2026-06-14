<!-- LANG SWITCH -->

**English** | [繁體中文](./DESIGN.zh-TW.md)

# Design Decisions

> This document records the key design decisions and trade-offs behind Compass's journey from a personal development SOP into a reusable skill.
> The value of a portfolio piece isn't *what* was built — it's *why it was built this way*. What follows is the reasoning.
> Coverage boundaries and future directions live in [SCOPE](./SCOPE.md); this doc is only about the *why*.

---

## Starting point: from a private SOP to a reusable skill

Compass's raw material wasn't conjured from nothing — it was a "PRD-driven development SOP" I'd long used myself, plus the "PRD Twelve Commandments" written into my personal `CLAUDE.md`. The first key insight was this:

> Turning an SOP **tailored to yourself** into a skill **others can use** isn't a copy-paste problem — it's a **de-privatization** problem.

My SOP was packed with things that only held for me: a hardcoded FastAPI structure, a specific project's PII module ordering, the private path `~/.claude/開發SOP/`, an `audit_prd_vs_code.py` I'd written myself. Useful to me, but to a stranger receiving the skill they're noise — or dead links.

**This set the tone for the whole project: one of Compass's core jobs is translating "holds for me" into "holds for any engineer" — keep the skeleton of discipline, strip out the personal flesh.**

---

## Decision 1: Position as Sentinel's "companion skill," not merged into one

**Options**: (A) cram PRD discipline into Sentinel as one mega-skill. (B) Make it a separate second skill, paired with Sentinel.

**Chose B.** Reasoning: Sentinel governs *how you think* (surface vs deep, root cause vs symptom) — a thinking layer that applies to any engineering task. Compass governs *how you execute to spec* — applicable only when there's a PRD/spec. The two have **different triggers and different scopes**. Forcing them into one would tangle even a typo fix in PRD discipline, violating Sentinel's principle of "thinking intensity scales with task weight."

**Consequence**: the two skills share the `.claude/` case files, but Compass's entries get a `[COMPASS]` prefix for retrieval. One watches thinking, one watches the spec — together they form the complete "before-you-act + while-you-act" toolkit.

> **Addendum (after Cartographer joined)**: this decision was originally a two-skill pairing (Sentinel + Compass); upstream [Cartographer](https://github.com/RayLi-Git/cartographer) (creates the PRD) was added later, forming a three-skill toolchain: **Cartographer draws the map → Compass builds to it → Sentinel stands guard**. The principle "separate skills, each its own job, triggered on demand" holds just as well for all three.

---

## Decision 2: DoR is the dual of DoD — adding an entry gate

**Insight**: the original SOP had only a DoD (Definition of Done, the exit gate), no DoR (Definition of Ready, the entry gate). But the most painful failure in practice isn't "finished without acceptance" — it's "**the PRD itself was incomplete, yet I coded against it for three days**."

**A vague PRD doesn't announce itself** — it bites when you reach the third file and try to assemble a return format you assumed was defined. By then you've made a pile of assumptions and written a pile of code coupled to them.

**Resolution**: add §2 Definition of Ready — before writing the first line, health-check whether the PRD itself *can be implemented* (per-endpoint method/path/auth/schema/error codes/idempotency, per-table constraints, auth ownership…). **DoR at the entrance, DoD at the exit — dual gates.** A bad PRD silently poisons everything downstream; DoR catches it at the source.

**Key discipline**: DoR is not "reject imperfect PRDs" — real PRDs are almost never perfect. DoR is "**tell which imperfections block and which don't**": send blockers back, annotate minor gaps as assumptions and continue.

---

## Decision 3: The core insight — enforce with tools, not discipline

This is Compass's most original contribution, and the one learned deepest through real testing (the original SOP §14, Compass §11's M-007~M-010).

**Problem**: no amount of "discipline," "rules," or "be careful next time" stops the self-rationalization that kicks in under deadline pressure. "Finished 9 of 12 endpoints, check it off"; "commit message says 'all done' but half is missing" — these aren't from not knowing the rules. They're because **rules depend on a human to remember and self-enforce**.

**Resolution**: turn judgment from "rely on memory" into "**mechanical enforcement**":
- **M-007 anti-aggregation**: checklists forbid aggregate items like "12 ⬜"; every item must be one checkbox — omissions have nowhere to hide.
- **M-008 reverse audit**: run a script comparing "what the PRD lists vs what the code implements." **Non-zero exit code = failure** — rely on the exit code, not discipline.
- **M-010 ban subjective commit words**: a git hook blocks unverifiable words like "complete/done/all," forcing concrete counts like "12/12 endpoints."

**Lesson**: **"rely on exit codes, not discipline."** A mechanical check that exists but isn't run is wasted; but once built, it catches every time and never slacks because you're tired. This runs through all of Compass's tool design.

---

## Decision 4: Scripts must be config-driven, not hardcoded to my project

**Tension**: my original `audit_prd_vs_code.py` hardcoded FastAPI's `@app.get` pattern and specific PRD section numbers. Runs for me, wrong for everyone else.

**Resolution**: make the scripts **config-driven** — read a `compass-audit.json` describing "where your PRD is, what regex extracts items, which code files to scan." **The script itself is project-agnostic**; each project writes its own config. When no config is found, print an example and exit 2 (by design, not a failure).

**A derived lesson** (logged in the case file): these emoji-printing scripts crash with `UnicodeEncodeError` on a Traditional-Chinese Windows (cp950 console), and the crash's exit 1 collides with the "PRD has gaps" business code — a silent misjudgment. The fix is `sys.stdout.reconfigure(encoding="utf-8")` everywhere. **Generalization isn't just stripping paths — it's surviving different environments.**

---

## Decision 5: "Done means done" — reconciling with Agile without abandoning anti-half-finished

**The original SOP said**: "write it all at once, no phasing, no V1/V2/V3." But that directly conflicts with mainstream practice (Agile / MVP / incremental delivery) — incremental delivery isn't laziness, it's a legitimate way to cut risk and get real feedback.

**Insight**: what the SOP really meant wasn't "no phasing," but "**no half-finished work**" — don't write half then run off to something else, don't promise "patch in V2" and never deliver V2.

**Fix**: soften "write it all at once, no phasing" to "**done means done, no half-finished work; you can ship in small slices, but no half-finished phasing**." Keep the anti-half-finished spirit while no longer opposing incremental delivery. The keyword shifts from "phase" to "**half-finished**."

**Lesson**: when turning "holds for me" into "holds for others," separate a rule's **spirit** from its **literal wording** — the literal may clash with how others work, but the spirit is usually shared.

---

## Decision 6: Conflict handling by track — static three + dynamic three

**Insight**: "the PRD differs from what I expected" is actually several different things; handling them together is a disaster.

**Static three** (PRD doesn't move, you find the problem reading it):
- **Vague**: either reading works → take the more specific one, **don't stop**.
- **Bug**: self-contradictory, no reading works → **stop and await a ruling**.
- **Gap + better implementation**: PRD didn't say it but you naturally added something aligned with the principles → 6-gate check, **keep and await a ruling** (don't just YAGNI-cut it).

**Dynamic three** (not covered by the original SOP, but the highest-frequency real conflicts):
- **Mid-flight PRD change**: the PRD bumps versions while you're coding — the most painful, because completed modules may silently become wrong.
- **Cross-document conflict**: PRD vs ADR vs OpenAPI vs ERD contradict each other; decide authority "by domain."
- **Multi-PRD dependencies**: ordering and shared contracts across sub-PRDs.

**Key design**: precisely route "what should stop" vs "what shouldn't" — so you don't waste time asking about vague points, nor barrel ahead on a real bug.

---

## Decision 7: Existing code is a "second document" — brownfield needs discipline too

**The original SOP listed brownfield / pure bug fixes as "not applicable."** But most real work IS brownfield. That's a gap.

**Core framing**: in an existing codebase, **the existing code is a second source of truth alongside the PRD** — it records "how the system actually runs now," and may hide implicit requirements, edge-case patches, and downstream dependencies the PRD never mentioned.

**Consequence**: when the PRD conflicts with existing code, that's not a "PRD bug" — it's a **cross-document conflict** (§5.3): existing code is one document, the PRD another; decide authority by domain, don't blindly overwrite to match the PRD. **Risk asymmetry**: in brownfield, breaking existing behavior costs far more than missing a new feature.

---

## Decision 8: A dedicated SCOPE — saying "no" is also design

The final insight: a tool's value lies not only in *what it does*, but in clearly stating what it **does not do**.

Compass's scope is far more complex than Sentinel's — the boundary between "PRD discipline" and "not PRD discipline" blurs easily (PRD writing? product discovery? PM tooling? architecture decisions?). So a dedicated [SCOPE](./SCOPE.md) spells out what's covered and what isn't, preventing misuse and mismatched expectations.

**It's also a division-of-labor declaration with Sentinel**: pure exploratory prototyping, pure copy edits, ways of thinking — those are Sentinel's territory, not Compass's. A tool that tries to "do everything" ends up doing nothing precisely.

---

## Overall architecture

| Layer | Role | Analogy |
|---|---|---|
| `SKILL.md` | always-on pointers + trigger protocol | doorpost sign (lean, loads references on demand) |
| `references/` | detailed discipline across 11 topic modules | library stacks (visited when needed) |
| `scripts/` + `templates/` | runnable examples of tool enforcement + tracking-doc templates | toolbox (the physical form of mechanical enforcement) |

The core principle matches Sentinel: **"pointers always on, detail on demand"** — SKILL.md stays lean (its description is also bound by a ~1024-character limit) to guarantee triggering, while the real discipline detail loads on demand per module, never blowing up the context.

---

> Compass isn't a silver bullet — it's a **precise tool for a specific situation**. In the same toolchain, [Cartographer](https://github.com/RayLi-Git/cartographer) explores "forcing fuzzy ideas into a verifiable PRD" and [Sentinel](https://github.com/RayLi-Git/sentinel) explores "encoding structured thinking into an AI coding partner"; Compass explores "how to encode the discipline of PRD-driven development into that partner's execution discipline."
