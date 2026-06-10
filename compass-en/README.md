<!-- LANG SWITCH -->

**English**

# Compass — The Compass of PRD Discipline

> A Claude Code skill that acts as "the compass between PRD and implementation" — making sure you build to spec, don't drift, and don't drop items. Pairs with the [Sentinel](https://github.com/RayLi-Git/sentinel) thinking OS to form a complete toolkit: Sentinel watches "how you think," Compass watches "how you execute to spec."

![license](https://img.shields.io/badge/license-MIT-blue)
![companion](https://img.shields.io/badge/companion-Sentinel-purple)

> §1–§11 all modules have content; bilingual (English + 繁體中文) ready. Full roadmap in [docs/SCOPE.md](./docs/SCOPE.md).

---

## The problem it solves

The three most common failure modes after you get a PRD:

1. **Drift** — halfway through you realize you've drifted from the PRD, but you've already written 3 days of code and can't get back
2. **Dropped items** — the checklist says "auth, 12 endpoints ⬜", you finish 9 and check it off, the remaining 3 never get written and nobody notices
3. **Half-finished** — you reach 70%, leave a TODO "circle back later," but "later" never comes

Compass blocks all three with **discipline + tool enforcement**.

## Core beliefs

1. **PRD is a contract, not a suggestion** — every deviation must be logged, aligned, ruled on
2. **Done means done, no half-finished work** — you can ship in small slices, but no half-finished phasing
3. **Rely on exit codes, not discipline** — mechanical checks beat stating rules, by a lot
4. **Brownfield needs discipline too** — PRD discipline isn't only for greenfield projects

## 11 topic modules

```
§1 Foundations             — five phases + core principles
§2 Definition of Ready     — pre-flight PRD health check ⭐ new
§3 Implementation          — in-flight SOP
§4 Quality Gates           — acceptance / self-review / tool enforcement
§5 Conflict Handling       — PRD conflicts: static three-track (vague/bug/gap) + dynamic (mid-flight change/cross-document/multi-PRD), all shipped
§6 Non-Functional (NFR)    — performance/observability/security/a11y/SLA ⭐ new
§7 Operations              — Migration / Rollback / Deployment ⭐ new
§8 Brownfield              — working in an existing codebase ⭐ new
§9 Collaboration           — cross-person / cross-AI ⭐ new
§10 Testing Strategy        — unit/integration/e2e split ⭐ new
§11 Tooling                — M-007~M-010 tool enforcement + general scripts
```

⭐ marks chapters written **from scratch** relative to the existing SOP.

## Relationship to Sentinel

[Sentinel](https://github.com/RayLi-Git/sentinel) is its **companion skill**:

| Dimension | Sentinel | Compass |
|---|---|---|
| Watches | your thinking | your relationship to the PRD |
| Trigger question | "Have I thought this through?" | "Am I following the PRD?" |
| Applies to | any engineering task | implementation work with a spec |

The two are often used together. Full split in [docs/SCOPE.md](./docs/SCOPE.md).

## Install

```bash
# Install as a user-level skill (applies to all projects)
mkdir -p ~/.claude/skills/compass
cp -r SKILL.md references ~/.claude/skills/compass/

# Verify structure
ls ~/.claude/skills/compass   # → SKILL.md  references
```

See [docs/INSTALL.md](./docs/INSTALL.md) for the full guide (skill + tool scripts + templates).

## Scope boundaries

**Compass does not cover**: PRD writing / product discovery / PM tooling / pure exploratory prototyping / pure copy edits.
**Detailed covers and does-not-cover list**: see [docs/SCOPE.md](./docs/SCOPE.md)

## Design philosophy

Read the full set of design decisions and trade-offs in **[docs/DESIGN.md](./docs/DESIGN.md)**.

## License

[MIT](./LICENSE) © Ray_Li

> This project is a portfolio piece exploring "how to encode the discipline of PRD-driven development into an AI coding partner." Its companion piece [Sentinel](https://github.com/RayLi-Git/sentinel) explores "how to encode structured thinking into an AI coding partner."
