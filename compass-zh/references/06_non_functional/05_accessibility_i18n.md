# §6.5 無障礙 (a11y) 與國際化 (i18n)

> Part of [Compass](../../SKILL.md) §6 — 非功能性需求 (NFR)。
> a11y 與 i18n 設計時內建幾乎免費，事後補做是地獄——所以它們屬於 DoR，不是上線前的補丁。

---

## 🎯 核心立場

兩者的共同性質：**設計階段內建 = 便宜；上線後回補 = 殘酷。**

| 維度 | 設計時內建 | 事後回補 |
|---|---|---|
| a11y | 語意 HTML + 鍵盤流，幾乎零成本 | 重寫 DOM、補 ARIA、重測每個元件 |
| i18n | 字串外置 + locale-aware 格式化 | 全 codebase 撈 hardcode、改版面、處理 RTL |

結論：**a11y / i18n 是否在範圍內，必須在 DoR 拍板**（見 [§2.1 DoR checklist](../02_definition_of_ready/01_dor_checklist.md)）。PRD 沒寫不代表不用做——代表「範圍未定義」，必須回去問。

---

## 🚩 DoR 攔截規則（PRD 對 a11y/i18n 沉默時）

PRD 沒提 a11y 或 i18n，不要當作「不用做」直接跳過。這是 PRD 缺漏，走 [§5.1 模糊/缺漏處置](../05_conflict_handling/01_vague_bug_gap.md)，在 DoR 標記並反問：

- 「這個 UI 要不要支援鍵盤操作 / 螢幕報讀器？」（a11y 範圍）
- 「未來會不會出多語言 / 多地區版本？」（i18n 範圍）
- 「有沒有法規要求？」（部分產業 a11y 是法律義務，非選配）

得到答案前，至少把**字串外置**與**語意 HTML** 當預設做掉——這兩項即使最後不上 i18n/a11y 也不虧，反向回補才虧。

---

## ♿ a11y：WCAG 基線

不背完整 WCAG。記住可在 PR 直接檢查的五條：

| 項目 | 規則 | 快速自檢 |
|---|---|---|
| 鍵盤可達 | 所有互動元素 Tab 可達、Enter/Space 可觸發、焦點順序合理 | 拔掉滑鼠走一遍 |
| 語意 HTML | 用 `<button>`/`<nav>`/`<label>` 而非 `<div onClick>` | 看 DOM 有沒有一堆裸 div 當按鈕 |
| 對比度 | 文字對背景 ≥ 4.5:1（大字 ≥ 3:1） | 用對比檢查器量一次 |
| 替代文字 | `<img>` 有 `alt`；裝飾圖 `alt=""` | grep 沒 alt 的 img |
| ARIA 兜底 | 原生語意不足才補 ARIA，且 role/state 要正確 | 沒有原生標籤時才碰 ARIA |

**鐵律：ARIA 是最後手段，不是第一手段。** 一個正確的 `<button>` 勝過 `<div role="button" tabindex="0" aria-pressed>` 兜出來的東西。錯的 ARIA 比沒有 ARIA 更糟。

### 每個 UI feature 的 a11y checklist

新增任何可互動 UI 時逐項過：

- [ ] 純鍵盤可完成整個操作流程（含開關 modal、提交表單）
- [ ] 焦點狀態可見（不是只有 `outline: none`）
- [ ] 表單欄位都有 `<label>` 關聯（`for`/`id` 或包裹）
- [ ] 圖片/icon 有文字替代；純裝飾標 `alt=""`/`aria-hidden`
- [ ] 顏色不是唯一資訊載體（錯誤不能只靠紅色，要有文字/icon）
- [ ] 動態內容變化有通知（`aria-live` 用於 toast/錯誤）
- [ ] Modal 開啟時焦點被困在內部、關閉後歸還觸發元素

### 範例（React/TS，非強制）

