# §7.1 Migration：schema 與資料變更

> Part of [Compass](../../SKILL.md) §7 — Operations。
> schema 與資料變更的安全程序：永遠先向後相容，把「停寫」與「刪除」拆成兩次部署。

---

## 🎯 核心鐵律

> **Migration 不是「改 schema」，是「在舊 code 還跑著的時候改 schema」。**

部署不是原子的。新舊版本的 code 會同時連到**同一個資料庫**——滾動部署期間如此，金絲雀如此，回滾的瞬間更如此。任何「新 code 才看得懂」的 schema 改法，都會讓舊 code（或回滾後的舊 code）當場炸掉。

四條不可違背：

1. **每次部署，新舊 code 都必須能讀寫當前 schema**（前後相容窗口）。
2. **schema 變更與讀寫切換，必須分多次部署**，不可塞進同一次。
3. **絕不在「停止寫入舊欄位」的同一次部署刪掉它**——刪除至少晚一個部署。
4. **backfill 必須可重跑、可中斷續跑**，不假設一次跑完。

---

## 📐 Expand / Contract（擴張－收縮模式）

不相容的變更要拆成「擴張 → 遷移 → 收縮」三階段，每階段是**獨立部署**，且每階段結束時系統都處於可回滾的相容狀態。

| 階段 | 動作 | 相容性保證 |
|---|---|---|
| **Expand** | 加新結構（nullable 欄位／新表／新索引），**不刪不改舊的** | 舊 code 完全無感 |
| **Migrate** | backfill 舊資料；雙寫（新舊欄位都寫）；逐步把讀切到新欄位 | 新舊 code 都能運作 |
| **Contract** | 確認沒人再讀寫舊欄位後，才 drop | 只有在舊 code 已全數下線後執行 |

### 範例：把 `users.name` 拆成 `first_name` / `last_name`

```text
部署 1 (Expand)   ── 加 first_name, last_name 兩個 nullable 欄位
                     舊 code 還在讀寫 name，無感

部署 2 (Migrate)  ── code 改成「寫入時同時寫 name + first/last」（雙寫）
                  ── 背景 backfill：把存量 name 拆進 first/last（分批、冪等）

部署 3 (切讀)     ── code 讀取改用 first/last，name 只寫不讀

部署 4 (Contract) ── 確認 name 無任何讀寫後，drop column name
```

四次部署，每次之間都可以安全停住、安全回滾。**急著合併成兩次 = 自找停機。**

---

## 🔁 Backfill 策略

存量資料的回填是 migration 最容易爆的一段：一條 `UPDATE ... WHERE ...` 掃全表會鎖表、撐爆 replication lag、跑到一半連線斷掉前功盡棄。

Backfill 必備三性質：

- **分批（batched）**：每批限定筆數（如 1000 列），批間留間隔讓 replica 跟上；不要一條 SQL 掃全表。
- **冪等（idempotent）**：重跑同一批不會壞資料。靠 `WHERE new_col IS NULL` 之類條件天然跳過已處理列，而非靠「跑到哪了」的外部狀態。
- **可續跑（resumable）**：用穩定游標（主鍵範圍）推進；中斷後從上次的游標接續，不從頭重來。

```text
範例（分批冪等回填的形狀，非實際指令）：
  last_id = 0
  loop:
    rows = SELECT id, name FROM users
           WHERE id > last_id AND first_name IS NULL   ← 冪等條件
           ORDER BY id LIMIT 1000                       ← 分批
    if rows empty: break
    for r in rows: UPDATE ... WHERE id = r.id
    last_id = rows[-1].id                               ← 可續跑游標
    sleep(短暫間隔)                                      ← 讓 replica 喘息
```

Backfill 檢查清單：

- [ ] 批次大小有上限，批間有間隔
- [ ] 條件天生跳過已處理列（重跑安全）
- [ ] 游標可持久化，中斷能續跑
- [ ] 監看 replication lag / 鎖等待，異常能暫停
- [ ] backfill 期間「新寫入」由雙寫照顧，不依賴 backfill 補

---

## ⏱️ Zero-downtime 原則

