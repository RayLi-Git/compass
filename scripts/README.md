# Scripts — Compass 工具腳本範例

> Compass §11 Tooling 的**參考實作**（M-007 / M-008 / M-010）。副檔名 `.example` 表示是範例骨架，不是即裝即用成品——每個專案的 PRD 結構不同，請依需求調整 regex / parser。

---

## 檔案

| 檔案 | 對應規則 | 做什麼 |
|---|---|---|
| `audit_prd_vs_code.example.py` | M-008 反向稽核 | 讀設定檔 `compass-audit.json`，比對「PRD 列了什麼」vs「code 實作了什麼」，印缺漏，exit code 表對齊 |
| `expand_checklist.example.py` | M-007 反聚合 | 把 PRD markdown 表格逐列展開成「一行一個 checkbox」 |
| `commit-msg-lint.sh` | M-010 commit 把關 | git `commit-msg` hook，擋下含主觀完成詞（完整/done…）的 commit |

---

## M-008 反向稽核（需要設定檔）

`audit_prd_vs_code.example.py` 是 **config-driven** 的——它不猜你的專案結構，而是讀一個 `compass-audit.json`。**沒有設定檔時會印出範例並 exit 2**（這是設計，不是故障）。

```bash
# 1. 複製範例設定到專案根目錄，改成你的 PRD / code 結構
cp templates/audit-config.example.json compass-audit.json

# 2. 跑（exit 0 = 對齊；1 = 有「PRD 列了但 code 沒實作」的缺漏；2 = 設定缺失）
python3 scripts/audit_prd_vs_code.example.py

# 只跑某個 check
python3 scripts/audit_prd_vs_code.example.py --section=endpoints
```

設定檔欄位（見 [`../templates/audit-config.example.json`](../templates/audit-config.example.json)）：
- `prd_path` — PRD markdown 路徑
- `checks[]` — 每個 check 一組：`name` / `prd_regex`（從 PRD 抓項目）/ `code_glob`（掃哪些 code 檔）/ `code_regex`（從 code 抓實作）

> 範例 regex 是針對 FastAPI + SQL migration 的佈局；換你的技術棧要改 regex。
>
> ⚠️ **已知限制**：範例的 endpoint check 只比對 path、不分辨 HTTP method（`GET /users` 與 `POST /users` 視為同一項，method 不符不會被抓出）。需 method 敏感度請讓 regex capture「method + path」成一組（code 端 method 大小寫需正規化）。

## M-007 反聚合 checklist 展開

```bash
python3 scripts/expand_checklist.example.py PRD.md > prd-checklist.md
# 可選：--section-header "§19 endpoints" 給每列加標籤
```

## M-010 commit 訊息把關

```bash
cp scripts/commit-msg-lint.sh .git/hooks/commit-msg
chmod +x .git/hooks/commit-msg
# 之後 commit 訊息含「完整/全部/done/finished…」會被擋下，要求改用具體計數
```

---

## 環境需求

- Python 3（標準庫即可，無 pip 依賴）— 兩支 `.py`
- bash — `commit-msg-lint.sh`
- 讀檔一律 UTF-8（腳本已指定 `encoding="utf-8"`）

詳見 [§11.1 工具強制 M-007 ~ M-010](../references/11_tooling/01_m007_to_m010.md)。
