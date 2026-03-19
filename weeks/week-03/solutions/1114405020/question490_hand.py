#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
UVA 490 - 文本旋轉 (手打版本)
"""

import sys

lines = [line.rstrip("\n") for line in sys.stdin]

if lines:
    max_width = max(len(line) for line in lines)
    lines = [line.ljust(max_width) for line in lines]

    for col in range(max_width - 1, -1, -1):
        print("".join(lines[row][col] for row in range(len(lines))))