```tsx
// ❌ 螢幕報讀器讀不到、鍵盤點不到
<div className="btn" onClick={handleDelete}>刪除</div>

// ✅ 原生語意，鍵盤與報讀器免費拿到
<button type="button" onClick={handleDelete}>刪除</button>

// 錯誤訊息：顏色 + 文字 + live region
<p role="alert" className="error">電子郵件格式不正確</p>
```

---

## 🌐 i18n：四大支柱

### 1. 字串外置（no hardcoded copy）

UI 文案一律走資源檔/翻譯函式，不直接寫在元件裡。

```tsx
// ❌ hardcode，之後撈到死
<h1>歡迎回來</h1>

// ✅ key 化，文案集中
<h1>{t("home.welcome_back")}</h1>
```

紅旗：PR 裡出現任何面向使用者的字面字串（按鈕、標題、錯誤、email 模板）。

### 2. Locale-aware 格式化

日期、數字、貨幣**絕不手動拼**。用平台的 locale API。

| 資料 | 錯誤做法 | 正確做法 |
|---|---|---|
| 日期 | `` `${y}/${m}/${d}` `` | `Intl.DateTimeFormat(locale)` |
| 數字 | 手動塞千分位 | `Intl.NumberFormat(locale)` |
| 貨幣 | `` `$${n}` `` | `Intl.NumberFormat(locale, {style:"currency", currency})` |
| 時區 | 存本地時間 | 存 UTC，顯示時轉 locale 時區 |

### 3. 複數形（pluralization）

別用 `count === 1 ? "item" : "items"` 硬切。不同語言複數規則不同（有些語言 3 種以上形式）。用 ICU MessageFormat / `Intl.PluralRules`。

```ts
// ❌ 只對英文/中文勉強成立
const label = `${n} ${n === 1 ? "file" : "files"}`;

// ✅ 交給 plural rules
t("file_count", { count: n }); // 翻譯檔內定義 one/other/...
```

### 4. RTL 覺知

支援阿拉伯文/希伯來文時版面會鏡像。CSS 用邏輯屬性，不用方向屬性。

| 不要 | 改用 |
|---|---|
| `margin-left` | `margin-inline-start` |
| `text-align: left` | `text-align: start` |
| `left: 0` | `inset-inline-start: 0` |

即使現在只做 LTR，養成用 logical properties 的習慣，未來開 RTL 幾乎零改動。

### i18n checklist

- [ ] 無面向使用者的 hardcode 字串
- [ ] 日期/數字/貨幣全走 `Intl` 或等效 locale API
- [ ] 時間以 UTC 儲存
- [ ] 複數走 plural rules，不靠 `=== 1`
- [ ] 版面用 logical properties（為 RTL 留路）
- [ ] 字串不靠拼接組句（語序因語言而異，整句一個 key）

---

## ⚖️ 決策程序：要不要現在做？

```
PRD 有寫 a11y/i18n 範圍？
├─ 有 → 照 PRD 範圍實作，列入 DoD
└─ 沒有 → DoR 反問使用者（見上方攔截規則）
          ├─ 確認要做 → 補進 PRD 範圍，當需求做
          ├─ 確認不做 → 仍把「字串外置 + 語意 HTML」當預設
          └─ 未定 → 標 ⚠️待裁決，預設做掉低成本兩項，不做高成本回補項
```

不適用 YAGNI 直接砍 i18n/a11y——「字串外置、語意 HTML、logical properties」是低成本前置投資，砍掉等於把未來的回補成本鎖死（見 [§3.5 YAGNI](../03_implementation/05_yagni.md)）。

---

## 🔗 Related Compass sections

- [§6 NFR overview](./01_nfr_overview.md) — a11y/i18n 在 NFR 全景中的位置
- [§2.1 DoR checklist](../02_definition_of_ready/01_dor_checklist.md) — 範圍在這裡拍板
- [§5.1 模糊/Bug/缺漏處置](../05_conflict_handling/01_vague_bug_gap.md) — PRD 沉默時的反問流程
- [§4.1 DoD](../04_quality_gates/01_dod.md) — 確認的 a11y/i18n 項目納入完成定義

## 📝 Status

v0.5.0 (Phase 2: original content)
