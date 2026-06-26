# §6 Non-Functional Requirements (NFR)

> Most PRDs over-specify functionality and badly underestimate NFRs. The reverse-audit script only catches the feature list (endpoints/schema/pages); NFRs get missed wholesale — so NFRs must be caught at DoR.

## Covered in this chapter (v0.5.0 / Phase 2 delivered)

- [§6.1 NFR overview: why PRDs keep missing them](01_nfr_overview.md) — NFR taxonomy + an NFR health-check checklist to slot into DoR
- [§6.2 Landing performance specs](02_performance.md) — turn "make it fast" into measurable targets (p50/p95/p99, throughput, budget)
- [§6.3 Observability](03_observability.md) — log / metrics / tracing + the four golden signals
- [§6.4 Security: beyond test-first](04_security.md) — OWASP Top 10 mapping + a STRIDE-lite per-feature review gate
- [§6.5 Accessibility and i18n](05_accessibility_i18n.md) — landing a11y (WCAG) / i18n
- [§6.6 Availability and SLA](06_availability_sla.md) — SLA/SLO/error budget + dependency-failure behavior (timeout/retry/circuit breaker/fallback/degradation)

## When to load

- At DoR, check whether the PRD wrote any NFRs
- Implementing a feature, passing the security review gate (§6.4)
- Before launch, confirm observability is in place (§6.3)

## 🔗 Related
- [§2.1 DoR health-check checklist](../02_definition_of_ready/01_dor_checklist.md) — missing NFRs should be caught here
- [§4.1 DoD](../04_quality_gates/01_dod.md) — observability/security are part of the DoD for a production service
