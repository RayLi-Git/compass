# §3.4 完成-比對-修正循環

> Part of [Compass](../../SKILL.md) §3 — Implementation.
> 每完成一個檔案/功能塊後，立即執行「完成 → 比對 PRD → 修正 → 驗收」的閉環，避免偏差累積。

---

## 1. 12 步循環

每完成一個檔案 / 功能塊：

```
1. 完成實作
2. 通過 DoD（詳見 §4.1）
3. 讀回 PRD 對應章節
4. 逐條比對：命名 / 行為 / 邊界條件 / 回傳與錯誤碼
5. 有偏差 → 以 PRD 為主修正
   例外：實作優於 PRD 且符合「實作優於 PRD」門檻 →
         走 §5 Conflict Handling 的對應流程
6. Self-review
7. PRD checklist 打勾或標 🟡
8. development log 記錄
9. progress 記錄更新
10. git commit
11. 列出測試步驟，請使用者驗收（見下方 §3 使用者驗收 Gate）
12. 通過 → 下一塊；失敗 → 修正後重測
```

> **DoD 細節不在本檔重複**：八項硬性 Gate 與工具化驗證請見 [§4.1 DoD](../04_quality_gates/01_dod.md)。

---

## 2. 禁止事項

以下行為任一發生，視為違反完成-比對-修正循環，必須立刻停下：

- ❌ 跳過比對直接前進
- ❌ 跳過 DoD 任一項
- ❌ 「之後再回頭檢查」式累積技術債
- ❌ 沒讀 PRD 憑記憶實作
- ❌ 多個模組未 commit 累積在 working tree
- ❌ 未經使用者測試驗收就進下一階段

> 核心精神：**完成就是完成，不留半成品；可分小塊交付，但不可半成品階段化**。

---

## 3. 階段驗收：使用者測試 Gate（User Acceptance Gate）

> 📌 用詞：本節「階段」= 一個可獨立驗收的「塊 / unit」。分小塊交付（鼓勵），
> 但每塊都要過完整驗收、不留半成品（呼應「完成就是完成」）。塊越小，測試指引越輕。

每完成一個階段（=「實作順序表」一個項目）且通過 DoD 後：

1. **停下來**，不主動進入下一階段
2. 列出「## 階段 N 測試指引」（內容包含：測試前提、測試步驟、預期結果、邊界與異常案例）
3. **先自己跑一遍**（自動自檢循環，最多 3 輪 — 見下方 §3.1）
4. 三輪內全綠 → 請使用者驗收
5. 三輪仍失敗 → 停下來通知使用者裁決
6. 使用者通過 → progress 記錄標 ✅ + commit + 進下一階段
7. 使用者失敗 → 進入修正循環

### 3.1 自動自檢循環規則

- 「全部 Test」指本階段測試指引列出的**全部** Test（含邊界 / 異常）
- 修正後必須重跑**全部** Test（防修一個壞兩個）
- 每輪在 development log 留紀錄：失敗點 + 採取的修正
- **達 3 次仍失敗 → 停下來，不要嘗試第 4 次**
- 只對「自動化可驗證」的 Test 適用；UI 體驗等需人類判斷的部分直接請使用者測試

### 3.2 可跳過使用者驗收 Gate 的例外

下列情況可跳過 Gate，直接進入下一塊：

- 純文件變更（如 CLAUDE.md / CHANGELOG.md 等說明文件）
- 純註解 / typo 修正
- 已被後續階段驗證涵蓋的中間重構

> 跳過時須在 development log 註明：「跳過使用者測試 — 理由：…」。

### 3.3 測試指引撰寫 4 規範（範本見 [templates/test-guide.md.template](../../templates/test-guide.md.template)）

1. **可獨立執行**：每步不依賴上一步的記憶，使用者照貼即可。
2. **明確指令**：給完整可貼上的指令，不寫「執行某個腳本」。
3. **預期結果具體**：「回傳 200 + 含 X 欄位」而非「成功」。
4. **失敗判定明確**：「若出現 Y → 表示 Z」，讓使用者自己就能判斷哪裡錯。

> 自檢 3 輪用盡或中途撞 blocker 時，用 [templates/selfcheck-fail.md.template](../../templates/selfcheck-fail.md.template) 彙整交裁決——第 3 輪須調用 Sentinel 診斷模式列 2-3 個假說，不只報「修不好」。

---

## 4. 循環失敗時的決策樹

| 狀態 | 動作 |
|---|---|
| 自檢 1–2 輪失敗 | 修正後重跑全部 Test |
| 自檢 3 輪仍失敗 | 停手，列出失敗點 + 已試方向，請使用者裁決 |
| 使用者驗收失敗 | 進入修正循環（回到步驟 1），不算進下一塊 |
| 比對發現 PRD 模糊 | 走 [§5 Conflict Handling](../05_conflict_handling/_index.md) 的「PRD 模糊」流程 |
| 比對發現 PRD 本身有 bug | 走 [§5 Conflict Handling](../05_conflict_handling/_index.md) 的「PRD bug」流程，等使用者裁決 |
| 實作優於 PRD | 走 [§5 Conflict Handling](../05_conflict_handling/_index.md) 的「實作優於 PRD」流程，保留實作 + 記錄 + 等裁決 |

---

## 🔗 Related Compass sections
- [§4.1 DoD](../04_quality_gates/01_dod.md) — 本循環第 2 步引用的硬性 Gate 細節
- [§3.3 Implementation Order](./03_implementation_order.md) — 階段切分依據，決定何時觸發本循環
- [§5 Conflict Handling](../05_conflict_handling/_index.md) — 比對發現 PRD 模糊／bug／實作更好時的處置流程
- [§3 Implementation](../03_implementation/_index.md) — 第 10 步 git commit 的訊息格式與顆粒度（commit convention）

## 📝 Status
v0.3.0 (+ §3.3 測試指引 4 規範 + test-guide / selfcheck-fail 範本接線 + 塊 vs 階段 用詞校正).
