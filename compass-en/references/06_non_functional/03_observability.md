# §6.3 Observability: log / metrics / tracing

> Part of [Compass](../../SKILL.md) §6 — Non-Functional Requirements.
> A production service with no logs and no metrics isn't "done" — it's blind. This chapter nails observability into the DoD.

---

## 🔒 Iron Rule

> **Observability is part of the DoD for production services. Feature coded but "when it breaks you see no signal" = not done.**

"Ship first, add monitoring later" is a lie. The incident happens before "later," and after "later" is always next time. Every feature that goes to production must, at wrap-up, answer two questions:

1. When it works, how do I **see** it running? (log / metric)
2. When it breaks, how do I **know first** and **pin it to a layer**? (alert / trace)

Can't answer = this slice isn't done.

---

## 🪵 Structured logging

A plain-text `print("error happened")` isn't a log, it's noise. Production logs are always **structured** (JSON or key=value) so machines can query them.

### Minimum fields per log line

| Field | Purpose |
|---|---|
| `timestamp` | ISO 8601, UTC |
| `level` | DEBUG / INFO / WARN / ERROR |
| `message` | One human-readable sentence, **don't splice dynamic values into the string** (values go in fields) |
| `trace_id` / `request_id` | Stitches together all logs for one request (see tracing section) |
| `service` / `module` | Which service, which layer emitted it |
| business key | `user_id`, `order_id`, etc. **identifiers** (not PII) |

### Choosing log level (don't make everything INFO, nor everything ERROR)

| Level | When to use | Wakes someone up? |
|---|---|---|
| `ERROR` | Request failed, anomaly needing human intervention | Goes into alert pool |
| `WARN` | Graceful degradation succeeded, retry, nearing a limit — **not broken yet but watch it** | No alert, watch the trend |
| `INFO` | Business milestones (order placed, payment completed) | No |
| `DEBUG` | Dev-time detail, off by default in production | No |

> Logging expected failures (404, form validation error) as ERROR = crying wolf; real ERRORs get drowned out.

### ❌ Never allowed in logs (same red line as [§6.4 Security](./04_security.md))

- Passwords, tokens, API keys, session ids, private keys
- Full credit card numbers, national ID numbers, full email/phone (mask if you must: `u***@x.com`)
- Full request body / header (often carries the above)
- Any PII in plaintext

> Logs get forwarded, retained long-term, seen by many people, backed up. **A secret written to a log = already leaked.** This is one of Sentinel's security red flags: "key/token printed into a log."

**Example (FastAPI / structlog, illustrative, framework not mandated)**

```python
log.info("order.created", order_id=order.id, user_id=user.id, amount=order.total)
# ❌ Don't do this:
# log.info(f"user {user.email} paid with card {card.number}")
```

---

## 📊 Metrics: naming convention + four golden signals

Logs answer "what happened for this one record," metrics answer "is the whole thing healthy right now."

### Naming convention

- Format: `namespace.subsystem.unit`, all lowercase, `_` or `.` separated, **consistent**
- Carry a unit suffix: `_seconds`, `_bytes`, `_total` (counter)
- Use **label/tag** to slice dimensions (`route`, `status`, `method`), **don't stuff values into the metric name**

```
✅ http_request_duration_seconds{route="/orders", status="500"}
❌ http_request_duration_orders_500          # dimension explosion, can't aggregate
```

> ⚠️ Label cardinality will kill your metrics backend. **Don't use user_id, order_id as labels** — that's the log's job, not the metric's.

### The four golden signals

Every outward-facing service measures at least these four; missing one is a blind spot:

| Signal | Measures | Typical metric |
|---|---|---|
| **Latency** | Request duration, **split p50/p95/p99**, and **success vs failure separated** | `*_duration_seconds` histogram |
| **Traffic** | Requests per second / QPS | `*_requests_total` counter |
| **Errors** | Failure rate (5xx, exceptions, timeouts) | `*_errors_total` / derived from status label |
| **Saturation** | Resources nearing a limit (CPU, memory, connection pool, queue length) | `*_pool_in_use`, `queue_depth` |

> Average latency lies — p99 is the one users are actually cursing about. If failed requests get mixed into latency stats, "fast failure" gets misread as "healthy." **Latency must be split by success/error.**

---

## 🔗 Tracing: follow one request across services

When a request crosses multiple services (API → service → DB → third party), a single service's logs can't reconstruct the whole picture. Tracing uses one **trace_id** to stitch the entire path together.

Minimum requirements:

- The entry point (gateway / first service) generates a `trace_id` and **propagates it end-to-end** (HTTP header like `traceparent`, MQ message attribute)
- Every layer writes `trace_id` into each of its log lines
- Cross-service calls always carry it, **don't drop it midway**

> Floor before you have distributed tracing: **at minimum let request_id run through all logs of a single service.** Without even that, in an incident you can only guess file by file.

Adopting a standard like OpenTelemetry (vendor-neutral) beats binding to one APM vendor — swapping backends doesn't require rewriting instrumentation. Actual choice still follows your project's PRD / existing infrastructure.

---

## ✅ Per-feature observability checklist

For each feature going to production, check item by item at wrap-up:

- [ ] **Success path has an INFO log** (with business identifier + trace_id), can cite evidence "it's running"
- [ ] **Every failure branch has an ERROR/WARN log**, can pin which layer, which cause
- [ ] **Logs structured**, dynamic values in fields not in the string
- [ ] **Scan the logs once: zero secrets, zero PII in plaintext** (cross-check [§6.4](./04_security.md))
- [ ] **Four golden signals measurable**: this endpoint's latency(p95/p99) / traffic / error rate / key-resource saturation all have metrics
- [ ] **Latency split by success/error**, failures not mixed in
- [ ] **Metric naming compliant**, no high-cardinality labels
- [ ] **trace_id / request_id runs through** all logs and downstream calls this slice touches
- [ ] **Key failures have an alert** (error rate / saturation crossing a line notifies a human, not passively waiting for users to report)
- [ ] **Imagine: in an incident, can these signals pin the cause in minutes?** If you can't answer, add until you can

> If any item can't be checked, this slice isn't done. Observability isn't a bonus question, it's a hard requirement of [§4 Definition of Done](../04_quality_gates/01_dod.md) for production services.

---

## 🔗 Related Compass sections

- [§6 NFR — Index](./_index.md)
- [§6.2 Performance](./02_performance.md) — only once latency / saturation are measured can you talk optimization
- [§6.4 Security](./04_security.md) — "no secrets/PII in logs" is the same red line
- [§4.1 Definition of Done](../04_quality_gates/01_dod.md) — how observability folds into the DoD

---

## 📝 Status

v0.5.0 (Phase 2: original content)
