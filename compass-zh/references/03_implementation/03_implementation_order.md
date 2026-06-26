# §3.3 實作順序與依賴

> Part of [Compass](../../SKILL.md) §3 — Implementation.
> 一條通用原則 + 一份示例順序表，幫你決定 PRD 落地時「先寫哪個、後寫哪個」，並守住安全模組與依賴鎖版的紀律。

---

## 1. 一般原則：從底層往上

> **基礎設施 → 安全核心 → 業務邏輯 → 整合 → 前端 → 補充**

這條原則跨語言、跨框架、跨領域通用。它的邏輯是：

- **基礎設施先**：目錄結構、套件管理、環境變數、啟動腳本若沒先穩住，後面每改一次都會牽動全域。
- **安全核心次之**：認證、授權、敏感資料偵測這類模組若事後補測，幾乎一定補不齊；要 **test-first** 寫進去。
- **業務邏輯接著**：核心 services / domain logic 在安全網內運作。
- **整合層**：API 路由 / endpoint / controller 把業務邏輯對外暴露。
- **前端最後**：UI / template / 前端互動建立在已穩定的 API 上。
- **補充收尾**：scripts、補測、文件。

**為什麼倒過來會出事**：先做 UI demo 給看，回頭補 auth 時會發現權限模型跟 UI 已寫死的假設衝突；先做 endpoint 再補 PII 偵測，PII 多半已經漏進 log 或回應裡。

---

## 2. 示例：典型 Web App 順序

以下是常見 Web 應用的 reference order，**僅供參考，不是強制**。你的專案是 CLI 工具、batch job、行動 App、或 ML pipeline，順序會不一樣——但「底層 → 安全 → 業務 → 整合 → 前端 → 補充」的骨架仍然成立。

| 順序 | 模組 | 測試策略 |
|---|---|---|
| 1 | 目錄結構 / 套件管理 / 環境變數 / 容器 / 啟動腳本 | smoke |
| 2 | 設定載入 / 資料庫初始化 / migration | smoke |
| 3 | **認證（登入/JWT/密碼雜湊/二階段驗證）** | **test-first** ⚠ |
| 4 | **授權 / 角色與權限邊界** | **test-first** ⚠ |
| 5 | **敏感資料偵測（PII 隔離鐵則）** | **test-first** ⚠ |
| 6 | Services / Domain logic（核心業務） | 同步寫 test |
| 7 | 外部模組（providers / processors / 第三方 SDK） | 用 fake / mock provider |
| 8 | Routes / API endpoints | 同步寫 test |
| 9 | 主程式整合 + 啟動驗證 | smoke |
| 10 | Frontend（HTML / template / 前端互動 / CSP） | 手動驗證 |
| 11 | 初始資料 / 系統檔案 / seeds | smoke |
| 12 | Scripts（init / ingest / backup / 維運工具） | 事後補 test |
| 13 | 其餘 tests 補齊 | — |
| 14 | 文件（CLAUDE.md / ARCHITECTURE.md / CHANGELOG.md） | — |

> ⚠ 標 **test-first** 的列是 **safety-critical modules**——這類模組若事後補測，多半補不齊。詳見下節。

---

## 3. Safety-critical modules：test-first 不能讓步

「安全核心」不是某個語言或框架的專屬概念，而是任何**一旦壞掉就會造成資料外洩、權限越界、或無法復原損害**的模組。這些模組必須先寫測試、再寫實作。

**通用判準**：

- 一旦失守，攻擊者可拿到別人的資料？→ 安全模組
- 一旦失守，使用者可做超出自己權限的事？→ 安全模組
- 一旦失守，敏感資料會落到 log / response / 第三方？→ 安全模組
- 一旦失守，無法事後從備份還原（如金鑰外洩）？→ 安全模組

**範例情境**（僅作說明，不代表所有專案都長這樣）：

