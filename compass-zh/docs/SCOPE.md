[English](../../docs/SCOPE.md) | **繁體中文**

# 範圍邊界

> 一個 skill 的價值不只在「它能做什麼」，更在「它清楚說自己不做什麼」。本文件明文列出 Compass 的涵蓋邊界，避免使用者誤用或期待錯位。

---

## 涵蓋的情境

**Compass 適用：**

- **有 PRD / 規格 / API spec 的實作工作** — 產品需求文件、Design Doc、OpenAPI spec、規格書、技術提案。
- **Greenfield** — 全新專案，從零依 PRD 蓋。
- **Brownfield** — 既有 codebase 加功能、修 bug、重構（§8 專門處理）。
- **單一 AI + 單一使用者協作** — 主流情境。
- **多 stakeholder 協作** — §9 涵蓋「誰決定什麼」的路由。
- **任何後端 / 前端語言** — 範例會用 FastAPI / TypeScript，但原則語言中立。
- **長期專案**（多 session、跨日跨週） — 中斷恢復協議（見 [§3.2 追蹤文件](../references/03_implementation/02_tracking_docs.md)）。

**涵蓋的決策類型：**

| 當你遇到… | 模組 |
|---|---|
| 拿到 PRD 後如何吸收 | §3.1 |
| PRD 寫得不清楚 | §5.1.1 |
| PRD 寫錯了 | §5.1.2 |
| PRD 沒寫但實作更好 | §5.1.3 |
| PRD 中途升版 | §5.2 |
| PRD 跟其他文件衝突 | §5.3 |
| 多 PRD 之間有依賴 | §5.4 |
| 效能 / 觀測性 / 安全 / a11y 規格怎麼落地 | §6 |
| 上線前的 migration plan 怎排 | §7.1 |
| 出事後的 rollback 怎做 | §7.2 |
| 加功能到既有 codebase 怎開始 | §8.4 |
| 沒有正式 PRD 但需要紀律 | §8.5 |
| AI session 之間怎麼交接 | §9.3 |

---

## 不涵蓋的情境

明確不在範圍內，避免誤用。

**不涵蓋的工作類型：**

- **PRD 撰寫本身** — Compass 假設 PRD 已存在。把模糊想法逼成規格是 [Cartographer](https://github.com/RayLi-Git/cartographer) 的範疇。
- **產品探索 / 使用者研究** — 這發生在 PRD 寫之前。Compass 從 PRD 已 ready 算起。
- **專案管理**（Jira / 排程 / 資源規劃） — Compass 是**實作紀律**，不是 PM 工具。
- **純探索性原型** — 還沒成 spec、邊做邊想的階段，請用 [Sentinel](https://github.com/RayLi-Git/sentinel) 思考 OS。
- **純改文案 / 樣式 / typo** — 這種輕量任務不需要 PRD 紀律。
- **無設計目標的自由發揮** — Compass 假設你有要達成的東西（spec / goal）。

**不涵蓋的工程主題：**

- **Design Patterns / 演算法選擇** — 這是工程基本功，不是 PRD 紀律問題。
- **語言特定最佳實踐**（Pythonic / Idiomatic Go） — Compass 是語言中立的。
- **DevOps / CI/CD pipeline 設計** — Compass 提到 deployment（§7.3）但不教 CI/CD。
- **架構決策**（單體 vs 微服務） — PRD 應已決定，Compass 確保照做。
- **思考方式 / 認知偏誤** — 這是 [Sentinel](https://github.com/RayLi-Git/sentinel) 的範圍。

---

## 邊界與常見誤解

以下邊界是刻意畫下的，不是缺漏。目前的 Compass（§1–§11 全模組 + 可執行工具腳本 + 中英雙語）已完整且可用。

- **「它是輕量提醒。」** 不是——Compass 偏重型紀律：它假設你願意花時間建追蹤文件、跑 audit、寫 checklist。輕量情境用 Sentinel。這是刻意取捨，不是侷限。
- **「它對任何技術棧開箱即用。」** *原則*語言中立，但可執行範例以 Python/FastAPI + TypeScript/React 為主。其他技術棧需自行改寫腳本的 regex。
- **「它能直接吃我的 OpenAPI / ERD。」** 目前以「一份文字 PRD」為主軸；OpenAPI / ERD 等結構化規格仍靠人轉成 checklist。（一個可能的未來方向，非保證：結構化規格自動轉換，讓 §2 DoR / §11 反向稽核能直接吃。）
- **「它跟敏捷對著幹。」** 它跟快速 MVP 文化*有張力*，不是對立。立場是「當你決定要照 PRD 走時，就照 PRD 走完」——*PRD 不是 Compass 的敵人，PRD 中途改才是*（[§5.2](../references/05_conflict_handling/02_prd_change.md) 處理這個問題）。
- **「它假設有完美 PRD。」** 恰恰相反——DoR 存在，正是因為真實 PRD 常常不完美，所以開工前要先檢查 PRD 本身，而不是盲信。

---

## 工具鏈分工

Compass 是四件式工具鏈裡的**照規格施工**段——每一件盯不同的事：

| Skill | 角色 | 盯什麼 |
|---|---|---|
| [Cartographer](https://github.com/RayLi-Git/cartographer) | 畫地圖 | 把模糊想法逼成一份扎實的 PRD |
| **Compass** | 照圖走 | 你有照 PRD 走嗎？（照規格蓋、不偏航） |
| [Sentinel](https://github.com/RayLi-Git/sentinel) | 站哨 | 你怎麼想（淺層 vs 深層、症狀 vs 根因） |
| [Lookout](https://github.com/RayLi-Git/lookout) | 在桅杆瞭望 | 獨立 context 的 code review |

**Cartographer 畫地圖 → Compass 照圖走 → Sentinel 站哨 → Lookout 瞭望。**

Compass 與 Sentinel 是最緊密的一對——在同一個任務上職責互補：

| 維度 | Sentinel | Compass |
|---|---|---|
| 主要看 | 你的「**思考**」 | 你跟「**PRD**」的關係 |
| 核心信念 | 不要在淺層打轉、症狀不是根因 | PRD 是合約、完成就是完成 |
| 觸發核心問題 | 「我有想清楚嗎？」 | 「我有照 PRD 走嗎？」 |
| 關鍵動作 | 動手前協定、五階段、根因樹 | DoR、追蹤文件、PRD 衝突處置、工具強制 |
| 適用範圍 | 任何工程任務 | 有 PRD 或目標規格的任務 |

**一起用的典型情境：**

1. **拿到 PRD 動工**：先用 Sentinel「動手前協定」想清楚 → 再 Compass §2 DoR + §3 開工。
2. **實作中卡關**：Sentinel 診斷階段抓根因；若根因是「PRD 沒寫到」，轉 Compass §5。
3. **既有 codebase 加大功能**：Compass §8 brownfield 流程 + Sentinel 動手前協定。
4. **上線前**：Compass §4 + §7 跑完整檢查；Sentinel 三條安全網（rollback 計畫）。段落完成後，由 [Lookout](https://github.com/RayLi-Git/lookout) 做獨立 context 審查。

---

## 反饋與貢獻

Compass 是個人作品集，但歡迎透過 GitHub Issues 提出：

- 找到 scope 描述不準的地方。
- 你遇到的情境本文件沒涵蓋、但你覺得應該涵蓋（或不涵蓋）。
- 整條工具鏈分工的盲點。

---

> **記住**：Compass 不是萬靈丹，是一把**特定情境下精準的工具**。用對情境，它幫你省下 80% 的偏差成本；用錯情境，它會變成程序負擔。先讀本文件，再決定要不要用。
