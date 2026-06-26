# §0.1 Scope boundary｜What Compass covers / does not cover

## ✅ Situations Compass covers

### Applicable situations
- **Implementation work backed by a PRD / spec / API spec**—product requirement docs, Design Docs, OpenAPI specs, spec sheets, technical proposals
- **Greenfield**—brand-new project, built from scratch per PRD
- **Brownfield**—adding features, fixing bugs, refactoring on an existing codebase ([§8](../08_brownfield/_index.md) handles this specifically)
- **Single AI + single user collaboration**—the mainstream case
- **Multi-stakeholder collaboration**—[§9](../09_collaboration/_index.md) covers "who decides what" routing
- **Any backend / frontend language**—examples use FastAPI / TypeScript, but the principles are language-neutral
- **Long-running projects** (multi-session, spanning days/weeks)—interrupt-recovery protocol: see [§3.2 tracking docs](../03_implementation/02_tracking_docs.md)

### Decision types covered
- How to absorb a PRD once you receive it ([§3.1](../03_implementation/01_prd_intake.md))
- PRD unclear / wrong / unspecified-but-implementation-is-better ([§5.1](../05_conflict_handling/01_vague_bug_gap.md))
- PRD bumps versions mid-flight / conflicts with other docs / multi-PRD dependencies ([§5.2](../05_conflict_handling/02_prd_change.md), [§5.3](../05_conflict_handling/03_cross_document.md), [§5.4](../05_conflict_handling/04_multi_prd.md))
- How to land performance / observability / security / a11y / SLA specs ([§6](../06_non_functional/_index.md))
- How to plan a migration, how to do rollback ([§7](../07_operations/_index.md))
- Adding features to an existing codebase, and the minimal approach when there's no formal PRD ([§8.4](../08_brownfield/04_add_feature.md), [§8.5](../08_brownfield/05_no_prd.md))
- How to hand off between AI sessions ([§9.3](../09_collaboration/03_session_handoff.md))

---

## ❌ Situations Compass does NOT cover

Explicitly out of scope, to avoid misuse:

### Work types not covered
- **PRD writing itself**—Compass assumes the PRD already exists; writing a good PRD is [Cartographer](https://github.com/RayLi-Git/cartographer)'s domain
- **Product discovery / user research**—this happens before the PRD is written; Compass starts from a ready PRD
- **Project management (Jira / scheduling / resource planning)**—Compass is **implementation discipline**, not a PM tool
- **Pure exploratory prototyping**—no spec yet, figuring it out as you go; just use [Sentinel](https://github.com/RayLi-Git/sentinel)
- **Pure copy / styling / typo changes**—lightweight tasks don't need PRD discipline
- **Free-form work with no design goal**—Compass assumes you have something to achieve (spec / goal)

### Engineering topics not covered
- **Design Patterns / algorithm selection**—engineering fundamentals, not a PRD discipline issue
- **Language-specific best practices** (Pythonic / Idiomatic Go)—Compass is language-neutral
- **DevOps / CI/CD pipeline design**—Compass mentions deployment ([§7.3](../07_operations/03_deployment.md)) but doesn't teach CI/CD
- **Architecture decisions (monolith vs microservices)**—the PRD should have decided; Compass ensures you follow it
- **Ways of thinking / cognitive biases**—this is [Sentinel](https://github.com/RayLi-Git/sentinel)'s scope

---

## 🤝 Division of labor with Sentinel

Compass is the middle of a four-skill toolchain (Cartographer creates the PRD → Compass builds to it → Sentinel stands guard → [Lookout](https://github.com/RayLi-Git/lookout) independently reviews when a section is done); complementary to Sentinel:

| Dimension | Sentinel | Compass |
|---|---|---|
| Primarily watches | Your "**thinking**" | Your relationship with the "**PRD**" |
| Core belief | Don't spin in the shallows, the symptom isn't the root cause | The PRD is a contract, done means done |
| Core trigger question | "Have I thought this through?" | "Am I following the PRD?" |
| Key actions | Pre-flight protocol, five phases, root-cause tree | DoR, tracking docs, PRD conflict handling, tool enforcement |
| Applicable scope | Any engineering task | Tasks with a PRD or target spec |

### Typical situations for using them together
1. **Starting work with a PRD**: think it through with Sentinel's "pre-flight protocol" → then Compass [§2 DoR](../02_definition_of_ready/_index.md) + [§3 kickoff](../03_implementation/_index.md)
2. **Stuck mid-implementation**: Sentinel's diagnosis phase finds the root cause; if the cause is "the PRD didn't cover it," switch to Compass [§5](../05_conflict_handling/_index.md)
3. **Adding a large feature to an existing codebase**: Compass [§8 brownfield](../08_brownfield/_index.md) + Sentinel's pre-flight protocol
4. **Before launch**: Compass [§4](../04_quality_gates/_index.md) + [§7](../07_operations/_index.md) run the full check; Sentinel's three safety nets

---

## 🧭 One-line test

> Compass isn't a cure-all — it's a **precise tool for a specific situation**.
> **Have a spec to align to → Compass is primary; just an idea, figuring it out as you go → Sentinel is enough.**
> Right situation, it saves 80% of drift cost; wrong situation, it becomes process overhead.

Full design trade-offs, future directions, and how to contribute: see the GitHub repo's [`docs/SCOPE.md`](https://github.com/RayLi-Git/compass/blob/main/docs/SCOPE.md).
