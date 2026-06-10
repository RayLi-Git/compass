<!-- LANG SWITCH -->

[English](./SCOPE.md) | **繁體中文**

# Compass 範圍邊界 (Scope)

> 一個 skill 的價值不只在「它能做什麼」，更在「它清楚說自己不做什麼」。本文件明確列出 Compass 的涵蓋邊界，避免使用者誤用或期待錯位。

---

## ✅ Compass 涵蓋的情境

### 適用情境

- **有 PRD / 規格 / API spec 的實作工作**——產品需求文件、Design Doc、OpenAPI spec、規格書、技術提案
- **Greenfield**——全新專案，從零依 PRD 蓋
- **Brownfield**——既有 codebase 加功能、修 bug、重構（§8 專門處理，已交付）
- **單一 AI + 單一使用者協作**——主流情境
- **多 stakeholder 協作**——§9 涵蓋「誰決定什麼」的路由（🚧 Phase 3）
- **任何後端 / 前端語言**——範例會用 FastAPI / TypeScript，但原則語言中立
- **長期專案**（多 session、跨日跨週）——中斷恢復協議（見 [§3.2 追蹤文件](../references/03_implementation/02_tracking_docs.md)）

### 涵蓋的決策類型

> 📍 標 🚧 者為後續 Phase 才交付的章節，目前僅在路線圖中；未標者已可用。

- 拿到 PRD 後如何吸收（§3.1，已交付）
- PRD 寫得不清楚怎辦（§5.1.1，已交付）
- PRD 寫錯了怎辦（§5.1.2，已交付）
- PRD 沒寫但實作更好怎辦（§5.1.3，已交付）
- PRD 中途升版怎辦（§5.2，已交付）
- PRD 跟其他文件衝突怎辦（§5.3，已交付）
- 多 PRD 之間有依賴怎辦（§5.4，已交付）
- 效能 / 觀測性 / 安全 / a11y 規格怎麼落地（§6，已交付）
- 上線前的 migration plan 怎排（§7.1，已交付）
- 出事後的 rollback 怎做（§7.2，已交付）
- 加功能到既有 codebase 怎開始（§8.4，已交付）
- 沒有正式 PRD 但需要紀律時的最小做法（§8.5，已交付）
- AI session 之間怎麼交接（§9，🚧 Phase 3）

---

## ❌ Compass 不涵蓋的情境

明確不在範圍內，避免誤用：

### 不涵蓋的工作類型

