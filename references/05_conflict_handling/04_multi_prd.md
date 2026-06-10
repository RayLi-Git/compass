# §5.4 多 PRD 依賴

> Part of [Compass](../../SKILL.md) §5 — Conflict Handling.
> 一個產品常拆成多份子 PRD（auth、billing、notifications…），彼此有依賴與共用介面；本檔規範如何排序與保持一致。

---

## 1. 問題本質

子 PRD 之間不是平行的，是有向的。

- auth-PRD 定義 token / user_id；billing-PRD 消費它。
- 若先做 billing，你只能**猜** auth 的介面 → 等 auth 真的寫出來，介面對不上 → billing 重工。
- 猜出來的介面還會反向污染：billing 的假設被當成既成事實，逼 auth 去遷就一個本不該長這樣的介面。

> 核心：**被依賴的先做，依賴別人的後做。** 違反這條的代價不是延遲，是重工。

---

## 2. 依賴盤點（動手前必做）

開工前先畫子 PRD 的依賴圖，別憑印象排。

### 2.1 建依賴圖

逐份子 PRD 問兩題：

1. 它**消費**哪些別份 PRD 定義的東西？（→ 它依賴誰）
2. 它**定義**哪些別份 PRD 會用的東西？（→ 誰依賴它）

把答案連成有向圖（A → B 表示 B 依賴 A）。

### 2.2 標出共用契約（shared contracts）

依賴幾乎都透過「共用契約」傳遞。逐項列出並指明 **owner PRD**：

| 契約類型 | 範例 | owner（定義方） | consumer（消費方） |
|---|---|---|---|
| 身分 token | `access_token` 結構與簽章 | auth-PRD | billing / notifications |
| 實體 ID | `user_id` 型別與生命週期 | auth-PRD | 幾乎所有人 |
| 事件 schema | `OrderPaid` event 欄位 | checkout-PRD | notifications-PRD |
| 共用資料模型 | `Product` 欄位定義 | catalog-PRD | cart / checkout |

> 每個共用契約**只能有一個 owner PRD**。兩份 PRD 都宣稱自己定義同一個 `user` → 那是衝突，走 §5.3。

---

## 3. 排序規則

排序 = 對依賴圖做拓撲排序，本質與 [§3.3 實作順序](../03_implementation/03_implementation_order.md) 同構，只是顆粒度從「檔案/模組」升到「整份 PRD」。

```
基礎 / 共用 PRD 先  →  葉節點 / 功能 PRD 後
(auth, core data model)     (個別 feature)
```

判定規則：

- ✅ **被最多人依賴的先做**：auth、核心資料模型、共用事件匯流排。
- ✅ **無出向依賴的葉節點最後做**：只消費不被消費的純功能 PRD。
- ✅ **同層（互不依賴）可並行**，但仍須共用同一份契約定義。
- ❌ 出現環（A 依賴 B 且 B 依賴 A）→ 停手。環代表契約歸屬沒切乾淨，先拆契約再排，不要硬排。

> 排序產物寫進 progress 記錄，當成跨 PRD 的「實作順序表」。

---

## 4. 共用介面紀律（contract discipline）

一旦 PRD-A 定義了 PRD-B 依賴的介面，**那個介面就是契約**，不是 A 的私有實作細節。

改契約 = 改合約，不是改 code。流程：

1. 任何對共用契約的修改，先觸發 [§5.2 PRD 變更協定](./02_prd_change.md)（影響評估 + 等裁決）。
2. 因為改動跨文件，同時走 [§5.3 跨文件衝突](./03_cross_document.md)：列出**所有** consumer PRD，逐一評估衝擊。
3. 未同步所有 consumer 前，契約視為未定，依賴它的 PRD 不得宣告完成（[§4.1 DoD](../04_quality_gates/01_dod.md) 不通過）。

紅線檢查（出現任一即停）：

- [ ] 改了 owner PRD 的共用欄位，但沒回查 consumer 清單
- [ ] consumer 私自 fork 一份契約定義「先擋著用」
- [ ] 契約用 `any` / 寬鬆型別蒙混，把對不上的問題往後拖

---

## 5. 一致性檢查

跨子 PRD 最隱蔽的偏差不是介面對不上，是**詞彙悄悄分岔**。

| 檢查項 | 要求 | 不一致時 |
|---|---|---|
| 同名同義 | auth-PRD 的 `user` == billing-PRD 的 `user` | 標記 → 走 §5.3 收斂 |
| 同義同名 | 別一份叫 `account`、一份叫 `user` 卻指同物 | 統一命名，留映射註記 |
| 邊界一致 | 「已停用 user」在各 PRD 行為定義一致 | 以 owner PRD 為準 |
| 狀態機一致 | 訂單狀態值集合跨 PRD 相同 | 對不上即契約衝突 |

實務做法：維護一份跨 PRD 的詞彙表（glossary），每個共用名詞標 owner 與定義。新子 PRD 進場時（見 [§3.1 PRD 吸收](../03_implementation/01_prd_intake.md)）先比對 glossary，命中分岔立即標記。

> 詞彙分岔不要自己「合理推斷哪個對」。兩份 PRD 對同一概念給了不同定義，是 PRD 之間的衝突 → 走 [§5.3 跨文件衝突](./03_cross_document.md) 由使用者裁決。

---

## 6. 範例：電商四份子 PRD

假設產品拆成 auth / catalog / cart / checkout 四份子 PRD。

依賴關係：

```
auth ──────────────┐
                   ▼
catalog ──► cart ──► checkout
```

- **auth**：定義 `user_id`、`access_token`。被所有人依賴，無出向依賴。
- **catalog**：定義 `Product`（id / price / 庫存）。被 cart、checkout 依賴。
- **cart**：消費 auth(`user_id`) + catalog(`Product`)；定義 `Cart`。被 checkout 依賴。
- **checkout**：消費以上全部；定義 `OrderPaid` 事件。葉節點。

拓撲排序得到實作順序：

```
1. auth      （token + user_id 契約先釘死）
2. catalog   （Product 契約）
3. cart      （依賴 1+2）
4. checkout  （依賴 1+2+3，產出事件給未來的 notifications-PRD）
```

共用契約清單：

| 契約 | owner | consumers |
|---|---|---|
| `user_id` / `access_token` | auth | catalog?, cart, checkout |
| `Product` | catalog | cart, checkout |
| `Cart` | cart | checkout |
| `OrderPaid` event | checkout | (未來) notifications |

決策示意：若做到 checkout 時發現需要 catalog 的 `Product` 多一個 `tax_rate` 欄位 — 那是改 catalog 的共用契約，**不在 checkout 裡偷加**。走 §5.2 + §5.3：評估 cart 是否受影響、更新 catalog-PRD、等裁決，再回來。

---

## 🔗 Related Compass sections
- [§5.3 跨文件衝突](./03_cross_document.md) — 共用契約改動 / 詞彙分岔的收斂流程，本檔多處回指
- [§5.2 PRD 變更協定](./02_prd_change.md) — 改共用契約即觸發的變更影響評估
- [§3.3 實作順序](../03_implementation/03_implementation_order.md) — 本檔排序規則的同構來源（顆粒度從模組升到 PRD）
- [§3.1 PRD 吸收](../03_implementation/01_prd_intake.md) — 新子 PRD 進場時比對詞彙表的時機
- [§4.1 DoD](../04_quality_gates/01_dod.md) — 契約未同步完成前，依賴方不得宣告完成

## 📝 Status
v0.5.0 (Phase 2: original content).
