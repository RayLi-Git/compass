#!/usr/bin/env bash
#
# commit-msg-lint.sh — Compass M-010 commit-msg hook (EXAMPLE / REFERENCE)
#
# WHAT this hook does:
#   Reads the commit message file (git passes it as the first argument $1) and scans it
#   against a blacklist of "subjective completion words". If the message contains any
#   blacklisted word, it prints the offending word + the rule to stderr and blocks the
#   commit with exit 1; otherwise it exits 0 and lets the commit through.
#
# WHY (corresponds to M-010):
#   Subjective "complete / done / all / done in one shot" descriptions mask the real
#   coverage and lead to misjudging progress. M-010 requires commits to describe results
#   with "concrete counts" (e.g. 12/12 endpoints), and to explicitly flag any omissions
#   (⚠ Known omission: ...) rather than glossing over them with feel-good phrasing.
#
# HOW TO INSTALL:
#   cp scripts/commit-msg-lint.sh .git/hooks/commit-msg
#   chmod +x .git/hooks/commit-msg
#
# NOTE:
#   * This is an EXAMPLE / reference implementation. Each project should "fine-tune the
#     blacklist" to its own wording (see the BANNED array below); do not adopt it wholesale.
#   * Pure bash, POSIX style; passes the `bash -n` syntax check.
#
# EXIT CODES:
#   0 = pass (no blacklisted words)
#   1 = blocked (contains a blacklisted word, or the message file cannot be read)

set -u

# --- Tunable blacklist (case-insensitive) -------------------------------------------------------
# Each project should add/remove entries per its team's wording.
#   * English terms are matched on WORD BOUNDARIES (grep -iqw) to avoid false positives on
#     legit words like incomplete / unfinished / abandoned / completion.
#     (Note: not -F, since some GNU grep builds crash when -F and -w are combined; the terms
#      are plain alphanumerics with no regex metacharacters, so BRE is safe.)
#   * CJK terms have no word boundaries, so match them as plain substrings (grep -Fq).
EN_BANNED="complete completed done finished all-done one-shot full-set shipped"
CJK_BANNED=""   # e.g. "完整 全部 一次到位 全套 已實作" for Chinese projects

# git passes the commit message file path as the first argument
MSG_FILE="${1:-}"
if [ -z "${MSG_FILE}" ] || [ ! -f "${MSG_FILE}" ]; then
	echo "commit-msg-lint: commit message file not found (\$1='${MSG_FILE}')" >&2
	exit 1
fi

RULE='Use concrete counts, e.g. 12/12 endpoints; flag omissions with ⚠ Known omission: ...'
HITS=""

# English: word boundary + case-insensitive (-iqw). "all done" is stored as all-done; restore the space.
for word in ${EN_BANNED}; do
	probe="$(printf '%s' "${word}" | tr '-' ' ')"
	if grep -iqw -- "${probe}" "${MSG_FILE}"; then
		HITS="${HITS} ${word}"
	fi
done

# CJK: plain substring (-Fq); CJK has no word boundaries.
for word in ${CJK_BANNED}; do
	if grep -Fq -- "${word}" "${MSG_FILE}"; then
		HITS="${HITS} ${word}"
	fi
done

if [ -n "${HITS}" ]; then
	echo "commit-msg-lint: detected banned subjective completion words →${HITS}" >&2
	echo "Rule: ${RULE}" >&2
	echo "(This is the M-010 EXAMPLE hook; tune the blacklist in scripts/commit-msg-lint.sh)" >&2
	exit 1
fi

exit 0
