# R5. 優先佇列 PriorityQueue（1.5）

import heapq


# 這個類別示範如何用 heapq 自己包裝一個「最大優先權先出列」的佇列。
# Python 的 heapq 本質是「最小堆」（數值越小越先出來），
# 所以我們在 push 時把 priority 變成負值，藉此模擬最大堆行為。
class PriorityQueue:
    def __init__(self):
        # _queue 會存放堆積資料，元素格式是三元組：(-priority, index, item)
        # 為什麼要三元組：
        # 1) -priority：讓原本優先權越大者，變成數值越小，先被 heappop 取出。
        # 2) index：當優先權相同時，依照插入順序決定先後，避免比較 item 本身造成錯誤。
        # 3) item：真正要儲存與回傳的資料。
        self._queue = []

        # _index 是遞增流水號，每 push 一次就加 1。
        # 作用：提供穩定排序依據（同優先權時先進先出）。
        self._index = 0

    def push(self, item, priority):
        # heappush 會維持最小堆特性。
        # 放入 (-priority, _index, item) 後，堆頂會是「優先權最高」且「最早加入」的元素。
        heapq.heappush(self._queue, (-priority, self._index, item))
        self._index += 1

    def pop(self):
        # heappop 取出的會是三元組中排序最前面的元素。
        # [-1] 代表只回傳原始 item，不把內部排序資訊暴露給使用者。
        return heapq.heappop(self._queue)[-1]


# 建立優先佇列實例。
pq = PriorityQueue()

# 先加入低優先權任務。
pq.push('low', 1)
print("加入 low，優先權是 1 後:", pq._queue)

# 再加入中優先權任務。
pq.push('medium', 3)
print("加入 medium，優先權是 3 後:", pq._queue)

# 最後加入高優先權任務。
pq.push('high', 5)
print("加入 high，優先權是 5 後:", pq._queue)

# 第一次取出時，應該拿到最高優先權的 high。
first_item = pq.pop()
print("第一次取出的元素:", first_item)
print("第一次取出後的佇列:", pq._queue)

# 第二次取出時，拿到剩下中間優先權的 medium。
second_item = pq.pop()
print("第二次取出的元素:", second_item)
print("第二次取出後的佇列:", pq._queue)

# 第三次取出時，最後才是 low。
third_item = pq.pop()
print("第三次取出的元素:", third_item)
print("第三次取出後的佇列:", pq._queue)
