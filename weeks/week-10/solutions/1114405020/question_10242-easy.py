# 題目 10242: ATM 搶劫問題 - 簡易版本（優化版）
#
# 簡化思路：
#   使用簡單的 DFS 遍歷，帶著「已搶劫的金額」和「已訪問的路口」進行深度優先搜索。
#   在每個路口決定：
#     1. 繼續到相鄰路口
#     2. 如果當前路口有酒吧，就停止並計算總金額
#
# 優化改進：
#   1. 使用不可變集合（frozenset）以支援記憶化
#   2. 添加記憶化搜索避免重複計算
#   3. 提前終止條件和剪枝策略
#   4. 減少集合複製開銷（使用位元遮罩或frozenset）

from typing import List, Set, Tuple, Dict
from collections import defaultdict


def max_robbery_easy(num_intersections: int,
                     road_list: List[Tuple[int, int]],
                     atm_amounts: List[int],
                     start_intersection: int,
                     bar_intersections: Set[int]) -> int:
    """
    簡易版本：DFS搜索最大搶劫金額（優化版）
    
    優化點：
      1. 使用frozenset支援記憶化（可哈希）
      2. 使用字典緩存結果
      3. 提前返回條件
      4. 減少集合操作開銷
    
    參數說明：
        num_intersections: 路口總數
        road_list: 道路列表 [(起點, 終點), ...]
        atm_amounts: 各路口ATM的金額
        start_intersection: 出發路口編號
        bar_intersections: 有酒吧的路口編號
    
    返回值：
        最多能搶劫的現金總額
    """
    # 建構有向圖：路口編號1-based
    adjacency_list = defaultdict(list)
    for from_intersection, to_intersection in road_list:
        adjacency_list[from_intersection].append(to_intersection)
    
    # 預先計算0-based的ATM金額
    atm_0based = {i + 1: atm_amounts[i] for i in range(len(atm_amounts))}
    
    # 記憶化字典：(當前位置, 已搶劫集合) -> 最大金額
    memo: Dict[Tuple[int, frozenset], int] = {}
    
    # 深度優先搜索（帶記憶化）
    def search(current_pos: int, visited_intersections: frozenset) -> int:
        """
        DFS搜索函數（優化版）
        
        參數：
            current_pos: 當前位置
            visited_intersections: 已訪問過的路口集合（用於追蹤已搶劫的ATM）
        
        返回值：
            從當前狀態開始能搶劫的最大金額
        """
        # 檢查記憶
        state = (current_pos, visited_intersections)
        if state in memo:
            return memo[state]
        
        # 計算當前已搶劫的總金額
        current_total = sum(atm_0based.get(pos, 0) for pos in visited_intersections)
        
        # 如果當前路口有酒吧，停止並返回
        if current_pos in bar_intersections:
            memo[state] = current_total
            return current_total
        
        # 尋找最優的下一步
        max_amount = current_total
        
        # 前往相鄰路口
        for next_pos in adjacency_list[current_pos]:
            # 新的已訪問集合
            if next_pos not in visited_intersections:
                new_visited = visited_intersections | frozenset([next_pos])
                amount = search(next_pos, new_visited)
                max_amount = max(max_amount, amount)
            else:
                # 已搶過的路口，不再搶，直接繼續遍歷
                amount = search(next_pos, visited_intersections)
                max_amount = max(max_amount, amount)
        
        memo[state] = max_amount
        return max_amount
    
    # 初始化：從起點開始，先搶起點的ATM
    initial_visited = frozenset([start_intersection])
    result = search(start_intersection, initial_visited)
    
    return result


if __name__ == "__main__":
    # 測試用例
    # 根據題目例子：
    # 6個路口，路線如題目所述
    roads = [(1, 2), (2, 4), (4, 1), (2, 3), (3, 5)]
    atms = [10, 15, 12, 8, 2]  # 各路口ATM金額
    bars = {3, 5}  # 有酒吧的路口
    
    result = max_robbery_easy(5, roads, atms, 1, bars)
    print(f"最多搶劫金額: {result}")
    
    # 額外測試
    print("\n額外測試:")
    # 簡單測試
    simple_roads = [(1, 2), (2, 3)]
    simple_atms = [100, 50, 75]
    simple_bars = {3}
    result = max_robbery_easy(3, simple_roads, simple_atms, 1, simple_bars)
    print(f"簡單路線: {result}")
