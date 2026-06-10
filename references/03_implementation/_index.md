# §3 Implementation｜開工中的 SOP

> 從 PRD 落地成 code 的全程紀律：吸收規格、建立追蹤文件、排定實作順序、邊寫邊比對、守住 YAGNI。

## 本章涵蓋

- [01_prd_intake.md](01_prd_intake.md) — 動手前先建立對 PRD 的完整心智模型，避免邊寫邊漏。
- [02_tracking_docs.md](02_tracking_docs.md) — 實作期間必備的三份追蹤文件，加上可選的跨 session 永久記憶。
- [03_implementation_order.md](03_implementation_order.md) — 用通用原則 + 示例順序表決定「先寫哪個」，守住安全模組與依賴鎖版。
- [04_compare_fix_loop.md](04_compare_fix_loop.md) — 每完成一塊就跑「完成 → 比對 PRD → 修正 → 驗收」閉環，防偏差累積。
- [05_yagni.md](05_yagni.md) — PRD 沒要求、也無實作必要的，不寫；把「少寫」當紀律。

## 何時載入

- 拿到 PRD/規格、準備動手寫 code 的那一刻。
- 實作進行中，需要排順序、建追蹤文件或自查是否偏離規格。
- 想加 PRD 沒寫的功能、欄位或依賴，需要 YAGNI 把關時。

## 🔗 相關
- [../02_definition_of_ready/_index.md](../02_definition_of_ready/_index.md) — 開工前的 DoR 檢查，吸收 PRD 的前一步。
- [../04_quality_gates/_index.md](../04_quality_gates/_index.md) — 完成判定與 DoD，比對-修正循環的驗收標準。
- [../05_conflict_handling/_index.md](../05_conflict_handling/_index.md) — 實作中發現 PRD 模糊／bug／缺漏時的三類處置。
