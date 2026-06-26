# §10 Testing Strategy

> 把每條 PRD 驗收標準放對測試層，用對 test-first 與 coverage，避免假覆蓋與假安全感。

## 本章涵蓋

- [01_test_pyramid.md](01_test_pyramid.md) — 測試金字塔分層規則、各層分工與反模式，含「PRD 驗收標準 → 測試層」對照程序。
- [02_test_first_boundary.md](02_test_first_boundary.md) — test-first 在哪回本／哪是 overhead，coverage 作為地板偵測器的正確用法，及 mutation testing 簡述。

## 何時載入

- 拿到 PRD 要決定每條驗收標準該寫哪一層測試（unit / integration / e2e）。
- 糾結要不要 test-first，或被「coverage 80%」當成過關證書綁住。
- E2E 跑太慢太脆（冰淇淋甜筒），想把測試重心調回該在的層。

## 🔗 相關
- [§4 Quality Gates](../04_quality_gates/_index.md) — DoD／DoR 對 Auth/權限/PII 強制 test-first 的來源。
- [§6 Non-Functional](../06_non_functional/_index.md) — 效能／安全等 NFR 走專屬測試型別，不塞進功能金字塔。
- [§8 Brownfield](../08_brownfield/_index.md) — 修 bug 的 red test 與 legacy 特徵測試安全網。
