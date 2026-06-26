# §7.1 Migration: schema and data changes

> Part of [Compass](../../SKILL.md) §7 — Operations.
> Safe procedure for schema and data changes: always backward-compatible first, split "stop writing" and "delete" into two separate deploys.

---

## 🎯 Core iron rules

> **Migration is not "change the schema" — it's "change the schema while old code is still running".**

Deploys are not atomic. New and old versions of the code connect to the **same database** at the same time — during a rolling deploy, during canary, and most acutely at the instant of a rollback. Any schema change that "only new code understands" will blow up old code (or the old code you roll back to) on the spot.

Four rules you cannot violate:

1. **On every deploy, both new and old code must be able to read and write the current schema** (forward/backward compatibility window).
2. **Schema changes and read/write switchovers must be split across multiple deploys** — never crammed into one.
3. **Never drop a column in the same deploy that "stops writing" it** — deletion comes at least one deploy later.
4. **Backfill must be re-runnable and resumable after interruption** — never assume it finishes in one pass.

---

## 📐 Expand / Contract

Incompatible changes are split into "expand → migrate → contract", three phases, each an **independent deploy**, and at the end of each phase the system is in a rollback-safe compatible state.

| Phase | Action | Compatibility guarantee |
|---|---|---|
| **Expand** | Add new structure (nullable columns / new tables / new indexes), **don't drop or change anything old** | Old code is completely unaffected |
| **Migrate** | Backfill old data; dual-write (write both old and new columns); gradually shift reads to the new column | Both new and old code work |
| **Contract** | Only after confirming no one reads or writes the old column, drop it | Executed only after old code is fully decommissioned |

### Example: split `users.name` into `first_name` / `last_name`

```text
Deploy 1 (Expand)   ── Add two nullable columns first_name, last_name
                       Old code still reads/writes name, unaffected

Deploy 2 (Migrate)  ── Code changed to "write name + first/last together" (dual-write)
                    ── Background backfill: split existing name into first/last (batched, idempotent)

Deploy 3 (cut reads)── Code reads from first/last, name is write-only

Deploy 4 (Contract) ── After confirming name has no reads/writes, drop column name
```

Four deploys, and you can safely stop and safely roll back between each one. **Rushing to merge them into two = asking for downtime.**

---

## 🔁 Backfill strategy

Backfilling existing data is the most explosive part of a migration: a single `UPDATE ... WHERE ...` scanning the whole table locks the table, blows out replication lag, and loses all progress if the connection drops halfway.

Backfill must have three properties:

- **Batched**: cap each batch to a fixed row count (e.g. 1000 rows), with gaps between batches so the replica can catch up; don't scan the whole table in one SQL statement.
- **Idempotent**: re-running the same batch doesn't corrupt data. Rely on conditions like `WHERE new_col IS NULL` to naturally skip already-processed rows, not on external "how far did I get" state.
- **Resumable**: advance with a stable cursor (primary-key range); after an interruption, resume from the last cursor rather than starting over.

```text
Example (the shape of a batched idempotent backfill, not actual commands):
  last_id = 0
  loop:
    rows = SELECT id, name FROM users
           WHERE id > last_id AND first_name IS NULL   ← idempotent condition
           ORDER BY id LIMIT 1000                       ← batched
    if rows empty: break
    for r in rows: UPDATE ... WHERE id = r.id
    last_id = rows[-1].id                               ← resumable cursor
    sleep(brief interval)                                ← let the replica breathe
```

Backfill checklist:

- [ ] Batch size is capped, with gaps between batches
- [ ] Condition inherently skips already-processed rows (safe to re-run)
- [ ] Cursor can be persisted, can resume after interruption
- [ ] Monitor replication lag / lock waits, can pause on anomaly
- [ ] "New writes" during backfill are handled by dual-write, not dependent on backfill to fill in

---

## ⏱️ Zero-downtime principles

