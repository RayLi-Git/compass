<!-- LANG SWITCH -->

**English**

# Compass — The Compass of PRD Discipline

> A Claude Code skill that acts as "the compass between PRD and implementation" — making sure you build to spec, don't drift, and don't drop items. Pairs with the [Sentinel](https://github.com/RayLi-Git/sentinel) thinking OS to form a complete toolkit: Sentinel watches "how you think," Compass watches "how you execute to spec."

![status](https://img.shields.io/badge/status-WIP%20v0.5.0-orange)
![license](https://img.shields.io/badge/license-MIT-blue)
![companion](https://img.shields.io/badge/companion-Sentinel-purple)

> ⚠️ **Currently at v0.5.0** — §1–§8 and §11 have content (Phase 1+2 done); §9/§10 and the English mirror are still pending. Full roadmap in [docs/SCOPE.md](./docs/SCOPE.md).

---

## The problem it solves

The three most common failure modes after you get a PRD:

1. **Drift** — halfway through you realize you've drifted from the PRD, but you've already written 3 days of code and can't get back
2. **Dropped items** — the checklist says "auth, 12 endpoints ⬜", you finish 9 and check it off, the remaining 3 never get written and nobody knows
3. **Half-finished** — you get to 70%, leave a TODO "circle back later," but "later" never comes

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
§5 Conflict Handling       — PRD conflict handling: static three-track (vague/bug/gap) + dynamic track (mid-flight change/cross-document/multi-PRD), all shipped
§6 Non-Functional (NFR)    — performance/observability/security/a11y ⭐ new
§7 Operations              — Migration / Rollback / Deployment ⭐ new
§8 Brownfield              — working in an existing codebase ⭐ new
§9 Collaboration           — cross-person/cross-AI ⭐ new
§10 Testing Strategy        — unit/integration/e2e split ⭐ new
§11 Tooling                — M-007~M-010 tool enforcement + general scripts
```

⭐ marks chapters written **from scratch** relative to the existing SOP.

## Relationship to Sentinel

[Sentinel](https://github.com/RayLi-Git/sentinel) is its "**companion skill**":

| Dimension | Sentinel | Compass |
|---|---|---|
| Watches | your thinking | your relationship to the PRD |
| Trigger question | "Have I thought this through?" | "Am I following the PRD?" |
| Applies to | any engineering task | implementation work with a spec |

The two are often used together. Full split in [docs/SCOPE.md](./docs/SCOPE.md).

## Install (formal publish once content is complete)

```bash
# v0.5.0: §1–§8 and §11 have content, loadable for real trial use
# Full install guide ships in Phase 5 (see roadmap)
```

## Scope boundaries

**Compass does not cover**: PRD writing / product discovery / PM tooling / pure exploratory prototyping / pure copy edits.
**Detailed covers and does-not-cover list**: see [docs/SCOPE.md](./docs/SCOPE.md)

## Design philosophy

Full design decisions and trade-offs will be collected in `docs/DESIGN.md` at v0.5.0 (🚧 in progress).

## Roadmap

| Version | Content | Status |
|---|---|---|
| v0.1.0-skeleton | architecture, naming, skeleton | ✅ |
| v0.2.0 | existing SOP consolidation (Phase 1) | ✅ |
| v0.5.0 | Critical gap fill (Phase 2) | ✅ current |
| v0.8.0 | Nice-to-have fill (Phase 3) | 🚧 next phase |
| v1.0.0 | Ship | ⏸ |

Full roadmap in [docs/SCOPE.md](./docs/SCOPE.md).

## License

[MIT](./LICENSE) © Ray_Li

> This project is a portfolio piece exploring "how to encode the discipline of PRD-driven development into an AI coding partner." Its companion piece [Sentinel](https://github.com/RayLi-Git/sentinel) explores "how to encode structured thinking into an AI coding partner."
