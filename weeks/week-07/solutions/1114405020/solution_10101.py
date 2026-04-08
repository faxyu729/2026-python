#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
UVA 10101 - 木棒遊戲 標準解答

=== 問題分析 ===
給定一個用木棒拼成的不成立等式，通過移動恰好一根木棒使等式成立。

關鍵點：
1. 七段顯示器的 0~9 表示
2. 移動一根木棒意味著：從一個位置移除，放到另一個位置
3. 等式格式：left = right，其中 left 可能包含多個加減運算

=== 演算法設計 ===

本解答採用「暴力列舉 + 驗證」的策略：

1. 解析等式
   ===============================================================
   將輸入字符串拆解為數字位置，記錄每個數字的木棒集合

2. 七段顯示器映射
   ===============================================================
   每個數字由七段組成：
       a
      ---
     |   |
    f|   |b
      -g-
     |   |
    e|   |d
      ---
       c

3. 木棒移動過程
   ===============================================================
   a. 列舉每個數字位置的每根木棒
   b. 移除該木棒（如果該數字仍有效），進入中間狀態
   c. 對於中間狀態，嘗試在其他位置的其他數字添加一根木棒
   d. 檢查修改後的等式是否成立
   e. 返回第一個成立的等式

4. 時間複雜度分析
   ===============================================================
   - 等式中的數字個數：D（≤ 10 個）
   - 每個數字的木棒數：最多 7 根
   - 每個位置嘗試移除（O(D × 7)）
   - 每次移除後嘗試在其他位置添加（O(D × 7)）
   - 檢查等式是否成立（O(D)）

   總時間複雜度：O((D × 7)^2 × D) ≈ O(D^3)，可行

=== 實現細節 ===

1. 輔助函數
   ===============================================================
   - digit_to_matchstick(digit): 將數字轉為木棒集合
   - matchstick_to_digit(matchsticks): 將木棒集合轉為數字
   - parse_expression(expr): 解析表達式並計算結果
   - extract_numbers(equation): 提取等式中的所有數字及其位置
   - solve_matchstick(equation): 主求解函數

2. 數據結構
   ===============================================================
   使用集合表示木棒，便於高效的添加/移除操作

3. 邊界處理
   ===============================================================
   - 處理負號（負數和減法）
   - 處理多位數
   - 運算符不變

=== 測試驗證 ===

