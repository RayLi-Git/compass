# §6.3 觀測性：log / metrics / tracing

> Part of [Compass](../../SKILL.md) §6 — Non-Functional Requirements.
> 一個沒有 log、沒有 metrics 的 production 服務不是「完成」，是「瞎了」——本章把觀測性釘進 DoD。

---

## 🔒 鐵律（Iron Rule）

> **觀測性是 production 服務 DoD 的一部分。功能寫完但「出事時你看不到任何訊號」= 未完成。**

「先上線，監控之後再補」是謊言。事故發生在補之前，補之後永遠是下一次。每一塊進 production 的功能，收尾時必須能回答兩個問題：

1. 它正常運作時，我怎麼**看得到**它在動？（log / metric）
2. 它壞掉時，我怎麼**第一時間知道**、並能**定位到哪一層**？（alert / trace）

答不出來 = 這塊還沒 done。

---

## 🪵 結構化 logging

純文字 `print("error happened")` 不是 log，是噪音。Production log 一律**結構化**（JSON 或 key=value），讓機器能 query。

### 一條 log 最少帶什麼

| 欄位 | 用途 |
|---|---|
| `timestamp` | ISO 8601，UTC |
| `level` | DEBUG / INFO / WARN / ERROR |
| `message` | 人讀的一句話，**不拼動態值進字串**（值放欄位） |
| `trace_id` / `request_id` | 串起同一次請求的所有 log（見 tracing 段） |
| `service` / `module` | 哪個服務、哪一層發的 |
| 業務 key | `user_id`、`order_id` 等**識別碼**（非 PII） |

### log level 怎麼選（不要全打 INFO，也不要全打 ERROR）

| Level | 何時用 | 會不會吵醒人 |
|---|---|---|
| `ERROR` | 請求失敗、需要人介入的異常 | 進 alert 池 |
| `WARN` | 降級成功、重試、逼近上限——**還沒壞但要盯** | 不 alert，看趨勢 |
| `INFO` | 業務里程碑（下單成功、付款完成） | 否 |
| `DEBUG` | 開發期細節，production 預設關 | 否 |

> 把可預期的失敗（如 404、表單驗證錯）打成 ERROR = 自製狼來了，真 ERROR 被淹沒。

### ❌ 永遠不准進 log（與 [§6.4 安全](./04_security.md) 同一條紅線）

- 密碼、token、API key、session id、私鑰
- 完整信用卡號、身分證字號、完整 email/手機（要記就 mask：`u***@x.com`）
- 完整請求 body / header（裡面常夾帶上述）
- 任何 PII 明文

> log 會被轉發、長期保存、被很多人看到、進備份。**寫進 log 的祕密 = 已外洩**。這是 Sentinel 資安紅旗之一：「金鑰／token 印進 log」。

**範例（FastAPI / structlog，示意，非強制框架）**

```python
log.info("order.created", order_id=order.id, user_id=user.id, amount=order.total)
# ❌ 不要這樣：
# log.info(f"user {user.email} paid with card {card.number}")
```

---

## 📊 Metrics：命名規範 + 四大黃金訊號

Log 回答「這一筆發生什麼」，metric 回答「整體現在健康嗎」。

### 命名規範

- 格式：`namespace.subsystem.unit`，全小寫，`_` 或 `.` 分隔，**一致**
- 帶單位後綴：`_seconds`、`_bytes`、`_total`（counter）
- 用 **label/tag** 切維度（`route`、`status`、`method`），**不要把值塞進 metric 名**

```
✅ http_request_duration_seconds{route="/orders", status="500"}
❌ http_request_duration_orders_500          # 維度爆炸，無法聚合
```

> ⚠️ label 基數（cardinality）會殺掉你的 metrics 後端。**不要拿 user_id、order_id 當 label**——那是 log 的工作，不是 metric 的。

### 四大黃金訊號（Golden Signals）

每個對外服務至少量這四項，缺一就有盲區：

| 訊號 | 量什麼 | 典型 metric |
|---|---|---|
| **Latency 延遲** | 請求耗時，**分 p50/p95/p99**，且**成功與失敗分開** | `*_duration_seconds` histogram |
| **Traffic 流量** | 每秒請求數 / QPS | `*_requests_total` counter |
| **Errors 錯誤** | 失敗率（5xx、例外、逾時） | `*_errors_total` / 由 status label 算 |
| **Saturation 飽和** | 資源逼近上限（CPU、記憶體、連線池、queue 長度） | `*_pool_in_use`、`queue_depth` |

> 平均延遲會騙你——p99 才是使用者實際在罵的那條。失敗請求若混進延遲統計，會把「快速失敗」誤判成「健康」。**latency 一定要按 success/error 分開。**

---

## 🔗 Tracing：跨服務追一條請求

當一次請求穿過多個服務（API → service → DB → 第三方），單一服務的 log 拼不出全貌。Tracing 用一個 **trace_id** 把整條路徑串起來。

最小要求：

- 入口（gateway / 第一個服務）生成 `trace_id`，**全程透傳**（HTTP header 如 `traceparent`、MQ message attribute）
- 每一層把 `trace_id` 寫進它的每一條 log
- 跨服務呼叫一律帶上，**不要在中途斷掉**

> 沒有 distributed tracing 之前的最低標：**至少讓 request_id 貫穿單一服務的所有 log**。連這個都沒有，事故時你只能逐檔猜。

採 OpenTelemetry 之類的標準（廠商中立）優於自綁某家 APM——換後端不用重寫埋點。具體選型仍以你專案 PRD / 既有基礎設施為準。

---

## ✅ Per-feature 觀測性 checklist

每塊進 production 的功能，收尾時逐項對：

- [ ] **成功路徑有 INFO log**（含業務識別碼 + trace_id），說得出「它在動」的證據
- [ ] **每個失敗分支有 ERROR/WARN log**，能定位是哪一層、哪個原因
- [ ] **log 結構化**，動態值在欄位不在字串
- [ ] **掃過一遍 log：零祕密、零 PII 明文**（對照 [§6.4](./04_security.md)）
- [ ] **四大黃金訊號可量**：這個 endpoint 的 latency(p95/p99) / traffic / error rate / 關鍵資源 saturation 都有 metric
- [ ] **latency 按 success/error 分開**，沒把失敗混進去
- [ ] **metric 命名合規**、無高基數 label
- [ ] **trace_id / request_id 貫穿**這塊涉及的所有 log 與下游呼叫
- [ ] **關鍵失敗有 alert**（error rate / saturation 越線會通知人，不是被動等使用者回報）
- [ ] **想得到：事故時靠這些訊號，幾分鐘能定位？** 答不出來就補到答得出來

> 任一項打不了勾，這塊就不是 done。觀測性不是加分題，是 [§4 Definition of Done](../04_quality_gates/01_dod.md) 對 production 服務的硬要求。

---

## 🔗 Related Compass sections

- [§6 NFR — Index](./_index.md)
- [§6.2 效能](./02_performance.md) — latency / saturation 量到了，才談得上優化
- [§6.4 安全](./04_security.md) — 「log 不准帶祕密/PII」是同一條紅線
- [§4.1 Definition of Done](../04_quality_gates/01_dod.md) — 觀測性如何併入 DoD

---

## 📝 Status

v0.5.0 (Phase 2: original content)
