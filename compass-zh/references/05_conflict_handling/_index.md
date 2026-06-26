# §5 Conflict Handling｜PRD 衝突處置

> 當 PRD 與現實對不上時，把衝突分流到不同的處置軌道——避免你在不該停的地方停、或在該停的地方硬幹。

## 本章涵蓋

### 已交付（v0.2.0 / Phase 1）— 靜態 PRD 三類
- [§5.1 PRD 模糊 / Bug / 缺漏：三類處置](01_vague_bug_gap.md)
  - §5.1.1 模糊（任一解讀都能做 → 不停手，採具體一方）
  - §5.1.2 Bug（任一解讀都做不出來 → 停手等裁決）
  - §5.1.3 缺漏 + 實作更好（保留 + 標記 + 等裁決，6 閘門檢查）
  - §5.1.4 三類處置分工速查表

### 已交付（v0.5.0 / Phase 2）— 動態衝突
- [§5.2 PRD 中途變更](02_prd_change.md)（寫到一半 PRD 升版，五步變更協定 + 影響分析）
- [§5.3 跨文件衝突](03_cross_document.md)（PRD vs ADR vs API contract vs ERD，按「誰的領域」裁定優先序）
- [§5.4 多 PRD 依賴](04_multi_prd.md)（多子 PRD 的依賴排序與共享契約一致性）

## 何時載入

- 實作中發現「PRD 寫得不清楚 / 自相矛盾 / 漏了什麼」→ §5.1
- PRD 中途升版 → §5.2（Phase 2）
- PRD 跟其他設計文件衝突 → §5.3（Phase 2）

## 🔗 相關
- [§1 核心原則](../01_foundations/01_principles.md) — 第 5/6/7/8 誡對應本章三類處置與 YAGNI 兜底
- [§3.5 YAGNI](../03_implementation/05_yagni.md) — 「PRD 沒寫也沒必要」走 YAGNI，與 §5.1.3「缺漏優化」互為一體兩面
