<!-- LANG SWITCH -->

**繁體中文**（English version coming in Phase 5）

# Compass — PRD 紀律的羅盤

> 一個 Claude Code skill，扮演「PRD 與實作之間的羅盤」——確保你照著規格蓋、不偏航、不漏項。配 [Sentinel](https://github.com/RayLi-Git/sentinel) 思考 OS 形成完整工具組：Sentinel 看「怎麼想」，Compass 看「怎麼照規格執行」。

![status](https://img.shields.io/badge/status-WIP%20v0.5.0-orange)
![license](https://img.shields.io/badge/license-MIT-blue)
![companion](https://img.shields.io/badge/companion-Sentinel-purple)

> ⚠️ **目前在 v0.5.0 階段** — §1–§8、§11 已有內容（Phase 1+2 完成）；§9/§10 與英文化待補。完整路線圖見 [docs/SCOPE.zh-TW.md](./docs/SCOPE.zh-TW.md)。

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

## 安裝（等內容齊全後再正式 publish）

```bash
# v0.5.0：§1–§8、§11 已有內容，可實際載入試用
# 完整安裝指南會在 Phase 5 提供（見路線圖）
```

## 範圍邊界

**Compass 不涵蓋**：PRD 撰寫 / 產品探索 / PM 工具 / 純探索性原型 / 純改文案。
**詳細涵蓋與不涵蓋清單**：見 [docs/SCOPE.zh-TW.md](./docs/SCOPE.zh-TW.md)

## 設計理念

完整設計決策與取捨會在 v0.5.0 收錄於 `docs/DESIGN.zh-TW.md`（🚧 撰寫中）。

## 路線圖

| 版本 | 內容 | 狀態 |
|---|---|---|
| v0.1.0-skeleton | 架構、命名、骨架 | ✅ |
| v0.2.0 | 既有 SOP 整理（Phase 1）| ✅ |
| v0.5.0 | Critical 缺口填補（Phase 2）| ✅ 目前 |
| v0.8.0 | Nice-to-have 填補（Phase 3）| 🚧 下一階段 |
| v1.0.0 | Ship | ⏸ |

完整路線圖見 [docs/SCOPE.zh-TW.md](./docs/SCOPE.zh-TW.md)。

## 授權

[MIT](./LICENSE) © Ray_Li

> 本專案是一個作品集，探索「如何把 PRD 驅動開發的紀律編碼成 AI 寫程式的搭檔」。配對作品 [Sentinel](https://github.com/RayLi-Git/sentinel) 探索「如何把結構化思考編碼成 AI 寫程式的夥伴」。
