# §8 Brownfield｜Working in an existing codebase

> SOP lists brownfield / bug fix as "not applicable" — but most real work is brownfield. Compass fills this gap. Core: existing code is a second source of truth beyond the PRD, and you must reverse-understand it before touching it.

## What this chapter covers (delivered in v0.5.0 / Phase 2)

- [§8.1 Brownfield overview](01_overview.md) — existing code as second source of truth, risk asymmetry, sub-workflow map
- [§8.2 Bug Fix Workflow](02_bug_fix.md) — reproduce first, root cause not symptom, characterization test, bug vs spec mismatch
- [§8.3 Refactor Workflow](03_refactor.md) — change structure not behavior, green before and after, small-step commits, refactor vs rewrite
- [§8.4 Adding a feature to an existing codebase](04_add_feature.md) — reverse-understand first, blast radius analysis, integration points and backward compatibility
- [§8.5 Minimum discipline when there's no formal PRD](05_no_prd.md) — write a 3-line mini-spec, when to insist on a PRD

## When to load

- Fixing a bug → §8.2
- Refactoring existing code → §8.3
- Adding a feature to an existing project → §8.4
- Scattered requirements with no formal PRD → §8.5

## 🔗 Related
- [§2 Definition of Ready](../02_definition_of_ready/_index.md) — brownfield feature-adds still run DoR
- [§5.3 Cross-document conflict](../05_conflict_handling/03_cross_document.md) — when existing code and PRD conflict, handle it as a "document"
- Pre-flight protocol, diagnosis, and root-cause trees are all Sentinel concepts, heavily reused in brownfield
