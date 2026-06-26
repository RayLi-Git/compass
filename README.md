**English** | [繁體中文](./compass-zh/README.md)

# Compass — The Compass of PRD Discipline

> A Claude Code skill that keeps your implementation true to the spec — **build to the PRD, no drift, no dropped items, no half-finished work.** Part of a four-skill toolchain: **Cartographer draws the map → Compass walks it → Sentinel stands guard → Lookout watches from the mast.**

![status](https://img.shields.io/badge/status-active-success)
![license](https://img.shields.io/badge/license-MIT-blue)
![toolchain](https://img.shields.io/badge/toolchain-Cartographer·Compass·Sentinel·Lookout-purple)

---

## The problem it solves

The three most common failure modes once you have a PRD and start building:

1. **Drift** — halfway in you realize you've strayed from the PRD, but 3 days of code are already written and there's no easy way back.
2. **Dropped items** — the checklist says "auth, 12 endpoints ⬜"; you finish 9, check it off, and the other 3 are never written — nobody notices.
3. **Half-finished** — you reach 70%, leave a `TODO: circle back`, and "later" never comes.

Compass blocks all three with **discipline + tool enforcement** (exit codes, not willpower).

## How it works

**Four core beliefs:**

1. **PRD is a contract, not a suggestion** — every deviation is logged, aligned, and ruled on.
2. **Done means done** — ship in small slices if you like, but never half-finished phases.
3. **Rely on exit codes, not discipline** — mechanical checks beat stated rules, by a lot.
4. **Brownfield needs discipline too** — PRD discipline isn't only for greenfield.

**11 topic modules** (loaded on demand from `references/`):

```
§1  Foundations          five phases + core principles
§2  Definition of Ready  pre-flight PRD health check
§3  Implementation       in-flight SOP
§4  Quality Gates        acceptance / self-review / tool enforcement
§5  Conflict Handling    vague / bug / gap + mid-flight change / cross-doc / multi-PRD
§6  Non-Functional       performance / observability / security / a11y / SLA
§7  Operations           migration / rollback / deployment
§8  Brownfield           working inside an existing codebase
§9  Collaboration        cross-person / cross-AI
§10 Testing Strategy     unit / integration / e2e split
§11 Tooling              M-007~M-010 tool enforcement + general scripts
```

## Quick start

```bash
# Install as a user-level skill (applies to all projects)
mkdir -p ~/.claude/skills/compass
cp -r SKILL.md references scripts templates ~/.claude/skills/compass/

# Verify
ls ~/.claude/skills/compass   # → SKILL.md  references  scripts  templates
```

Full guide (skill + tool scripts + templates) in **[docs/INSTALL.md](./docs/INSTALL.md)**.

## The toolchain

Compass is the **build-to-spec** stage of a four-skill toolchain — each watches a different thing:

| Skill | Role | Watches |
|---|---|---|
| [Cartographer](https://github.com/RayLi-Git/cartographer) | draws the map | turning a fuzzy idea into a solid PRD |
| **Compass** | walks the map | are you following the PRD? (build to spec, no drift) |
| [Sentinel](https://github.com/RayLi-Git/sentinel) | stands guard | how you think (shallow vs. deep, symptom vs. root cause) |
| [Lookout](https://github.com/RayLi-Git/lookout) | watches from the mast | independent-context code review |

**Cartographer draws the map → Compass walks it → Sentinel stands guard → Lookout watches.** Full division of labor in [docs/SCOPE.md](./docs/SCOPE.md).

## Structure

```
compass/
├── SKILL.md            skill entry (loaded by Claude Code)
├── references/         11 modules, loaded on demand
├── scripts/            tool-enforcement scripts (lint / audit)
├── templates/          PRD checklist / progress / dev-log templates
├── docs/               DESIGN · INSTALL · SCOPE
└── compass-zh/         Traditional Chinese mirror
```

## Docs

- **[DESIGN](./docs/DESIGN.md)** — design philosophy, key decisions & trade-offs
- **[INSTALL](./docs/INSTALL.md)** — full install (skill + scripts + templates) & verification
- **[SCOPE](./docs/SCOPE.md)** — what it covers, what it doesn't, and the toolchain split

## License

[MIT](./LICENSE) © Ray_Li

> A portfolio piece exploring "how to encode the discipline of PRD-driven development into an AI coding partner." Its companion [Sentinel](https://github.com/RayLi-Git/sentinel) explores "how to encode structured thinking into an AI coding partner."
