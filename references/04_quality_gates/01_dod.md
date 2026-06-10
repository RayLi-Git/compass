# §4.1 Definition of Done (DoD)

> Part of [Compass](../../SKILL.md) §4 — Quality Gates.
> 定義一塊工作「真正完成」的硬性閘門：哪些檢查必過、哪些建議補上、以及違反時的鐵律。

---

## 🔒 鐵律（Iron Rule）

> **任何一項 Required 沒過 = 未完成。未完成就不准開始下一塊。**

不能用「之後再回頭補」、「先 commit 再說」、「等下一輪一起跑」來繞過。DoD 是一道閘門，不是一張願望清單。半成品不可進主線、不可標記為完成、不可解鎖下一塊工作。

呼應核心心法：**「完成就是完成，不留半成品；可分小塊交付，但不可半成品階段化。」**

---

## ✅ Required（永遠適用）

前置條件：**程式碼寫完**（涵蓋這塊承諾的範圍，不留 TODO 占位）。在此之上，下列**八項**必須全部通過：

- [ ] **1. Lint 通過**（使用你語言的 lint 工具）
- [ ] **2. Typecheck 通過**（若你的語言有靜態型別檢查工具）
- [ ] **3. 相關 unit test 通過**（既有測試不可因這塊改動而紅）
- [ ] **4. 手動 smoke test**：在真實環境（不是測試替身）跑一次最小可行路徑，眼睛看過確認沒爆　⚠️ **library / CLI 等無可執行入口的專案可豁免本項**，但須在 DoD 紀錄註明豁免理由
- [ ] **5. PRD checklist 對照打勾**（這塊涉及的每一行都必須伴隨「在 codebase 中親眼驗證過」的確認，不可純記憶打勾）
- [ ] **6. Self-review 完成**（把自己的 diff 當陌生人寫的來讀；完整 checklist 見 [§4.2 Code Review](02_code_review.md)）
- [ ] **7. Git commit 完成**（訊息格式見 [§3 Implementation](../03_implementation/_index.md) 或你專案的既有 commit 慣例）
- [ ] **8. progress.md 更新**（把這塊的完成狀態、決策、未解事項寫進跨 session 持久記憶，機制依你的設定而異）

這八項是底線。少一項（smoke 的 library 豁免除外）就是未完成，沒有討論空間。

> 📌 **條件式第 9 項**：一旦你的專案建立了反向稽核腳本（見 [§11 工具化稽核](../11_tooling/01_m007_to_m010.md) 的 reverse-audit script），**「反向稽核 exit code 0」即升為 Required**——機械化檢查存在卻不跑，等於白建。

---

## 🟡 Recommended additions（強烈建議補上）

下列項目不是每個專案都強制，但只要你的專案規模或風險高於玩具等級，幾乎都應該納入：

- [ ] **更廣的整合 / e2e 測試**（見 [§10.1 測試金字塔](../10_testing_strategy/01_test_pyramid.md)）
- [ ] **觀測性就位**（log / metrics，見 [§6.3 觀測性](../06_non_functional/03_observability.md)）——production 服務的隱性完成條件

這些項目的價值在於：當你回頭、切 session、或交接給下一個 agent 時，**未來的你/別人** 能立刻接上，不必重新考古。

---

## 📐 專案層級的擴充

> **DoD 是專案層級的決定。**

不同專案會在 Required 與 Recommended 之上再疊加自己的關卡，例如：

- 無障礙檢查（a11y audit）
- 效能預算（performance budget / bundle size 上限）
- 安全掃描（SAST、相依套件 CVE 檢查）
- i18n 字串覆蓋
- 文件同步更新（API 參考、CHANGELOG）
- 視覺回歸測試（visual regression snapshot）

選哪些、放在 Required 還是 Recommended，由專案團隊決定並寫進專案根目錄的 DoD 定義中。Compass 提供的是 **共通最小集**，不是天花板。

---

## 🧭 怎麼使用這份 DoD

1. **動手前**：把這份清單對到當前這塊工作，心裡有譜這塊收尾要過哪幾關。
2. **動作中**：寫完一段就跑 lint / typecheck，不要累積到最後才一次跑（出問題時 blast radius 較小）。
3. **收尾前**：照清單逐項打勾。打不下去的項目 = 還沒做完，回去做。
4. **打完勾**：才能 commit、才能宣告完成、才能開始下一塊。

> 如果你發現自己在心裡盤算「這項先跳過，等下一塊再補」——這就是紅旗。停手，補完，再前進。

---

## 🚫 常見偷跑姿勢（不被接受）

- 「lint 只是 warning，不影響功能」→ 不接受。warning 也要在這塊處理掉，或顯式記錄為已知例外。
- 「test 紅是既有的，不是我弄壞的」→ 確認後若屬實，獨立開一塊修。但**這塊**不能在紅燈下宣告完成。
- 「smoke test 等整個 feature 做完一起跑」→ 不接受。每塊都要至少跑過自己這塊的最小路徑。
- 「commit 等等再寫，先做下一塊」→ 不接受。未 commit = 未完成（見 [§3 實作紀律](../03_implementation/_index.md)）。

---

## 🔗 Related Compass sections
- [§3 Implementation](../03_implementation/_index.md) — DoD 是實作紀律的收尾閘門；commit 慣例與分塊節奏在這裡。
- [§2 Definition of Ready](../02_definition_of_ready/_index.md) — 動手前的對偶閘門：開工前該確認什麼。
- [§5 Conflict Handling](../05_conflict_handling/_index.md) — DoD 卡關但有正當理由時的升級與裁決流程。
- [§11 Tooling](../11_tooling/01_m007_to_m010.md) — reverse-audit script 等自動化稽核工具的細節。

## 📝 Status
v0.2.0 (Phase 1: ported from prior SOP, generalized and de-privatized).
