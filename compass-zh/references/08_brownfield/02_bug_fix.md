# §8.2 Bug Fix Workflow

> Part of [Compass](../../SKILL.md) §8 — Brownfield.
> 在既有 code 上修 bug：先重現、追根因、鎖行為、最小改、留回歸。

修 bug 不是「讓錯誤訊息消失」。錯誤訊息消失有兩種：bug 被修好，或 bug 被藏起來。
這份流程的存在就是逼你走第一種。

---

## 🚦 開工前：先確認這是不是 bug

「使用者覺得不對」≠「程式有 bug」。動手前先分類：

| 情況 | 判準 | 去處 |
|---|---|---|
| Code bug | spec 說 X，code 做 Y，X 才對 | 本流程繼續 |
| PRD / spec mismatch | spec 說 X，code 做 Y，但**不確定哪個對** | 走 [§5.3 跨文件衝突](../05_conflict_handling/03_cross_document.md) 裁決 |
| 規格沒講到 | spec 對這情境隻字未提 | 走 [§5.1 模糊/缺漏](../05_conflict_handling/01_vague_bug_gap.md) |
| 使用者要的新行為 | spec 沒寫、現在也不報錯，只是不夠用 | 這是 feature，去 [§8.4 Add Feature](./04_add_feature.md) |

**最常見的陷阱**：spec 說 X、code 做 Y，你直接把 code 改成 X——結果 X 才是過時的規格，Y 是上次正確的修正。
→ spec 與 code 不一致時，先問「哪個是對的」，不要預設 code 一定錯。這一步走 §5.3，不要在 bug 流程裡擅自裁決。

---

## 1️⃣ 重現優先：No repro, no fix

**沒有穩定重現步驟之前，不准動 production code。**

改一個你無法重現的 bug，你無法證明你修好了——你只是改了一段 code 然後祈禱。

重現清單：

- [ ] 寫下**精確**重現步驟（輸入、前置狀態、操作順序）
- [ ] 至少跑 **2 次**確認穩定重現，不是偶發
- [ ] 記下「預期 vs 實際」兩行對照
- [ ] 確認重現環境（版本、資料、設定）與回報者一致

若**無法穩定重現**：

| 狀況 | 動作 |
|---|---|
| 偶發、時有時無 | 先找出觸發條件（並發？時序？特定資料？），不要瞎改 |
| 只在 prod 出現 | 補 log / trace 縮小範圍，這是 Sentinel 診斷階段的「加儀器」，不是亂槍 |
| 完全重現不了 | 標記為「待補重現」，**不修**——降級為觀察任務 |

> ⚠️ 「加一堆 log 卻沒方向」是 Sentinel 的淺層紅旗。加 log 前先有假說，log 是為了證偽假說，不是撒網。

---

## 2️⃣ 根因，不是症狀

錯誤跳出來的地方，往往不是錯誤產生的地方。永遠往上游追一層。

這是 Sentinel 診斷階段的核心。修 bug 前問：

1. **這個錯誤是症狀還是源頭？** 例如 `null pointer` 在 A，但 null 是 B 塞進來的，根因在 B。
2. **為什麼這個壞值/壞狀態會到這裡？** 一路往回追到「第一個不該發生的事」。
3. **同一個根因還會從哪冒出來？** 若只補當前這個點，其他入口仍會炸。

### 繞過 ≠ 解決（紅旗）

以下都是「關掉警報」而非「滅火」，看到就停：

```text
✗ try { risky() } catch { /* 吞掉，讓它過 */ }
✗ if (x == null) return;        // 特例擋住症狀，沒問 x 為何是 null
✗ value as any                  // 把型別錯誤壓下去
✗ 加第 3 個特例 if 打補丁
```

> 想用 try/except 蓋錯誤、加第 3 個特例 if、改成 `any`——三者任一出現，退出改 code 模式，進 Sentinel 診斷模式。

---

## 3️⃣ Characterization test：先鎖、後修

修既有 code 最大的風險是**改 A 壞 B**。防線是：在改任何邏輯前，先用測試把「現在的行為」釘住。

順序很重要：

