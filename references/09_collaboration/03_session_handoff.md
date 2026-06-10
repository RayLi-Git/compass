# §9.3 跨 session / 跨 AI 交接

> Part of [Compass](../../SKILL.md) §9 — Collaboration.
> 一份 PRD 橫跨多個 Claude Code session / 多個 agent：交接零摩擦，下一棒不重新考古。

長 PRD 不會在一個 session 內寫完。context 會滿、會跨日、會切 agent。
交接做不好，下一棒得花半小時重建脈絡——而且常常重建錯，在已經改過的地方又改一次。
這份流程的目的：**讓接手的 session 在 5 分鐘內知道「現在在哪、下一步動哪、別碰什麼」，靠檔案不靠記憶。**

交接不是一份新文件。它是把 [§3.2 追蹤文件三件套](../03_implementation/02_tracking_docs.md) 留在「可被冷讀」的狀態，外加一個 git 快照。

---

## 🧠 核心原則：交接靠檔案，不靠對話

接手的 session **沒有**上一棒的對話記憶。它只看得到：

- 你 commit 進 git 的東西
- 你寫進 `progress.md` / `development-log.md` / `prd-checklist.md` 的東西

→ 任何「只活在對話裡」的決策、進度、半成品，對下一棒等於不存在。

這就是 Sentinel 的回錨——但寫成純文字、留在檔案裡，不是丟在 chat history 等壓縮吃掉。

---

## 📤 交出方（OUTGOING）：離場前必留五樣

離場前，下一棒要能單靠這五樣冷啟動。缺一樣，交接就有洞。

| # | 留什麼 | 狀態要求 |
|---|---|---|
| 1 | `progress.md` | 「進行中」指向當前那一塊 + **下一個動作一句話** |
| 2 | `development-log.md` | 最後一筆是「我這段做了什麼決策 / 卡在哪」，附日期 + PRD 錨點 |
| 3 | `prd-checklist.md` | 動到的條目狀態正確（⬜ / 🟡 / 🟢），沒有「做了但忘記改狀態」 |
| 4 | **「從這裡接手」指針** | `progress.md` 頂端一行：下一棒第一個動作是什麼、在哪個檔案 |
| 5 | **乾淨 git** | WIP 也要 commit；不留髒 working tree 給下一棒 |

### 「從這裡接手」指針（範例）

放在 `progress.md` 最頂端，下一棒第一眼就看到：

```markdown
## ▶ RESUME HERE
- 進行中：PRD §4.3 退款 webhook 簽章驗證（第 5 塊 / 共 9 塊）
- 下一動作：在 src/webhooks/refund.py 補 timestamp 容忍窗（±5 分），red test 已寫好在
  tests/test_refund_sig.py::test_stale_timestamp_rejected（現在紅）
- 別碰：src/webhooks/charge.py 已驗收完成，勿順手重構
```

> 指針要寫成**動作**（「補 X / 讓某測試轉綠」），不是狀態（「webhook 做到一半」）。
> 狀態讓下一棒還得自己推下一步；動作直接可執行。

### WIP commit 紀律

context 將滿、半塊沒寫完也要交接——這時 git 不可能乾淨。做法：

```bash
git add -A
git commit -m "WIP [PRD §4.3] refund webhook：簽章驗證寫到一半，red test 已紅，見 progress.md RESUME HERE"
```

- WIP commit 的訊息要點名「停在哪、紅在哪」，呼應 `progress.md` 的指針。
- 別用 `git stash` 交接——stash 不會被下一棒主動看到，等於藏起來。
- 下一棒接手後第一塊做完，可選擇 `git commit --amend` 或 squash 掉 WIP（見 §3.2 commit 紀律）。

---

## 📥 接手方（INCOMING）：開工先讀，順序固定

接手的 session **第一件事不是寫 code，是冷讀**。按這個順序，由「我在哪」往「我能不能動手」收斂：

