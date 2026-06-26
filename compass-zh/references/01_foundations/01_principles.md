# §1.1 核心原則 + 五階段總覽

> Part of [Compass](../../SKILL.md) §1 — Foundations。
> 本檔說明 PRD 驅動開發的 10 條核心原則，以及把整個流程拆成五個階段的總覽地圖。

---

PRD 驅動開發的精神，是讓「規格 → 程式碼」的轉換成為一條可重複、可驗證、可追溯的流水線。任何偏差都不靠記憶判斷，而是回到 PRD 對照。本檔提供兩件事：(1) 動手前必須內化的 10 條原則；(2) 整個流程的五階段地形圖，讓你知道自己現在站在哪一格。

細節操作流程請見後續章節（§2 Stage 0 吸收 PRD、§3 Stage 1 追蹤骨架、§4 Stage 2–4 實作迴圈、§5 衝突處理 等）。

---

## 0. 核心原則（10 條）

| # | 原則 | 說明 |
|---|---|---|
| 1 | PRD 為唯一事實來源 | 任何偏差，一律以 PRD 為準修正；不依靠記憶或臆測 |
| 2 | 完成就是完成，不留半成品 | 可分小塊交付，但每一塊都必須做完整；**不可以「半成品階段化」**（例如先放一個只回 200 的假 endpoint、之後再回來補邏輯） |
| 3 | 完成即比對 | 每完成一塊，立刻回查 PRD 對應章節，確認一致再前進 |
| 4 | 偏差即記錄 | 任何不一致 / PRD 內部矛盾，全部寫進開發紀錄檔（development log） |
| 5 | PRD 模糊用較具體一方 | 詳見 [§5 Conflict Handling](../05_conflict_handling/01_vague_bug_gap.md) 的「模糊條款」處理 |
| 6 | PRD bug 先停手等裁決 | 詳見 [§5 Conflict Handling](../05_conflict_handling/01_vague_bug_gap.md) 的「PRD bug」處理 |
| 7 | PRD 缺漏 + 實作更好走「缺漏優化」流程 | **不要直接以 YAGNI 砍掉**，先記錄等裁決，詳見 [§5 Conflict Handling](../05_conflict_handling/01_vague_bug_gap.md) |
| 8 | YAGNI 嚴格執行 | 不寫 PRD 沒要求的東西（細則見 [§3.5 YAGNI](../03_implementation/05_yagni.md)） |
| 9 | 階段完成必請使用者測試 | 通過 DoD 後停下來，列詳細測試步驟；未通過不進下一階段 |
| 10 | 關鍵脈絡寫入永久記憶 | 啟動 / 重大決策後寫入跨 session 持久化記憶（機制依環境而異） |

### 原則 #2 補充說明

「不留半成品」不是禁止小塊交付，而是禁止**用「先佔位、之後補」當常態**。具體紅旗：

- 只開了一個 endpoint 但 handler 是 `return {"ok": True}`，理由是「等下一塊再補邏輯」
- DB schema 開了欄位卻沒任何讀寫路徑使用
- 寫了一個 class / function 但裡面是 `pass` 或 `raise NotImplementedError`
- commit 訊息出現「WIP」「先這樣」「之後再回來」第 2 次以上

這些都會在 [§5 Conflict Handling](../05_conflict_handling/01_vague_bug_gap.md) 與 [§3 Implementation Loop](../03_implementation/_index.md) 的 DoD 檢查中被攔下。

---

## 1. 流程總覽（五階段）

```
階段 0：吸收 PRD          → 全量讀取 + 拆解功能清單
階段 1：建立追蹤文件骨架  → progress 檔 / development log / PRD checklist
階段 2：依 PRD 順序實作   → 從基礎設施到上層功能，依序完成
階段 3：完成-比對-修正循環 → 每塊功能完成後立即回比 PRD
階段 4：最終全面對齊      → 全量 PRD vs 程式碼校驗，補漏
```

### 五階段對應的 Compass 章節

| 階段 | 名稱 | 主要動作 | 對應章節 |
|---|---|---|---|
| 0 | 吸收 PRD | 全量讀取、拆功能清單、識別模糊/矛盾 | [§3 PRD Intake](../03_implementation/01_prd_intake.md) |
| 1 | 建立追蹤骨架 | 三件套檔案就位（進度 / 紀錄 / 清單） | [§3 Tracking Docs](../03_implementation/02_tracking_docs.md) |
| 2 | 依序實作 | 由下而上，安全模組先 test-first | [§3 Implementation Loop](../03_implementation/_index.md) |
| 3 | 完成即比對 | 每塊收尾跑 DoD、回比 PRD | [§3 Compare-Fix Loop](../03_implementation/04_compare_fix_loop.md) |
| 4 | 最終對齊 | 反向稽核腳本掃全專案，補漏 | [§11.1 反向稽核 M-008](../11_tooling/01_m007_to_m010.md) |

### 階段之間的硬規則

- **階段 0 沒做完不能進階段 1**：你連功能清單都沒列完，做什麼追蹤骨架？
- **階段 1 沒做完不能進階段 2**：沒有 PRD checklist，DoD 比對沒有對照基準。
- **每塊功能在階段 2 → 3 之間是同一個迴圈**：不是「先全部寫完再來比對」。
- **階段 4 之前必須回看所有 [SKIPPED] / [SKIPPED-PRD] 標記**：跳過的紀錄全部要結案。

---

## 2. 何時不適用這套流程

以下情境本流程過重，不必硬套（但 [Sentinel 思考 OS](../../SKILL.md) 仍然常駐運作）：

- 閒聊、純文件 / typo 修正
- 純 bug 修復（無新功能、無 PRD 章節對應）
- 探索性原型（規格還在發散）
- 規格頻繁變動的早期專案（PRD 尚未穩定到能當合約）

判斷準則：**有沒有一份你願意拿來當「事後驗收依據」的 PRD？** 沒有就不要硬套。

---

## 🔗 Related Compass sections
- [§3 PRD Intake](../03_implementation/01_prd_intake.md) — 階段 0 的詳細做法
- [§3 Tracking Docs](../03_implementation/02_tracking_docs.md) — 階段 1 的三件套檔案
- [§3 Implementation Loop](../03_implementation/_index.md) — 階段 2–3 的實作 + 比對迴圈
- [§5 Conflict Handling](../05_conflict_handling/01_vague_bug_gap.md) — 原則 #5、#6、#7 的衝突處置細則
- [§3.5 YAGNI](../03_implementation/05_yagni.md) — 原則 #8 的執行界線
- [§11.1 反向稽核 M-008](../11_tooling/01_m007_to_m010.md) — 階段 4 最終對齊用的反向稽核工具

## 📝 Status
v0.2.0 (Phase 1: ported from prior SOP, generalized and de-privatized).
