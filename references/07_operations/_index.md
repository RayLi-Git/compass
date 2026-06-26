# §7 Operations｜Migration / Rollback / Deployment

> The last mile of landing a PRD: how to safely upgrade schema, how to roll back when things break, what to check before going live. The SOP doesn't cover this at all — it's the high-risk part of real work.

## Covered in this chapter (delivered in v0.5.0 / Phase 2)

- [§7.1 Migration](01_migration.md) — expand/contract three-phase, dual-write backfill, zero-downtime, forward/backward compatibility window
- [§7.2 Rollback](02_rollback.md) — mandatory rollback plan before deploy, feature flag, blue-green/canary, migration-rollback pitfalls
- [§7.3 Deployment Checklist](03_deployment.md) — pre-launch gates (not a CI/CD tutorial) + post-deploy verification

## When to load

- schema / data model is changing → §7.1
- planning any deploy (must have a rollback plan first) → §7.2
- final check before going live → §7.3

## 🔗 Related
- [§5.2 PRD change mid-flight](../05_conflict_handling/02_prd_change.md) — PRD changes often trigger schema migration
- [§6.3 Observability](../06_non_functional/03_observability.md) — verify after deploy via golden signals
- The retreat route is one of Sentinel's three safety nets; Compass reuses it for rollback
