# §4 Quality Gates｜acceptance / self-review / tool enforcement

> Defines what "done" actually means — the hard checks a slice of work must pass and how self / peer / AI review divides the labor — so quality is enforced by gates, not by hope.

## This chapter covers

- [01_dod.md](01_dod.md) — Definition of Done: the mandatory vs. recommended checks for "truly done" and the iron rule when one is skipped.
- [02_code_review.md](02_code_review.md) — Code review across three modes (self / peer / AI): who reviews what, what a good review looks for, and the trust boundary on AI review.

## When to load

- A slice of work feels "finished" and you need to confirm it actually clears the bar before committing or handing off.
- You're about to do (or request) a self-review, peer review, or AI-assisted review and want to scope what each should catch.
- You want quality enforced by tool-checked gates rather than by discipline alone.

## 🔗 Related
- [../03_implementation/_index.md](../03_implementation/_index.md) — the implement → compare → fix loop that feeds work into these gates.
- [../11_tooling/_index.md](../11_tooling/_index.md) — wiring DoD checks to exit codes so gates fail hard instead of relying on memory.
- [../05_conflict_handling/_index.md](../05_conflict_handling/_index.md) — handling spec conflicts surfaced during review.
