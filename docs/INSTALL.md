<!-- LANG SWITCH -->

**English** | [繁體中文](./INSTALL.zh-TW.md)

# Installation Guide

> Compass has three parts: the **skill itself** (`SKILL.md` + `references/`, an on-demand PRD-discipline knowledge base), the **tooling scripts** (`scripts/`, runnable examples for M-007/008/010), and the **tracking-doc templates** (`templates/`). The skill itself is required; installing the tools and templates alongside it is recommended for the full experience.

---

## Prerequisites

- [Claude Code](https://docs.claude.com) installed.
- To use the reverse audit / checklist expansion in `scripts/`: **Python 3** (standard library only, no pip dependencies).
- To use the commit-msg hook: **bash** + a git repo.
- Recommended to install alongside [Sentinel](https://github.com/RayLi-Git/sentinel) (Compass handles "how to execute against the spec," Sentinel handles "how to think").

---

## 1. Install the skill itself (required)

A skill is, at its core, "a folder containing a `SKILL.md`." Installing it just means putting it in a skills directory Claude Code scans.

### Option A: Global install (recommended, applies to all projects)

```bash
mkdir -p ~/.claude/skills/compass

# If you received a packaged .skill / .zip file
unzip compass.skill -d ~/.claude/skills/compass

# Or if you cloned this repo, copy the contents directly
cp -r SKILL.md references ~/.claude/skills/compass/
```

### Option B: Project-level install (applies to a single project only)

```bash
mkdir -p .claude/skills/compass
cp -r SKILL.md references .claude/skills/compass/
```

### Verify the structure (important)

```bash
ls ~/.claude/skills/compass
# Must show: SKILL.md  references

ls ~/.claude/skills/compass/references
# Should show 11 module folders: 01_foundations … 11_tooling
```

> ⚠️ Common mistake: after unzipping you end up with an extra nesting level, `compass/compass/SKILL.md`.
> `SKILL.md` must sit **directly** under `~/.claude/skills/compass/`. If there's an extra level, move the inner contents up.

---

## 2. (Recommended) Install the tooling scripts and templates

The tooling scripts are runnable examples of the §11 rules; the templates are the starting point for the §3.2 tracking docs. Recommended to put them in **the project you're working in** (not the skills directory).

```bash
# In your project root
cp -r /path/to/compass/scripts ./scripts
cp -r /path/to/compass/templates ./templates
```

For each tool's usage, see [`scripts/README.md`](../compass-en/scripts/README.md) and [`templates/README.md`](../compass-en/templates/README.md). Highlights:

```bash
# M-008 reverse audit: copy the example config first, then adapt it to your project structure
cp templates/audit-config.example.json compass-audit.json
python3 scripts/audit_prd_vs_code.example.py        # exit 0 aligned / 1 gaps / 2 config missing

# M-007 expand a PRD table into a checklist
python3 scripts/expand_checklist.example.py PRD.md > prd-checklist.md

# M-010 commit-message gate (install as a git hook)
cp scripts/commit-msg-lint.sh .git/hooks/commit-msg
chmod +x .git/hooks/commit-msg
```

---

## 3. Start using it

1. Open a **new** Claude Code session (only a fresh start will scan the new skill).
2. Throw it a PRD implementation task (e.g. "implement the auth module of this PRD," "I'm starting on this spec"). Compass triggers automatically and runs the matching flow per task size.

### Quickly confirm Compass actually triggered

After opening a new session, throw this test:

> "I have a PRD to start implementing — run a pre-flight health check first."

Compass should guide you through **§2 Definition of Ready** (the PRD implementability health-check list). If it doesn't mention DoR / health check, the skill wasn't scanned — go back and check the install structure.

### Where do the tracking docs Compass produces live?

Compass tracks PRD progress with these docs in **the project directory you're working in**:

```
your-project/
└── .claude/
    ├── progress.md            # PRD task progress + todo + in-progress
    ├── development-log.md     # decisions + PRD deviations (vague/bug/gap) records
    └── prd-checklist.md       # PRD section ↔ implementation mapping (one line per item)
```

> 💡 Recommended to add the project's `.claude/` to git, so PRD progress and decisions persist across sessions / machines.

---

## 4. Pairing with Sentinel

Compass and Sentinel share the `.claude/` case-history files (`debug-log.md` / `patterns.md`). With both installed:

- Got a PRD, pre-flight → Compass §1+§2 + Sentinel pre-flight protocol
- Hit a complex bug mid-implementation → Sentinel diagnosis phase + Compass §5 (if it's a PRD deviation)
- Before shipping → Compass §4+§7 + Sentinel's three safety nets

---

## Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| skill not triggered | didn't open a new session | restart Claude Code |
| can't find references files | extra folder nesting | confirm `SKILL.md` is directly under `compass/` |
| `audit_prd_vs_code` exits 2 every time | no `compass-audit.json` | copy `templates/audit-config.example.json` and adapt it to your structure |
| `python3` not found / is a stub | Windows Store alias | use the real Python path or the `py` launcher |
| tracking docs not generated | task didn't enter the 🟡/🔴 flow | normal — pure typo/style changes don't start tracking |

---

## Uninstall

```bash
rm -rf ~/.claude/skills/compass
# Remove the project's scripts/ templates/ .claude/ yourself as needed
```
