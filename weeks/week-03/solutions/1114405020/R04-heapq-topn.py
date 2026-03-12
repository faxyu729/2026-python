# R4. heapq 取 Top-N（1.4）

import heapq

# 一組數字資料，後面會示範如何快速找出最大/最小的前 N 筆。
nums = [1, 8, 2, 23, 7, -4, 18, 23, 42, 37, 2]

# nlargest(n, iterable)：找出前 n 大元素。
# nsmallest(n, iterable)：找出前 n 小元素。
# 這兩個函式都會回傳 list，適合用在「只需要前幾名」的情境。
largest_three = heapq.nlargest(3, nums)
smallest_three = heapq.nsmallest(3, nums)

print("原始資料:", nums)
print("最大的 3 個數字:", largest_three)
print("最小的 3 個數字:", smallest_three)

# 這裡示範資料不是單純數字，而是字典物件。
# 每個元素代表一檔股票，包含名稱、張數與價格。
portfolio = [
    {'name': 'IBM', 'shares': 100, 'price': 91.1},
    {'name': 'AAPL', 'shares': 50, 'price': 543.22},
]

# key 參數決定「用哪個欄位比較大小」。
# 這裡用 price 當排序依據，所以會找出價格最低的 1 檔股票。
cheapest_stock = heapq.nsmallest(1, portfolio, key=lambda s: s['price'])
print("價格最低的股票:", cheapest_stock)

# 把 nums 複製一份給 heap，避免直接改到原始資料。
heap = list(nums)

# heapify 會把 list 原地轉成「最小堆」結構。
# 注意：最小堆不等於整體排序。
# 它只保證父節點 <= 子節點，因此 heap 的外觀看起來不一定是遞增序列。
heapq.heapify(heap)
print("整理成最小堆後:", heap)

# heappop 會彈出最小堆中的最小值（也就是目前堆頂）。
# 取出後，heapq 會自動重整堆結構，維持最小堆性質。
smallest_value = heapq.heappop(heap)
print("取出的最小值:", smallest_value)
print("取出最小值後的堆:", heap)
