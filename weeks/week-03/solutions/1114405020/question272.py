#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
UVA 272 - TeX 引號轉換

問題描述：
    將普通的雙引號（"）轉換為 TeX 方向雙引號：
    - 第一個 " → `` （左雙引號）
    - 第二個 " → '' （右雙引號）
    - 以此類推交替出現

    其他字符保持不變。

演算法說明：
    1. 使用狀態追蹤：是否正在引號內部
    2. 每次遇到 " 時，檢查當前狀態
    3. 奇數個引號使用 ``，偶數個使用 ''

時間複雜度：O(N)，其中N為輸入文本長度
空間複雜度：O(N)，用於存儲輸出
"""


def solve_tex_quotes():
    """
    主函數：轉換 TeX 引號。
    """
    try:
        import sys

        # 追蹤是否在引號內部
        open_quote = True  # 下一個引號應該是開引號

        for line in sys.stdin:
            result = []
            for char in line:
                if char == '"':
                    if open_quote:
                        result.append("``")
                    else:
                        result.append("''")
                    open_quote = not open_quote
                else:
                    result.append(char)

            print("".join(result), end="")

    except EOFError:
        pass


if __name__ == "__main__":
    solve_tex_quotes()
