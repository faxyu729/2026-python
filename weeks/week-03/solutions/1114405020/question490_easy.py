#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
UVA 490 - 文本旋轉 (簡化版本)

用於競賽練習的簡潔版本。

核心概念：
1. 讀取所有行
2. 填充到最大寬度
3. 從右到左，逐列輸出（每列從上到下）
"""

import sys

lines = [line.rstrip("\n") for line in sys.stdin]

if lines:
    max_width = max(len(line) for line in lines)
    lines = [line.ljust(max_width) for line in lines]

    for col in range(max_width - 1, -1, -1):
        print("".join(lines[row][col] for row in range(len(lines))))
