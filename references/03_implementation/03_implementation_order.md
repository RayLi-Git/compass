# §3.3 Implementation Order and Dependencies

> Part of [Compass](../../SKILL.md) §3 — Implementation.
> One general principle + one example order table to help you decide "which to write first, which later" when landing a PRD, while holding the discipline of safety-critical modules and dependency version-locking.

---

## 1. General Principle: Bottom-Up

> **Infrastructure → Security Core → Business Logic → Integration → Frontend → Supplements**

This principle is universal across languages, frameworks, and domains. Its logic:

- **Infrastructure first**: directory structure, package management, environment variables, startup scripts — if these aren't stabilized first, every later change ripples globally.
- **Security core next**: auth, authorization, sensitive-data detection — modules like these almost never get fully covered if you bolt on tests afterward; write them **test-first**.
- **Business logic then**: core services / domain logic operating inside the safety net.
- **Integration layer**: API routes / endpoints / controllers expose business logic externally.
- **Frontend last**: UI / templates / frontend interactions built on top of an already-stable API.
- **Supplements to wrap up**: scripts, supplemental tests, docs.

**Why going in reverse blows up**: build a UI demo to show first, and when you come back to add auth you'll find the permission model conflicts with assumptions already hardcoded into the UI; build the endpoint first then add PII detection, and the PII has usually already leaked into logs or responses.

---

## 2. Example: Typical Web App Order

The following is a reference order for a common web application — **for reference only, not mandatory**. If your project is a CLI tool, batch job, mobile app, or ML pipeline, the order will differ — but the skeleton "infrastructure → security → business → integration → frontend → supplements" still holds.

| Order | Module | Test Strategy |
|---|---|---|
| 1 | Directory structure / package management / env vars / containers / startup scripts | smoke |
| 2 | Config loading / database init / migration | smoke |
| 3 | **Authentication (login / JWT / password hashing / 2FA)** | **test-first** ⚠ |
| 4 | **Authorization / roles and permission boundaries** | **test-first** ⚠ |
| 5 | **Sensitive-data detection (PII isolation iron rule)** | **test-first** ⚠ |
| 6 | Services / Domain logic (core business) | write tests in step |
| 7 | External modules (providers / processors / third-party SDKs) | use fake / mock provider |
| 8 | Routes / API endpoints | write tests in step |
| 9 | Main-program integration + startup validation | smoke |
| 10 | Frontend (HTML / template / frontend interaction / CSP) | manual verification |
| 11 | Initial data / system files / seeds | smoke |
| 12 | Scripts (init / ingest / backup / ops tools) | add tests afterward |
| 13 | Fill in remaining tests | — |
| 14 | Docs (CLAUDE.md / ARCHITECTURE.md / CHANGELOG.md) | — |

> ⚠ Rows marked **test-first** are **safety-critical modules** — bolt tests on afterward and they mostly won't be fully covered. See next section.

---

## 3. Safety-Critical Modules: test-first, No Compromise

"Security core" isn't a concept exclusive to some language or framework — it's any module that, **once broken, causes data leakage, privilege escalation, or unrecoverable damage**. These modules must have tests written first, implementation second.

**General criteria**:

- Once breached, can an attacker get someone else's data? → security module
- Once breached, can a user do things beyond their permissions? → security module
- Once breached, does sensitive data land in log / response / a third party? → security module
- Once breached, is it unrecoverable from backup afterward (e.g. key leakage)? → security module

**Example scenarios** (illustrative only; not every project looks like this):

- *A web app's login flow (JWT issuance, password hashing, 2FA, step-up)*
- *Roles and permission system (admin / user / guest escalation-demotion boundaries, IDOR protection)*
- *PII / sensitive-data detection (detect and filter before entering logs, returning responses, or sending to third parties)*
- *Payment / quota / balance-related charging and reconciliation logic*
- *Generation, storage, and rotation of encryption keys*

For these modules, **write tests first** — and the tests must include "how a bad actor would use it" negative cases, not just the happy path.

> Dev-environment fake / mock strategy, and secret-management flow, change with your runtime environment; document them clearly in the project-level runbook.

---

## 4. Implementation Rules

Discipline to hold for each slice as it lands:

- **Save each file as soon as it's done** — don't accumulate unsaved batched changes
- **`git commit` as soon as each module is done**, suggested message format: `[PRD §X.Y] module: brief description`
- **Don't fabricate features not present in the PRD** (YAGNI)
- **Don't introduce packages not specified in the PRD dependency section** — if you find during implementation that one is genuinely required, go through the PRD gap flow in [§5 Conflict Handling](../05_conflict_handling/_index.md); don't add it on your own authority
- **Preserve the PRD's original wording** (Chinese paths, glossary terms, domain language) — don't rename on your own authority
- **self-review after each module is done**: re-read as if you were the code reviewer, checking especially:
  - Any fabricated fields / endpoints
  - Any PRD "do it tomorrow" hardcoded straight into "never do it"
  - Any try/except masking an error that should propagate upward

**Definition of "done"**: done means done, no half-finished work; ship in small slices, but no half-finished phasing. Don't carve into V1/V2/V3, don't leave TODOs to revisit.

---

## 5. Dependency Version-Locking

The moment order-table item 1 (package management) is done, **lock versions immediately** — this is the first anchor that nails "reproducible environment" into the repo.

**General practice**: use your language's dependency-lock mechanism (lockfile) to freeze the current dependency versions, and commit it into the repo.

**Common mappings**:

| Language Ecosystem | Lock Mechanism (examples) |
|---|---|
| Python | `pip freeze` / `uv lock` / `poetry lock` / `pipenv lock` |
| Node.js | `package-lock.json` / `yarn.lock` / `pnpm-lock.yaml` |
| Ruby | `Gemfile.lock` |
| Rust | `Cargo.lock` |
| Go | `go.sum` |
| PHP | `composer.lock` |

**Discipline thereafter**:

- Add any dependency → re-lock → commit lockfile
- Don't edit the lockfile directly
- CI / deployment environments always install from the lockfile, never grab latest from upstream

**Why this anchor needs to be this early**: once dependency versions drift, later debugging gains an extra "environment difference" variable, and the root-cause tree becomes hard to draw. Lock it down at the earliest point and every later problem can rule out "is it a different package version".

---

## 6. Judgment When Order Is Deviated From

If you must deviate from this order (e.g. a stakeholder is rushing to see a UI demo), at least hold:

1. **Security core still test-first** — even if the UI goes first, write the auth/permission/PII tests first
2. **Mark the deviated parts `⚠️inferred` or TODO**, and write them into the "in progress" section of `.claude/progress.md`
3. **When you come back to fill in, trace the module's dependencies back from the order table** — don't fill in one piece and assume it's stable

---

## 🔗 Related Compass sections
- [§3.1 PRD Intake](01_prd_intake.md) — upstream of the order table: turning the PRD into a checklist
- [§3.4 Compare-Fix Loop](04_compare_fix_loop.md) — comparison and acceptance after each slice is done
- [§4.1 Definition of Done](../04_quality_gates/01_dod.md) — acceptance conditions for each slice
- [§5 Conflict Handling](../05_conflict_handling/_index.md) — handling when PRD is vague / a bug / a gap

## 📝 Status
v0.2.0 (Phase 1: ported from prior SOP, generalized and de-privatized).
