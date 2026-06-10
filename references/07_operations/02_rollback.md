# §7.2 Rollback：出事後安全回退

> Part of [Compass](../../SKILL.md) §7 — Operations。
> 每次 deploy 上線前就要備好回退方案，不是凌晨三點臨場硬湊。

---

## 🎯 核心鐵律

**回退計畫必須在 ship 之前就存在。** 上線後才開始想「怎麼回退」已經太晚——那時你在壓力下、缺乏睡眠、監控紅成一片，做的每個決定都更容易出錯。

> 如果你答不出「這次 deploy 怎麼回退、回退要幾分鐘、誰按按鈕」，這個 deploy 還沒準備好上線。

對應 Sentinel 的安全網「撤退路線」：動既有 production 前，先確保有一條乾淨、已驗證、可在數分鐘內執行的退路。沒有退路就不要往前。

---

## 🔀 Deploy ≠ Release：用 feature flag 解耦

最強的回退手段，是讓「上線程式碼」和「啟用功能」變成兩件事。

| 概念 | 意思 | 回退方式 |
|---|---|---|
| **Deploy** | 程式碼進入 production 環境 | 需要重新部署舊版本（慢） |
| **Release** | 功能對使用者真正生效 | 關掉 flag（秒級，不需重部署） |

把新功能包在 feature flag 後面，出事時不必 rollback 整個版本，只要把 flag 關掉——這就是 **kill-switch**。

```python
# 範例（FastAPI）：功能藏在 flag 後面，出事直接關
if flags.is_enabled("new_checkout_flow", user=user):
    return new_checkout(cart)
return legacy_checkout(cart)   # flag 關掉 → 秒級回到舊路徑
```

**Flag 使用守則：**
- kill-switch flag 預設值必須是「關」或「安全的舊行為」（呼應 Sentinel 資安「預設安全」）
- 關 flag 的人不需要是工程師、不需要重新部署、不需要碰 git
- flag 開關記入 audit log（誰、何時、為什麼）
- 上線穩定後要排程**清掉舊 flag**，否則 flag 墳場會變成下一個技術債（YAGNI 反向：留著沒用的 flag 也是債）

---

## 🟦🟩 Blue-green 與 canary 基礎

兩種降低 deploy 爆炸半徑的部署策略，回退邏輯不同：

| 策略 | 做法 | 回退動作 | 適合 |
|---|---|---|---|
| **Blue-green** | 兩套完整環境，流量一次性切換 | 把 router 切回舊環境（blue） | 回退要快、要乾淨 |
| **Canary** | 新版本先吃 1% → 5% → 25% 流量 | 把流量比例調回 0% | 想先用小流量驗證 |
| **Rolling** | 逐台替換實例 | 反向 rolling 回舊版（較慢） | 資源受限 |

- **Blue-green** 的回退最乾淨：舊環境還活著，切回去即可，幾乎零延遲。但要付兩套環境的成本。
- **Canary** 的價值在「早期偵測」：壞東西只影響 1% 使用者時你就該攔住它，而不是等 100% 才發現。canary 階段必須**盯著指標**，否則只是把全量爆炸延後幾分鐘。

---

## ⚠️ Migration-rollback 陷阱：程式碼可退，資料未必

**這是回退裡最容易致命的盲點。** 你可以把程式碼切回舊版，但資料庫的 schema 變更和已寫入的資料**不會自動跟著回去**。

典型死法：

```
1. 部署 v2，migration 把欄位 full_name 拆成 first_name / last_name 並 DROP full_name
2. v2 出事，回退程式碼到 v1
3. v1 的 code 去讀 full_name → 欄位已經不存在 → 全站 500
   （而且這幾分鐘寫進去的 first/last 資料也回不去 full_name）
```

**根因**：破壞性 schema 變更（DROP / RENAME / NOT NULL）和程式碼回退耦合在一起，回退程式碼時資料層沒有對應的退路。

**解法**：用 §7.1 的 **expand / contract（擴張—收縮）**。先只做相容的擴張變更上線，等程式碼穩定後，下一個 deploy 才做收縮（刪舊欄位）。如此「回退程式碼」這個動作永遠不需要「回退資料」。

> 鐵律：**破壞性 migration 永遠不和啟用該變更的程式碼放在同一次 deploy。** 收縮步驟單獨成一個後續 deploy。詳見 [§7.1 Migration](./01_migration.md)。

---

## 📊 回退決策準則：什麼情況下按下按鈕

回退不能靠「感覺怪怪的」。上線前就先寫死觸發門檻，現場照表操課，不臨場辯論。

| 訊號 | 觸發回退的門檻（範例，依服務調整） |
|---|---|
| Error rate | 5xx 比例 > baseline + 1%，持續 > 2 分鐘 |
| Latency | p99 > SLO 上限，持續 > 5 分鐘 |
| 關鍵業務指標 | checkout 成功率 / 登入成功率掉 > X% |
| 飽和度 | DB 連線池 / queue 持續逼近上限且仍在惡化 |
| 資料正確性 | 出現任何資料毀損或寫入錯誤 → **立即回退，不等門檻** |

**決策原則：**
- **回退優先於 debug**：production 出事時，先恢復服務、再慢慢找根因。別在著火的房子裡查線路（呼應 Sentinel：先止血，根因事後復盤補追）。
- 門檻在 deploy 前談好，現場不重新討論「這算不算嚴重」。
- 指定一個有權拍板的人（roll-back owner），不要全員投票。
- 設**觀察窗**：deploy 後留一段時間（如 30 分鐘）主動盯指標，別 deploy 完就走人。

---

## 🛡️ 回退本身要先驗證過

最危險的回退，是**從來沒人演練過、按下去才發現它也壞了**的回退。

- 回退流程要在 staging 實際跑過一次，量出回退耗時。
- 確認舊版本的 artifact / image 還在、還能部署（別被自動清理刪掉了）。
- 確認回退後舊程式碼能正常讀現有資料（這正是 migration 陷阱的檢查點）。

---

## ✅ Pre-deploy 回退檢查清單

deploy 前逐項打勾，任一項打不了勾 → 這個 deploy 還沒 ready：

- [ ] 回退方法已寫下來（切 flag？切 blue-green？重部署舊版？）
- [ ] 回退預估耗時已知（秒級 / 分鐘級 / 小時級），且可接受
- [ ] 舊版本 artifact 仍可用、且回退流程在 staging 演練過
- [ ] 本次有破壞性 schema 變更嗎？→ 有的話確認已拆成 expand/contract，回退程式碼不需回退資料
- [ ] 新功能是否包在 feature flag / kill-switch 後面
- [ ] 回退觸發門檻已定義（error rate / latency / 業務指標的具體數字）
- [ ] roll-back owner 已指定（誰有權按、誰知道怎麼按）
- [ ] 監控與告警已就位，能在門檻被踩到時主動通知
- [ ] deploy 後觀察窗時間已排，有人會盯
- [ ] 回退後的驗證方式已知（怎麼確認「已經回到安全狀態」）

---

## 🔗 Related Compass sections

- [§7.1 Migration](./01_migration.md) — expand/contract，讓資料層也有退路
- [§7.3 Deployment](./03_deployment.md) — 部署流程本身
- [§7 Operations](./_index.md) — 本模組總覽
- [§6.3 Observability](../06_non_functional/03_observability.md) — 沒有監控就量不到回退門檻

---

## 📝 Status

v0.5.0 (Phase 2: original content)
