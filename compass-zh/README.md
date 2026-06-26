[English](../README.md) | **繁體中文**

# Compass — PRD 紀律的羅盤

> 一個 Claude Code skill，讓你的實作忠於規格——**照 PRD 蓋、不偏航、不漏項、不留半成品。** 四件式工具鏈的一環：**Cartographer 畫地圖 → Compass 照圖走 → Sentinel 站哨 → Lookout 瞭望。**

![status](https://img.shields.io/badge/status-active-success)
![license](https://img.shields.io/badge/license-MIT-blue)
![toolchain](https://img.shields.io/badge/toolchain-Cartographer·Compass·Sentinel·Lookout-purple)

---

## 它解決的問題

拿到 PRD、開始實作後，最常見的三種失敗模式：

1. **偏航** — 寫到一半才發現偏離 PRD，但已經寫了 3 天的 code，回不去了。
2. **漏項** — checklist 寫「auth 12 個 endpoint ⬜」，你寫完 9 個就打勾，剩下 3 個從沒寫——沒人發現。
3. **半成品** — 寫到 70% 留個 `TODO: 之後再回頭`，但「之後」從來不會到。

Compass 用**紀律 + 工具強制**（靠 exit code，不靠意志力）把這三點全擋住。

## 運作方式

**四個核心信念：**

1. **PRD 是合約，不是建議** — 任何偏差都要記、要對齊、要裁決。
2. **完成就是完成** — 想分小塊交付沒問題，但絕不留半成品階段。
3. **靠 exit code 不靠紀律** — 機械化檢查遠勝規則陳述。
4. **Brownfield 也要紀律** — PRD 紀律不只適用於全新專案。

**11 個主題模組**（按需從 `references/` 載入）：

```
§1  Foundations          五階段 + 核心原則
§2  Definition of Ready  開工前的 PRD 健檢
§3  Implementation       開工中的 SOP
§4  Quality Gates        驗收 / 自檢 / 工具強制
§5  Conflict Handling    模糊 / bug / 缺漏 + 中途變更 / 跨文件 / 多 PRD
§6  Non-Functional       效能 / 觀測性 / 安全 / a11y / SLA
§7  Operations           migration / rollback / deployment
§8  Brownfield           在既有 codebase 裡工作
§9  Collaboration        跨人 / 跨 AI
§10 Testing Strategy     unit / integration / e2e 分工
§11 Tooling              M-007~M-010 工具強制 + 通用腳本
```

## 快速開始

```bash
# 安裝為使用者層級 skill（所有專案生效）
mkdir -p ~/.claude/skills/compass
cp -r SKILL.md references scripts templates ~/.claude/skills/compass/

# 驗證
ls ~/.claude/skills/compass   # → SKILL.md  references  scripts  templates
```

完整指南（skill + 工具腳本 + 範本）見 **[docs/INSTALL.md](./docs/INSTALL.md)**。

## 工具鏈

Compass 是四件式工具鏈裡的**照規格施工**段——每一件盯不同的事：

| Skill | 角色 | 盯什麼 |
|---|---|---|
| [Cartographer](https://github.com/RayLi-Git/cartographer) | 畫地圖 | 把模糊想法逼成一份扎實的 PRD |
| **Compass** | 照圖走 | 你有照 PRD 走嗎？（照規格蓋、不偏航） |
| [Sentinel](https://github.com/RayLi-Git/sentinel) | 站哨 | 你怎麼想（淺層 vs 深層、症狀 vs 根因） |
| [Lookout](https://github.com/RayLi-Git/lookout) | 在桅杆瞭望 | 獨立 context 的 code review |

**Cartographer 畫地圖 → Compass 照圖走 → Sentinel 站哨 → Lookout 瞭望。** 完整分工見 [docs/SCOPE.md](./docs/SCOPE.md)。

## 目錄結構

```
compass/
├── SKILL.md            skill 入口（Claude Code 載入）
├── references/         11 個模組，按需載入
├── scripts/            工具強制腳本（lint / audit）
├── templates/          PRD checklist / progress / dev-log 範本
├── docs/               DESIGN · INSTALL · SCOPE
└── compass-zh/         繁體中文鏡像
```

## 文件

- **[DESIGN](./docs/DESIGN.md)** — 設計理念、關鍵決策與取捨
- **[INSTALL](./docs/INSTALL.md)** — 完整安裝（skill + 腳本 + 範本）與驗證
- **[SCOPE](./docs/SCOPE.md)** — 涵蓋什麼、不涵蓋什麼、以及工具鏈分工

## 授權

[MIT](./LICENSE) © Ray_Li

> 本專案是一個作品集，探索「如何把 PRD 驅動開發的紀律，編碼成 AI 寫程式的搭檔」。同一工具鏈的 [Sentinel](https://github.com/RayLi-Git/sentinel) 探索「把結構化思考編碼成 AI 寫程式的夥伴」。
