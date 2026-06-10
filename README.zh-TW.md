<!-- LANG SWITCH -->

[English](./README.md) | **繁體中文**

# Compass — PRD 紀律的羅盤

> 一個 Claude Code skill，扮演「PRD 與實作之間的羅盤」——確保你照著規格蓋、不偏航、不漏項。配 [Sentinel](https://github.com/RayLi-Git/sentinel) 思考 OS 形成完整工具組：Sentinel 看「怎麼想」，Compass 看「怎麼照規格執行」。

![status](https://img.shields.io/badge/status-WIP%20v0.5.0-orange)
![license](https://img.shields.io/badge/license-MIT-blue)
![companion](https://img.shields.io/badge/companion-Sentinel-purple)

> §1–§11 全模組已有內容、中英雙語齊備。完整路線圖見 [docs/SCOPE.zh-TW.md](./docs/SCOPE.zh-TW.md)。

---

## 它解決的問題

拿到 PRD 後最常見的三種失敗模式：

1. **偏航** — 寫到一半發現偏離 PRD，但已寫了 3 天回不去
2. **漏項** — checklist 寫「auth 12 個 endpoint ⬜」，寫完 9 個就打勾，剩 3 個沒寫但不知道
3. **半成品** — 寫到 70% 留 TODO「之後再回頭」，但「之後」從來不會到

Compass 用**紀律 + 工具強制** 防住這三點。

## 核心信念

1. **PRD 是合約，不是建議** — 任何偏差都要記、要對齊、要裁決
2. **完成就是完成，不留半成品** — 可分小塊交付，但不可半成品階段化
3. **靠 exit code 不靠紀律** — 機械化檢查比規則陳述強得多
4. **Brownfield 也要紀律** — 不只全新專案才適用 PRD

## 11 個主題模組

```
§1 Foundations             — 五階段 + 核心原則
§2 Definition of Ready     — 開工前的 PRD 健檢 ⭐ 新
§3 Implementation          — 開工中的 SOP
§4 Quality Gates           — 驗收 / 自檢 / 工具強制
§5 Conflict Handling       — PRD 衝突處置：靜態三類（模糊/bug/缺漏）+ 動態類（中途變更/跨文件/多PRD），皆已交付
§6 Non-Functional (NFR)    — 效能/觀測性/安全/a11y ⭐ 新
§7 Operations              — Migration / Rollback / Deployment ⭐ 新
§8 Brownfield              — 既有 codebase 工作 ⭐ 新
§9 Collaboration           — 跨人/跨 AI ⭐ 新
§10 Testing Strategy        — unit/integration/e2e 分工 ⭐ 新
§11 Tooling                — M-007~M-010 工具強制 + 通用腳本
```

⭐ 標的章節是相對既有 SOP **全新撰寫**的。

## 跟 Sentinel 的關係

[Sentinel](https://github.com/RayLi-Git/sentinel) 是它的「**配對 skill**」：

| 維度 | Sentinel | Compass |
|---|---|---|
| 看什麼 | 你的思考 | 你跟 PRD 的關係 |
| 觸發問題 | 「我有想清楚嗎？」 | 「我有照 PRD 走嗎？」 |
| 適用 | 任何工程任務 | 有 spec 的實作工作 |

兩個常一起用。完整分工見 [docs/SCOPE.zh-TW.md](./docs/SCOPE.zh-TW.md)。

## 安裝

```bash
# 安裝為使用者層級 skill（所有專案生效）
mkdir -p ~/.claude/skills/compass
cp -r SKILL.md references ~/.claude/skills/compass/

# 驗證結構
ls ~/.claude/skills/compass   # → SKILL.md  references
```

完整安裝指南（skill + 工具腳本 + 範本）見 [docs/INSTALL.zh-TW.md](./docs/INSTALL.zh-TW.md)。

## 範圍邊界

**Compass 不涵蓋**：PRD 撰寫 / 產品探索 / PM 工具 / 純探索性原型 / 純改文案。
**詳細涵蓋與不涵蓋清單**：見 [docs/SCOPE.zh-TW.md](./docs/SCOPE.zh-TW.md)

## 設計理念

完整的設計決策與取捨記錄在 **[docs/DESIGN.zh-TW.md](./docs/DESIGN.zh-TW.md)**。

## 授權

[MIT](./LICENSE) © Ray_Li

> 本專案是一個作品集，探索「如何把 PRD 驅動開發的紀律編碼成 AI 寫程式的搭檔」。配對作品 [Sentinel](https://github.com/RayLi-Git/sentinel) 探索「如何把結構化思考編碼成 AI 寫程式的夥伴」。
