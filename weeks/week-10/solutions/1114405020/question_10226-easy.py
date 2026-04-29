# 題目 10226: 排列禁止位置問題 - 簡易版本（優化版）
#
# 簡化思路：
#   1. 使用Python內建的itertools.permutations生成所有排列
#   2. 過濾符合條件的排列
#   3. 按字典序輸出，相同部分省略
#
# 優化改進：
#   1. 使用生成器避免一次性載入所有排列
#   2. 快速檢查限制條件（提前退出）
#   3. 優化差異檢測（使用ZIP而不是索引）
#   4. 減少字串轉換開銷

from itertools import permutations


def find_valid_arrangements(num_people: int, 
                             forbidden_positions: list) -> list:
    """
    找出所有有效的排列（優化版）
    
    優化點：
      1. 使用生成器表達式避免過多中間列表
      2. 快速檢查限制條件
      3. 使用字典查詢代替列表查詢（若禁止位置較多）
      4. 提早過濾無效排列
    
    參數：
        num_people: 人數
        forbidden_positions: 禁止位置列表
                            forbidden_positions[i] 是第i個人禁止的位置列表
    
    返回值：
        所有有效排列的列表
    """
    if num_people == 0:
        return []
    
    # 預先轉換為集合以加快查詢
    forbidden_sets = [set(pos) for pos in forbidden_positions]
    
    valid = []
    
    # 使用生成器處理排列
    for perm in permutations(range(num_people)):
        # 檢查這個排列是否符合所有限制
        is_valid = True
        
        for person_id, position in enumerate(perm):
            # 檢查該人是否在禁止位置上（轉換為1-indexed）
            if (position + 1) in forbidden_sets[person_id]:
                is_valid = False
                break
        
        if is_valid:
            valid.append(perm)
    
    # 排序（確保字典序）
    valid.sort()
    
    # 轉換為列表（如果需要保持原始格式）
    return [list(perm) for perm in valid]


def print_arrangements_optimized(arrangements: list) -> None:
    """
    輸出排列，相同部分省略（優化版）
    
    優化點：
      1. 使用ZIP和enumerate簡化差異檢測
      2. 避免重複的字典轉換
      3. 使用生成器表達式
      4. 減少變數複製
    
    策略：
      1. 第一個排列完整輸出
      2. 後續排列只輸出與前一個排列不同的部分
    """
    if not arrangements:
        return
    
    # 轉換函數：數字轉字母
    to_letter = lambda x: chr(ord('A') + x)
    
    # 第一個排列：完整輸出
    current_arrangement = arrangements[0]
    print(''.join(to_letter(p) for p in current_arrangement))
    
    # 後續排列
    for current_arrangement in arrangements[1:]:
        # 使用ZIP找出第一個不同的位置
        first_diff_pos = next(
            (i for i, (curr, prev) in enumerate(zip(current_arrangement, arrangements[-1]))
             if curr != prev),
            len(current_arrangement)  # 如果沒有不同，返回長度
        )
        
        # 輸出從第一個不同位置開始的部分
        if first_diff_pos < len(current_arrangement):
            print(''.join(to_letter(p) for p in current_arrangement[first_diff_pos:]))
        
        # 更新前一個排列引用
        arrangements[-1] = current_arrangement


def print_arrangements(arrangements: list) -> None:
    """
    輸出排列，相同部分省略（簡化版，保持原始邏輯但優化細節）
    
    策略：
      1. 第一個排列完整輸出
      2. 後續排列只輸出與前一個排列不同的部分
    """
    if not arrangements:
        return
    
    previous_arrangement = None
    
    for current_arrangement in arrangements:
        if previous_arrangement is None:
            # 第一個排列：完整輸出
            line = ''.join(chr(ord('A') + person_id) 
                          for person_id in current_arrangement)
            print(line)
        else:
            # 找出第一個不同的位置（優化：不使用index）
            first_diff_pos = 0
            for idx in range(len(current_arrangement)):
                if current_arrangement[idx] != previous_arrangement[idx]:
                    first_diff_pos = idx
                    break
            else:
                # 迴圈正常結束（沒有break），所有元素都相同
                first_diff_pos = len(current_arrangement)
            
            # 輸出從第一個不同位置開始的部分
            if first_diff_pos < len(current_arrangement):
                line = ''.join(chr(ord('A') + person_id) 
                              for person_id in current_arrangement[first_diff_pos:])
                print(line)
        
        previous_arrangement = current_arrangement


if __name__ == "__main__":
    # 測試用例1：2個人，A不能在位置1
    print("Test case 1: 2人，A禁止位置1")
    test_restrictions = [
        [1],      # A禁止位置1
        []        # B無限制
    ]
    
    results = find_valid_arrangements(2, test_restrictions)
    print(f"Valid arrangements: {results}")
    print("Output:")
    print_arrangements(results)
    
    # 測試用例2：3個人，無限制
    print("\nTest case 2: 3人，無限制")
    results = find_valid_arrangements(3, [[], [], []])
    print(f"Total arrangements: {len(results)}")
    print("Output:")
    print_arrangements(results)
    
    # 測試用例3：3個人，A禁止位置1
    print("\nTest case 3: 3人，A禁止位置1")
    results = find_valid_arrangements(3, [[1], [], []])
    print(f"Total arrangements: {len(results)}")
    print("Output:")
    print_arrangements(results)
