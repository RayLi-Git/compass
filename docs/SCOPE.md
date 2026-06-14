<!-- LANG SWITCH -->

**English** | [繁體中文](./SCOPE.zh-TW.md)

# Compass Scope

> A skill's value lies not only in "what it can do," but also in clearly stating "what it does not do." This document explicitly lists Compass's coverage boundaries to prevent misuse or mismatched expectations.

---

## ✅ Situations Compass covers

### Applicable situations

- **Implementation work backed by a PRD / spec / API spec**—product requirement docs, Design Docs, OpenAPI specs, spec sheets, technical proposals
- **Greenfield**—brand-new project, built from scratch per PRD
- **Brownfield**—adding features, fixing bugs, refactoring on an existing codebase (§8 handles this specifically, shipped)
- **Single AI + single user collaboration**—the mainstream case
- **Multi-stakeholder collaboration**—§9 covers "who decides what" routing (delivered)
- **Any backend / frontend language**—examples use FastAPI / TypeScript, but the principles are language-neutral
- **Long-running projects** (multi-session, spanning days/weeks)—interrupt-recovery protocol (see [§3.2 tracking docs](../compass-en/references/03_implementation/02_tracking_docs.md))

### Decision types covered

- How to absorb a PRD once you receive it (§3.1, shipped)
- What to do when the PRD is unclear (§5.1.1, shipped)
- What to do when the PRD is wrong (§5.1.2, shipped)
- What to do when the PRD didn't specify but implementation is better (§5.1.3, shipped)
- What to do when the PRD bumps versions mid-flight (§5.2, shipped)
- What to do when the PRD conflicts with other documents (§5.3, shipped)
- What to do when multiple PRDs have dependencies (§5.4, shipped)
- How to land performance / observability / security / a11y specs (§6, shipped)
- How to plan the pre-launch migration plan (§7.1, shipped)
- How to do rollback after an incident (§7.2, shipped)
- How to start adding features to an existing codebase (§8.4, shipped)
- The minimal approach when there's no formal PRD but you still need discipline (§8.5, shipped)
- How to hand off between AI sessions (§9.3, delivered)

---

## ❌ Situations Compass does NOT cover

Explicitly out of scope, to avoid misuse:

### Work types not covered