- **New columns are always nullable or carry a default first**: adding a `NOT NULL` column with no default makes old code's INSERTs fail outright. Make it nullable first; only add the constraint as the last step, after backfill completes and dual-write is stable.
- **Add indexes non-blockingly**: build indexes on large tables online / concurrently (e.g. PostgreSQL `CREATE INDEX CONCURRENTLY`), don't lock the whole table inside a transaction.
- **Changing a column type = expand/contract**: don't `ALTER COLUMN` to change the type directly. Add a new column, dual-write, backfill, cut reads, drop the old column.
- **Rename equals drop + add**: a rename makes old code lose the column instantly. Treat it as expand/contract.
- **Decouple destructive DDL (drop/rename) on large data from backfill**: DDL goes through a deploy, backfill goes through a background task, neither blocks the other.

---

## 🪟 Forward/backward compatibility window

The "window" = the span from when a change ships to when old code is fully decommissioned, during which **new and old versions coexist**. If either side fails within the window, that's a production incident.

| What you want to do | Must guarantee within the window |
|---|---|
| Add a column | Old code that doesn't write it can still INSERT normally (hence nullable / default) |
| Change a read source | The new column has been filled by dual-write before reads are cut over, otherwise you read NULL |
| Drop a column | Confirm **no** still-running version reads or writes it |
| Rollback | The old version you roll back to still runs correctly on the new schema |

> When designing each step, ask yourself: "If we **roll back** at this instant, will old code blow up on the **new schema**?" If yes → this step isn't split finely enough.

---

## ⛔ "Stop-writing and delete in different deploys" rule

The most common, most fatal shortcut: in the same deploy, "code no longer writes X" + "DDL drop X".

Why it blows up:

- Deploys aren't atomic. The drop has taken effect, but old instances are still writing X → write failures.
- Once you need to roll back, the old code you roll back to still has to write/read X, but X is gone → rollback is a disaster.

Correct order: **first deploy the code that "stops reading/writing X" and run it stably (observe for one window) → only on the next deploy do you drop X.** A drop is always the last, independent action, taken only after old code is confirmed not to depend on it.

---

## 🧪 Migration testing

A migration script is itself code; an untested migration is an unverified production change.

- [ ] **Run up on a database replica**: with data volume and distribution close to production, not an empty table.
- [ ] **Run down (rollback script)**: every migration needs a corresponding down, and actually verify on a replica that it returns to the pre-change state.
- [ ] **up → down → up round-trip**: confirm it's reversible and idempotent, and doesn't explode on the second up.
- [ ] **Measure duration and locks**: estimate lock time and total duration on a replica; if it exceeds the acceptable window → switch to batched / online DDL.
- [ ] **Backfill interrupt-and-restart test**: deliberately kill it midway, confirm resume doesn't duplicate or skip.
- [ ] **Cross-test new and old code**: old code against new schema, new code against old schema; at least one must hold within the window.

> Evidence grading (Sentinel's evidence grading): before claiming "the migration is safe", tag a level. Actually ran up+down on a replica = 🟢; only read the SQL without running = 🟡, explicitly recommend verifying on a replica first.

---

## 🔗 Relationship with §5.2 PRD changes

PRD changes very commonly trigger schema changes: new columns, changed relations, dropping obsolete columns. The flow is reconcile first, migrate second:

1. A PRD change first goes through blast-radius assessment per [§5.2](../05_conflict_handling/02_prd_change.md), don't touch the schema directly.
2. The schema differences the assessment surfaces are **always landed via expand/contract**, not a direct `ALTER` / `DROP` just because "the PRD says change it to this".
3. If a destructive change (drop/rename) isn't explicitly required by the PRD to preserve a compatibility window, treat it as a [§5.1](../05_conflict_handling/01_vague_bug_gap.md) gap — record it and add the compatibility steps, don't unilaterally cut it cleanly.

---

## 🔗 Related Compass sections

- [§7.2 Rollback](./02_rollback.md) — rollback and compatible-fallback strategy when a migration fails
- [§5.2 PRD change](../05_conflict_handling/02_prd_change.md) — the upstream trigger for schema changes
- [§4.1 Definition of Done](../04_quality_gates/01_dod.md) — a migration counts as done only after up+down are tested
- [§7 Operations](./_index.md) — overview of this module

---

## 📝 Status

`v0.5.0` (Phase 2: original content)
