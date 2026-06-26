# §8 Brownfield｜既有 codebase 工作

> SOP 把 brownfield / bug fix 列為「不適用」——但大部分真實工作就是 brownfield。Compass 補上這個缺口。核心：既有 code 是 PRD 之外的第二個事實來源，動它之前必須先逆向理解。

## 本章涵蓋（v0.5.0 / Phase 2 已交付）

- [§8.1 Brownfield 總覽](01_overview.md) — 既有 code 是第二事實來源、風險不對稱、子流程地圖
- [§8.2 Bug Fix Workflow](02_bug_fix.md) — 先重現、根因非症狀、characterization test、bug vs spec 不符
- [§8.3 Refactor Workflow](03_refactor.md) — 改結構不改行為、前後綠燈、小步提交、refactor vs rewrite
- [§8.4 加功能到既有 codebase](04_add_feature.md) — 先逆向理解、影響範圍分析、整合點與向後相容
- [§8.5 無正式 PRD 時的最小紀律](05_no_prd.md) — 寫 3 行 mini-spec、何時堅持要 PRD

## 何時載入

- 修 bug → §8.2
- 重構既有 code → §8.3
- 加功能到既有專案 → §8.4
- 沒有正式 PRD 的零散需求 → §8.5

## 🔗 相關
- [§2 Definition of Ready](../02_definition_of_ready/_index.md) — brownfield 加功能仍要跑 DoR
- [§5.3 跨文件衝突](../05_conflict_handling/03_cross_document.md) — 既有 code 與 PRD 衝突時當「文件」處置
- 動手前協定、診斷、根因樹皆為 Sentinel 概念，brownfield 大量沿用
