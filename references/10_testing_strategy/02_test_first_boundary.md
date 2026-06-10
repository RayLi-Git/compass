# §10.2 test-first 的真正邊界 + coverage 目標

> Part of [Compass](../../SKILL.md) §10 — Testing Strategy.
> test-first 在哪裡真的回本、哪裡只是儀式；coverage 是地板偵測器，不是品質證明。

[§4.1 DoD](../04_quality_gates/01_dod.md) 與 DoR 對 Auth / 權限 / PII **強制** test-first。
這份檔處理剩下的灰色地帶：除了安全模組，**還有哪裡該 test-first**，哪裡 test-first 純粹是 overhead，以及 coverage 數字到底證明了什麼、沒證明什麼。

兩個常見的反向錯誤：
- 把「強制 test-first」誤讀成「所有東西都 test-first」→ 在丟棄式原型上寫測試，浪費。
- 把「coverage 80%」當成過關證書 → 數字漂亮但一個 assert 都沒有，等於沒測。

---

## 1️⃣ test-first 在哪裡回本（安全模組之外）

test-first 的價值不是「測試」，是**逼你先把行為講清楚再寫**。值不值得，看「行為定義的難度」高不高。

| 場景 | test-first？ | 為什麼 |
|---|---|---|
| Auth / 權限 / PII | ✅ 強制（[§4.1](../04_quality_gates/01_dod.md)） | 出錯成本最高、靠肉眼看不出漏洞 |
| 複雜業務邏輯（計費、折扣、稅務、排程） | ✅ 強烈建議 | 規則多、邊界多、改一處連動多處 |
| 有刁鑽 edge case（off-by-one、時區、空集合、溢位） | ✅ 強烈建議 | 邊界正是 bug 溫床，先寫 case 才不會漏 |
| 修 bug | ✅ red test 先行 | 見 [§8.2](../08_brownfield/02_bug_fix.md)，red test 證明你真的重現了 |
| 演算法 / 純函式（輸入→輸出明確） | ✅ 划算 | 無副作用、好斷言，test-first 幾乎零摩擦 |

> **判準一句話**：如果你**寫之前說不清楚「正確」長什麼樣**，就 test-first——寫測試會逼你想清楚。

---

## 2️⃣ test-first 在哪裡是 overhead

不是偷懶，是這些場景「行為定義」便宜到測試先寫反而拖慢，或測試本身沒有保護力。

| 場景 | test-first？ | 改用 |
|---|---|---|
| 丟棄式原型 / spike | ❌ | 跑通就好，驗證完即丟（見 [§3.5 YAGNI](../03_implementation/05_yagni.md)） |
| 純 glue（把 A 的輸出接到 B、轉個格式） | ❌ | 一條 integration / smoke 測串接點即可 |
| 平凡 CRUD（無業務規則、框架直出） | ⚠️ 低優先 | 測「接線對不對」，別測 ORM 本身 |
| 配置 / 常數 / DTO 宣告 | ❌ | 沒邏輯就沒東西可斷言 |
| 第三方函式庫的行為 | ❌ | 那是它的測試，不是你的 |

⚠️ 紅旗：你發現自己在寫「測試 framework 有沒有照它文件運作」的測試——停。那不是你的職責邊界。

> 原型例外**不適用** Auth/PII：原型一旦碰真實使用者憑證或 PII，立刻升回強制 test-first，不再是丟棄式。

---

## 3️⃣ coverage 目標：80% 是啟發式，不是法律

「全專案 80% coverage」是一個**方便的預設**，不是每個檔案都該達到的硬線。逐區間調：

| 區域 | 合理目標 | 理由 |
|---|---|---|
| 付款 / 金額 / 權限判斷 | 趨近 100%（含分支） | 錯一條分支就是真金白銀或越權 |
| 核心業務邏輯 | 85–95% | 連動廣，回歸成本高 |
| 一般應用層 | 70–80% | 80% 啟發式的來源區間 |
| 生成碼 / boilerplate / DTO | 低或排除 | 測它＝測產生器，無資訊量 |
| UI 膠水 / 框架樣板 | 低 | 投報率差，靠 smoke 兜底 |