```text
① 寫 characterization test → 鎖住目前『正確』的相鄰行為（會綠）
② 寫 failing test          → 表達 bug 該有的正確行為（現在會紅）
③ 改 production code        → 讓 ② 變綠，且 ① 不能變紅
```

- **①** 不是測 bug，是測「這次改動絕不能弄壞的東西」。它一開始就是綠的——若它先紅，代表你對現狀的理解錯了，回到第 2 步。
- **②** 是 bug 的 red test：精準對應第 1 步寫下的重現步驟。它紅，證明你真的重現了 bug。
- 安全模組（Auth / 權限 / PII）的 bug **強制 test-first**，見 [§4.1 DoD](../04_quality_gates/01_dod.md)。

> **範例**（FastAPI，僅示意，非必須）
> bug：折扣碼過期仍可用。
> ① `test_valid_code_still_applies()` — 鎖住「未過期的碼照常生效」（綠）
> ② `test_expired_code_rejected()` — 過期碼應回 400（現在紅，因為 bug）
> ③ 修 `apply_discount()` 加過期判斷 → ② 轉綠、① 維持綠

---

## 4️⃣ 最小 diff 紀律

**修 bug 的 commit 只做一件事：修這個 bug。**

看到旁邊的爛 code 很想順手重構——忍住。理由：

- 重構混進 bug fix，review 時無法分辨「哪行是修 bug、哪行是手癢」。
- 真的回歸時，`git bisect` / revert 會把你的修正和重構一起捲走。
- 擴大 diff = 擴大「改 A 壞 B」的面積，正好違背第 3 步的防線。

| 該做 | 不該做 |
|---|---|
| 改最少的行讓 ② 轉綠 | 順手改變數命名、調排版、抽函式 |
| 重構欲望記成獨立 task | 在同一 commit 重構 |
| commit：`[fix] 模組：根因一句話` | 一個 commit 混 fix + refactor + 格式化 |

想重構是合理的——但它是**另一個 PR**，走 [§8.3 Refactor](./03_refactor.md)。

---

## 5️⃣ 回歸測試是 DoD，不是加分

第 3 步的 failing test（②）轉綠後**留在 codebase 裡**，它就是回歸測試——保證這個 bug 不會復活。

收工前對齊 [§4.1 DoD](../04_quality_gates/01_dod.md)：

- [ ] **重現步驟可重現** → 修完後照原步驟，bug 不再出現（🟢 已驗證，附實跑結果）
- [ ] **failing test 現在綠** → 且把它留下當回歸測試
- [ ] **characterization test 仍綠** → 證明沒弄壞相鄰行為
- [ ] **lint / typecheck / 全測試** 通過
- [ ] **diff 最小** → self-review 確認沒夾帶重構
- [ ] **commit** 訊息點名根因，不只寫「fix bug」
- [ ] 若屬「夠痛」案例（誤判過根因 / ≥2 假說被證偽 / 根因跨層）→ 寫進 Sentinel 病歷 `.claude/debug-log.md`

> 🔬 宣稱「修好了」前標證據強度：🟢 已驗證（跑過、附證據）／🟡 已檢視（讀過邏輯沒跑）／🔴 推測。沒跑過絕不說「我跑過了」。

---

## ✅ Bug fix 全流程速查

```text
1. 分類：code bug? 還是 spec mismatch?（mismatch → §5.3）
2. 重現：穩定 repro，否則不修
3. 根因：往上游追，別停在症狀
4. 鎖行為：characterization test（綠）
5. red test：表達正確行為（紅）
6. 最小改：讓 red 轉綠、characterization 維持綠
7. DoD：回歸測試留下、diff 乾淨、commit 點名根因
```

---

## 🔗 Related Compass sections

- [§5.3 跨文件衝突](../05_conflict_handling/03_cross_document.md) — spec 說 X、code 做 Y 時誰對誰錯
- [§4.1 Definition of Done](../04_quality_gates/01_dod.md) — 回歸測試與收工門檻
- [§8.3 Refactor Workflow](./03_refactor.md) — 把「順手重構」的衝動移到這裡
- [§8 Brownfield 總覽](./_index.md) — 既有 code 的修改地圖

---

## 📝 Status

v0.5.0 (Phase 2: original content)
