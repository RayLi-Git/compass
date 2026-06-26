# §1.2 三級制紀律強度縮放

> Part of [Compass](../../SKILL.md) §1 — Foundations.
> Compass 不是一套要套在所有任務上的重型流程。它按任務份量分三級，讓紀律強度與風險成正比，避免在改錯字時走十一節流程、也避免在做 migration 時草率帶過。

---

## 為什麼需要分級

如果所有任務都跑完整 Compass 流程，使用者會在第二次就放棄；如果所有任務都跳過紀律，brownfield 大功能就會在第三週爆炸。
分級的目的：**紀律強度 = 任務風險 × 不可逆程度**。

| 級別 | 觸發情境 | 套用的 Compass 紀律 | 可以省略什麼 | 階段標記範例 |
|---|---|---|---|---|
| 🟢 light | 改錯字、調樣式、改文案、加註解、單行明確修正 | 幾乎不套；保留「證據強度標記」即可 | DoR、compare-fix、checklist、commit message 格式 | 不需階段標記 |
| 🟡 medium | 新增一個 endpoint、寫一個函式/元件、改一段邏輯、整合一個 API | 動手前跑 DoR quick check；做完一塊跑 compare-fix loop；commit 帶上 PRD 區段引用 | 完整 11 節流程；reverse-audit；root-cause tree | `[PRD §X.Y] 模組：簡述` |
| 🔴 heavy | 實作一整個 PRD 區塊、schema migration、rollback 機制、brownfield 大功能、安全相關模組、跨多檔重構 | 全套 11 節流程（DoR → 計畫 → 實作 → compare-fix → DoD → commit → progress → 復盤）；reverse-audit；如卡關產出根因樹 | 不可省略；如時間真不夠走「緊急閥」 | `[PRD §X.Y] 模組：簡述` |

---

## 🟢 Light（輕量）

**觸發條件**（任一即可）：
- 改錯字、文案、註解
- 單檔單行明確修正（例：把 `console.log` 拿掉）
- 純樣式調整（顏色、間距）
- 不影響行為的 rename / 格式化

**套用紀律**：
- 直接做。
- 保留「證據強度標記」：宣稱完成前仍須標 🟢已驗證 / 🟡已檢視 / 🔴推測（這是 Sentinel 三條安全網之一的「證據強度分級」，Compass 沿用）。

**可以省略**：
- DoR（Definition of Ready）檢查
- compare-fix loop
- DoD checklist
- 階段標記
- progress 更新（除非該檔被多人協作）

**反面案例**：把「改一個 typo」升級成走完 11 節流程 — 這是過度紀律，會讓人對 Compass 反感。

---

## 🟡 Medium（中量）

**觸發條件**（任一即可）：
- 新增一個 endpoint / route
- 寫一個新函式或元件
- 改一段既有邏輯（< 100 行影響範圍）
- 整合一個外部 API
- 加一個欄位、改一個 schema 局部（非破壞性）

**套用紀律**：
1. **動手前**：跑 DoR quick check —「我知道驗收條件嗎？影響哪些檔案？有沒有對應的 PRD 區段？」（見 [§2 Definition of Ready](../02_definition_of_ready/_index.md)）。
2. **實作中**：完成就是完成，不留半成品；可分小塊交付，但不可半成品階段化。
3. **完成一塊**：立刻跑 compare-fix loop — 對照 PRD 原文檢查是否偏離，偏了立刻修，不批次累積（見 [§4 Compare-Fix Loop](../03_implementation/04_compare_fix_loop.md)）。
4. **commit**：訊息帶 PRD 區段引用，例 `[PRD §X.Y] 模組：簡述`（無 PRD 編號時用 `feat: 簡述`）。

**可以省略**：
- 完整 11 節流程的「§6 reverse-audit」（除非該模組已是 brownfield 痛點）
- 根因樹（除非開發中卡關 ≥ 2 個方向被證偽）
- progress.md 完整更新（commit message 已足夠記錄）

---

## 🔴 Heavy（重量）

**觸發條件**（任一即可）：
- 實作一整個 PRD 區塊
- schema migration / data migration
- rollback / recovery 機制
- brownfield 既有系統的大功能加入或重構
- 安全相關模組（認證、授權、PII、金鑰處理）
- 跨多檔 / 跨模組的 bug 或重構
- 卡關超過 1 次、想加第 3 個 if 特例、想用 try/except 蓋錯誤

