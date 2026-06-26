# §11 Tooling｜工具強制 M-007 ~ M-010

> 把「靠人記得」的紀律換成「靠 exit code / git hook / TodoWrite」的機械化強制。靠紀律有限，靠工具可靠。

## 本章涵蓋

- [§11.1 工具強制 4 條 (M-007 ~ M-010)](01_m007_to_m010.md) — 反聚合 checklist、反向稽核、TodoWrite、commit 禁主觀詞

## 可執行腳本範例

§11.1 規則的參考實作，位於 [`/scripts/`](../../scripts/README.md)：

| 腳本 | 規則 | 做什麼 |
|---|---|---|
| `audit_prd_vs_code.example.py` | M-008 | config-driven 反向稽核（讀 `compass-audit.json`），PRD 列的 vs code 實作的，exit code 表對齊 |
| `expand_checklist.example.py` | M-007 | PRD 表格逐列展開成一行一 checkbox |
| `commit-msg-lint.sh` | M-010 | git hook 擋下含主觀完成詞的 commit |

設定範例：[`/templates/audit-config.example.json`](../../templates/README.md)

## 何時載入

- 想把某條紀律從「靠記得」升級成「工具擋住」
- 建立反向稽核 / checklist 展開 / commit lint

## 🔗 相關
- [§4.1 DoD](../04_quality_gates/01_dod.md) — 反向稽核 exit 0（建立 script 後升 Required）
- [§3.2 追蹤文件](../03_implementation/02_tracking_docs.md) — checklist 顆粒度（M-007）