- **PRD writing itself**—Compass assumes the PRD already exists. How to "write a good PRD" is another skill's domain
- **Product discovery / user research**—this happens before the PRD is written. Compass starts from a PRD that's already ready
- **Project management (Jira / scheduling / resource planning)**—Compass is **implementation discipline**, not a PM tool
- **Pure exploratory prototyping**—the phase where there's no spec yet and you're figuring it out as you go; just use the [Sentinel](https://github.com/RayLi-Git/sentinel) thinking OS
- **Pure copy / styling / typo changes**—such lightweight tasks don't need PRD discipline
- **Free-form work with no design goal**—Compass assumes you have something to achieve (spec / goal)

### Engineering topics not covered

- **Design Patterns / algorithm selection**—this is engineering fundamentals, not a PRD discipline issue
- **Language-specific best practices** (Pythonic / Idiomatic Go)—Compass is language-neutral
- **DevOps / CI/CD pipeline design**—Compass mentions deployment (§7.3) but doesn't teach CI/CD
- **Architecture decisions (monolith vs microservices)**—the PRD should have decided already; Compass ensures you follow it
- **Ways of thinking / cognitive biases**—this is [Sentinel](https://github.com/RayLi-Git/sentinel)'s scope

---

## 🤝 Division of labor with Sentinel

Compass is the middle of a **three-skill toolchain** (Cartographer creates the PRD → Compass builds to it → Sentinel stands guard throughout); it complements Sentinel:

| Dimension | Sentinel | Compass |
|---|---|---|
| Primarily watches | Your "**thinking**" | Your relationship with the "**PRD**" |
| Core belief | Don't spin in the shallows, the symptom isn't the root cause | The PRD is a contract, done means done |
| Core trigger question | "Have I thought this through?" | "Am I following the PRD?" |
| Key actions | Pre-flight protocol, five phases, root-cause tree | DoR, tracking docs, PRD conflict handling, tool enforcement |
| Applicable scope | Any engineering task | Tasks with a PRD or target spec |
| Case-record contribution | Thinking misjudgments / cross-layer root-cause cases | PRD deviations / spec bugs / design trade-offs |

### Typical situations for using them together

1. **Starting work with a PRD**: first think it through with Sentinel's "pre-flight protocol" → then Compass §2 DoR + §3 kickoff
2. **Stuck mid-implementation**: Sentinel's diagnosis phase finds the root cause; if the root cause is "the PRD didn't cover it," switch to Compass §5
3. **Adding a large feature to an existing codebase**: Compass §8 brownfield flow + Sentinel's pre-flight protocol
4. **Before launch**: Compass §4 + §7 run the full check; Sentinel's three safety nets (rollback plan)

---

## 🧭 Scope & Future Work

> The list below is not a TODO. The current Compass (all modules §1–§11 + runnable tool scripts + EN/ZH bilingual) is complete and usable, and is published on [GitHub](https://github.com/RayLi-Git/compass). This section records where the design's boundaries currently sit and what directions further evolution could take — a deliberate reflection, not a gap.

### Boundaries deliberately drawn

- **Leans heavy-discipline**: Compass assumes you're willing to spend time building tracking docs, running audits, writing checklists. For lightweight situations, use Sentinel — this is a deliberate trade-off, not a limitation (see "Design trade-offs" below).
- **Language-neutral, but examples concentrated**: the principles are language-neutral; the runnable examples center on Python/FastAPI + TypeScript/React. Other stacks require you to adapt the scripts' regexes.
- **Single text PRD as the core assumption**: currently built around "one text PRD"; structured specs like OpenAPI / ERD still rely on a human to turn them into a checklist.

### Where it could evolve (not guaranteed)

- **Structured-spec auto-conversion**: add templates like "OpenAPI spec → checklist auto-expand" and "ERD → schema audit" so §2 DoR / §11 reverse audit can consume structured specs directly.
- **Tooling spin-out**: if the generic scripts in `scripts/` mature, extract them into a standalone PyPI / npm package for cross-repo reuse.
- **More language examples**: add Go / Rust / Ruby examples beyond Python/TS.
- **DESIGN decision record**: add a "why it's designed this way" decision narrative to align with Sentinel's `DESIGN.md` (the README already reserves the link).

---

## 📐 Design trade-offs

The trade-offs Compass deliberately made during design, recorded here:

### 1. Favors "heavyweight discipline" over "lightweight hints"

Compass assumes the user is willing to spend time building tracking docs, running audits, and writing checklists. **It is not a "lightweight reminder" tool**—if you want lightweight, use Sentinel.

### 2. Favors "mechanical enforcement" over "relying on discipline"

A core insight from SOP §14: "discipline only goes so far; tool enforcement is more reliable." Compass heavily recommends "block with exit code," "block with git hook," "block with TodoWrite."

### 3. Favors "PRD-first" over "agile-experiment-first"

Compass has **tension** with Lean Startup / rapid MVP culture. We're not against them; we're saying "**once you decide to follow the PRD, follow it all the way through**."

> In one line: "**The PRD is not Compass's enemy; changing the PRD mid-flight is.**" ([§5.2](../compass-en/references/05_conflict_handling/02_prd_change.md) handles this problem)

### 4. Doesn't assume a perfect PRD

§1 Definition of Ready is precisely the acknowledgment that "real PRDs are often imperfect"—so before kickoff you check the PRD itself rather than blindly trusting it.

---

## 💬 Feedback & contribution

Compass is a personal portfolio piece, but contributions are welcome via GitHub Issues:
- Spots where the scope description is inaccurate
- Situations you hit that this document doesn't cover but you think it should (or shouldn't)
- Blind spots in the division of labor with Sentinel

---

> **Remember**: Compass is not a panacea; it's a **tool that's precise in specific situations**. Use it in the right situation and it saves you 80% of deviation cost; use it in the wrong situation and it becomes process overhead. Read this document first, then decide whether to use it.
