# §10 Testing Strategy

> Maps each PRD acceptance criterion to the right test layer, and decides where test-first earns its keep vs. where it's ritual — so coverage proves something instead of padding a number.

## This chapter covers

- [01_test_pyramid.md](01_test_pyramid.md) — Test pyramid and per-layer division of labor: which layer tests what, how many E2E is "enough," and how to map PRD acceptance criteria to unit/integration/E2E.
- [02_test_first_boundary.md](02_test_first_boundary.md) — The real boundary of test-first beyond Auth/PII, where it's overhead, and why coverage is a floor detector — not a proof of quality (incl. mutation testing).

## When to load

- Planning a test suite for a PRD and deciding which layer each acceptance criterion belongs to.
- Tempted to chase a global coverage percentage, or unsure whether to test-first a given module.
- CI is slow/flaky from too many E2E, or "the tests broke again, just rerun it" has become the team catchphrase.

## 🔗 Related
- [§4 Quality Gates](../04_quality_gates/_index.md) — source of mandatory test-first for Auth/PII and the DoD wrap-up gate.
- [§6 Non-Functional Requirements](../06_non_functional/_index.md) — performance/security test types that live outside the functional pyramid.
- [§8 Brownfield](../08_brownfield/_index.md) — characterization tests and red-test-first ordering for legacy code and bug fixes.
