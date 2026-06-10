# Templates — Compass 追蹤文件範本

> Compass §3.2 依賴的追蹤文件範本，外加 §11 反向稽核的設定範例。複製到專案（`.claude/` 或專案根）後填入。

---

## 檔案

| 檔案 | 對應 | 用途 |
|---|---|---|
| `progress.md.template` | [§3.2](../references/03_implementation/02_tracking_docs.md) | 進度 + 待辦 + 進行中（§9.3 交接的恢復指標） |
| `development-log.md.template` | [§3.2](../references/03_implementation/02_tracking_docs.md) / [§5](../references/05_conflict_handling/_index.md) | 決策 + PRD Ambiguity / Issues / Gaps 紀錄 |
| `prd-checklist.md.template` | [§3.2](../references/03_implementation/02_tracking_docs.md) / [§11 M-007](../references/11_tooling/01_m007_to_m010.md) | PRD 章節 ↔ 實作對照（一行一條，禁聚合） |
| `audit-config.example.json` | [§11 M-008](../references/11_tooling/01_m007_to_m010.md) | 反向稽核腳本 `audit_prd_vs_code.example.py` 的設定範例 |

> 📌 跨 session 永久記憶（auto memory）的範本尚未提供——目前請參考 [§3.2 追蹤文件](../references/03_implementation/02_tracking_docs.md) 末段的「跨 session 記憶」說明手動建立。

---

## 用法

```bash
cp templates/progress.md.template .claude/progress.md
cp templates/development-log.md.template .claude/development-log.md
cp templates/prd-checklist.md.template .claude/prd-checklist.md
cp templates/audit-config.example.json compass-audit.json   # 改成你的 PRD/code 結構
```

`prd-checklist.md` 可用 [`../scripts/expand_checklist.example.py`](../scripts/README.md) 從 PRD 表格自動展開，避免手抄漏行。
