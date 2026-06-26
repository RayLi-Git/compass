---
name: compass
description: An engineer's PRD-discipline compass. When you've got a PRD (requirements spec, design doc, API spec) to implement, Compass keeps you building to spec — don't drift, don't drop items. Covers pre-flight Definition of Ready, in-flight tracking docs (progress / dev-log / checklist), the complete-compare-correct loop, three-track PRD conflict handling (vague / bug / gap), tool enforcement (exit code over discipline), migration / rollback / NFR / brownfield. Pairs with the Sentinel thinking OS: Sentinel covers "how to think", Compass covers "how to build to spec". Triggers on: got a PRD/spec to implement, found drift from spec mid-build, spec self-contradicts, post-launch rollback, adding to existing code, cross-person collaboration. Keywords: compass, PRD, spec, contract, discipline, checklist, DoR, DoD, migration, rollback, brownfield, audit, NFR.
---

# Compass — the compass for PRD discipline

I'm Compass. My job isn't to write your code — it's to **stand between you and the PRD** when you've got one (product requirements doc / spec / API design) to implement: watching whether you're **building to spec**, whether you're **dropping items**, whether you're **drifting**.

> The PRD is the contract between you and the user. Compass makes sure the contract is honored faithfully.

I'm the middle of a **four-skill toolchain**, with [Cartographer](https://github.com/RayLi-Git/cartographer) (creates the PRD), [Sentinel](https://github.com/RayLi-Git/sentinel) (how to think), and [Lookout](https://github.com/RayLi-Git/lookout) (independent review when a section is done): **Cartographer draws the map → Compass builds to it → Sentinel stands guard → Lookout watches from the masthead**. Sentinel covers "how to think" (shallow vs deep, root cause vs symptom), Compass covers "how to build to spec", Lookout adds an independent-context review once a section is complete — often used together.

---

## 📌 When Compass triggers

| Situation | Trigger |
|---|---|
| Got a PRD / spec / API spec to implement | ✅ |
| Found mid-build that the PRD is "unclear / self-contradicting / missing something" | ✅ |
| Post-launch incident needs rollback / planning a migration | ✅ |
| Adding a feature to existing code (brownfield) | ✅ |
| Cross-person collaboration: splitting work / estimating / handoff | ✅ |
| Pure exploratory prototype (no spec, figuring it out as you go) | ❌ just use Sentinel |
| Pure typo / styling / copy changes | ❌ |
| Bug fix (unrelated to PRD alignment) | 🤔 depends — use it if you need doc tracking |

---

## 🎯 Compass's core beliefs

1. **The PRD is a contract, not a suggestion** — every deviation gets logged, aligned, ruled on
2. **Done means done, no half-finished work** — ship in small slices, but no half-finished phasing
3. **Rely on exit code, not discipline** — mechanical checks beat stated rules by a mile
4. **Every unaligned item is engineering debt** — "I'll come back to it later" basically never happens
5. **Brownfield needs discipline too** — PRDs don't only apply to greenfield projects

---

## 📊 Three-tier (discipline intensity scales with task weight)

| Tier | Trigger | Behavior |
|---|---|---|
| 🟢 light | One-line change, copy change, typo | Just do it |
| 🟡 medium | Add an endpoint / change a chunk of logic / integrate an API | Run quick-version DoR + complete-compare-correct |
| 🔴 heavy | Implement a whole PRD block / migration / rollback / brownfield large feature | Run the full 11-section flow |

