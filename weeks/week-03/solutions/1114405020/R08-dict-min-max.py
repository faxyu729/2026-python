# R8. 字典運算：min/max/sorted + zip（1.8）

# 一個股票代號對應價格的字典：
# key 是股票代號（字串），value 是價格（浮點數）。
prices = {'ACME': 45.23, 'AAPL': 612.78, 'FB': 10.75}

# zip(prices.values(), prices.keys()) 會產生 (價格, 股票代號) 的配對，
# 例如 (45.23, 'ACME')。
# 這種「把價格放在前面」的 tuple 很適合直接做大小比較。
# 因為 Python 比較 tuple 時，會先比較第 1 個元素，
# 若第 1 個元素相同，才比較第 2 個元素。
min_price = min(zip(prices.values(), prices.keys()))
max_price = max(zip(prices.values(), prices.keys()))
sorted_prices = sorted(zip(prices.values(), prices.keys()))

# min_price / max_price 回傳的是 tuple：
# (最低價格, 對應股票代號) / (最高價格, 對應股票代號)
# sorted_prices 會依照價格由小到大排序。
print("原始價格字典:", prices)
print("價格最低的股票與價格:", min_price)
print("價格最高的股票與價格:", max_price)
print("依價格排序後的結果:", sorted_prices)

# 另一種常見寫法：直接對字典做 min，並指定 key 函式。
# min(prices, key=lambda k: prices[k]) 的意思是：
# 在所有股票代號中，找出對應價格最小的那個「代號」。
# 注意：這行回傳的是 key（股票代號），不是 (價格, 代號) tuple。
lowest_stock = min(prices, key=lambda k: prices[k])  # 回傳 key
print("價格最低的股票代號:", lowest_stock)
