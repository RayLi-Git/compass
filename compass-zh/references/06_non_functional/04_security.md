# §6.4 安全：beyond test-first

> Part of [Compass](../../SKILL.md) §6 — 非功能需求（NFR）。
> §3.3 / DoR 已要求 Auth / authz / PII test-first；本檔處理「其餘所有功能」的逐功能安全審查門。

---

## 🎯 定位

test-first 只蓋住三個高敏感模組（Auth / 權限 / PII），但**注入、SSRF、XSS、IDOR 不挑模組**——任何吃外部輸入、發外部請求、拼字串、回傳資料給瀏覽器的功能都可能中招。

本檔提供一個 **per-feature 安全審查門**：每實作一塊功能，過一遍 OWASP 對照表 + STRIDE-lite，30 秒內判斷「這塊要不要補安全工作」。不是寫一份威脅模型文件，是當作 DoD 前的一道快篩。

> 對應 Sentinel 的「資安五大類」思考：#不信任輸入、#認證授權、#最小權限、#敏感資料、#預設安全。本檔把它落成可勾的清單。

---

## ✅ 觸發條件：哪些功能必須過這道門

| 功能特徵 | 必過審查門 |
|---|---|
| 吃 `req.body` / `query` / `params` / 上傳檔 / webhook | ✅ |
| 拼 SQL / shell / 路徑 / 模板字串 | ✅ |
| 把資料 render 進 HTML / 回傳前端 | ✅ |
| 用使用者給的 URL / ID 發請求或抓資源 | ✅ |
| 讀寫「屬於某使用者」的資源 | ✅ |
| 碰金鑰 / token / 密碼 / 第三方憑證 | ✅ |
| 純內部計算、不碰 I/O、不碰外部輸入 | ⛔ 跳過 |

只要中一條 → 過下方 OWASP 對照 + STRIDE-lite。全不中 → 直接走 DoD。

---

## 🔟 OWASP Top 10 快速對照（審查 checklist）

逐項問「這塊功能有沒有這個面」，有就勾，勾了就要有對應防護。

- [ ] **A01 權限失效 / IDOR** — 有用 URL/body 的 ID 取資源嗎？查的時候有沒有**同時驗 `resource.owner == current_user`**？只驗「有登入」不算。
- [ ] **A02 加密失效** — 敏感資料落地有加密？傳輸走 HTTPS？密碼用 bcrypt/argon2 而非 MD5/SHA？
- [ ] **A03 注入** — 拼 SQL / shell / LDAP / NoSQL query 了嗎？一律參數化 / ORM 綁定，**永不字串拼接**。
- [ ] **A04 不安全設計** — 這功能本身的流程有沒有邏輯漏洞（如改價、重放、負數數量）？
- [ ] **A05 安全設定錯誤** — debug mode、預設密碼、過寬 CORS、目錄列表、堆疊軌跡外洩？
- [ ] **A06 過時/有漏洞元件** — 新加的依賴查過 CVE 嗎？版本鎖了嗎？
- [ ] **A07 認證失效** — 有暴力破解防護？session 過期？token 會撤銷？
- [ ] **A08 完整性失效** — 反序列化不信任資料？CI/CD 拉未驗證來源？
- [ ] **A09 紀錄/監控失效** — 安全事件（登入失敗、權限拒絕）有 log？log 裡**沒有**密碼/token？
- [ ] **A10 SSRF** — 用使用者給的 URL 發請求嗎？有沒有擋內網網段 / metadata endpoint（`169.254.169.254`）？

> 不是每項都要做。是每項都要**問**——勾不到的記為「不適用」，勾到的進待辦。

---

## 🛡️ STRIDE-lite：逐功能威脅自問

不需要畫完整威脅模型。每塊功能花 1 分鐘，對 6 個面各問一句：

| 面向 | 一句話自問 | 沒答好的後果 |
|---|---|---|
| **S 欺騙 Spoofing** | 我怎麼確定請求方是他宣稱的人？ | 假冒身分 |
| **T 竄改 Tampering** | 資料在傳輸/儲存中可被改嗎？改了我察覺得到嗎？ | 資料被動手腳 |
| **R 否認 Repudiation** | 出事後查得到「誰、何時、做了什麼」嗎？ | 無法追責 |
| **I 資訊洩漏 Information disclosure** | 這條路徑會不會回傳超過該看的資料 / 錯誤訊息洩底？ | 越權讀取 |
| **D 阻斷 Denial of service** | 能用一個請求拖垮它嗎（無分頁、無限迴圈、巨檔）？ | 服務癱瘓 |
| **E 提權 Elevation of privilege** | 一般使用者能不能摸到 admin 能力 / 別人的資源？ | 越權操作 |

