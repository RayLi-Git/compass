# §6.5 Accessibility (a11y) and Internationalization (i18n)

> Part of [Compass](../../SKILL.md) §6 — Non-functional requirements (NFR).
> a11y and i18n are nearly free when built in at design time; retrofitting them is hell — so they belong in DoR, not as a pre-launch patch.

---

## 🎯 Core stance

Both share the same nature: **built in at design time = cheap; retrofitted after launch = brutal.**

| Dimension | Built in at design time | Retrofitted afterward |
|---|---|---|
| a11y | Semantic HTML + keyboard flow, near zero cost | Rewrite DOM, add ARIA, retest every component |
| i18n | Externalized strings + locale-aware formatting | Hunt hardcoded copy across the codebase, rework layout, handle RTL |

Conclusion: **whether a11y / i18n is in scope must be settled at DoR** (see [§2.1 DoR checklist](../02_definition_of_ready/01_dor_checklist.md)). PRD silence doesn't mean "skip it" — it means "scope undefined," go back and ask.

---

## 🚩 DoR interception rule (when PRD is silent on a11y/i18n)

If the PRD doesn't mention a11y or i18n, don't treat it as "not needed" and skip. This is a PRD gap — run [§5.1 vague/bug/gap handling](../05_conflict_handling/01_vague_bug_gap.md), flag it in DoR, and ask back:

- "Does this UI need keyboard operation / screen reader support?" (a11y scope)
- "Will there be multi-language / multi-region versions later?" (i18n scope)
- "Any regulatory requirement?" (in some industries a11y is a legal obligation, not optional)

Before you get an answer, at least do **string externalization** and **semantic HTML** as the default — these two cost nothing even if i18n/a11y never ships, while retrofitting them is what costs.

---

## ♿ a11y: WCAG baseline

Don't memorize all of WCAG. Remember the five you can check directly in a PR:

| Item | Rule | Quick self-check |
|---|---|---|
| Keyboard reachable | All interactive elements Tab-reachable, Enter/Space triggerable, focus order sensible | Unplug the mouse and walk through it |
| Semantic HTML | Use `<button>`/`<nav>`/`<label>`, not `<div onClick>` | Check the DOM for piles of bare divs acting as buttons |
| Contrast | Text against background ≥ 4.5:1 (large text ≥ 3:1) | Measure once with a contrast checker |
| Alt text | `<img>` has `alt`; decorative images use `alt=""` | grep for imgs without alt |
| ARIA fallback | Add ARIA only when native semantics fall short, and get role/state right | Only touch ARIA when there's no native tag |

**Iron rule: ARIA is the last resort, not the first.** One correct `<button>` beats anything cobbled together with `<div role="button" tabindex="0" aria-pressed>`. Wrong ARIA is worse than no ARIA.

### a11y checklist per UI feature

When adding any interactive UI, go through every item:

- [ ] The entire operation flow can be completed with keyboard alone (including opening/closing modals, submitting forms)
- [ ] Focus state is visible (not just `outline: none`)
- [ ] Form fields all have associated `<label>` (`for`/`id` or wrapping)
- [ ] Images/icons have text alternatives; pure decoration marked `alt=""`/`aria-hidden`
- [ ] Color is not the sole information carrier (errors can't rely on red alone — need text/icon)
- [ ] Dynamic content changes are announced (`aria-live` for toasts/errors)
- [ ] When a modal opens, focus is trapped inside; on close, focus returns to the triggering element

### Example (React/TS, not mandatory)

```tsx
// ❌ Screen reader can't read it, keyboard can't reach it
<div className="btn" onClick={handleDelete}>Delete</div>

// ✅ Native semantics, keyboard and screen reader for free
<button type="button" onClick={handleDelete}>Delete</button>

// Error message: color + text + live region
<p role="alert" className="error">Email format is invalid</p>
```

---

## 🌐 i18n: four pillars

### 1. String externalization (no hardcoded copy)

All UI copy goes through resource files / translation functions, never written directly in the component.

```tsx
// ❌ hardcoded, you'll be hunting it forever
<h1>Welcome back</h1>

// ✅ key-ified, copy centralized
<h1>{t("home.welcome_back")}</h1>
```

Red flag: any user-facing literal string in a PR (buttons, titles, errors, email templates).

### 2. Locale-aware formatting

Dates, numbers, currency: **never assemble by hand.** Use the platform's locale API.

| Data | Wrong way | Right way |
|---|---|---|
| Date | `` `${y}/${m}/${d}` `` | `Intl.DateTimeFormat(locale)` |
| Number | Manually inserting thousands separators | `Intl.NumberFormat(locale)` |
| Currency | `` `$${n}` `` | `Intl.NumberFormat(locale, {style:"currency", currency})` |
| Timezone | Store local time | Store UTC, convert to locale timezone on display |

### 3. Pluralization

Don't hard-split with `count === 1 ? "item" : "items"`. Plural rules differ across languages (some have 3+ forms). Use ICU MessageFormat / `Intl.PluralRules`.

```ts
// ❌ Barely works for English/Chinese only
const label = `${n} ${n === 1 ? "file" : "files"}`;

// ✅ Hand it to plural rules
t("file_count", { count: n }); // define one/other/... inside the translation file
```

### 4. RTL awareness

When supporting Arabic/Hebrew, the layout mirrors. Use CSS logical properties, not directional properties.

| Don't | Use instead |
|---|---|
| `margin-left` | `margin-inline-start` |
| `text-align: left` | `text-align: start` |
| `left: 0` | `inset-inline-start: 0` |

Even if you only do LTR now, build the habit of using logical properties — turning on RTL later becomes near zero change.

### i18n checklist

- [ ] No user-facing hardcoded strings
- [ ] Dates/numbers/currency all go through `Intl` or an equivalent locale API
- [ ] Time stored as UTC
- [ ] Plurals via plural rules, not `=== 1`
- [ ] Layout uses logical properties (leaving a path for RTL)
- [ ] Strings don't assemble sentences by concatenation (word order varies by language — one key per whole sentence)

---

## ⚖️ Decision procedure: do it now or not?

```
PRD specifies a11y/i18n scope?
├─ Yes → implement to PRD scope, include in DoD
└─ No  → ask the user back at DoR (see interception rule above)
          ├─ Confirmed do → add to PRD scope, build it as a requirement
          ├─ Confirmed skip → still do "string externalization + semantic HTML" by default
          └─ Undecided → flag ⚠️await ruling, do the two low-cost items by default, skip the high-cost retrofit items
```

YAGNI doesn't apply to just cutting i18n/a11y — "string externalization, semantic HTML, logical properties" are low-cost upfront investments; cutting them locks in the future retrofit cost (see [§3.5 YAGNI](../03_implementation/05_yagni.md)).

---

## 🔗 Related Compass sections

- [§6 NFR overview](./01_nfr_overview.md) — where a11y/i18n sits in the NFR landscape
- [§2.1 DoR checklist](../02_definition_of_ready/01_dor_checklist.md) — scope is settled here
- [§5.1 Vague/Bug/Gap handling](../05_conflict_handling/01_vague_bug_gap.md) — the ask-back flow when the PRD is silent
- [§4.1 DoD](../04_quality_gates/01_dod.md) — confirmed a11y/i18n items fold into the definition of done

## 📝 Status

v0.5.0 (Phase 2: original content)
