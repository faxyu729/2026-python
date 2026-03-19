#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
UVA 490 - 文本旋轉（Text Rotation）

問題描述：
    將輸入的矩形文本順時針旋轉90度。
    - 最後一行變成最左列
    - 第一行變成最右列
    - 原始文本的每列都需要用空格對齊，形成正確的矩形

演算法說明：
    1. 讀取所有輸入行，存儲到列表
    2. 將所有行填充到相同寬度（最寬行的寬度）
    3. 逐列提取，從右到左的列提取為頂到底的行
    4. 每行右側的尾隨空格保留

時間複雜度：O(N × M)，其中N為行數，M為最寬行的長度
空間複雜度：O(N × M)
"""


def rotate_text_90_clockwise():
    """
    主函數：讀取文本並順時針旋轉90度。
    """
    try:
        import sys

        # 讀取所有行
        lines = []
        for line in sys.stdin:
            # 移除末尾的換行符，但保留其他空格
            lines.append(line.rstrip("\n"))

        if not lines:
            return

        # 找到最大寬度
        max_width = max(len(line) for line in lines) if lines else 0

        # 將所有行填充到相同寬度
        padded_lines = []
        for line in lines:
            padded_lines.append(line.ljust(max_width))

        # 旋轉90度：從最後一列開始，逐列從下到上輸出
        # 原始的最後一行變成第一列（從下往上讀）
        # 原始的第一行變成最後一列（從下往上讀）
        for col in range(max_width - 1, -1, -1):
            row_chars = []
            for row in range(len(padded_lines)):
                row_chars.append(padded_lines[row][col])

            print("".join(row_chars))

    except EOFError:
        pass


if __name__ == "__main__":
    rotate_text_90_clockwise()
