# §2 Definition of Ready｜The pre-flight PRD health check

> DoD guards "is it done?", DoR guards "is this spec ready to start?". They are duals: DoR at the entrance, DoD at the exit.

## Covered in this chapter (v0.5.0 / Phase 2 shipped)

- [§2.1 DoR implementability health-check checklist](01_dor_checklist.md) — per-endpoint / per-table / auth ownership / NFR / boundaries / acceptance-criteria health-check checklist, three-tier quick-check vs full check
- [§2.2 PRD health report and failed-check handling](02_prd_health_report.md) — health-report format + go/no-go decision tree for imperfect PRDs (healthy / minor gaps so start with assumptions flagged / has a blocker so send back)

## When to load

- Got a new PRD / spec, before starting work
- Taking over a PRD block, unsure whether it's written clearly enough

## 🔗 Related
- [§4.1 Definition of Done](../04_quality_gates/01_dod.md) — DoR's dual gate
- [§5 Conflict Handling](../05_conflict_handling/_index.md) — gaps/ambiguities caught by DoR get handled here
- [§6 NFR](../06_non_functional/_index.md) — DoR checks whether the PRD wrote NFRs at all
