# §6 Non-Functional Requirements (NFR)

> 多數 PRD 過度規範功能、嚴重低估 NFR。反向稽核腳本只抓功能清單（端點/schema/頁面），NFR 整批漏掉——所以 NFR 必須在 DoR 就抓。

## 本章涵蓋（v0.5.0 / Phase 2 已交付）

- [§6.1 NFR 總覽：為何 PRD 常漏](01_nfr_overview.md) — NFR 分類 + 插進 DoR 的 NFR 健檢清單
- [§6.2 效能規格落地](02_performance.md) — 把「要快」變成可測目標（p50/p95/p99、throughput、budget）
- [§6.3 觀測性](03_observability.md) — log / metrics / tracing + 四個黃金訊號
- [§6.4 安全：beyond test-first](04_security.md) — OWASP Top 10 對照 + STRIDE-lite 逐功能審查門
- [§6.5 無障礙與國際化](05_accessibility_i18n.md) — a11y (WCAG) / i18n 落地
- [§6.6 可用性與 SLA](06_availability_sla.md) — SLA/SLO/error budget + 依賴失效行為（timeout/retry/circuit breaker/fallback/降級）

## 何時載入

- DoR 階段檢查 PRD 有沒有寫 NFR
- 實作一塊功能，過安全審查門（§6.4）
- 上線前確認觀測性就位（§6.3）

## 🔗 相關
- [§2.1 DoR 健檢清單](../02_definition_of_ready/01_dor_checklist.md) — NFR 缺漏要在這裡抓
- [§4.1 DoD](../04_quality_gates/01_dod.md) — 觀測性/安全是 production 服務的 DoD 一部分
