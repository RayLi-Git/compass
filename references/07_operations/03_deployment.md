# §7.3 Deployment Checklist
> Part of [Compass](../../SKILL.md) §7 — Operations.
> 上線前的一道閘門：逐項確認該過的都過了，再讓 code 進 production。

---

這是一份**紀律檢查清單**，不是 CI/CD 教學。
本文不教你怎麼設計 pipeline、選 GitHub Actions 還是 ArgoCD、寫 Dockerfile。
它只回答一個問題：**「現在這版可以上嗎？」**

把它當成起飛前的 checklist——機師再資深，每次起飛還是逐項唸過。

---

## ✅ Pre-deploy gate（上線前閘門）

下列每一項都要明確回答 **是 / 否 / 不適用**。任何一項是「否」→ **不上**。

| # | 檢查項 | 通過標準 | 出處 |
|---|---|---|---|
| 1 | **DoD 全綠** | lint / typecheck / unit / smoke 全過，無 skip 掩蓋 | [§4.1](../04_quality_gates/01_dod.md) |
| 2 | **Migration plan 就緒** | schema 變更有正反向腳本，演練過、可回退 | [§7.1](./01_migration.md) |
| 3 | **Rollback plan 就緒** | 知道怎麼退、退到哪個版本、退要多久 | [§7.2](./02_rollback.md) |
| 4 | **Observability 到位** | 新路徑有 log / metric / trace，告警有設 | [§6.3](../06_non_functional/03_observability.md) |
| 5 | **Secrets 不寫死** | 金鑰/token 走環境變數或 secret store，不在 code、不在 log、不進 git | [§6.4](../06_non_functional/04_security.md) |
| 6 | **Feature flag 設定確認** | 新功能預設值正確；灰度範圍明確 | 本文 |
| 7 | **Staging smoke 通過** | 在類正式環境跑過關鍵路徑，不是只在本機過 | 本文 |

> 鐵律：**沒演練過的 rollback 不算 rollback**。第 3 項打勾前，問自己「我真的退過一次嗎？」

---

## 🔍 各項展開

### 1 · DoD green
不是「我覺得寫完了」，是 [§4.1 DoD](../04_quality_gates/01_dod.md) 八項逐條對過。
特別盯：有沒有為了讓 CI 過而 `skip` / `xfail` / 註解掉測試。那是把警報關掉，不是修好。

### 5 · Secrets configured, not hardcoded
這是資安紅旗，獨立成關。上線前掃一遍：

```bash
# 範例：上線前粗篩（命中即停下人工確認，不是自動判生死）
git grep -nE "(api[_-]?key|secret|password|token)\s*=\s*['\"]" -- '*.py' '*.ts'
```

命中不代表一定是洩漏，但**每一筆都要人看過**。詳見 [§6.4 Security](../06_non_functional/04_security.md)。

### 6 · Feature flags
- 新功能上線時 flag **預設 off**，靠灰度逐步開——除非 PRD 明確要求全量。
- flag 的「開」與「程式 deploy」**解耦**：先 deploy（flag off），確認穩，再開 flag。
- 記下每個 flag 的「該移除日期」。長期殘留的 flag 是技術債。

### 7 · Staging smoke test
在**盡量貼近正式**的環境跑關鍵路徑（登入 → 核心交易 → 登出之類）。
本機過不算數——本機沒有正式的 DNS、憑證、網路延遲、資料量。

```text
# 範例 smoke 清單（按專案調整，非強制）
[ ] 健康檢查 endpoint 回 200
[ ] 一條核心 happy path 走得通
[ ] 一條已知錯誤路徑回正確錯誤碼（不是 500）
[ ] 對外依賴（DB / 第三方 API）連得上
```

---

## 🚀 Deploy 當下

- 挑**低流量時段**上，不在尖峰、不在週五下班前。
- 上線時**有人盯著**——不是按下 deploy 就走人。
- Migration 與 code 的順序照 [§7.1](./01_migration.md) 走（通常 expand → deploy → contract）。

---

## 📡 Post-deploy verification（上線後守觀）

Deploy 成功 ≠ 上線成功。盯住 **4 個黃金訊號**（golden signals）至少 **N 分鐘**
（N 依流量定，建議 ≥15 分鐘或一個完整流量週期）：

| 黃金訊號 | 看什麼 | 異常徵兆 |
|---|---|---|
| **Latency** 延遲 | p95 / p99 回應時間 | 比上線前明顯變慢 |
| **Traffic** 流量 | QPS / RPS | 突然掉到接近 0（可能整個掛了） |
| **Errors** 錯誤率 | 5xx / 例外比例 | 比基線高 |
| **Saturation** 飽和度 | CPU / 記憶體 / 連線池 | 逼近上限 |

> 定義出處見 [§6.3 Observability](../06_non_functional/03_observability.md)。
> **任一訊號惡化且無法快速止血 → 立刻啟動 [§7.2 Rollback](./02_rollback.md)，不戀戰。**
> 別在錯誤上疊補丁救（Sentinel 的沉沒成本警戒）——先退，乾淨環境再查根因。

---

## 📣 Who to notify（通知對象）

| 時機 | 通知誰 | 內容 |
|---|---|---|
| Deploy 前 | 團隊頻道 | 「準備上線 X，預計 Y 分鐘」 |
| Deploy 完 | 團隊頻道 | 版本號、變更摘要、監看中 |
| 守觀通過 | 團隊頻道 | 「X 已穩定上線」 |
| 異常 / rollback | 團隊頻道 + on-call + 受影響的下游 | 現象、影響範圍、已退版 |

通知不是儀式——是讓**別人也知道現在系統處於什麼狀態**，出事時不用從零釐清。

---

## 🚩 不上線的紅旗

出現任一個 → 停，別上：

- DoD 有項目靠 skip / any / 註解掉測試硬過。
- Rollback「理論上可以」但**從沒退過一次**。
- Secrets 掃描有命中還沒人確認。
- 只有本機 smoke 過，staging 沒跑。
- 「先上再說，有問題再修」——這句話本身就是紅旗。

---

## 🔗 Related Compass sections
- [§7.1 Migration Plan](./01_migration.md) — schema 變更與正反向腳本
- [§7.2 Rollback Plan](./02_rollback.md) — 退版的觸發、步驟與演練
- [§6.3 Observability](../06_non_functional/03_observability.md) — 黃金訊號與告警
- [§4.1 Definition of Done](../04_quality_gates/01_dod.md) — 上線前必過的完成定義

## 📝 Status
v0.5.0 (Phase 2: original content)
