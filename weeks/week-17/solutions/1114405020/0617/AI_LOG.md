任務一：timeit
- AI 問：repeat < 1 時的行為？ $\to$ 
我答：報錯 (ValueError)。
- AI 問：回傳值處理與保留元數據的工具？ $\to$
 我答：回傳值不變，使用 functools.wraps。
- AI 問：邊界案例與驗收標準？ $\to$ 
我答：測試 repeat=1 及有/無回傳值；records 數量正確且 last_elapsed 為平均值。

任務二：搜尋評估
- AI 問：簽名、回傳值與空列表處理？ $\to$ 
我答：統一回傳 -1，空列表也回 -1。
- AI 問：binary_search 未排序時的行為？ $\to$
 我答：拋出錯誤。
- AI 問：邊界案例與驗收標準？ $\to$ 
我答：測試首/中/末位、不存在、空列表及未排序拋錯，且全部通過。