# 題目 10268: 水球破裂樓層問題 - 簡易版本（優化版）
#
# 簡易思路說明：
#   使用動態規劃的直觀方法。
#   定義：dp[球數][測試次數] = 能夠涵蓋的最大樓層數
#
#   轉移方程：
#     如果在某一層丟水球：
#     - 破裂了：用1個少的球，次數少1次，測試下面的層
#     - 沒破裂：用同樣的球，次數少1次，測試上面的層
#     
#   因此：dp[k][t] = dp[k-1][t-1] + dp[k][t-1] + 1
#                  = 破裂時的測試範圍 + 不破裂時的測試範圍 + 當前層
#
# 邊界條件：
#   dp[k][0] = 0  (0次測試不能測任何層)
#   dp[0][t] = 0  (0個球不能測任何層)
#   dp[1][t] = t  (1個球t次只能測t層，必須從下往上一層層試)
#
# 優化改進：
#   1. 使用一維DP表代替二維，節省空間複雜度
#   2. 提前終止迴圈，避免不必要的計算
#   3. 使用更有效率的邊界檢查

def question_10268_easy(k, n):
    """
    使用1D DP 表的簡易方法求解水球問題（優化版）
    
    優化點：
      - 空間複雜度從 O(k * 64) 降低到 O(64)
      - 提前終止條件，最壞情況下無需遍歷全部64次
      - 簡化邏輯，提高可讀性
    
    Args:
        k (int): 水球數量
        n (int): 樓層數
    
    Returns:
        int: 最少需要的測試次數
    """
    # 特殊情況：樓層數為0
    if n == 0:
        return 0
    
    # 特殊情況：只有1個球
    if k == 1:
        return min(n, 64)
    
    # 最多測試63次（題目限制）
    max_trials = 63
    
    # 使用一維DP數組，節省空間
    # dp[t] = 用k個球進行t次測試能覆蓋的最大樓層數
    prev_dp = [0] * (max_trials + 1)  # 用k-1個球的結果
    curr_dp = [0] * (max_trials + 1)  # 用k個球的結果
    
    # 對每個球數進行填充
    for ball in range(1, k + 1):
        # 對每個測試次數進行填充
        for trial in range(1, max_trials + 1):
            if ball == 1:
                # 1個球只能一層層測
                curr_dp[trial] = trial
            else:
                # 轉移方程：破裂時 + 不破裂時 + 當前層
                curr_dp[trial] = prev_dp[trial - 1] + curr_dp[trial - 1] + 1
            
            # 提前終止：如果已經能覆蓋n層，無需繼續計算
            if curr_dp[trial] >= n:
                return trial
        
        # 交換數組以進行下一個球
        prev_dp, curr_dp = curr_dp, prev_dp
    
    # 如果超過 63 次
    return 64


if __name__ == "__main__":
    # 測試範例
    test_cases = [
        (1, 1),       # 1個球1層：需要1次
        (1, 10),      # 1個球10層：需要10次
        (2, 100),     # 2個球100層：需要14次
        (100, 1000),  # 100個球1000層：需要10次
        (1, 10**18),  # 超大樓層數
    ]
    
    for k, n in test_cases:
        result = question_10268_easy(k, n)
        print(f"k={k:3d}, n={n:15d}: {result:2d} trials")