| 序 | 讀什麼 | 回答的問題 |
|---|---|---|
| 1 | `progress.md` 的 **RESUME HERE + 進行中** | 現在在哪？下一動作是什麼？ |
| 2 | `development-log.md` **最後 3 筆** | 上一棒為什麼這樣做？有沒有卡關/等裁決？ |
| 3 | `prd-checklist.md` **下一條 ⬜/🟡** | 還剩什麼？這一塊的驗收條件是什麼？ |
| 4 | `git log --oneline -10` + `git status` | 物理現狀對得上文件嗎？有沒有 WIP / 髒 tree？ |
| 5 | 確認 **DoD 環境可跑**（lint / typecheck / test 指令能起來）| 我能不能驗證「修好了」？ |

讀完 1–4，輸出一段**回錨**確認自己對齊了（純文字，給使用者過目）：

```text
📍回錨（接手 PRD §4.3）
- 最初目標：退款 webhook 全鏈路，含簽章驗證（§4 共 9 塊）
- 進度：8 塊已 commit，第 5 塊簽章驗證進行中
- 待辦：補 timestamp 容忍窗 → 讓 test_stale_timestamp_rejected 轉綠
- 偏離檢查：dev-log 無等裁決項；charge.py 標記勿動，遵守
```

> 第 5 步常被跳過——然後接手方改完才發現測試根本跑不起來，分不清是自己改壞還是環境本來就壞。
> **先確認環境綠，再動 production code。** 對不上時先查 git 與文件的落差，別假設文件是對的。

### 文件與 git 對不上時

冷讀第 4 步若發現矛盾（例如 `progress.md` 說某塊已完成，但 git 沒有對應 commit）：

| 矛盾 | 處置 |
|---|---|
| 文件說做了、git 沒有 | 以 **git（寫下來的物理快照）為準**，文件可能在 commit 前就斷了 |
| git 有 commit、checklist 沒勾 | 補勾 + 填證據欄，別重做那一塊 |
| 兩邊都對不上、搞不清狀態 | **停**，回錨列出落差問使用者，不要猜著往下寫 |

---

## ⏳ 主動交接的觸發點：別等 context 爆掉

交接最常壞在「拖到最後一刻」——context 滿到模型開始忘事，才匆忙留檔，於是 `progress.md` 也寫得語焉不詳。

**主動交接觸發條件（出現任一 → 立刻進交接流程，不要再開新一塊）：**

- context 用量接近上限（感覺開始記不住前面的決策）
- 一塊剛 commit 完、正要開下一塊之際（天然的乾淨切點）
- 要切換 agent / 換人接手
- 使用者說「先停這 / 下次再繼續」

> 黃金切點是**「一塊剛 commit、下一塊還沒開」**：git 乾淨、checklist 狀態剛對齊、指針好寫。
> 在一塊寫到一半時被迫交接，成本最高（要寫 WIP commit + 解釋紅在哪）——能撐到塊邊界就撐。

---

## ✅ 交接 checklist（離場前逐項確認）

```text
OUTGOING（交出方）
[ ] progress.md「進行中」指向當前塊，頂端有 RESUME HERE（下一動作=可執行）
[ ] development-log.md 最後一筆說清「做了什麼決策 / 卡在哪」+ 日期 + PRD 錨點
[ ] prd-checklist.md 動到的條目狀態正確（⬜/🟡/🟢），沒有做了忘改的
[ ] git 已 commit（WIP 也 commit，訊息點名停在哪/紅在哪），working tree 乾淨
[ ] 等裁決 / blocker 已在 dev-log 標記（[SKIPPED-PRD] 等），下一棒看得到

INCOMING（接手方）
[ ] 已讀 progress RESUME HERE → dev-log 最後 3 筆 → checklist 下一條 → git log/status
[ ] 已確認 DoD 環境能跑（lint / typecheck / test 起得來）
[ ] 已輸出回錨，與使用者確認對齊，且文件 vs git 無未解矛盾
[ ] 才開始動 production code
```

---

## 🔗 Related Compass sections

- [§3.2 追蹤文件三件套](../03_implementation/02_tracking_docs.md) — 交接的物理載體，這裡只是把它留在可冷讀狀態
- [§4.1 Definition of Done](../04_quality_gates/01_dod.md) — 接手第 5 步要確認的 DoD 環境
- [§9.1 誰來拍板](./01_who_decides.md) — 跨棒遇到等裁決項時的責任歸屬
- [§9 Collaboration index](./_index.md) — 多人 / 多 agent 協作地圖

---

## 📝 Status

v0.8.0 (Phase 3: original content)
