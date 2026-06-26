#!/usr/bin/env python3
"""
audit_prd_vs_code.example.py — Compass M-008 反向稽核（reverse audit）

【做什麼 / WHAT】
  比對「PRD 列出的項目」與「程式碼實際實作的項目」，找出三類差異：
    ✅ aligned            — PRD 有、code 也有（對齊）
    ❌ in PRD but not code — PRD 寫了但 code 沒實作（這是會讓 DoD 不過的缺口）
    ⚠️ in code but not PRD — code 有但 PRD 沒寫（先過 §5.1.3 六道 gate；多數越界應砍，少數對齊原則的小補強才保留等裁決）

【為什麼 / WHY — 對應哪條 M 規則】
  M-008「反向稽核」：一般檢查只確認「PRD→code」（有沒有漏做），
  反向稽核同時檢查「code→PRD」（有沒有偷加 PRD 沒授權的東西）。
  前者守 DoD 完成度，後者守 YAGNI / §5.1.3 越界。

【如何設定 / HOW TO CONFIGURE】
  本腳本「專案無關」(project-agnostic)：所有 regex、路徑、glob 都來自設定檔，
  腳本本身不寫死任何特定專案的 PRD 結構。
  設定檔名固定為 compass-audit.json（與本腳本同目錄或當前工作目錄），
  也可用 --config 指定路徑。設定檔用 JSON（走 stdlib json，不依賴 pyyaml）。
  Schema 範例見下方 CONFIG_EXAMPLE。

【已知限制 / LIMITATION】
  CONFIG_EXAMPLE 的 endpoint check 只 capture「path」，不分辨 HTTP method：
  PRD 的 `GET /users` 與 code 的 `POST /users` 會被當成同一項 → method 不符
  「不會」被抓成缺口（假陰性）。若你的 PRD 需要 method 敏感度，請讓
  prd_regex / code_regex 各自把「method + path」capture 成同一組可比對字串
  （注意 code 端 method 多為小寫如 @app.post，需正規化大小寫後再比）。

【如何執行 / HOW TO RUN】
  python3 audit_prd_vs_code.example.py                 # 跑全部 checks
  python3 audit_prd_vs_code.example.py --section=tables # 只跑名為 tables 的 check
  python3 audit_prd_vs_code.example.py --config path/to/compass-audit.json

【離開碼 / EXIT CODES】
  0 — 沒有「in PRD but not code」缺口（可能仍有 ⚠️ 警告，但不阻擋）
  1 — 至少一個 check 出現「in PRD but not code」缺口（DoD 未達成）
  2 — 設定檔缺失或無法解析（會印出說明 + 可直接複製的 JSON 範例）

僅依賴 Python 標準函式庫（argparse / json / re / pathlib / sys）。
"""

import argparse
import json
import re
import sys
from pathlib import Path

# Windows console 預設編碼可能是 cp950 / cp1252，無法編碼結果中的 ✅ / ❌ 等字元。
# 若不處理，print 那一行會丟 UnicodeEncodeError 讓腳本中途崩潰，使行程以 exit 1 退出——
# 而 exit 1 在本腳本語意上代表「PRD 有缺口」，會把「完全對齊」的專案誤報成有缺口。
# 故在此強制 stdout / stderr 走 UTF-8；reconfigure 失敗（非 TextIO 或舊版）則靜默略過。
for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8")
    except (AttributeError, ValueError):
        pass

# 設定檔預設檔名（固定）。找尋順序：--config > 當前工作目錄 > 腳本所在目錄。
DEFAULT_CONFIG_NAME = "compass-audit.json"

# 缺設定檔時印給使用者直接複製的範例。
CONFIG_EXAMPLE = """{
  "prd_path": "PRD.md",
  "checks": [
    {
      "name": "endpoints",
      "prd_regex": "`(?:GET|POST|PUT|PATCH|DELETE)\\\\s+(/[\\\\w/{}-]+)`",
      "code_glob": "backend/**/*.py",
      "code_regex": "@app\\\\.(?:get|post|put|patch|delete)\\\\(\\\"(/[\\\\w/{}-]+)\\\""
    },
    {
      "name": "tables",
      "prd_regex": "(?:table|資料表)\\\\s+`(\\\\w+)`",
      "code_glob": "migrations/**/*.sql",
      "code_regex": "CREATE\\\\s+TABLE\\\\s+(?:IF\\\\s+NOT\\\\s+EXISTS\\\\s+)?`?(\\\\w+)`?"
    }
  ]
}"""


def die_no_config(searched):
    """設定檔缺失：印說明 + 範例，回傳 exit code 2。"""
    print("❌ 找不到設定檔 compass-audit.json。", file=sys.stderr)
    print("   已嘗試以下位置：", file=sys.stderr)
    for p in searched:
        print(f"     - {p}", file=sys.stderr)
    print("", file=sys.stderr)
    print("請在專案根目錄建立 compass-audit.json，內容範例（可直接複製修改）：",
          file=sys.stderr)
    print("", file=sys.stderr)
    print(CONFIG_EXAMPLE, file=sys.stderr)
    print("", file=sys.stderr)
    print("提示：所有 regex / glob 由設定檔提供，本腳本與專案無關。", file=sys.stderr)
    sys.exit(2)


def find_config(explicit):
    """依序尋找設定檔；找不到回傳 (None, 試過的清單)。"""
    candidates = []
    if explicit:
        candidates.append(Path(explicit))
    else:
        candidates.append(Path.cwd() / DEFAULT_CONFIG_NAME)
        candidates.append(Path(__file__).resolve().parent / DEFAULT_CONFIG_NAME)
    for c in candidates:
        if c.is_file():
            return c, candidates
    return None, candidates