**反模式**：為了把全域數字從 78% 推到 80%，去替 getter/DTO 補一堆無斷言測試。數字達標了，付款邏輯那條沒測的分支還在。**你優化了指標，沒優化安全。**

---

## 4️⃣ 為什麼 coverage 高 ≠ 安全

line/branch coverage 量的是「這行**被執行過**」，不是「這行的結果**被斷言過**」。兩者差很遠。

```text
範例：100% 行覆蓋，零保護力

def apply_discount(price, code):
    rate = lookup_rate(code)      # 被執行 ✓
    return price * (1 - rate)     # 被執行 ✓

# 測試：
def test_discount():
    apply_discount(100, "SAVE10")   # 沒有 assert！
```

`apply_discount` 兩行都「covered」，coverage 工具回報 100%。但這測試**沒斷言任何結果**——把 `rate` 算錯成兩倍它也照樣綠。

> coverage 只告訴你「**哪裡完全沒被碰過**」（地板偵測器）。它**不**告訴你「碰過的地方是否正確」。高覆蓋率＋弱斷言＝假的安全感。

地板偵測的正確用法：

- [ ] 看 coverage report 找 **0% / 紅色**的區塊——那是「連執行都沒有」的盲區，先補。
- [ ] 對高風險檔案看**分支**覆蓋，不只看行覆蓋（error 分支常是 0）。
- [ ] **不要**把全域百分比當品質 KPI 追；它升高最廉價的方式就是灌水。

---

## 5️⃣ mutation testing：較真的訊號（簡述）

想知道「測試是否真的會抓到錯」，coverage 答不了，mutation testing 可以。

機制：工具自動竄改 production code（把 `>` 改成 `>=`、`+` 改成 `-`、刪掉一行……）製造「變異體」，重跑你的測試。

- 測試**紅了** → 變異被「殺死」，代表測試真的在守這段邏輯。
- 測試仍**綠** → 變異「存活」，代表這段就算寫錯，你的測試也察覺不到——assert 缺失或太弱。

§4 開頭那個無 assert 的 `apply_discount` 測試，會讓幾乎所有變異存活：mutation score 趨近 0，即使 coverage 100%。這正是 coverage 看不見的破洞。

> 用法務實：別全專案跑（慢）。對**付款 / 權限 / 核心業務**這幾個高風險模組跑一次，看哪些變異存活，回頭補斷言。當作收尾體檢，不是日常門檻。

---

## ✅ 決策速查

```text
要不要 test-first？
  碰 Auth/權限/PII ............ 一律 YES（強制，§4.1）
  說不清「正確」長怎樣 ......... YES（測試逼你想清楚）
  複雜業務 / 刁鑽 edge case .... YES
  修 bug ...................... red test 先行（§8.2）
  丟棄原型 / 純 glue / 平凡CRUD  NO（或一條 smoke 兜底）

coverage 怎麼用？
  當地板偵測器 → 找 0%/紅色盲區，優先補
  不當品質證書 → 別追全域百分比，別灌無 assert 測試
  高風險檔看分支覆蓋，不只行覆蓋
  想驗測試真有效 → 對高風險模組跑 mutation testing
```

何時**不**寫測試：原型、純配置/常數、第三方行為、生成碼、以及「為了把數字推過門檻」——後者尤其要警惕，那是優化指標不是優化安全。

---

## 🔗 Related Compass sections

- [§10.1 測試金字塔](./01_test_pyramid.md) — 該寫哪一層的測試（單元/整合/E2E 比例）
- [§4.1 Definition of Done](../04_quality_gates/01_dod.md) — Auth/PII 強制 test-first 的來源與收工門檻
- [§8.2 Bug Fix Workflow](../08_brownfield/02_bug_fix.md) — 修 bug 的 red test / characterization test 順序
- [§3.5 YAGNI](../03_implementation/05_yagni.md) — 原型與不該寫的東西的邊界

---

## 📝 Status

v0.8.0 (Phase 3: original content)
