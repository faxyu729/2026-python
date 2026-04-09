# Remember（記憶）- 迭代器基礎概念
# 本程式展示 Python 迭代器的核心概念和用法
# 包括：協議、常見物件、自訂迭代器、例外處理等

# ── 1. 迭代器協議的核心方法 ──────────────────────────
# 迭代器協議：任何物件若實現 __iter__() 和 __next__() 方法，就是迭代器
# iter(obj)   → 呼叫 obj.__iter__()，傳回迭代器
# next(iter) → 呼叫 iter.__next__()，傳回下一個元素，無元素時擲出 StopIteration

items = [1, 2, 3]

# iter() 呼叫物件的 __iter__() 方法，傳回迭代器
it = iter(items)
# it 現在是一個迭代器物件，具有 __next__() 方法
print(f"迭代器: {it}")
# 輸出類似：<list_iterator object at 0x...>

# next() 呼叫迭代器的 __next__() 方法，傳回下一個元素
print(f"第一個: {next(it)}")  # 1
print(f"第二個: {next(it)}")  # 2
print(f"第三個: {next(it)}")  # 3

# 沒有更多元素時，__next__() 擲出 StopIteration 例外
# for 迴圈和其他工具會自動捕捉此例外以結束迭代
try:
    next(it)
except StopIteration:
    print("迭代結束!")  # 觸發此訊息


# ── 2. 常見可迭代物件 ────────────────────────────────
# 「可迭代物件」(iterable)：實現 __iter__() 方法的物件
# 它們可以傳入 iter() 以獲得迭代器
# 常見的：列表、字典、字串、集合、元組、檔案等

print("\n--- 常見可迭代物件 ---")

# 列表：最常用的可迭代物件
# iter([1,2,3]) 傳回一個 list_iterator 物件
print(f"列表 iter: {iter([1, 2, 3])}")
# 輸出：<list_iterator object at ...>

# 字串：逐字元迭代
# iter('abc') 傳回一個 str_iterator 物件
print(f"字串 iter: {iter('abc')}")
# 輸出：<str_iterator object at ...>

# 字典：迭代時預設為鍵 (keys)
# iter({'a': 1, 'b': 2}) 等同於 iter({'a': 1, 'b': 2}.keys())
print(f"字典 iter: {iter({'a': 1, 'b': 2})}")
# 輸出：<dict_keyiterator object at ...>

# 檔案：逐行迭代
import io

f = io.StringIO("line1\nline2\nline3")
# 檔案物件是可迭代的，遍歷時逐行讀取
print(f"檔案 iter: {iter(f)}")
# 輸出：<_io.StringIO object at ...>


# ── 3. 自訂可迭代物件和迭代器 ────────────────────────
# 要建立自訂可迭代物件，需要分開兩個類：
# 1. 可迭代物件類（Iterable）：實現 __iter__()，傳回迭代器
# 2. 迭代器類（Iterator）：實現 __next__()，傳回下一個元素


class CountDown:
    """可迭代物件：從 start 倒數到 1"""

    def __init__(self, start):
        self.start = start
        # 注意：可迭代物件通常不儲存迭代狀態

    def __iter__(self):
        # 每次 iter() 被呼叫，都傳回一個新的迭代器物件
        # 這樣允許多個迭代器同時遍歷同一個物件
        return CountDownIterator(self.start)


class CountDownIterator:
    """迭代器：實現實際的迭代邏輯"""

    def __init__(self, start):
        # 迭代器儲存遍歷狀態（current 位置）
        self.current = start

    def __next__(self):
        # 傳回下一個元素，或擲出 StopIteration 結束迭代
        if self.current <= 0:
            # 沒有更多元素，擲出 StopIteration
            raise StopIteration
        self.current -= 1
        # 傳回倒數的數字（current 遞減後才傳回）
        return self.current + 1


print("\n--- 自訂迭代器 ---")
for i in CountDown(3):
    print(i, end=" ")  # 3 2 1
# 說明：
#   - CountDown(3) 是可迭代物件
#   - for 迴圈呼叫 iter(CountDown(3))，得到 CountDownIterator(3)
#   - 然後重複呼叫 next()，直到 StopIteration 被擲出


# ── 4. 迭代器 vs 可迭代物件 ────────────────────────────
# 重要區分：
# 可迭代物件（Iterable）：實現 __iter__()，傳回迭代器
# 迭代器（Iterator）：實現 __iter__() 和 __next__()

print("\n--- 迭代器 vs 可迭代物件 ---")

# 列表是可迭代物件，不是迭代器
my_list = [1, 2, 3]
print(f"列表: 可迭代物件 ✓, 迭代器 ✗")
# 說明：列表有 __iter__()，但沒有 __next__()
#      每次 iter(my_list) 都傳回新的迭代器
#      可以多次遍歷，每次都重新開始

# 列表的 iter() 傳回迭代器
my_iter = iter(my_list)
print(f"iter(列表): 可迭代物件 ✗, 迭代器 ✓")
# 說明：iter(my_list) 傳回的物件同時有 __iter__() 和 __next__()
#      擁有內部狀態（當前位置）
#      一旦建立就無法重置，只能往前進行

# 迭代器本身就是可迭代物件（重要！）
print(f"迭代器: 可迭代物件 ✓ (有__iter__), 迭代器 ✓ (有__next__)")
# 說明：迭代器的 __iter__() 傳回它自己
#      這樣 iter(iterator) 就傳回該迭代器本身
#      這讓迭代器也能用於 for 迴圈


# ── 5. StopIteration 例外 ────────────────────────────
# 迭代結束時，__next__() 應擲出 StopIteration
# for 迴圈和其他工具會自動捕捉此例外以結束迭代

print("\n--- StopIteration 用法 ---")


# 方法 1：手動捕捉 StopIteration（章節 4.1 風格）
# 這展示 StopIteration 如何用來結束迭代
def manual_iter(items):
    """手動遍歷元素，捕捉 StopIteration 以結束迴圈"""
    it = iter(items)
    while True:
        try:
            item = next(it)
            # 成功取得下一個元素，進行處理
            print(f"取得: {item}")
        except StopIteration:
            # 迭代器已耗盡，沒有更多元素，結束迴圈
            break


manual_iter(["a", "b", "c"])
# 輸出：
# 取得: a
# 取得: b
# 取得: c


# 方法 2：使用 next() 的預設值參數
# next(iterator, default) 傳回預設值而不是擲出 StopIteration
def manual_iter_default(items):
    """使用預設值避免例外"""
    it = iter(items)
    while True:
        # next(it, None) 傳回下一個元素，或 None（如果迭代已完成）
        item = next(it, None)
        if item is None:
            # 接收到預設值，表示迭代結束
            break
        print(f"取得: {item}")


print("\n使用預設值:")
manual_iter_default(["a", "b", "c"])
# 輸出：
# 取得: a
# 取得: b
# 取得: c

# 比較：
#   - 方法 1：顯式捕捉 StopIteration，更清楚地表達意圖
#   - 方法 2：使用預設值，避免例外，更簡潔
#   - for 迴圈：最簡潔，會自動處理 StopIteration