def load_config(path):
    """讀 JSON 設定。解析失敗一律走 exit 2。"""
    try:
        text = path.read_text(encoding="utf-8")
        cfg = json.loads(text)
    except (OSError, json.JSONDecodeError) as e:
        print(f"❌ 無法解析設定檔 {path}：{e}", file=sys.stderr)
        print("", file=sys.stderr)
        print("正確格式範例：", file=sys.stderr)
        print(CONFIG_EXAMPLE, file=sys.stderr)
        sys.exit(2)
    if not isinstance(cfg, dict) or "checks" not in cfg:
        print("❌ 設定檔缺少必要欄位 'checks'（應為陣列）。", file=sys.stderr)
        print(CONFIG_EXAMPLE, file=sys.stderr)
        sys.exit(2)
    return cfg


def extract_from_text(text, pattern):
    """對單一文字套用 regex，回傳擷取項目的 set。
    若 regex 有 capture group 取 group(1)，否則取整段 match。"""
    found = set()
    for m in re.finditer(pattern, text):
        item = m.group(1) if m.groups() else m.group(0)
        if item:
            found.add(item.strip())
    return found


def extract_prd_items(prd_path, pattern):
    """從 PRD 檔擷取項目集合。PRD 不存在則視為空集合並警告。"""
    p = Path(prd_path)
    if not p.is_file():
        print(f"⚠️ 找不到 PRD 檔 {prd_path}（視為空集合）", file=sys.stderr)
        return set()
    try:
        text = p.read_text(encoding="utf-8", errors="replace")
    except OSError as e:
        print(f"⚠️ 讀取 PRD 檔失敗 {prd_path}：{e}", file=sys.stderr)
        return set()
    return extract_from_text(text, pattern)


def extract_code_items(code_glob, pattern):
    """用 pathlib glob/rglob 遍歷符合的檔案，擷取 code 端項目集合。
    支援 ** 遞迴（透過 rglob）。"""
    found = set()
    base = Path(".")
    # 含 ** 用 rglob 較自然；pathlib 的 glob 也支援 **，這裡直接交給 glob。
    try:
        files = list(base.glob(code_glob))
    except (ValueError, re.error) as e:
        print(f"⚠️ glob 模式無效 '{code_glob}'：{e}", file=sys.stderr)
        return found
    for f in files:
        if not f.is_file():
            continue
        try:
            text = f.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        found |= extract_from_text(text, pattern)
    return found


def run_check(check, prd_path):
    """執行單一 check，回傳是否有「in PRD but not code」缺口（bool）。"""
    name = check.get("name", "<unnamed>")
    prd_regex = check.get("prd_regex")
    code_glob = check.get("code_glob")
    code_regex = check.get("code_regex")

    print(f"\n=== check: {name} ===")
    missing_fields = [k for k in ("prd_regex", "code_glob", "code_regex")
                      if not check.get(k)]
    if missing_fields:
        print(f"  ⚠️ 設定不完整，略過。缺少欄位：{', '.join(missing_fields)}")
        return False

    prd_set = extract_prd_items(prd_path, prd_regex)
    code_set = extract_code_items(code_glob, code_regex)

    aligned = sorted(prd_set & code_set)
    prd_only = sorted(prd_set - code_set)   # ❌ DoD 缺口
    code_only = sorted(code_set - prd_set)  # ⚠️ 可能 §5.1.3 越界

    print(f"  PRD 列出 {len(prd_set)} 項；code 實作 {len(code_set)} 項。")

    if aligned:
        print(f"  ✅ aligned ({len(aligned)}): {', '.join(aligned)}")
    if prd_only:
        print(f"  ❌ in PRD but not code ({len(prd_only)}): "
              f"{', '.join(prd_only)}")
        print("     → 這些 PRD 要求尚未實作，DoD 不過。")
    if code_only:
        print(f"  ⚠️ in code but not PRD ({len(code_only)}): "
              f"{', '.join(code_only)}")
        print("     → 先過 §5.1.3 六道 gate：多數越界（新 endpoint/表/欄位/依賴/改 API）應砍，少數對齊原則的小補強才保留等裁決。")
    if not (aligned or prd_only or code_only):
        print("  （PRD 與 code 兩端皆無匹配項目，請檢查 regex 是否正確）")

    return bool(prd_only)


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="M-008 反向稽核：比對 PRD 列出 vs code 實作的項目。")
    parser.add_argument("--config", default=None,
                        help="設定檔路徑（預設找 compass-audit.json）")
    parser.add_argument("--section", default=None,
                        help="只執行指定名稱的單一 check")
    args = parser.parse_args(argv)

    config_path, searched = find_config(args.config)
    if config_path is None:
        die_no_config(searched)

    cfg = load_config(config_path)
    prd_path = cfg.get("prd_path", "PRD.md")
    checks = cfg.get("checks", [])

    if args.section:
        checks = [c for c in checks if c.get("name") == args.section]
        if not checks:
            print(f"❌ 設定檔中找不到名為 '{args.section}' 的 check。",
                  file=sys.stderr)
            sys.exit(2)

    print(f"Compass M-008 reverse audit — 設定檔: {config_path}")
    print(f"PRD: {prd_path}")

    has_gap = False
    for check in checks:
        if run_check(check, prd_path):
            has_gap = True

    print("\n" + "=" * 40)
    if has_gap:
        print("結果：❌ 存在 PRD 缺口（in PRD but not code）— DoD 未達成。")
        sys.exit(1)
    print("結果：✅ 無 PRD 缺口。")
    sys.exit(0)


if __name__ == "__main__":
    main()