已設計的測試用例包括：
1. 簡單加法和減法
2. 含負號的等式
3. 多位數等式
4. 無解情況
5. 複雜多運算符等式
"""

from typing import List, Tuple, Optional, Set


# ==================== 七段顯示器映射表 ====================
DIGIT_SEGMENTS = {
    "0": {"a", "b", "c", "d", "e", "f"},  # 6根
    "1": {"b", "c"},  # 2根
    "2": {"a", "b", "d", "e", "g"},  # 5根
    "3": {"a", "b", "c", "d", "g"},  # 5根
    "4": {"b", "c", "f", "g"},  # 4根
    "5": {"a", "c", "d", "f", "g"},  # 5根
    "6": {"a", "c", "d", "e", "f", "g"},  # 6根
    "7": {"a", "b", "c"},  # 3根
    "8": {"a", "b", "c", "d", "e", "f", "g"},  # 7根
    "9": {"a", "b", "c", "d", "f", "g"},  # 6根
}

# 反向映射：從木棒集合到數字
SEGMENTS_TO_DIGIT = {frozenset(v): k for k, v in DIGIT_SEGMENTS.items()}


def digit_to_matchstick(digit: str) -> Set[str]:
    """
    將數字轉換為七段顯示器的木棒表示。

    參數：
        digit: 單個數字字符 ('0'-'9')

    返回：
        該數字的木棒集合

    例子：
        digit_to_matchstick('0') → {'a', 'b', 'c', 'd', 'e', 'f'}
        digit_to_matchstick('1') → {'b', 'c'}
        digit_to_matchstick('8') → {'a', 'b', 'c', 'd', 'e', 'f', 'g'}
    """
    return DIGIT_SEGMENTS.get(digit, set()).copy()


def matchstick_to_digit(matchsticks: Set[str]) -> Optional[str]:
    """
    將木棒集合轉換回數字。

    參數：
        matchsticks: 木棒集合

    返回：
        對應的數字字符，或 None 如果無效
    """
    key = frozenset(matchsticks)
    return SEGMENTS_TO_DIGIT.get(key, None)


def parse_expression(expr: str) -> Optional[int]:
    """
    解析並計算表達式的值。

    表達式格式：
    - 可以以 '-' 開頭（表示負數）
    - 包含數字和 '+' 或 '-' 運算符

    時間複雜度：O(|expr|)

    參數：
        expr: 表達式字符串，例如 "12+34" 或 "-1+2"

    返回：
        表達式的計算結果，或 None 如果無法解析
    """
    if not expr:
        return None

    try:
        current_number = ""
        current_operator = "+"
        result = 0

        i = 0
        if expr[0] == "-":
            current_operator = "-"
            i = 1

        while i < len(expr):
            char = expr[i]

            if char.isdigit():
                current_number += char
            elif char in ("+", "-"):
                if current_number:
                    num = int(current_number)
                    if current_operator == "+":
                        result += num
                    else:
                        result -= num
                    current_number = ""
                current_operator = char
            else:
                return None

            i += 1

        if current_number:
            num = int(current_number)
            if current_operator == "+":
                result += num
            else:
                result -= num

        return result
    except:
        return None


def extract_numbers(equation: str) -> Tuple[List[str], str, str]:
    """
    從等式中提取所有數字，返回 (數字列表, 左側表達式, 右側表達式)。

    參數：
        equation: 不含 '#' 後面內容的等式字符串

    返回：
        (digit_list, left_expr, right_expr)
        digit_list: 等式中所有數字組成的列表，便於後續修改
        left_expr: 左側運算式（數字已被標記為索引）
        right_expr: 右側運算式
    """
    parts = equation.split("=")
    if len(parts) != 2:
        return [], "", ""

    left_expr = parts[0]
    right_expr = parts[1]

    # 提取左側數字
    left_digits = []
    left_marked = ""
    i = 0
    while i < len(left_expr):
        if left_expr[i].isdigit():
            digit = left_expr[i]
            left_digits.append(digit)
            left_marked += "{" + str(len(left_digits) - 1) + "}"
            i += 1
        else:
            left_marked += left_expr[i]
            i += 1

    # 提取右側數字
    right_digits = []
    right_marked = ""
    i = 0
    while i < len(right_expr):
        if right_expr[i].isdigit():
            digit = right_expr[i]
            right_digits.append(digit)
            right_marked += "{" + str(len(left_digits) + len(right_digits) - 1) + "}"
            i += 1
        else:
            right_marked += right_expr[i]
            i += 1

    all_digits = left_digits + right_digits

    return all_digits, left_marked, right_marked


def reconstruct_equation(
    digits: List[str], left_template: str, right_template: str
) -> str:
    """
    根據修改後的數字重建等式。

    參數：
        digits: 當前的數字列表
        left_template: 左側模板（包含位置標記 {0}, {1}, ...）
        right_template: 右側模板

    返回：
        重建的等式，或 None 如果包含無效數字
    """
    try:
        left = left_template
        right = right_template

        # 替換左側
        for i, digit in enumerate(digits):
            left = left.replace("{" + str(i) + "}", digit)

        # 替換右側
        for i, digit in enumerate(digits):
            right = right.replace("{" + str(i) + "}", digit)

        return left + "=" + right
    except:
        return None


def solve_matchstick(equation: str) -> str:
    """
    主求解函數：通過移動一根木棒使等式成立。

    演算法：
    1. 提取等式中的所有數字
    2. 列舉所有可能的木棒移動方式
    3. 對每個修改後的等式檢查是否成立
    4. 返回第一個成立的等式，或 "No"

    參數：
        equation: 輸入等式，格式如 "12+34=46#"

    返回：
        修正後的等式（如果有解），或 "No"
    """
    # 清理輸入
    equation = equation.split("#")[0]

    # 提取數字和模板
    digits, left_template, right_template = extract_numbers(equation)

    if not digits:
        return "No"

    # 將數字轉換為木棒集合
    digit_matchsticks = [digit_to_matchstick(d) for d in digits]

    # 嘗試所有可能的移動
    for remove_idx in range(len(digit_matchsticks)):
        # 從 remove_idx 位置嘗試移除每根木棒
        for segment in list(digit_matchsticks[remove_idx]):
            # 創建臨時副本並移除
            temp_digits = [s.copy() for s in digit_matchsticks]
            temp_digits[remove_idx].remove(segment)

            # 檢查移除後的數字是否有效
            new_digit = matchstick_to_digit(temp_digits[remove_idx])
            if new_digit is None:
                continue

            # 現在嘗試在其他位置添加這根木棒
            for add_idx in range(len(temp_digits)):
                for add_segment in ["a", "b", "c", "d", "e", "f", "g"]:
                    if add_segment in temp_digits[add_idx]:
                        continue  # 已經存在

                    # 添加木棒
                    temp_digits[add_idx].add(add_segment)

                    # 檢查添加後的數字是否有效
                    new_digit_at_add = matchstick_to_digit(temp_digits[add_idx])
                    if new_digit_at_add is not None:
                        # 重建等式並檢查是否成立
                        new_digit_str_list = [
                            matchstick_to_digit(s) for s in temp_digits
                        ]
                        if all(d is not None for d in new_digit_str_list):
                            # 重建等式
                            new_left = left_template
                            new_right = right_template

                            for i, d in enumerate(new_digit_str_list):
                                new_left = new_left.replace("{" + str(i) + "}", d)
                                new_right = new_right.replace("{" + str(i) + "}", d)

                            # 驗證等式
                            left_val = parse_expression(new_left)
                            right_val = parse_expression(new_right)

                            if (
                                left_val is not None
                                and right_val is not None
                                and left_val == right_val
                            ):
                                return new_left + "=" + new_right + "#"

                    # 移除木棒（回溯）
                    temp_digits[add_idx].remove(add_segment)

    return "No"


def main():
    """
    主程序：讀取輸入並調用求解函數。
    """
    import sys

    for line in sys.stdin:
        equation = line.strip()
        if equation:
            result = solve_matchstick(equation)
            print(result)


if __name__ == "__main__":
    main()