- *Web 應用的登入流程（JWT 簽發、密碼雜湊、二階段驗證、Step-up）*
- *角色與權限系統（admin / user / guest 的升降級邊界、IDOR 防護）*
- *PII / 敏感資料偵測（在進 log、回 response、送第三方前先偵測過濾）*
- *支付 / 額度 / 餘額相關的扣款與對帳邏輯*
- *加密金鑰的生成、儲存、輪替*

對這些模組，**先寫測試**——而且測試要包含「壞人會怎麼用」的負面案例，不是只有 happy path。

> Dev 環境的 fake / mock 策略、以及 secret 管理流程，會跟著你的執行環境變化；建議在專案層的 runbook 寫清楚。

---

## 4. 實作規則

每一塊在落地時都要守的紀律：

- **每個檔案完成即存檔**，不累積批次未存的修改
- **每完成一個模組即 `git commit`**，訊息格式建議：`[PRD §X.Y] 模組：簡述`
- **不臆造未在 PRD 出現的功能**（YAGNI）
- **不引入 PRD 依賴章節未指定的套件**——若實作中發現非加不可，走 [§5 衝突處理](../05_conflict_handling/_index.md) 的 PRD 缺漏流程，不擅自加
- **保留 PRD 原始用語**（中文路徑、術語表詞彙、領域語言）——不擅自改名
- **每模組完成後 self-review**：當自己是 code reviewer 重讀一遍，特別檢查：
  - 是否有臆造欄位 / endpoint
  - 是否有把 PRD 的「明天再說」直接寫死成「永遠不做」
  - 是否有用 try/except 蓋掉應該往上拋的錯誤

**「完成」的定義**：完成就是完成，不留半成品；可分小塊交付，但不可半成品階段化。不切 V1/V2/V3，不留 TODO 等回頭。

---

## 5. 依賴鎖版

順序表第 1 項（套件管理）一完成，**立刻鎖版**——這是把「環境可重現」釘進 repo 的第一個錨點。

**通用做法**：用你的語言的依賴鎖機制（lockfile），把當下的依賴版本固化下來，並 commit 進 repo。

**常見對應**：

| 語言生態 | 鎖版機制（範例） |
|---|---|
| Python | `pip freeze` / `uv lock` / `poetry lock` / `pipenv lock` |
| Node.js | `package-lock.json` / `yarn.lock` / `pnpm-lock.yaml` |
| Ruby | `Gemfile.lock` |
| Rust | `Cargo.lock` |
| Go | `go.sum` |
| PHP | `composer.lock` |

**之後的紀律**：

- 新增任何依賴 → 重新 lock → commit lockfile
- 不直接編輯 lockfile
- CI / 部署環境一律用 lockfile 安裝，不從上游現抓最新

**為什麼這個錨點要這麼早**：依賴版本一漂移，後面 debug 會多出「環境差異」這個變數，根因樹會變得難畫。把它鎖死在最早，後面所有問題都可以排除「是不是套件版本不同」。

---

## 6. 順序偏離時的判斷

如果你不得不偏離這個順序（例如 stakeholder 急著看 UI demo），請至少守住：

1. **安全核心仍然 test-first**——即使 UI 先做，auth/權限/PII 的測試也要先寫
2. **偏離的部分標 `⚠️推測` 或 TODO**，並寫進 `.claude/progress.md` 的「進行中」
3. **回頭補時，從順序表往回找該模組的依賴**——別只補一塊就以為穩了

---

## 🔗 Related Compass sections
- [§3.1 PRD 吸收](01_prd_intake.md) — 順序表的上游：PRD 的 checklist 化
- [§3.4 完成-比對-修正循環](04_compare_fix_loop.md) — 每塊完成後的比對與驗收
- [§4.1 Definition of Done](../04_quality_gates/01_dod.md) — 每塊完成的驗收條件
- [§5 衝突處理](../05_conflict_handling/_index.md) — PRD 模糊 / bug / 缺漏時的處置

## 📝 Status
v0.2.0 (Phase 1: ported from prior SOP, generalized and de-privatized).
