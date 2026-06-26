# §6.1 非功能需求 (NFR) 總覽：為何 PRD 常漏

> Part of [Compass](../../SKILL.md) §6 — 非功能需求 (Non-Functional Requirements)
> 為何 PRD 的功能列表寫滿、NFR 卻一片空白，以及如何在 DoR 階段就把它逼出來。

---

## 🎯 核心問題：PRD 結構性地過度規格化功能、欠規格化 NFR

大多數 PRD 長這樣：

- 「使用者可以建立訂單」→ 寫了三段、附 schema、附 wireframe
- 「訂單列表要快」→ **沒寫**。多快？P95 幾毫秒？幾筆資料下測？沒人說。

功能是「會不會做」，看得見、demo 得出來、PM 寫得出來。
NFR 是「做得夠不夠好」，看不見、要壓測才現形、PM 通常**沒意識到要寫**。

結果：功能 spec 詳到逐欄位，NFR 整類缺席。等到上線壓力一來才發現「原來沒人定義過目標」——而此時改的是架構，不是一行 if。

---

## 🚨 為何反向稽核（§11）救不了你

§11 的反向稽核機制（M007–M010）拿 PRD 的**功能清單**回頭比對實作：endpoint 列了沒、schema 欄位對不對、頁面缺不缺。

> 它逐項比對的是「PRD 寫了 → 實作做了沒」。
> **NFR 從來沒被寫進 PRD，所以反向稽核根本沒東西可比。** 它整類穿過漏洞，零告警。

這是 NFR 最危險的地方：**自動化防線對它無感**。功能漏實作會被 M008 抓；NFR 漏定義，沒有任何 gate 會亮。唯一的攔截點在更上游——DoR。

詳見 [§11 反向稽核工具鏈](../11_tooling/01_m007_to_m010.md)。

---

## 📋 Compass 追蹤的 NFR 類別

| 類別 | 一句話 | 漏了會怎樣 |
|---|---|---|
| ⚡ 效能 | P95/P99 延遲、吞吐、資料量級下的目標 | 沒目標就沒人優化；上線才發現列表 8 秒、查詢全表掃描 |
| 🔭 觀測性 | log / metric / trace / 告警 | 出事時兩眼一抹黑，只能猜；MTTR 失控 |
| 🔒 安全 | authN/authZ、輸入驗證、機密管理、PII | 一個 IDOR 或注入點，全表外洩；補的是信任邊界不是補丁 |
| 🟢 可用性 (SLA) | 目標可用率、降級策略、依賴失效行為 | 第三方一掛你整站陪葬，因為沒人定義「它死了我怎麼辦」 |
| ♿ a11y | 鍵盤、對比、ARIA、screen reader | 改完才知道整套元件不可用；retrofit a11y 是重寫不是微調 |
| 🌐 i18n | 文案外提、日期/數字/貨幣、RTL、複數規則 | 硬編字串散落全 codebase；要支援第二語言時等於重做 UI 層 |

六類各有專章：效能（[§6.2](02_performance.md)）、觀測性（[§6.3](03_observability.md)）、安全（[§6.4](04_security.md)）、a11y+i18n（[§6.5](05_accessibility_i18n.md)）、可用性/SLA（[§6.6](06_availability_sla.md)）。

---

## 🔑 KEY：NFR 必須在 DoR（§2.1）就攔下

這是本章唯一最重要的規則：

> **「PRD 沒寫效能目標」是一個要在寫 code 之前 flag 出來的 gap，不是壓測當天的驚喜。**

NFR 缺失的處理路徑，和功能 gap 走的是同一條 Sentinel 的「動手前協定」——向內問清楚、向外推影響範圍。差別只在：功能 gap 你看 PRD 就知道缺；NFR gap **PRD 上是一片空白，你得主動去問「這裡是不是該有個目標」**。

把它接進 [DoR 檢查清單](../02_definition_of_ready/01_dor_checklist.md)：DoR 不只看「功能寫齊沒」，還要看「NFR 有沒有被明確定義或明確標記為 N/A」。

「沒寫」和「不需要」是兩件事——
- ✅ 合格：「本功能無效能要求（內部後台、單一管理員、資料量 < 100 筆）」← 明確標 N/A
- ❌ 不合格：效能欄整段空白 ← 這是 gap，不是 N/A

空白要在 DoR 變成 [PRD 健檢報告](../02_definition_of_ready/02_prd_health_report.md)上的一條紅字。

---

