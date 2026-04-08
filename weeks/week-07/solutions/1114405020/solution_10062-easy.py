"""
題目 10062 - 乳牛排隊問題（簡單易記版本）

====== 問題理解 ======
• 有N頭乳牛，編號1到N
• 農夫記錄了：每頭牛前面有多少頭編號比它小的牛
• 根據這個信息，重建排列順序

====== 解題策略 ======
簡單想法：依序為每個位置選擇合適的牛編號
• 位置1：任意牛都可以
• 位置i (i>=2)：選擇使得「前面編號<它的牛數 = info[i-2]」的牛

複雜之處：不是所有選擇都能通往最終解
解決方案：使用回溯法 - 如果某個選擇失敗，就回退並嘗試其他選擇

====== 演算法概述 ======
1. 遞歸函數 try_place(位置, 當前排列, 已使用編號)
2. 基礎情況：位置超過N，說明已完成，返回結果
3. 遞歸情況：嘗試編號1到N
   - 跳過已使用編號
   - 檢查該編號是否滿足當前位置的要求
   - 如果滿足：加入排列，遞歸處理下一位置
   - 如果遞歸成功，返回結果
   - 如果失敗，移除該編號（回溯），嘗試下一個編號
4. 所有編號都嘗試過仍失敗，返回None

====== 複雜度分析 ======
最壞情況：O(N! * N)
• 需要嘗試N!種排列
• 每次檢查前面編號小於候選的牛，需要O(N)時間
但實際情況遠優於此，因為約束條件大幅剪枝
"""


def solve(input_string):
    """
    簡單易記的解法 - 使用遞歸和回溯

    參數：
        input_string (str)：輸入字符串

    返回：
        list：重建的排列（編號1到N）

    ====== 核心思想 ======
    為每個位置依次選擇一頭牛，該牛前面必須有指定個數的編號更小的牛。
    若無法完成，就回溯到上一位置，換個牛試試。
    """
    # ====== 輸入解析 ======
    lines = input_string.strip().split("\n")
    n = int(lines[0])  # 乳牛總數

    # info[i-2] = 第i個位置的牛前面應該有多少頭編號<它的牛
    # 例如 info[0] 對應位置2，info[1]對應位置3，以此類推
    info = [int(lines[i]) for i in range(1, n)]

    def try_place(pos, result, used):
        """
        遞歸函數：嘗試在位置pos放入牛編號

        參數：
            pos (int)：當前要填充的位置（1到n）
            result (list)：已填充位置的牛編號序列
            used (set)：已使用過的牛編號集合

        返回：
            list：找到的完整排列
            None：無法完成排列
        """
        # ====== 基礎情況：已填充所有位置 ======
        if pos == n + 1:
            # 所有位置都已填充，返回結果
            return result[:]

        # ====== 遞歸情況：嘗試為當前位置放入牛 ======
        for cow_id in range(1, n + 1):
            # 跳過已使用的牛編號
            if cow_id in used:
                continue

            # ====== 檢查該牛是否符合當前位置的要求 ======
            ok = False

            if pos == 1:
                # 位置1沒有限制，任何未使用的牛都可以
                ok = True
            else:
                # 位置2及以後：檢查前面有多少頭牛編號<cow_id
                smaller = sum(1 for x in result if x < cow_id)

                # 該數量必須等於該位置的要求 info[pos-2]
                if smaller == info[pos - 2]:
                    ok = True

            # ====== 如果符合要求，嘗試用這頭牛 ======
            if ok:
                # 標記為已使用
                used.add(cow_id)
                # 加入排列
                result.append(cow_id)

                # 遞歸：嘗試填充下一個位置
                answer = try_place(pos + 1, result, used)

                # 如果遞歸成功（找到完整排列），返回
                if answer is not None:
                    return answer

                # ====== 回溯：撤銷選擇，嘗試其他編號 ======
                result.pop()  # 移除剛加入的牛
                used.remove(cow_id)  # 標記為未使用

        # ====== 無法為當前位置找到合適的牛 ======
        return None

    # ====== 開始求解 ======
    return try_place(1, [], set())


# ====== 測試和驗證 ======
if __name__ == "__main__":
    # 測試用例
    tests = [
        # (輸入, 預期輸出)
        ("4\n1\n2\n3", [1, 2, 3, 4]),  # 簡單遞增
        ("3\n1\n2", [1, 2, 3]),  # 更簡單的遞增
        ("5\n0\n0\n2\n1", [5, 3, 1, 4, 2]),  # 複雜交替
        ("2\n0", [2, 1]),  # 最小情況
        ("6\n0\n1\n0\n2\n3", [6, 2, 5, 1, 3, 4]),  # 更複雜的情況
    ]

    print("====== 簡單易記版本測試結果 ======")
    all_pass = True
    for idx, (inp, expected) in enumerate(tests, 1):
        result = solve(inp)
        match = result == expected
        status = "PASS" if match else "FAIL"
        all_pass = all_pass and match
        print(f"Test {idx}: {status}")
        if not match:
            print(f"  Expected: {expected}")
            print(f"  Got: {result}")

    print(f"\n====== 總結 ======")
    print(f"{'All tests passed!' if all_pass else 'Some tests failed'}")
