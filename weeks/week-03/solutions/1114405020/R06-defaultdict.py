# R6. 多值字典 defaultdict / setdefault（1.6）

from collections import defaultdict

# defaultdict 的核心概念：
# 當你存取一個「不存在的鍵」時，它會自動建立預設值，
# 不用先寫 if key not in d 這種初始化程式。

# 這裡指定預設工廠是 list，表示新鍵預設值會是空串列 []。
d = defaultdict(list)

# 第一次存取 d['a'] 時，因為 a 不存在，會自動建立 d['a'] = []。
# 接著 append 1、append 2，結果會是 {'a': [1, 2]}。
d['a'].append(1); d['a'].append(2)

# 轉成一般 dict 只是為了輸出更直觀，資料內容不變。
print("使用 defaultdict(list) 後的結果:", dict(d))

# 這裡改成 set 當預設工廠，表示新鍵預設值會是空集合 set()。
d = defaultdict(set)

# 集合的特性是元素不重複。
# 即使重複 add 同一個值，結果中也只會保留一份。
d['a'].add(1); d['a'].add(2)
print("使用 defaultdict(set) 後的結果:", dict(d))

# setdefault 是一般 dict 也能用的做法。
# 語意是：
# - 如果鍵存在，回傳該鍵的值。
# - 如果鍵不存在，先建立鍵與預設值，再回傳該值。
d = {}

# 這行等價於：
# if 'a' not in d:
#     d['a'] = []
# d['a'].append(1)
d.setdefault('a', []).append(1)
print("使用 setdefault 後的結果:", d)
