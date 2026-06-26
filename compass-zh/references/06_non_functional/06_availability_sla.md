# §6.6 可用性與 SLA：依賴掛了會怎樣

> Part of [Compass](../../SKILL.md) §6 — 非功能需求（NFR）。
> 把「系統要穩」變成可量的目標（SLO / error budget），並為**每一個外部依賴**先定義「它死了我怎麼辦」。

---

## 🎯 定位

可用性是六類 NFR 裡最容易被當成「上線後再說」的一類——直到某個第三方掛掉、你整站陪葬，才發現**沒人定義過降級行為**。

本檔處理三件事：
1. 把可用性寫成可驗收的目標（SLA / SLO / error budget）。
2. 對**每個外部依賴**問「它逾時 / 掛掉 / 變慢時，我的系統怎麼反應」。
3. 把這些在 [§2.1 DoR](../02_definition_of_ready/01_dor_checklist.md) 就抓出來，不要等 production 事故。

---

## 1. SLA / SLO / Error Budget：先分清楚

| 詞 | 是什麼 | 誰看 |
|---|---|---|
| **SLA**（協議）| 對外承諾的可用率，違反有罰則（退費 / 賠償）| 客戶 / 合約 |
| **SLO**（目標）| 你內部設的目標，比 SLA 嚴一點當緩衝 | 工程團隊 |
| **SLI**（指標）| 實際量到的數字（成功率 / 延遲 / 正常運行時間）| 監控 |
| **Error Budget** | `1 − SLO`，允許「壞掉」的額度 | 決定還能不能冒險發版 |

**Error budget 的用法**：SLO 99.9% → 每月允許 ~43 分鐘 down。預算還有 → 可以大膽發版 / 做風險實驗；預算燒光 → 凍結功能，只准修穩定性。這把「要不要上這個險」從吵架變成看數字。

### 可用率的「幾個 9」對照（先有感）

| 可用率 | 每月允許停機 | 適合 |
|---|---|---|
| 99%（兩個 9）| ~7.2 小時 | 內部工具 |
| 99.9%（三個 9）| ~43 分鐘 | 一般 SaaS |
| 99.95% | ~22 分鐘 | 付費關鍵服務 |
| 99.99%（四個 9）| ~4.4 分鐘 | 金流 / 基礎設施 |

> ⚠️ 每多一個 9，成本與複雜度**指數上升**。別預設追四個 9——先問 PRD / 業務「停機一小時真正的代價是多少」，再回推需要幾個 9。沒寫 → 這是 [§2.1 DoR](../02_definition_of_ready/01_dor_checklist.md) 的缺口。

---

## 2. 依賴失效行為：每個外部依賴都要定義

**鐵律：每多接一個外部依賴（DB / 第三方 API / 訊息佇列 / 快取），就多一個「它掛了怎麼辦」要回答。** 答不出來 = DoR 缺口。

對每個依賴，定義五個行為：

| 機制 | 問題 | 預設做法 |
|---|---|---|
| **Timeout** | 它卡住不回，我要等多久？ | **一律設逾時**。沒設 timeout = 一個慢依賴拖垮你所有執行緒 |
| **Retry** | 失敗要不要重試？ | 只對「暫時性失敗」重試，且**指數退避 + 上限 + jitter**。對非冪等操作重試前先確認冪等 |
| **Circuit Breaker** | 它持續掛，我要不要停止打它？ | 連續失敗達閾值 → 跳閘，直接 fail fast 一段時間，別讓請求堆積 |
| **Fallback** | 它不可用時，我回什麼？ | 回快取的舊值 / 預設值 / 部分結果 / 明確的降級訊息——**不是 500** |
| **Graceful Degradation** | 哪些功能可以「先關掉但主流程還活」？ | 推薦欄掛了 → 隱藏推薦，不要讓首頁整個 500 |

### 範例（依賴失效決策，逐依賴註解）

```python
# 依賴：推薦服務 recommendations-api（非關鍵）
# Timeout: 300ms（首頁不能為了推薦等它）
# Retry: 不重試（非關鍵，重試只會拖更久）
# Circuit Breaker: 5 次連續失敗 → 跳閘 30s
# Fallback: 回空清單 → 前端隱藏推薦區塊
# Degradation: 首頁其他區塊照常 render
async def get_homepage(user):
    try:
        recs = await rec_client.get(user.id, timeout=0.3)
    except (TimeoutError, CircuitOpen):
        recs = []                      # ← fallback，不是讓整頁炸
    return render(user, recommendations=recs)
```

> 對照：**關鍵依賴**（如金流、主 DB）失效時，正解通常不是 fallback 假裝成功，而是**明確 fail closed + 清楚錯誤 + 告警**（見 [§6.4 安全](04_security.md) 的 secure-by-default）。降級的前提是「這塊不影響正確性」。

---

## 3. Bulkhead：別讓一個依賴拖垮全部

艙壁（bulkhead）原則：把資源（連線池 / 執行緒）**按依賴隔開**，這樣一個依賴慢掉，只吃光它自己那池，不會耗盡整個服務的資源。

- 推薦服務一池、金流一池、主 DB 一池——互不搶。
- 沒有 bulkhead：一個慢依賴 → 執行緒全卡在它身上 → 連健康的依賴都沒執行緒可用 → 雪崩。

---

## 4. 插進 DoR 的可用性五問

對每個會碰外部依賴 / 有可用性要求的功能，[§2.1 DoR](../02_definition_of_ready/01_dor_checklist.md) 補問：

- [ ] 這功能依賴哪些外部服務？（列出來）
- [ ] 每個依賴的 timeout 設多少？（沒設 = 紅旗）
- [ ] 每個依賴掛掉時的 fallback 行為是什麼？（fail closed 還是降級？）
- [ ] PRD 有沒有定可用率目標（SLA/SLO）？沒有 → 標缺口問 owner（見 [§6.1](01_nfr_overview.md)）
- [ ] 哪些功能屬「可降級」、哪些屬「必須正確否則 fail closed」？

---

## 5. 怎麼驗證（寫進 DoD）

可用性不是「希望它穩」，要能證明：

- **混沌測試（chaos）**：在測試環境**主動讓依賴逾時 / 回 500 / 變慢**，看你的 fallback / circuit breaker 有沒有真的生效。沒測過的 fallback 等於不存在。
- **超時實測**：別只在 code 設 timeout，要實際模擬慢依賴確認它真的在設定時間放棄。
- **降級路徑可見**：每條「依賴掛掉」的路徑，至少手動跑過一次，眼睛看到降級行為而不是 500。

> 反面教材：本地第三方永遠用 mock 回 200，從沒測過它逾時——上線第一次第三方抖動就整站掛。

---

## 🔗 Related Compass sections
- [§6.1 NFR 總覽](01_nfr_overview.md) — 可用性是六類 NFR 之一，本檔是它的專章
- [§7.2 Rollback](../07_operations/02_rollback.md) — 服務層級失效的回退；與依賴失效降級互補
- [§6.3 觀測性](03_observability.md) — SLI 要靠 metrics 量；error budget 要靠監控算
- [§6.4 安全](04_security.md) — 關鍵依賴失效要 fail closed（secure-by-default）
- [§2.1 DoR](../02_definition_of_ready/01_dor_checklist.md) — 可用性目標與依賴失效行為要在開工前抓

## 📝 Status
v0.9.0 (Phase 4: completes the §6 NFR set — the SLA/availability chapter deferred from Phase 2).
