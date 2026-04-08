#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
UVA 10101 - 木棒遊戲 簡化版本

=== 核心思路 ===
1. 七段顯示器：每個數字由不同的木棒組成
2. 移動一根木棒：從一個位置移除，移到另一個位置
3. 暴力列舉所有可能的移動方式，檢查等式是否成立

=== 七段顯示器對應表 ===
     a
    ---
   |   |
  f|   |b
    -g-
   |   |
  e|   |d
    ---
     c

0: {a,b,c,d,e,f}        (6根)
1: {b,c}                (2根)
2: {a,b,d,e,g}          (5根)
3: {a,b,c,d,g}          (5根)
4: {b,c,f,g}            (4根)
5: {a,c,d,f,g}          (5根)
6: {a,c,d,e,f,g}        (6根)
7: {a,b,c}              (3根)
8: {a,b,c,d,e,f,g}      (7根)
9: {a,b,c,d,f,g}        (6根)
"""

from typing import List, Optional, Set


# 七段顯示器映射表
DIGIT_SEGMENTS = {
    "0": {"a", "b", "c", "d", "e", "f"},
    "1": {"b", "c"},
    "2": {"a", "b", "d", "e", "g"},
    "3": {"a", "b", "c", "d", "g"},
    "4": {"b", "c", "f", "g"},
    "5": {"a", "c", "d", "f", "g"},
    "6": {"a", "c", "d", "e", "f", "g"},
    "7": {"a", "b", "c"},
    "8": {"a", "b", "c", "d", "e", "f", "g"},
    "9": {"a", "b", "c", "d", "f", "g"},
}

# 反向映射：木棒集合 → 數字
SEGMENTS_TO_DIGIT = {frozenset(v): k for k, v in DIGIT_SEGMENTS.items()}


def digit_to_matchstick(digit: str) -> Set[str]:
    """
    將數字轉為木棒集合。
    例如：'0' → {'a', 'b', 'c', 'd', 'e', 'f'}
    """
    return DIGIT_SEGMENTS.get(digit, set()).copy()


def matchstick_to_digit(matchsticks: Set[str]) -> Optional[str]:
    """
    將木棒集合轉回數字。
    例如：{'a', 'b', 'c', 'd', 'e', 'f'} → '0'
    如果無有效數字，返回 None。
    """
    key = frozenset(matchsticks)
    return SEGMENTS_TO_DIGIT.get(key, None)


def parse_expression(expr: str) -> Optional[int]:
    """
    計算表達式的值。
    例如：parse_expression("12+34") → 46
          parse_expression("-5+3") → -2
    """
    if not expr:
        return None

    try:
        current_number = ""
        current_op = "+"
        result = 0

        # 處理開頭的負號
        i = 0
        if expr[0] == "-":
            current_op = "-"
            i = 1

        # 掃描整個表達式
        while i < len(expr):
            if expr[i].isdigit():
                current_number += expr[i]
            elif expr[i] in ("+", "-"):
                # 遇到運算符，先處理前一個數字
                if current_number:
                    num = int(current_number)
                    result += num if current_op == "+" else -num
                    current_number = ""
                current_op = expr[i]
            else:
                return None
            i += 1

        # 處理最後一個數字
        if current_number:
            num = int(current_number)
            result += num if current_op == "+" else -num

        return result
    except:
        return None


def extract_numbers(equation: str) -> tuple:
    """
    提取等式中的所有數字。
    返回：(數字列表, 左側模板, 右側模板)

    例如：
    "12+34=46" → (['1','2','3','4','4','6'], '1{0}2+3{1}4', '4{2}6')
    模板中用 {i} 表示第 i 個數字的位置。
    """
    parts = equation.split("=")
    if len(parts) != 2:
        return [], "", ""

    left_expr = parts[0]
    right_expr = parts[1]

    # 提取左側數字
    left_digits = []
    left_marked = ""
    for char in left_expr:
        if char.isdigit():
            left_digits.append(char)
            left_marked += "{" + str(len(left_digits) - 1) + "}"
        else:
            left_marked += char

    # 提取右側數字
    right_digits = []
    right_marked = ""
    for char in right_expr:
        if char.isdigit():
            right_digits.append(char)
            right_marked += "{" + str(len(left_digits) + len(right_digits) - 1) + "}"
        else:
            right_marked += char

    all_digits = left_digits + right_digits
    return all_digits, left_marked, right_marked


def solve_matchstick(equation: str) -> str:
    """
    主求解函數。

    思路：
    1. 提取等式中的所有數字
    2. 列舉所有可能的木棒移動
    3. 檢查修改後的等式是否成立
    4. 返回第一個成立的等式
    """
    # 清理輸入（移除 # 後的內容）
    equation = equation.split("#")[0]

    # 提取數字和模板
    digits, left_template, right_template = extract_numbers(equation)

    if not digits:
        return "No"

    # 轉換為木棒集合
    digit_matchsticks = [digit_to_matchstick(d) for d in digits]

    # 列舉所有移動方式
    for remove_idx in range(len(digit_matchsticks)):
        # 嘗試從 remove_idx 移除每根木棒
        for segment in list(digit_matchsticks[remove_idx]):
            # 創建副本並移除
            temp = [s.copy() for s in digit_matchsticks]
            temp[remove_idx].remove(segment)

            # 檢查移除後是否有效
            if matchstick_to_digit(temp[remove_idx]) is None:
                continue

            # 嘗試在其他位置添加
            for add_idx in range(len(temp)):
                for add_seg in ["a", "b", "c", "d", "e", "f", "g"]:
                    if add_seg in temp[add_idx]:
                        continue

                    # 添加木棒
                    temp[add_idx].add(add_seg)

                    # 檢查添加後是否有效
                    if matchstick_to_digit(temp[add_idx]) is not None:
                        # 重建等式
                        new_digits = [matchstick_to_digit(s) for s in temp]
                        if all(d is not None for d in new_digits):
                            # 替換模板
                            new_left = left_template
                            new_right = right_template
                            for i, d in enumerate(new_digits):
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

                    # 回溯
                    temp[add_idx].remove(add_seg)

    return "No"


def main():
    """讀取輸入並輸出結果。"""
    import sys

    for line in sys.stdin:
        equation = line.strip()
        if equation:
            print(solve_matchstick(equation))


if __name__ == "__main__":
    main()
