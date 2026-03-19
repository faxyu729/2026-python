#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
UVA 272 - TeX 引號轉換 (AI簡化版本)

用於競賽練習的簡潔版本，包含詳細中文註解。

核心概念：
1. 使用布林值追蹤是否在開引號狀態
2. 遇到 " 時根據狀態輸出 `` 或 ''
3. 交替切換狀態
"""

import sys

open_quote = True

for line in sys.stdin:
    result = []
    for char in line:
        if char == '"':
            result.append("``" if open_quote else "''")
            open_quote = not open_quote
        else:
            result.append(char)

    print("".join(result), end="")
