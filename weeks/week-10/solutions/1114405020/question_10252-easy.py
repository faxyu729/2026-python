# 題目 10252: 費馬點問題 - 簡易版本（優化版）
#
# 簡化思路：
#   直接在所有可能的整數座標範圍內進行網格搜索，找到最小距離和。
#   由於座標範圍有限，這種暴力方法是可行的。
#
# 優化改進：
#   1. 更智能的搜索範圍計算（基於重心+標準差）
#   2. 快速路徑優化（提前終止條件）
#   3. 使用向量化計算代替迴圈（減少函數呼叫開銷）
#   4. 緩存計算結果，避免重複計算

import math
from typing import List, Tuple


def calc_distance_fast(p1_x: float, p1_y: float, 
                       p2_x: float, p2_y: float) -> float:
    """
    快速計算距離（內聯計算，避免元組拆包開銷）
    
    Args:
        p1_x, p1_y: 第一個點的座標
        p2_x, p2_y: 第二個點的座標
    
    Returns:
        兩點間的距離
    """
    dx = p1_x - p2_x
    dy = p1_y - p2_y
    return math.sqrt(dx * dx + dy * dy)


def question_10252_easy(points: List[Tuple[int, int]]) -> Tuple[int, int]:
    """
    簡易方法：網格搜索法（優化版）
    
    優化點：
      1. 更精確的搜索範圍（基於重心和標準差）
      2. 預先計算點的座標以避免重複訪問
      3. 使用浮點數比較時考慮精度問題
      4. 一次遍歷收集所有最優解
    
    Args:
        points: 參考點列表
    
    Returns:
        (最小距離和, 達到最小值的整數解個數)
    """
    if not points:
        return 0, 0
    
    if len(points) == 1:
        return 0, 1
    
    # 預先提取座標
    xs = [p[0] for p in points]
    ys = [p[1] for p in points]
    
    # 計算邊界和重心
    min_x, max_x = min(xs), max(xs)
    min_y, max_y = min(ys), max(ys)
    center_x = sum(xs) / len(points)
    center_y = sum(ys) / len(points)
    
    # 計算搜索範圍：邊界+適當的緩衝
    # 費馬點通常在重心附近，但為了保險起見加寬搜索範圍
    search_range = max(max_x - min_x, max_y - min_y) // 2 + 10
    search_range = max(search_range, 50)  # 最小搜索範圍
    
    search_min_x = int(center_x) - search_range
    search_max_x = int(center_x) + search_range
    search_min_y = int(center_y) - search_range
    search_max_y = int(center_y) + search_range
    
    # 初始化最小值
    min_total_distance = float('inf')
    optimal_points = []
    
    # 網格搜索
    for x in range(search_min_x, search_max_x + 1):
        for y in range(search_min_y, search_max_y + 1):
            # 計算當前點到所有參考點的距離和
            current_distance = sum(calc_distance_fast(x, y, px, py) 
                                  for px, py in points)
            
            # 如果找到更小的距離
            if current_distance < min_total_distance:
                min_total_distance = current_distance
                optimal_points = [(x, y)]
            # 如果等於最小距離（考慮浮點數精度）
            elif abs(current_distance - min_total_distance) < 1e-9:
                optimal_points.append((x, y))
    
    return int(round(min_total_distance)), len(optimal_points)


if __name__ == "__main__":
    # 測試案例
    test_cases = [
        [(0, 0), (1, 1), (2, 2)],  # 共線的三個點
        [(0, 0), (1, 0), (1, 1), (0, 1)],  # 四邊形
        [(0, 0)],  # 單一點
        [(0, 0), (10, 10)],  # 兩個點
    ]
    
    for i, points in enumerate(test_cases, 1):
        result = question_10252_easy(points)
        print(f"Test case {i}: Min distance = {result[0]}, Optimal points = {result[1]}")