**判讀規則**：任一面向答不出來或答案是「會」→ 該面向進待辦，不能直接 DoD。

### 範例（FastAPI，逐功能 STRIDE-lite 註解）

```python
# Feature: GET /orders/{order_id}
# S: 靠 JWT 驗身分 ✅
# T: HTTPS only ✅
# R: access log 記 user_id + order_id ✅
# I: ⚠️ 回傳前未過濾——order 含 internal_cost 欄位 → 待辦：DTO 白名單
# D: ⚠️ 無 rate limit → 待辦
# E: ⚠️ 只驗登入沒驗 owner → 待辦（IDOR，最優先）
@router.get("/orders/{order_id}")
async def get_order(order_id: int, user=Depends(current_user)):
    order = await repo.get(order_id)
    if order.user_id != user.id:        # ← E 的修正：驗 owner
        raise HTTPException(404)         # 用 404 不用 403，避免洩漏存在性
    return OrderDTO.from_orm(order)      # ← I 的修正：白名單欄位
```

---

## 🔑 機密處理（secrets handling）

絕對紅線，違反即停手重做：

- [ ] 金鑰 / 密碼 / token **不寫死在 code**、不進 git（含 commit 歷史）。
- [ ] 一律從環境變數 / secret manager 注入；repo 只留 `.env.example`（無真值）。
- [ ] `.env`、`*.pem`、`credentials.*` 已在 `.gitignore`。
- [ ] **log / 錯誤訊息 / 回應 body 不印 secret**（含部分遮罩前的原值）。
- [ ] token 有過期時間；不設「永不過期」。
- [ ] 第三方 webhook / callback 驗簽章，不裸信來源。

> 若發現 secret 已進 git 歷史 → 不是「下次 commit 拿掉」就好：**輪換金鑰**（rotate），舊值視為已洩漏。

---

## 🔒 預設安全（secure-by-default）

設計選擇在「方便」與「安全」衝突時，預設選安全：

| 反模式（fail open） | 預設安全（fail closed） |
|---|---|
| `try { check() } catch { 放行 }` | catch → 拒絕 + 記錄 |
| 找不到權限規則 → 允許 | 找不到規則 → 拒絕 |
| 新欄位預設回傳給前端 | 預設不回傳，白名單才回 |
| 給 admin / 全域權限圖方便 | 給剛好夠用的最小權限（#最小權限） |
| 錯誤回傳完整堆疊 | 對外回通用訊息，細節只進內部 log |
| CORS `*` | 明列允許來源 |

---

## 🚦 審查門結論（接到 DoD 之前）

跑完這道門，產出三選一：

1. 🟢 **全數不適用 / 已防護** → 記一行「安全審查：無新增風險」，進 [DoD](../04_quality_gates/01_dod.md)。
2. 🟡 **有待辦但非阻斷** → 列入 tracking doc，本塊完成前修掉（Compass 不分階段 → 不留「之後再補安全」）。
3. 🔴 **碰到 Auth / 權限 / PII** → 退回 [DoR](../02_definition_of_ready/01_dor_checklist.md) 的 test-first 要求，先寫測試再實作。

> 安全待辦**不可批次累積到最後**。每塊功能的安全洞，在那塊 commit 前清掉——這是 §6.4 對 compare-fix loop 的延伸。

---

## 🔗 Related Compass sections

- [§6 NFR 模組總覽](./_index.md) — 安全在 NFR 中的定位
- [§6.3 可觀測性](./03_observability.md) — STRIDE 的 R（否認）/ A09（紀錄）落地處
- [§4.1 DoD](../04_quality_gates/01_dod.md) — 安全審查門接在 DoD 之前
- [§2.1 DoR checklist](../02_definition_of_ready/01_dor_checklist.md) — Auth/authz/PII 的 test-first 要求源頭

---

## 📝 Status

v0.5.0 (Phase 2: original content)