- **新欄位一律先 nullable 或帶 default**：加 `NOT NULL` 無 default 的欄位，舊 code 的 INSERT 會直接失敗。先 nullable，backfill 完、雙寫穩定後，最後一步才補上約束。
- **加索引用非阻塞方式**：大表建索引要用線上／併發建立（如 PostgreSQL `CREATE INDEX CONCURRENTLY`），別在交易裡鎖整張表。
- **改欄位型別＝expand/contract**：不要 `ALTER COLUMN` 直接改型別。加新欄位、雙寫、backfill、切讀、drop 舊欄位。
- **rename 等同 drop + add**：rename 會讓舊 code 瞬間找不到欄位。當成 expand/contract 處理。
- **大資料量的破壞性 DDL（drop/rename）和 backfill 解耦**：DDL 走部署，backfill 走背景任務，互不阻塞。

---

## 🪟 前後相容窗口

「窗口」= 從變更上線到舊 code 完全下線之間，**新舊版本並存**的那段時間。窗口內任何一方掛掉，就是線上事故。

| 你要做的事 | 窗口內必須保證 |
|---|---|
| 加欄位 | 舊 code 不寫它也能正常 INSERT（故須 nullable／default） |
| 改讀取來源 | 新欄位在切讀前已被雙寫填滿，否則讀到 NULL |
| 刪欄位 | 確認**沒有任何**仍在運行的版本會讀或寫它 |
| 回滾 | 回滾到的舊版本，仍能在新 schema 上正常跑 |

> 設計每一步時自問：「如果這一刻**回滾**，舊 code 在**新 schema** 上會炸嗎？」會炸 → 這步拆得不夠細。

---

## ⛔ 「停寫與刪除不同部署」規則

最常見、最致命的偷懶：在同一次部署裡「code 不再寫 X」+「DDL drop X」。

為什麼炸：

- 部署不是原子的。drop 已生效、但仍有舊 instance 在寫 X → 寫入失敗。
- 一旦需要回滾，回滾到的舊 code 還要寫／讀 X，但 X 已經沒了 → 回滾即災難。

正確順序：**先部署「停止讀寫 X」的 code 並穩定運行（觀察一個窗口）→ 下一次部署才 drop X。** drop 永遠是最後、獨立、且舊 code 已確定不依賴它之後的動作。

---

## 🧪 Migration 測試

migration 腳本本身就是 code，未測過的 migration 等於未驗證的 production 變更。

- [ ] **在資料庫副本上跑 up**：用接近 production 的資料量與分佈，不是空表。
- [ ] **跑 down（回滾腳本）**：每個 migration 都要有對應 down，且實際在副本上驗證能回到變更前狀態。
- [ ] **up → down → up 來回**：確認可逆且冪等，不會第二次 up 就爆。
- [ ] **量測耗時與鎖**：在副本上估算鎖表時間與總耗時；超出可接受窗口 → 改用分批／線上 DDL。
- [ ] **backfill 中斷重啟測試**：故意中途砍掉，確認續跑不重複、不漏。
- [ ] **新舊 code 交叉測**：舊 code 對新 schema、新 code 對舊 schema，至少其一在窗口內要成立。

> 證據強度（Sentinel 的證據強度）：宣稱「migration 安全」前要標等級。在副本上實跑過 up+down = 🟢；只讀過 SQL 沒跑 = 🟡，明說建議先在副本驗證。

---

## 🔗 與 §5.2 PRD 變更的關係

PRD 改動極常觸發 schema 變更：新欄位、改關聯、刪過時欄位。流程是先比對、後遷移：

1. PRD 變更先依 [§5.2](../05_conflict_handling/02_prd_change.md) 走影響範圍評估，別直接動 schema。
2. 評估出的 schema 差異，**一律用 expand/contract 落地**，不因「PRD 說改成這樣」就直接 `ALTER`／`DROP`。
3. 破壞性變更（drop/rename）若 PRD 沒明確要求保留相容窗口，視為 [§5.1](../05_conflict_handling/01_vague_bug_gap.md) 的缺漏 — 記錄並補上相容步驟，不擅自一刀切。

---

## 🔗 Related Compass sections

- [§7.2 Rollback](./02_rollback.md) — 遷移失敗時的回滾與相容回退策略
- [§5.2 PRD 變更](../05_conflict_handling/02_prd_change.md) — schema 變更的上游觸發
- [§4.1 Definition of Done](../04_quality_gates/01_dod.md) — migration 測過 up+down 才算完成
- [§7 Operations](./_index.md) — 本模組總覽

---

## 📝 Status

`v0.5.0` (Phase 2: original content)
