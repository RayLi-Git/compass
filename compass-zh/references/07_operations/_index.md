# §7 Operations｜Migration / Rollback / Deployment

> PRD 落地的最後一哩：schema 怎麼安全升級、出事怎麼回退、上線前該檢查什麼。SOP 完全沒涵蓋這塊，是真實工作的高風險環節。

## 本章涵蓋（v0.5.0 / Phase 2 已交付）

- [§7.1 Migration](01_migration.md) — expand/contract 三階段、雙寫 backfill、零停機、前後相容窗口
- [§7.2 Rollback](02_rollback.md) — 部署前必備回退計畫、feature flag、blue-green/canary、migration-rollback 陷阱
- [§7.3 Deployment Checklist](03_deployment.md) — 上線前閘門（非 CI/CD 教學）+ 部署後驗證

## 何時載入

- schema / 資料模型要變更 → §7.1
- 規劃任何一次部署（必須先有 rollback 計畫）→ §7.2
- 上線前最後檢查 → §7.3

## 🔗 相關
- [§5.2 PRD 中途變更](../05_conflict_handling/02_prd_change.md) — PRD 變更常觸發 schema migration
- [§6.3 觀測性](../06_non_functional/03_observability.md) — 部署後靠黃金訊號驗證
- 撤退路線是 Sentinel 三條安全網之一，Compass 在 rollback 沿用
