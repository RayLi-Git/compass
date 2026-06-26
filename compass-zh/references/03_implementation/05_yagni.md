# §3.5 YAGNI：「不寫什麼」明確清單

> Part of [Compass](../../SKILL.md) §3 — Implementation.
> 實作當下的自律：PRD 沒要求、也沒實作必要的東西，不寫。把「少寫」當成一種紀律，而不是偷懶。

---

## 適用前提（先讀，免得誤砍）

本清單針對「**PRD 沒寫且沒實作必要**」的東西。

⚠️ **重要例外**：若實作時自然冒出 PRD 未列、但**對齊設計原則的合理補強**，**不要直接套本清單砍掉**——改走 [§5 Conflict Handling](../05_conflict_handling/01_vague_bug_gap.md) 的「PRD 缺漏 + 實作更好」軌道（記錄、暫留、等裁決）。

YAGNI 與「PRD 缺漏優化」是一體兩面：
- 純粹多寫、無設計理由 → YAGNI 砍（本檔）
- 有設計理由、對齊原則 → 走 §5 缺漏軌道，不砍

---

## 程式碼層級

- ❌ PRD 沒提的 endpoint / 欄位 / 參數
- ❌ 「以防萬一」的 try/except（讓它噴錯；PRD 有規定錯誤碼才接）
- ❌ 預留給未來功能的參數（例 `def foo(x, future_y=None)`）
- ❌ 通用化抽象（PRD 只要兩種就寫兩種，別預先寫 strategy pattern）
- ❌ 多於一行的 inline 註解（除非 PRD 明文要求）
- ❌ 模組 docstring 寫「這個模組做 X」（檔名 / 類名已經說了）
- ❌ 把同一邏輯包成 helper（出現第三次再說）
- ❌ 自製 logger / config loader（用標準函式庫或 PRD 指定套件）

## 檔案層級

- ❌ `utils.py` / `helpers.py`（沒有明確歸屬就不要建）
- ❌ `TODO.md` / `NOTES.md`（資訊放 `progress.md` / `development-log.md`，見 [§3.2 追蹤文件](02_tracking_docs.md)）
- ❌ 任何 PRD 目錄結構沒列出的檔案

## 依賴層級

- ❌ PRD 技術選型沒列出的套件
- ❌ 「方便一點」的 quality-of-life 套件（語法糖型、輸出美化型等，非 PRD 指定的不裝）

---

## 唯一例外

PRD 留白處（明確寫「待定」、「自選」、「實作者決定」）才允許自行決定，且**必須寫進 `development-log.md`** 留下決策軌跡。

---

## 為什麼 YAGNI 是紀律不是偷懶

每多寫一行 PRD 沒要求的 code，就多一份：
- 要維護的表面積
- 可能與未來 PRD 衝突的猜測
- 讓 reviewer 困惑「這是 PRD 要的還是你加的」的成本

YAGNI 的精神是「**證明你需要它，再寫它**」——這跟 [§5 Conflict Handling](../05_conflict_handling/01_vague_bug_gap.md) 的「PRD 缺漏要等裁決」是同一套紀律：**不擅自擴張合約**。

---

## 🔗 Related Compass sections
- [§5.1 PRD 模糊 / Bug / 缺漏](../05_conflict_handling/01_vague_bug_gap.md) — YAGNI 的反面：有設計理由的缺漏優化走這條，不砍
- [§3.2 追蹤文件三件套](02_tracking_docs.md) — 例外決策寫進 development-log.md
- [§3.3 實作順序與依賴](03_implementation_order.md) — 不引入 PRD 外的依賴

## 📝 Status
v0.2.0 (Phase 1: ported from prior SOP §11, generalized and de-privatized).