- **PRD 撰寫本身**——Compass 假設 PRD 已存在。如何「寫一份好 PRD」是另一個 skill 的範疇
- **產品探索 / 使用者研究**——這發生在 PRD 寫之前。Compass 從 PRD 已 ready 算起
- **專案管理（Jira / 排程 / 資源規劃）**——Compass 是**實作紀律**，不是 PM 工具
- **純探索性原型**——還沒成 spec、邊做邊想的階段，請用 [Sentinel](https://github.com/RayLi-Git/sentinel) 思考 OS 即可
- **純改文案 / 樣式 / typo**——這種輕量任務不需要 PRD 紀律
- **無設計目標的自由發揮**——Compass 假設你有要達成的東西（spec / goal）

### 不涵蓋的工程主題

- **Design Patterns / 演算法選擇**——這是工程基本功，不是 PRD 紀律問題
- **語言特定最佳實踐**（Pythonic / Idiomatic Go）——Compass 是語言中立的
- **DevOps / CI/CD pipeline 設計**——Compass 提到 deployment（§7.3）但不教 CI/CD
- **架構決策（單體 vs 微服務）**——PRD 應已決定，Compass 確保照做
- **思考方式 / 認知偏誤**——這是 [Sentinel](https://github.com/RayLi-Git/sentinel) 的範圍

---

## 🤝 跟 Sentinel 的分工

Compass 跟 Sentinel 是**配對 skill**，職責互補：

| 維度 | Sentinel | Compass |
|---|---|---|
| 主要看 | 你的「**思考**」 | 你跟「**PRD**」的關係 |
| 核心信念 | 不要在淺層打轉、症狀不是根因 | PRD 是合約、完成就是完成 |
| 觸發核心問題 | 「我有想清楚嗎？」 | 「我有照 PRD 走嗎？」 |
| 關鍵動作 | 動手前協定、五階段、根因樹 | DoR、追蹤文件、PRD 衝突處置、工具強制 |
| 適用範圍 | 任何工程任務 | 有 PRD 或目標規格的任務 |
| 病歷貢獻 | 思考誤判 / 根因跨層案例 | PRD 偏差 / 規格 bug / 設計取捨 |

### 一起用的典型情境

1. **拿到 PRD 動工**：先 Sentinel「動手前協定」想清楚 → 再 Compass §2 DoR + §3 開工
2. **實作中卡關**：Sentinel 診斷階段抓根因；若根因是「PRD 沒寫到」，轉 Compass §5
3. **既有 codebase 加大功能**：Compass §8 brownfield 流程 + Sentinel 動手前協定
4. **上線前**：Compass §4 + §7 跑完整檢查；Sentinel 三條安全網（rollback 計畫）

---

## 🗺️ 開發路線圖（versioning roadmap）

Compass 是迭代開發的。**目前在 v0.5.0 階段**（Phase 1+2 完成：§1–§8、§11 有內容）。

### 進度

| Phase | 內容 | 狀態 | 對應版本 |
|---|---|---|---|
| 0 | 架構決定、命名、SKILL.md skeleton、SCOPE | ✅ 完成 | v0.1.0-skeleton |
| 1 | 既有 SOP 移植（§1 原則、§3 實作、§4.1 DoD、§5.1 衝突、§11 工具）| ✅ 完成 | v0.2.0 |
| 2 | Critical 缺口（§2 DoR、§5.2-5.4 動態衝突、§6 NFR、§7 Operations、§8 Brownfield）| ✅ 完成 | v0.5.0 |
| 3 | Nice-to-have（§9 Collaboration、§10 Testing Strategy、§4 補 code review）| ⏸ 待開始 | v0.8.0 |
| 4 | 工具範例 & 拋光（M-007/8/10 通用骨架、SLA 專章、交叉引用對齊）| ⏸ 待開始 | v0.9.0 |
| 5 | 精簡 SKILL.md 最終版 + DESIGN/INSTALL + 中英雙語化 | ⏸ 待開始 | v1.0.0-rc |
| 6 | 上架 GitHub、ship | ⏸ 待開始 | v1.0.0 |

每階段完成都會 tag 對應版本，並更新本文件「進度」表。

### 未來可能延伸（非保證）

- **多 PRD 模板**：除了單純文字 PRD，加入「OpenAPI spec → checklist 自動展開」「ERD → schema audit」等模板
- **跨 repo 工具**：scripts/ 裡的通用腳本如果成熟，獨立成 PyPI / npm package
- **更多語言範例**：目前以 Python/FastAPI + TypeScript/React 為主，未來可加 Go / Rust / Ruby

---

## 📐 設計取捨

Compass 在設計時刻意做的取捨，記在這裡：

### 1. 偏「重型紀律」而非「輕量提示」

Compass 假設使用者願意花時間建立追蹤文件、跑 audit、寫 checklist。**它不是「輕量提醒型」工具**——如果你想要輕量，請用 Sentinel。

### 2. 偏「機械化強制」而非「靠紀律」

來自 SOP §14 的核心洞見：「靠紀律有限，靠工具強制更可靠」。Compass 大量推薦「用 exit code 擋」「用 git hook 擋」「用 TodoWrite 擋」。

### 3. 偏「PRD 為主」而非「敏捷實驗為主」

Compass 跟 Lean Startup / 快速 MVP 文化**有張力**。我們不是反對它們，是說「**當你決定要照 PRD 走時，就照 PRD 走完**」。

> 一句話：「**PRD 不是 Compass 的敵人，PRD 中途改才是。**」（[§5.2](../references/05_conflict_handling/02_prd_change.md) 處理這個問題）

### 4. 不假設有完美 PRD

§1 Definition of Ready 就是承認「真實 PRD 常常不完美」——所以開工前要先檢查 PRD 本身，而不是盲信。

---

## 💬 反饋與貢獻

Compass 是個人作品集，但歡迎透過 GitHub Issues 提出：
- 找到 scope 描述不準的地方
- 你遇到的情境本文件沒涵蓋、但你覺得應該涵蓋（或不涵蓋）
- 跟 Sentinel 分工的盲點

---

> **記住**：Compass 不是萬靈丹，是一把**特定情境下精準的工具**。用對情境，它幫你省下 80% 的偏差成本；用錯情境，它會變成程序負擔。先讀本文件，再決定要不要用。
