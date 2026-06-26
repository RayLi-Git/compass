**English** | [繁體中文](../compass-zh/docs/SCOPE.md)

# Scope

> A skill's value lies not only in "what it can do," but in clearly stating "what it does not do." This document lists Compass's coverage boundaries explicitly, to prevent misuse or mismatched expectations.

---

## In scope

**Situations Compass covers:**

- **Implementation work backed by a PRD / spec / API spec** — product requirement docs, Design Docs, OpenAPI specs, spec sheets, technical proposals.
- **Greenfield** — brand-new project, built from scratch per PRD.
- **Brownfield** — adding features, fixing bugs, refactoring on an existing codebase (§8 handles this specifically).
- **Single AI + single user collaboration** — the mainstream case.
- **Multi-stakeholder collaboration** — §9 covers "who decides what" routing.
- **Any backend / frontend language** — examples use FastAPI / TypeScript, but the principles are language-neutral.
- **Long-running projects** (multi-session, spanning days/weeks) — interrupt-recovery protocol (see [§3.2 tracking docs](../references/03_implementation/02_tracking_docs.md)).

**Decision types covered:**

| When… | Module |
|---|---|
| How to absorb a PRD once you receive it | §3.1 |
| The PRD is unclear | §5.1.1 |
| The PRD is wrong | §5.1.2 |
| The PRD didn't specify but implementation is better | §5.1.3 |
| The PRD bumps versions mid-flight | §5.2 |
| The PRD conflicts with other documents | §5.3 |
| Multiple PRDs have dependencies | §5.4 |
| Landing performance / observability / security / a11y specs | §6 |
| Planning the pre-launch migration plan | §7.1 |
| Rollback after an incident | §7.2 |
| Starting to add features to an existing codebase | §8.4 |
| No formal PRD but you still need discipline | §8.5 |
| Handing off between AI sessions | §9.3 |

---

## Out of scope

Explicitly out of scope, to avoid misuse.

**Work types not covered:**

- **PRD writing itself** — Compass assumes the PRD already exists. Turning a fuzzy idea into a spec is [Cartographer](https://github.com/RayLi-Git/cartographer)'s domain.
- **Product discovery / user research** — this happens before the PRD is written. Compass starts from a PRD that's already ready.
- **Project management** (Jira / scheduling / resource planning) — Compass is **implementation discipline**, not a PM tool.
- **Pure exploratory prototyping** — the phase where there's no spec yet and you're figuring it out as you go; use the [Sentinel](https://github.com/RayLi-Git/sentinel) thinking OS instead.
- **Pure copy / styling / typo changes** — such lightweight tasks don't need PRD discipline.
- **Free-form work with no design goal** — Compass assumes you have something to achieve (spec / goal).

**Engineering topics not covered:**

- **Design Patterns / algorithm selection** — engineering fundamentals, not a PRD discipline issue.
- **Language-specific best practices** (Pythonic / Idiomatic Go) — Compass is language-neutral.
- **DevOps / CI/CD pipeline design** — Compass mentions deployment (§7.3) but doesn't teach CI/CD.
- **Architecture decisions** (monolith vs. microservices) — the PRD should have decided already; Compass ensures you follow it.
- **Ways of thinking / cognitive biases** — this is [Sentinel](https://github.com/RayLi-Git/sentinel)'s scope.

---

## Boundaries & common misconceptions

These boundaries are drawn on purpose, not gaps. The current Compass (all modules §1–§11 + runnable tool scripts + EN/ZH bilingual) is complete and usable.

- **"It's a lightweight reminder."** No — Compass leans heavy-discipline: it assumes you're willing to spend time building tracking docs, running audits, and writing checklists. For lightweight situations, use Sentinel. This is a deliberate trade-off, not a limitation.
- **"It works out of the box for any stack."** The *principles* are language-neutral, but the runnable examples center on Python/FastAPI + TypeScript/React. Other stacks require you to adapt the scripts' regexes.
- **"It can consume my OpenAPI / ERD directly."** Currently built around "one text PRD"; structured specs like OpenAPI / ERD still rely on a human to turn them into a checklist. (A possible future direction, not a guarantee: structured-spec auto-conversion so §2 DoR / §11 reverse audit can consume them directly.)
- **"It fights Agile."** It has *tension* with rapid-MVP culture, not opposition. The stance is "once you decide to follow the PRD, follow it all the way through" — *the PRD is not Compass's enemy; changing the PRD mid-flight is* ([§5.2](../references/05_conflict_handling/02_prd_change.md) handles that).
- **"It assumes a perfect PRD."** The opposite — DoR exists precisely because real PRDs are often imperfect, so before kickoff you check the PRD itself rather than blindly trusting it.

---

## Toolchain split

Compass is the **build-to-spec** stage of a four-skill toolchain — each watches a different thing:

| Skill | Role | Watches |
|---|---|---|
| [Cartographer](https://github.com/RayLi-Git/cartographer) | draws the map | turning a fuzzy idea into a solid PRD |
| **Compass** | walks the map | are you following the PRD? (build to spec, no drift) |
| [Sentinel](https://github.com/RayLi-Git/sentinel) | stands guard | how you think (shallow vs. deep, symptom vs. root cause) |
| [Lookout](https://github.com/RayLi-Git/lookout) | watches from the mast | independent-context code review |

**Cartographer draws the map → Compass walks it → Sentinel stands guard → Lookout watches.**

Compass and Sentinel are the closest pair — complementary responsibilities on the same task:

| Dimension | Sentinel | Compass |
|---|---|---|
| Primarily watches | Your "**thinking**" | Your relationship with the "**PRD**" |
| Core belief | Don't spin in the shallows, the symptom isn't the root cause | The PRD is a contract, done means done |
| Core trigger question | "Have I thought this through?" | "Am I following the PRD?" |
| Key actions | Pre-flight protocol, five phases, root-cause tree | DoR, tracking docs, PRD conflict handling, tool enforcement |
| Applicable scope | Any engineering task | Tasks with a PRD or target spec |

**Typical situations for using them together:**

1. **Starting work with a PRD**: first think it through with Sentinel's pre-flight protocol → then Compass §2 DoR + §3 kickoff.
2. **Stuck mid-implementation**: Sentinel's diagnosis phase finds the root cause; if it's "the PRD didn't cover it," switch to Compass §5.
3. **Adding a large feature to an existing codebase**: Compass §8 brownfield flow + Sentinel's pre-flight protocol.
4. **Before launch**: Compass §4 + §7 run the full check; Sentinel's three safety nets (rollback plan). After a unit lands, [Lookout](https://github.com/RayLi-Git/lookout) does an independent-context review.

---

## Feedback & contribution

Compass is a personal portfolio piece, but contributions are welcome via GitHub Issues:

- Spots where the scope description is inaccurate.
- Situations you hit that this document doesn't cover but you think it should (or shouldn't).
- Blind spots in the division of labor across the toolchain.

---

> **Remember**: Compass is not a panacea; it's a **tool that's precise in specific situations**. Use it in the right situation and it saves you 80% of deviation cost; use it in the wrong situation and it becomes process overhead. Read this document first, then decide whether to use it.
