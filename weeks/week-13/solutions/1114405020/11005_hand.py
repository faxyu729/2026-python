# -*- coding: utf-8 -*-
"""
UVA 11005 — Cheapest Base（手打程式）

題目：給定 36 個字元（0-9, A-Z）的印刷成本，對於每個查詢數字 N，
      找出在 2 到 36 進位制中，讓印刷成本最低的所有進位制。
"""

def to_base_digits(n, base):
    """將十進位數字 n 轉換為指定進位制，回傳各位數的整數值列表"""
    if n == 0:
        return [0]
    digits = []
    while n > 0:
        digits.append(n % base)
        n //= base
    return digits


def cheapest_bases(n, costs):
    """計算數字 n 在 2~36 進位制中，印刷成本最低的所有進位制"""
    min_cost = float('inf')
    result = []
    for base in range(2, 37):
        total = 0
        for d in to_base_digits(n, base):
            total += costs[d]
        if total < min_cost:
            min_cost = total
            result = [base]
        elif total == min_cost:
            result.append(base)
    return result


def solve_case(costs, queries):
    """處理單一測試案例的查詢，回傳輸出行列表"""
    output = []
    for n in queries:
        bases = cheapest_bases(n, costs)
        output.append(f"Cheapest base(s) for number {n}: " + " ".join(map(str, bases)))
    return output


def solve_all(input_data):
    """解析完整輸入，處理所有測試案例，回傳完整輸出字串"""
    lines = input_data.strip().splitlines()
    idx = 0
    t = int(lines[idx].strip())
    idx += 1
    case_outputs = []
    for case_no in range(1, t + 1):
        costs = []
        for _ in range(4):
            costs.extend(map(int, lines[idx].strip().split()))
            idx += 1
        q = int(lines[idx].strip())
        idx += 1
        queries = []
        for _ in range(q):
            queries.append(int(lines[idx].strip()))
            idx += 1
        result_lines = solve_case(costs, queries)
        case_outputs.append(f"Case {case_no}:")
        case_outputs.extend(result_lines)
        if case_no < t:
            case_outputs.append("")
    return "\n".join(case_outputs)


def main():
    """主程式：從標準輸入讀取資料並輸出結果"""
    import sys
    data = sys.stdin.read()
    print(solve_all(data))


if __name__ == "__main__":
    main()
