# §6.4 Security: beyond test-first

> Part of [Compass](../../SKILL.md) §6 — Non-Functional Requirements (NFR).
> §3.3 / DoR already require Auth / authz / PII test-first; this file handles the per-feature security review gate for "everything else."

---

## 🎯 Positioning

Test-first covers only three high-sensitivity modules (Auth / authz / PII), but **injection, SSRF, XSS, IDOR don't pick modules**—any feature that takes external input, makes external requests, concatenates strings, or returns data to a browser can get hit.

This file provides a **per-feature security review gate**: for each feature you implement, run through an OWASP cross-reference table + STRIDE-lite, and decide in 30 seconds "does this need extra security work?" It's not writing a threat-model document—it's a quick screen before DoD.

> Maps to Sentinel's "five security categories" thinking: #distrust-input, #authn-authz, #least-privilege, #sensitive-data, #secure-by-default. This file turns it into a checkable list.

---

## ✅ Trigger conditions: which features must pass this gate

| Feature trait | Must pass gate |
|---|---|
| Takes `req.body` / `query` / `params` / uploaded file / webhook | ✅ |
| Concatenates SQL / shell / path / template string | ✅ |
| Renders data into HTML / returns to frontend | ✅ |
| Uses a user-supplied URL / ID to make a request or fetch a resource | ✅ |
| Reads/writes a resource "belonging to some user" | ✅ |
| Touches keys / tokens / passwords / third-party credentials | ✅ |
| Pure internal computation, no I/O, no external input | ⛔ Skip |

Match any one → run the OWASP cross-reference + STRIDE-lite below. Match none → go straight to DoD.

---

## 🔟 OWASP Top 10 quick cross-reference (review checklist)

For each item, ask "does this feature have this surface?" If yes, check it; if checked, it needs corresponding protection.

- [ ] **A01 Broken access control / IDOR** — Does it fetch a resource by an ID from URL/body? When querying, does it **also verify `resource.owner == current_user`**? Verifying "logged in" alone doesn't count.
- [ ] **A02 Cryptographic failures** — Is sensitive data encrypted at rest? Transport over HTTPS? Passwords with bcrypt/argon2, not MD5/SHA?
- [ ] **A03 Injection** — Concatenating SQL / shell / LDAP / NoSQL query? Always parameterize / ORM-bind, **never string concatenation**.
- [ ] **A04 Insecure design** — Does the feature's own flow have logic holes (price tampering, replay, negative quantity)?
- [ ] **A05 Security misconfiguration** — debug mode, default passwords, overly-broad CORS, directory listing, stack-trace leakage?
- [ ] **A06 Vulnerable/outdated components** — Did you check the new dependency for CVEs? Is the version pinned?
- [ ] **A07 Authentication failures** — Brute-force protection? Session expiry? Tokens revocable?
- [ ] **A08 Integrity failures** — Deserializing untrusted data? CI/CD pulling unverified sources?
- [ ] **A09 Logging/monitoring failures** — Are security events (failed login, access denied) logged? Do logs **not** contain passwords/tokens?
- [ ] **A10 SSRF** — Making requests with a user-supplied URL? Do you block internal network ranges / metadata endpoints (`169.254.169.254`)?

> Not every item needs to be done. Every item needs to be **asked**—record what doesn't apply as "N/A," and put what does into your to-dos.

---

## 🛡️ STRIDE-lite: per-feature threat self-questioning

You don't need a full threat model. For each feature, spend 1 minute asking one question per surface across 6 axes:

| Axis | One-line self-question | Consequence if unanswered |
|---|---|---|
| **S Spoofing** | How do I confirm the requester is who they claim to be? | Identity impersonation |
| **T Tampering** | Can data be altered in transit/storage? Would I detect it? | Data tampered with |
| **R Repudiation** | After an incident, can I trace "who, when, did what"? | Cannot assign accountability |
| **I Information disclosure** | Could this path return more data than it should / error messages that leak internals? | Unauthorized reads |
| **D Denial of service** | Can one request take it down (no pagination, infinite loop, huge file)? | Service outage |
| **E Elevation of privilege** | Can a regular user reach admin capabilities / someone else's resources? | Unauthorized operations |

**Decision rule**: if any axis can't be answered or the answer is "yes (it can)" → that axis goes into to-dos, no straight-to-DoD.

### Example (FastAPI, per-feature STRIDE-lite annotations)

```python
# Feature: GET /orders/{order_id}
# S: identity via JWT ✅
# T: HTTPS only ✅
# R: access log records user_id + order_id ✅
# I: ⚠️ not filtered before return—order contains internal_cost field → to-do: DTO whitelist
# D: ⚠️ no rate limit → to-do
# E: ⚠️ only verifies login, not owner → to-do (IDOR, top priority)
@router.get("/orders/{order_id}")
async def get_order(order_id: int, user=Depends(current_user)):
    order = await repo.get(order_id)
    if order.user_id != user.id:        # ← E fix: verify owner
        raise HTTPException(404)         # use 404 not 403 to avoid leaking existence
    return OrderDTO.from_orm(order)      # ← I fix: whitelist fields
```

---

## 🔑 Secrets handling

Absolute red lines—violate one and stop, redo:

- [ ] Keys / passwords / tokens **not hardcoded in code**, not committed to git (including commit history).
- [ ] Always injected from environment variables / secret manager; repo keeps only `.env.example` (no real values).
- [ ] `.env`, `*.pem`, `credentials.*` are in `.gitignore`.
- [ ] **Logs / error messages / response bodies don't print secrets** (including the raw value before partial masking).
- [ ] Tokens have an expiry; never "never expires."
- [ ] Third-party webhooks / callbacks verify the signature; don't blindly trust the source.

> If a secret already made it into git history → "remove it next commit" isn't enough: **rotate the key**, treat the old value as leaked.

---

## 🔒 Secure-by-default

When a design choice pits "convenient" against "secure," default to secure:

| Anti-pattern (fail open) | Secure by default (fail closed) |
|---|---|
| `try { check() } catch { allow }` | catch → deny + log |
| No permission rule found → allow | No rule found → deny |
| New field returned to frontend by default | Not returned by default, only on whitelist |
| Grant admin / global permissions for convenience | Grant the minimum sufficient privilege (#least-privilege) |
| Return full stack trace on error | Return generic message externally, details only to internal log |
| CORS `*` | Explicitly list allowed origins |

---

## 🚦 Review gate verdict (before reaching DoD)

After running this gate, produce one of three:

1. 🟢 **All N/A or already protected** → record one line "security review: no new risk," proceed to [DoD](../04_quality_gates/01_dod.md).
2. 🟡 **To-dos exist but non-blocking** → put into the tracking doc, fix before this slice is complete (Compass doesn't phase work → no "add security later").
3. 🔴 **Touches Auth / authz / PII** → bounce back to [DoR](../02_definition_of_ready/01_dor_checklist.md)'s test-first requirement, write tests before implementing.

> Security to-dos **must not be batched up to the end**. Each feature's security hole gets cleared before that slice's commit—this is §6.4's extension of the compare-fix loop.

---

## 🔗 Related Compass sections

- [§6 NFR module overview](./_index.md) — security's place within NFR
- [§6.3 Observability](./03_observability.md) — where STRIDE's R (repudiation) / A09 (logging) land
- [§4.1 DoD](../04_quality_gates/01_dod.md) — security review gate sits before DoD
- [§2.1 DoR checklist](../02_definition_of_ready/01_dor_checklist.md) — source of the test-first requirement for Auth/authz/PII

---

## 📝 Status

v0.5.0 (Phase 2: original content)