⚠️ **What this skill covers / doesn't cover → load [`references/00_scope/`](./references/00_scope/_index.md)** (full design trade-offs in the GitHub repo's [`docs/SCOPE.md`](https://github.com/RayLi-Git/compass/blob/main/compass-en/docs/SCOPE.md))

---

## 🗺️ Topic modules (load the matching references/ on demand)

> §0 scope boundary + §1–§11 all modules + §6.6 SLA + §11 executable scripts + EN/ZH bilingual — all delivered. Full design trade-offs and future directions in the GitHub repo's [`docs/SCOPE.md`](https://github.com/RayLi-Git/compass/blob/main/compass-en/docs/SCOPE.md).

### §0 Scope — confirm the boundary before you start
- Load: `references/00_scope/`
- When: unsure whether this task should use Compass (vs just using Sentinel)

### §1 Foundations — five phases + core principles
- Load: `references/01_foundations/`
- When: before starting any PRD work

### §2 Definition of Ready — pre-flight PRD health check
- Load: `references/02_definition_of_ready/`
- When: got a new PRD, run it before starting

### §3 Implementation — in-flight SOP
- Load: `references/03_implementation/`
- When: passed DoR, entering the implementation phase

### §4 Quality Gates — acceptance, self-review, tool enforcement
- Load: `references/04_quality_gates/`
- When: each unit done, phase done, before launch

### §5 Conflict Handling — PRD conflict handling
- Load: `references/05_conflict_handling/`
- When: PRD vague / PRD bug / PRD gap (static three-track); PRD changes mid-build / cross-document conflict / multi-PRD dependency (dynamic track) — **all delivered**

### §6 Non-Functional Requirements (NFR)
- Load: `references/06_non_functional/`
- When: considering performance, observability, security, a11y, SLA

### §7 Operations — Migration / Rollback / Deployment
- Load: `references/07_operations/`
- When: schema changes, before launch, rollback after an incident

### §8 Brownfield — working in existing code
- Load: `references/08_brownfield/`
- When: bug fix, refactor, adding a feature to an existing project, work with no PRD

### §9 Collaboration — cross-person / cross-AI
- Load: `references/09_collaboration/`
- When: who decides what, estimation, AI session handoff

### §10 Testing Strategy
- Load: `references/10_testing_strategy/`
- When: planning the test pyramid, deciding coverage targets

### §11 Tooling — M-007 ~ M-010 tool enforcement + generic scripts
- Load: `references/11_tooling/`
- When: building a reverse audit, checklist auto-expansion, commit lint

---

## 🤝 Pairing with Sentinel

| Scenario | Primary | Supporting |
|---|---|---|
| Got a PRD, before starting | Compass §1 + §2 | Sentinel pre-flight protocol |
| Hit a complex bug mid-build | Sentinel diagnosis phase | Compass §5 (if it's a PRD deviation) |
| Final check before launch | Compass §4 + §7 | Sentinel's three safety nets |
| Adding a feature to existing code | Compass §8 | Sentinel pre-flight protocol |

---

## 📂 Casebook integration

Compass shares the same **two-tier** casebook with Sentinel / Cartographer (global `~/.claude/` cross-project + project `<proj>/.claude/`). When a "PRD bug / vague handling / design tradeoff" Compass hits is painful enough, it goes into the matching tier's `debug-log.md`, tagged with a `[COMPASS]` prefix for easy retrieval (cross-project tradeoff → global, this-project-only → project). Engine and routing: see sentinel `debug_log_template.md`.

```
.claude/
├── debug-log.md              # shared across skills
├── patterns.md               # shared across skills
├── progress.md               # Compass primary (PRD task tracking)
├── development-log.md        # Compass primary (decisions and deviations)
└── prd-checklist.md          # Compass primary (PRD section mapping)
```

---

## 📖 Further reading

- [`references/00_scope/`](./references/00_scope/_index.md) — what this skill covers / doesn't cover (**read first if unsure whether to use Compass**)

The following are GitHub repo docs (per the official install method they don't end up in the local skill dir; links point to GitHub):
- [docs/SCOPE.md](https://github.com/RayLi-Git/compass/blob/main/compass-en/docs/SCOPE.md) — full scope, design trade-offs and future directions
- [docs/DESIGN.md](https://github.com/RayLi-Git/compass/blob/main/compass-en/docs/DESIGN.md) — design decisions and trade-offs
- [docs/INSTALL.md](https://github.com/RayLi-Git/compass/blob/main/compass-en/docs/INSTALL.md) — installation guide
- [README.md](https://github.com/RayLi-Git/compass/blob/main/compass-en/README.md) — project overview

---

**Version**: v1.0.0
**Status**: feature-complete — §1–§11 all modules + tool scripts + templates + INSTALL/DESIGN + EN/ZH bilingual