## ✅ NFR present? 檢查清單（插進 DoR）

對每一條 PRD 功能，過一遍以下六問。**任一條答不出來 = gap，回頭問 PRD owner。** 你可以提一個標明「待確認」的合理起點值（[§6.2](02_performance.md) 對效能目標就這麼做），但**不可把腦補值當成既定目標靜默帶過**——最終值仍須 owner 裁決。

```text
[ ] ⚡ 效能：有沒有給出可量測目標？
      P95/P99 延遲？吞吐量？在多大資料量級下測？
      （答不出 → 不是「先不管」，是 flag 給 owner）

[ ] 🔭 觀測性：出事時看什麼？
      關鍵路徑有沒有 log？有沒有 metric？告警閾值定了沒？

[ ] 🔒 安全：信任邊界在哪？
      誰能呼叫？驗的是「有登入」還是「是本人」（IDOR）？
      輸入有沒有驗證？有沒有碰 PII / 機密？

[ ] 🟢 可用性 (SLA)：依賴掛了會怎樣？
      目標可用率？降級策略？第三方逾時 / 失敗的行為定義了沒？

[ ] ♿ a11y：（有 UI 才適用）
      鍵盤可達？對比達標？互動元件有語意/ARIA？

[ ] 🌐 i18n：（有面向使用者文案才適用）
      字串外提了沒？日期/貨幣/複數有沒有 locale 處理？要不要 RTL？
```

**判讀規則**：每一格只有三種合法狀態——

| 狀態 | 意思 | DoR 是否放行 |
|---|---|---|
| 🟢 有目標 | 寫了可量測的值 | ✅ 放行 |
| ⚪ 標 N/A + 理由 | 明確說「此功能不需要，因為 ___」 | ✅ 放行 |
| 🔴 空白 | 沒人想過 | ❌ 擋下，flag 成 gap |

---

## 🪤 陷阱：NFR 在進 production 前是隱形的

功能漏了，第一次跑就壞給你看——回饋即時。
NFR 漏了，**開發、測試、demo 全程一路綠燈**，因為：

- 效能：dev 機上 50 筆資料，當然快。production 50 萬筆才現形。
- 可用性：本地第三方 mock 永遠回 200，沒人測過它逾時。
- 觀測性：能 demo 的功能不需要 log；要 log 的是凌晨三點的 production。
- a11y / i18n：開發者用滑鼠、看英文，永遠不會自己踩到。

> 隱形 ≠ 不存在。它只是把帳記在 production 那天，連本帶利。

**範例**（FastAPI，非強制，僅示意 NFR 如何在 dev 隱形）：

```python
# dev 看起來完美。production 全表掃描，P95 飆到數秒。
@app.get("/orders")
def list_orders(db: Session):
    return db.query(Order).all()   # 沒分頁、沒索引提示、沒 limit
```

PRD 若有一行「列表 P95 < 200ms @ 10 萬筆」，這段在 DoR / code review 就會被質疑。沒有那行，它一路綠燈直到上線。

這就是為什麼 NFR 的攔截點必須往上游搬到 **DoR**，而不是寄望下游某個 gate 會接住——下游沒有 gate 接得住隱形的東西。

---

## 🧭 往下走

| 章節 | 內容 |
|---|---|
| [§6.2 效能](./02_performance.md) | 可量測效能目標怎麼定、怎麼接進 DoD |
| [§6.3 觀測性](./03_observability.md) | log / metric / trace / 告警的最小集 |
| [§6.4 安全](./04_security.md) | 信任邊界、輸入驗證、test-first 安全模組 |
| [§6.5 a11y / i18n](./05_accessibility_i18n.md) | 為何 retrofit 是重寫，怎麼一開始就內建 |
| [§6 模組索引](./_index.md) | 本資料夾全覽 |

---

## 🔗 Related Compass sections

- [§2.1 DoR 檢查清單](../02_definition_of_ready/01_dor_checklist.md) — NFR present? 清單的掛載點
- [§2.2 PRD 健檢報告](../02_definition_of_ready/02_prd_health_report.md) — NFR 空白如何呈現為紅字
- [§5.1 模糊 / bug / 缺漏處理](../05_conflict_handling/01_vague_bug_gap.md) — NFR 缺失走的同一條 gap 路徑
- [§11 反向稽核工具鏈](../11_tooling/01_m007_to_m010.md) — 為何它攔不到 NFR

---

## 📝 Status

`v0.5.0` (Phase 2: original content)
