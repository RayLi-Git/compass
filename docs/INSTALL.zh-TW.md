<!-- LANG SWITCH -->

**繁體中文**（English version coming in Phase 5）

# 安裝指南 (Installation Guide)

> Compass 由三部分組成：**skill 本體**（`SKILL.md` + `references/`，按需載入的 PRD 紀律知識庫）、**工具腳本**（`scripts/`，M-007/008/010 的可執行範例）、**追蹤文件範本**（`templates/`）。skill 本體必裝；工具與範本建議一起裝以獲得完整體驗。

---

## 前置需求

- 已安裝 [Claude Code](https://docs.claude.com)。
- 若要用 `scripts/` 的反向稽核 / checklist 展開：**Python 3**（標準庫即可，無 pip 依賴）。
- 若要用 commit-msg hook：**bash** + 一個 git repo。
- 建議搭配 [Sentinel](https://github.com/RayLi-Git/sentinel) 一起裝（Compass 看「怎麼照規格執行」，Sentinel 看「怎麼想」）。

---

## 一、安裝 skill 本體（必裝）

skill 的本質是「一個資料夾，裡面有 `SKILL.md`」。安裝就是把它放到 Claude Code 掃描的 skills 目錄。

### 方式 A：全域安裝（推薦，所有專案生效）

```bash
mkdir -p ~/.claude/skills/compass

# 若你拿到的是 .skill / .zip 打包檔
unzip compass.skill -d ~/.claude/skills/compass

# 或若你 clone 了這個 repo，直接複製內容
cp -r SKILL.md references ~/.claude/skills/compass/
```

### 方式 B：專案層級安裝（只對單一專案生效）

```bash
mkdir -p .claude/skills/compass
cp -r SKILL.md references .claude/skills/compass/
```

### 驗證結構（重要）

```bash
ls ~/.claude/skills/compass
# 必須看到：SKILL.md  references

ls ~/.claude/skills/compass/references
# 應看到 11 個模組資料夾：01_foundations … 11_tooling
```

> ⚠️ 常見錯誤：解壓後變成多包一層 `compass/compass/SKILL.md`。
> `SKILL.md` 必須**直接**在 `~/.claude/skills/compass/` 底下。若多了一層，把內層內容往上搬。

---

## 二、（建議）安裝工具腳本與範本

工具腳本是 §11 規則的可執行範例，範本是 §3.2 追蹤文件的起點。建議放在**你工作的專案**裡（不是 skills 目錄）。

```bash
# 在你的專案根目錄
cp -r /path/to/compass/scripts ./scripts
cp -r /path/to/compass/templates ./templates
```

各工具用法見 [`scripts/README.md`](../scripts/README.md) 與 [`templates/README.md`](../templates/README.md)。重點：

```bash
# M-008 反向稽核：先複製設定範例再改成你的專案結構
cp templates/audit-config.example.json compass-audit.json
python3 scripts/audit_prd_vs_code.example.py        # exit 0 對齊 / 1 有缺漏 / 2 設定缺失

# M-007 PRD 表格展開成 checklist
python3 scripts/expand_checklist.example.py PRD.md > prd-checklist.md

# M-010 commit 訊息把關（裝成 git hook）
cp scripts/commit-msg-lint.sh .git/hooks/commit-msg
chmod +x .git/hooks/commit-msg
```

---

## 三、開始使用

1. 開一個**新的** Claude Code session（重開才會掃描到新 skill）。
2. 丟一個 PRD 實作任務（例：「實作這份 PRD 的 auth 模組」、「這份 spec 我要開始寫」）。Compass 會自動觸發，依任務份量走對應流程。

### 快速確認 Compass 真的觸發了

開新 session 後，丟這句測試：

> 「我有一份 PRD 要開始實作，幫我先做開工前的健檢。」

預期 Compass 會引導你跑 **§2 Definition of Ready**（PRD 可實作性健檢清單）。若它沒提到 DoR / 健檢，代表 skill 沒被掃到——回頭檢查安裝結構。

### Compass 產生的追蹤文件會長在哪？

Compass 在**你工作的專案目錄**裡用這幾份文件追蹤 PRD 進度：

```
你的專案/
└── .claude/
    ├── progress.md            # PRD 任務進度 + 待辦 + 進行中
    ├── development-log.md     # 決策 + PRD 偏差（模糊/bug/缺漏）紀錄
    └── prd-checklist.md       # PRD 章節 ↔ 實作對照（一行一條）
```

> 💡 建議把專案的 `.claude/` 加入 git，PRD 進度與決策才能跨 session / 跨機器保存。

---

## 四、跟 Sentinel 搭配

Compass 與 Sentinel 共用 `.claude/` 病歷檔（`debug-log.md` / `patterns.md`）。兩個都裝時：

- 拿到 PRD、動工前 → Compass §1+§2 + Sentinel 動手前協定
- 實作中遇到複雜 bug → Sentinel 診斷階段 + Compass §5（若是 PRD 偏差）
- 上線前 → Compass §4+§7 + Sentinel 三條安全網

---

## 疑難排解

| 症狀 | 可能原因 | 解法 |
|---|---|---|
| skill 沒被觸發 | 沒開新 session | 重開 Claude Code |
| 找不到 references 檔 | 多包了一層資料夾 | 確認 `SKILL.md` 直接在 `compass/` 底下 |
| `audit_prd_vs_code` 每次 exit 2 | 沒有 `compass-audit.json` | 複製 `templates/audit-config.example.json` 並改成你的結構 |
| `python3` 找不到 / 是空殼 | Windows Store 別名 | 用真實 Python 路徑或 `py` launcher |
| 追蹤文件沒生成 | 任務未進入 🟡/🔴 流程 | 正常——純 typo/樣式不會啟動追蹤 |

---

## 解除安裝

```bash
rm -rf ~/.claude/skills/compass
# 專案內的 scripts/ templates/ .claude/ 視需要自行移除
```