**套用紀律**：
1. **全套 11 節流程**：從 DoR → 計畫 → 實作 → compare-fix → DoD → commit → progress → 復盤，一節都不跳。
2. **Reverse-audit**：對照你的後端框架的路由定義 / schema 定義 / config，跑一輪反向稽核——是否有 PRD 沒寫但 code 裡有的，或反之（見 [§6 Reverse Audit](../11_tooling/01_m007_to_m010.md)）。
3. **安全模組 test-first**：認證、授權、PII 處理一律先寫測試再寫實作。
   - **Example: typical web app stack** — Auth flow / token issuance / password hashing / 2FA / PII redaction，這些範例僅供參考，實際清單依你的技術棧而定。
4. **卡關產出根因樹**：≥ 2 個方向假說被證偽 → 停下來畫根因樹，不繼續疊補丁（根因樹是 Sentinel 的思考概念）。
5. **commit message 格式**：`[PRD §X.Y] 模組：簡述`，其中 §X.Y 指向 PRD 區段。
6. **progress 更新**：每塊完成更新 progress 檔（cross-session persistent memory，mechanism varies by setup）。

**可以省略**：無。如時間真不夠走「緊急閥」（見下方）。

---

## 🧷 升級不降級（Iron Rule）

**規則**：級別只能由低往高升，不能由高往低降。

- 使用者說「深一點 / 好好想 / 幫我規劃 / 為什麼 / 根因是什麼」→ 從 🟡 升 🔴。
- 使用者說「快點 / 簡單改 / 小修正」→ 若任務實際符合 🔴 觸發條件，**拒絕降級**。
  - 直接說明：「這個改動實際符合重量級觸發條件（理由 X），無法走輕量；如果真的趕，我們走緊急閥。」
- Compass 自我判斷符合 🔴 觸發條件但使用者沒明說 → 直接升 🔴，並告知為何升級。

**為什麼**：降級往往發生在最該認真的時刻（migration 趕死線、demo 前夜、線上炸了）。這些正是紀律最需要存在的時候。允許降級 = Compass 形同虛設。

---

## 🚨 緊急閥（Emergency Override Valve）

**用途**：當「真的、確實、不騙人」緊急時（例：production down、demo 30 分鐘後開始），允許跳過部分紀律先止血。

**規則**：
1. **只能跳過流程，不能跳過記錄**。在 debug 或變更日誌中標 `🔴[SKIPPED]`，記下：
   - 跳過了哪幾節（例：跳過 DoR、跳過 reverse-audit）
   - 為什麼緊急（一句話）
   - 何時必須補追（例：「事後 24 小時內回頭跑完整流程」）
2. **事後必須復盤補追**。緊急閥不是免死金牌，是延後付款。沒補追 = 技術債 + 紀律債雙重累積。
3. **不能對「安全相關模組」用緊急閥**。認證、授權、金鑰處理就算趕也要 test-first。緊急閥用在這裡 = 製造下一次事故。
4. **不能連用兩次**。同一個專案、同一週內第二次想開緊急閥 → 強制停下檢討為什麼一直在救火，這是上游有問題的訊號。

**反面案例**：每次都用緊急閥跳過 compare-fix loop，三個月後發現 code 跟 PRD 已經完全對不起來 — 此時要做的不是再開一次緊急閥，而是停下來跑 reverse-audit。

---

## 🔗 Related Compass sections
- [§1.1 核心原則 + 五階段總覽](./01_principles.md) — Compass 的定位與紀律強度為何分級
- [§2 Definition of Ready](../02_definition_of_ready/_index.md) — 🟡 / 🔴 動手前的入場檢查
- [§3.4 完成-比對-修正循環](../03_implementation/04_compare_fix_loop.md) — 🟡 / 🔴 完成一塊後的對照修正
- [§11.1 反向稽核 (M-008)](../11_tooling/01_m007_to_m010.md) — 🔴 必跑的反向稽核
- 證據強度分級、根因樹皆為 Sentinel 概念，Compass 在 🔴 重級任務沿用

## 📝 Status
v0.2.0 (Phase 1: ported from prior SOP, generalized and de-privatized).
