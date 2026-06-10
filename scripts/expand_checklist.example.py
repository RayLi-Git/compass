#!/usr/bin/env python3
"""expand_checklist.example.py — Compass Phase 4 / M-007 anti-aggregation.

WHAT (做什麼)
------------
讀一個 PRD markdown 檔，找出其中的 markdown 表格（以 "|" 開頭的行），
跳過表頭列與分隔列（如 "|---|---|"），把每一筆「資料列」展開成
**一行一個 checkbox** 的 checklist：

    - [ ] <section> | <first meaningful cell>

REFERENCE / EXAMPLE 用途
------------------------
本檔副檔名為 `.example.py`，是參考實作。可直接用 python3 標準庫執行，
不依賴任何 pip 套件。請依自己專案的 PRD 結構調整，不要假設欄位固定。

WHY (為什麼 — 對應 M-007 規則)
------------------------------
M-007「反聚合 (anti-aggregation)」：PRD 裡常見一行寫
"12 endpoints ⬜" 這種聚合條目，會把 12 件待辦藏在一個勾選框後面，
驗收時容易整批被當成「做完」。本工具把它攤成 12 條獨立 ⬜，
讓任何一條沒做都藏不住。

HOW TO CONFIGURE (怎麼設定)
---------------------------
本工具用「命令列旗標」驅動，不在程式內寫死任何特定專案的 PRD 結構：

    --section-header TEXT   每條 checklist 前綴的 section 標籤
                            （預設取最近一個 markdown 標題 "# / ## ..."）
    --cell-index N          取資料列的第幾欄當內容（0 起算，預設 0；
                            跳過空白欄找第一個有意義的欄）
    --min-cols N            少於 N 欄的表格列視為雜訊跳過（預設 1）

HOW TO RUN (怎麼執行)
---------------------
    python3 expand_checklist.example.py PRD.md > prd-checklist.md
    python3 expand_checklist.example.py PRD.md --section-header "API" --cell-index 1

EXIT CODES (離開碼)
-------------------
    0  成功（有找到表格並輸出，或檔案可讀但無表格 — 印提示到 stderr）
    1  參數錯誤 / 缺少輸入檔（印用法與設定範例）
    2  輸入檔不存在或無法讀取
"""

import sys
import os
import argparse

# Windows console 預設可能是 cp950 / cp1252，無法編碼 PRD 內的 emoji（如 🟢/🪤）等字元。
# 不處理會在 print 該列時丟 UnicodeEncodeError 中途崩潰，造成「部分輸出 + 截斷」或「看似無輸出」，
# 使用者誤以為展開失敗。故強制 stdout / stderr 走 UTF-8；失敗（非 TextIO 或舊版）則靜默略過。
for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8")
    except (AttributeError, ValueError):
        pass


def split_row(line):
    """把一行 markdown 表格列切成 cell 串列（去掉前後的管線與空白）。"""
    s = line.strip()
    if s.startswith("|"):
        s = s[1:]
    if s.endswith("|"):
        s = s[:-1]
    return [c.strip() for c in s.split("|")]


def is_separator_row(cells):
    """判斷是否為分隔列，如 |---|:--:|---|。允許 -、:、空白。"""
    seen = False
    for c in cells:
        if c == "":
            continue
        if set(c) <= set("-:"):
            seen = True
        else:
            return False
    return seen


def first_meaningful_cell(cells, start_index):
    """從 start_index 起找第一個非空欄；找不到就退回任何非空欄。"""
    for i in range(start_index, len(cells)):
        if cells[i]:
            return cells[i]
    for c in cells:
        if c:
            return c
    return ""


def expand(lines, default_section, cell_index, min_cols):
    """掃描所有行，回傳展開後的 checklist 字串串列。"""
    out = []
    current_section = default_section
    in_table = False
    header_consumed = False

    for raw in lines:
        line = raw.rstrip("\n")
        stripped = line.strip()

        # 追蹤最近的 markdown 標題，當作 section 標籤（除非使用者指定）
        if stripped.startswith("#") and default_section is None:
            current_section = stripped.lstrip("#").strip() or current_section
            in_table = False
            header_consumed = False
            continue

        if stripped.startswith("|"):
            cells = split_row(line)
            if not in_table:
                # 表格的第一行 = 表頭，跳過
                in_table = True
                header_consumed = True
                continue
            if is_separator_row(cells):
                continue
            if len([c for c in cells if c]) < min_cols:
                continue
            content = first_meaningful_cell(cells, cell_index)
            if not content:
                continue
            section = current_section if current_section else "(no-section)"
            out.append("- [ ] {} | {}".format(section, content))
        else:
            # 離開表格區塊
            in_table = False
            header_consumed = False

    return out


def print_config_example(stream):
    stream.write(
        "用法 / Usage:\n"
        "  python3 expand_checklist.example.py PRD.md > prd-checklist.md\n\n"
        "設定範例 / Config example:\n"
        "  --section-header \"API endpoints\"   給每條 checklist 一個固定 section 標籤\n"
        "  --cell-index 1                      取第 2 欄當內容（0 起算）\n"
        "  --min-cols 2                        少於 2 個非空欄的列視為雜訊\n"
    )


def main(argv):
    parser = argparse.ArgumentParser(
        add_help=True,
        description="M-007 anti-aggregation: 把 PRD 表格展開成一行一個 checkbox。",
    )
    parser.add_argument("input", nargs="?", help="輸入的 PRD markdown 檔路徑")
    parser.add_argument("--section-header", default=None,
                        help="固定的 section 標籤（預設取最近的 markdown 標題）")
    parser.add_argument("--cell-index", type=int, default=0,
                        help="取資料列的第幾欄當內容（0 起算，預設 0）")
    parser.add_argument("--min-cols", type=int, default=1,
                        help="少於 N 個非空欄的列視為雜訊跳過（預設 1）")
    args = parser.parse_args(argv[1:])

    if not args.input:
        sys.stderr.write("[expand] 錯誤：缺少輸入檔 argv[1]。\n\n")
        print_config_example(sys.stderr)
        return 1

    if not os.path.isfile(args.input):
        sys.stderr.write("[expand] 錯誤：找不到輸入檔: {}\n".format(args.input))
        return 2

    try:
        with open(args.input, "r", encoding="utf-8") as f:
            lines = f.readlines()
    except (OSError, UnicodeDecodeError) as e:
        sys.stderr.write("[expand] 錯誤：無法讀取 {}: {}\n".format(args.input, e))
        return 2

    items = expand(lines, args.section_header, args.cell_index, args.min_cols)

    if not items:
        sys.stderr.write(
            "[expand] 提示：在 {} 找不到任何 markdown 表格資料列。\n"
            "         確認檔內有以 '|' 開頭的表格，或調整 --min-cols / --cell-index。\n"
            .format(args.input)
        )
        return 0

    for item in items:
        sys.stdout.write(item + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
