# R3. deque 保留最後 N 筆（1.3）

from collections import deque

# deque 是 double-ended queue（雙向佇列），
# 可以在左端與右端都快速加入/移除元素。
# 常見用途：
# 1) 固定長度的最新資料緩衝區
# 2) 需要在兩端操作的佇列

# 建立一個最大長度為 3 的 deque。
# 當元素超過 3 筆時，會自動丟掉「最舊」的資料（左端）。
q = deque(maxlen=3)

# 依序從右端加入 1、2、3。
# 目前內容會是 [1, 2, 3]。
q.append(1); q.append(2); q.append(3)
print("加入 1、2、3 後:", list(q))

# 再從右端加入 4，因為已達 maxlen=3，
# 左端最舊的 1 會被自動移除，結果變成 [2, 3, 4]。
q.append(4)  # 自動丟掉最舊的 1
print("再加入 4 後:", list(q))

# 建立一個沒有長度上限的 deque，示範左右兩端操作。
q = deque()

# append(x)：從右端加入。
# appendleft(x)：從左端加入。
# 所以加入後結果會是 [2, 1]。
q.append(1); q.appendleft(2)
print("從右邊加入 1、從左邊加入 2 後:", list(q))

# pop()：從右端移除並回傳元素。
# 此時會取出 1，deque 變成 [2]。
right_value = q.pop()
print("從右邊移除的值:", right_value)
print("從右邊移除後的雙向佇列:", list(q))

# popleft()：從左端移除並回傳元素。
# 此時會取出 2，deque 變成空串列 []。
left_value = q.popleft()
print("從左邊移除的值:", left_value)
print("從左邊移除後的雙向佇列:", list(q))
