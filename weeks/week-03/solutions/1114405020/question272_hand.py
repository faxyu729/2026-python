#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
UVA 272 - TeX 引號轉換 (手打版本)
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
