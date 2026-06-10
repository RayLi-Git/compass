#!/usr/bin/env bash
#
# commit-msg-lint.sh — Compass M-010 commit-msg hook (EXAMPLE / REFERENCE)
#
# WHAT 這個 hook 做什麼：
#   讀取 commit message 檔（git 以第一個參數 $1 傳入），掃描一份「主觀完成詞」
#   黑名單。若 message 含任一黑名單詞，印出違規詞 + 規則到 stderr，並以
#   exit 1 擋下 commit；否則 exit 0 放行。
#
# WHY 為什麼（對應 M-010）：
#   主觀的「完成 / done / 全部 / 一次到位」描述會掩蓋真實覆蓋率，讓人誤判
#   進度。M-010 要求 commit 用「具體計數」描述成果（如 12/12 endpoints），
#   漏項要顯式標註（⚠ 已知漏項：...），而不是用感覺良好的字眼帶過。
#
# HOW TO INSTALL 安裝方式：
#   cp scripts/commit-msg-lint.sh .git/hooks/commit-msg
#   chmod +x .git/hooks/commit-msg
#
# NOTE 注意：
#   * 這是 EXAMPLE / 參考實作。各專案應依自身用語「微調黑名單」
#     （見下方 BANNED 陣列），不要照單全收。
#   * 純 bash、POSIX 風格；可通過 `bash -n` 語法檢查。
#
# EXIT CODES：
#   0 = 通過（無黑名單詞）
#   1 = 擋下（含黑名單詞，或 message 檔讀不到）

set -u

# --- 可微調黑名單（case-insensitive，盡量比對成獨立詞/詞組）---------------
# 各專案請依團隊用語增刪。中文詞不分詞邊界，直接子字串比對。
BANNED="complete completed done finished all-done 完整 全部 一次到位 全套 已實作"

# git 把 commit message 檔路徑當第一參數傳入
MSG_FILE="${1:-}"
if [ -z "${MSG_FILE}" ] || [ ! -f "${MSG_FILE}" ]; then
	echo "commit-msg-lint: 找不到 commit message 檔（\$1='${MSG_FILE}'）" >&2
	exit 1
fi

# 轉小寫以便 case-insensitive 比對（英文）。中文不受影響。
MSG_LOWER="$(tr '[:upper:]' '[:lower:]' < "${MSG_FILE}")"

RULE='用具體計數，如 12/12 endpoints；漏項用 ⚠ 已知漏項：...'
HITS=""

for word in ${BANNED}; do
	# "all done" 在黑名單以 all-done 表示，比對時還原成空白
	probe="$(printf '%s' "${word}" | tr '-' ' ' | tr '[:upper:]' '[:lower:]')"
	case "${MSG_LOWER}" in
		*"${probe}"*)
			HITS="${HITS} ${word}"
			;;
	esac
done

if [ -n "${HITS}" ]; then
	echo "commit-msg-lint: 偵測到禁用的主觀完成詞 →${HITS}" >&2
	echo "規則：${RULE}" >&2
	echo "（這是 M-010 EXAMPLE hook；可在 scripts/commit-msg-lint.sh 微調黑名單）" >&2
	exit 1
fi

exit 0
