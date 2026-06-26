# §0.1 範圍邊界｜Compass 涵蓋什麼 / 不涵蓋什麼

## ✅ Compass 涵蓋的情境

### 適用情境
- **有 PRD / 規格 / API spec 的實作工作**——產品需求文件、Design Doc、OpenAPI spec、規格書、技術提案
- **Greenfield**——全新專案，從零依 PRD 蓋
- **Brownfield**——既有 codebase 加功能、修 bug、重構（[§8](../08_brownfield/_index.md) 專門處理）
- **單一 AI + 單一使用者協作**——主流情境
- **多 stakeholder 協作**——[§9](../09_collaboration/_index.md) 涵蓋「誰決定什麼」的路由
- **任何後端 / 前端語言**——範例會用 FastAPI / TypeScript，但原則語言中立
- **長期專案**（多 session、跨日跨週）——中斷恢復協議見 [§3.2 追蹤文件](../03_implementation/02_tracking_docs.md)

### 涵蓋的決策類型
- 拿到 PRD 後如何吸收（[§3.1](../03_implementation/01_prd_intake.md)）
- PRD 模糊 / 寫錯 / 沒寫但實作更好怎辦（[§5.1](../05_conflict_handling/01_vague_bug_gap.md)）
- PRD 中途升版 / 跨文件衝突 / 多 PRD 依賴（[§5.2](../05_conflict_handling/02_prd_change.md)、[§5.3](../05_conflict_handling/03_cross_document.md)、[§5.4](../05_conflict_handling/04_multi_prd.md)）
- 效能 / 觀測性 / 安全 / a11y / SLA 規格怎麼落地（[§6](../06_non_functional/_index.md)）
- migration plan 怎排、rollback 怎做（[§7](../07_operations/_index.md)）
- 加功能到既有 codebase、沒有正式 PRD 但需要紀律時的最小做法（[§8.4](../08_brownfield/04_add_feature.md)、[§8.5](../08_brownfield/05_no_prd.md)）
- AI session 之間怎麼交接（[§9.3](../09_collaboration/03_session_handoff.md)）

---

## ❌ Compass 不涵蓋的情境

明確不在範圍內，避免誤用：

### 不涵蓋的工作類型
- **PRD 撰寫本身**——Compass 假設 PRD 已存在；如何「寫一份好 PRD」是 [Cartographer](https://github.com/RayLi-Git/cartographer) 的範疇
- **產品探索 / 使用者研究**——這發生在 PRD 寫之前；Compass 從 PRD 已 ready 算起
- **專案管理（Jira / 排程 / 資源規劃）**——Compass 是**實作紀律**，不是 PM 工具
- **純探索性原型**——還沒成 spec、邊做邊想的階段，請用 [Sentinel](https://github.com/RayLi-Git/sentinel) 即可
- **純改文案 / 樣式 / typo**——輕量任務不需要 PRD 紀律
- **無設計目標的自由發揮**——Compass 假設你有要達成的東西（spec / goal）

### 不涵蓋的工程主題
- **Design Patterns / 演算法選擇**——工程基本功，不是 PRD 紀律問題
- **語言特定最佳實踐**（Pythonic / Idiomatic Go）——Compass 語言中立
- **DevOps / CI/CD pipeline 設計**——Compass 提到 deployment（[§7.3](../07_operations/03_deployment.md)）但不教 CI/CD
- **架構決策（單體 vs 微服務）**——PRD 應已決定，Compass 確保照做
- **思考方式 / 認知偏誤**——這是 [Sentinel](https://github.com/RayLi-Git/sentinel) 的範圍

---

## 🤝 跟 Sentinel 的分工

Compass 是四件式工具鏈的中段（Cartographer 生 PRD → Compass 照圖走 → Sentinel 全程站哨 → [Lookout](https://github.com/RayLi-Git/lookout) 段落完成獨立審）；與 Sentinel 職責互補：

| 維度 | Sentinel | Compass |
|---|---|---|
| 主要看 | 你的「**思考**」 | 你跟「**PRD**」的關係 |
| 核心信念 | 不要在淺層打轉、症狀不是根因 | PRD 是合約、完成就是完成 |
| 觸發核心問題 | 「我有想清楚嗎？」 | 「我有照 PRD 走嗎？」 |
| 關鍵動作 | 動手前協定、五階段、根因樹 | DoR、追蹤文件、PRD 衝突處置、工具強制 |
| 適用範圍 | 任何工程任務 | 有 PRD 或目標規格的任務 |

### 一起用的典型情境
1. **拿到 PRD 動工**：先 Sentinel「動手前協定」想清楚 → 再 Compass [§2 DoR](../02_definition_of_ready/_index.md) + [§3 開工](../03_implementation/_index.md)
2. **實作中卡關**：Sentinel 診斷階段抓根因；若根因是「PRD 沒寫到」，轉 Compass [§5](../05_conflict_handling/_index.md)
3. **既有 codebase 加大功能**：Compass [§8 brownfield](../08_brownfield/_index.md) + Sentinel 動手前協定
4. **上線前**：Compass [§4](../04_quality_gates/_index.md) + [§7](../07_operations/_index.md) 跑完整檢查；Sentinel 三條安全網

---

## 🧭 一句話判準

> Compass 不是萬靈丹，是一把**特定情境下精準的工具**。
> **有 spec 要對齊 → Compass 主；只是想法、邊做邊想 → Sentinel 就好。**
> 用對情境，它幫你省下 80% 的偏差成本；用錯情境，它會變成程序負擔。

完整的設計取捨、未來方向與貢獻方式見 GitHub repo 的 [`docs/SCOPE.zh-TW.md`](https://github.com/RayLi-Git/compass/blob/main/docs/SCOPE.zh-TW.md)。
