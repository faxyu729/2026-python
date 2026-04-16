# Understand（理解）- 生成器概念
# 本文件展示了 Python 生成器的核心概念和高級用法：
# 1. 生成器函數和 yield 關鍵字
# 2. 生成器的延遲執行特性
# 3. yield from 的用法
# 4. 生成器在遞迴中的應用

# ========== 1. 基本生成器函數 ==========
# 生成器是一種特殊的函數，使用 yield 而不是 return
# 特點：
# - 執行到 yield 時會暫停，並返回 yield 的值
# - 呼叫 next() 時會從暫停處繼續執行
# - 比返回整個列表更節省記憶體


def frange(start, stop, step):
    """
    浮點數範圍生成器
    類似於內建的 range()，但支持浮點數步長

    參數：
        start: 起始值
        stop: 結束值（不包含）
        step: 步長
    """
    x = start
    while x < stop:
        yield x  # 返回當前值，並暫停執行
        x += step  # 下次呼叫時從這裡繼續


# 生成器函數返回一個生成器物件，它是延遲計算的
# list() 會消耗整個生成器，執行所有迭代直到 StopIteration
result = list(frange(0, 2, 0.5))
print(f"frange(0, 2, 0.5): {result}")


# ========== 2. 生成器的延遲執行 ==========
# 生成器不會在定義時執行，而是在呼叫 next() 時才執行
# 這樣可以處理無限序列或大資料集


def countdown(n):
    """
    倒數計時生成器
    演示生成器的延遲執行：
    - print("Starting...") 不會立即執行
    - 只有呼叫 next() 時才會執行
    """
    print(f"Starting countdown from {n}")
    while n > 0:
        yield n  # 暫停並返回當前的倒數值
        n -= 1
    print("Done!")


print("\n--- 建立生成器 ---")
# 呼叫生成器函數不會執行函數體
# 而是返回一個生成器物件
c = countdown(3)
print(f"生成器物件: {c}")

print("\n--- 逐步迭代 ---")
# 第一次呼叫 next() 時：
# - 執行 print("Starting countdown from 3")
# - 執行 yield 3，暫停並返回 3
print(f"next(c): {next(c)}")  # 執行程式碼，輸出 "Starting countdown from 3"，返回 3

# 第二次呼叫 next() 時：
# - 從上次暫停的地方繼續執行（n -= 1）
# - n 變為 2
# - 執行 yield 2，暫停並返回 2
print(f"next(c): {next(c)}")  # 返回 2

# 第三次呼叫 next() 時：
# - 從上次暫停的地方繼續執行（n -= 1）
# - n 變為 1
# - 執行 yield 1，暫停並返回 1
print(f"next(c): {next(c)}")  # 返回 1

# 第四次呼叫 next() 時：
# - 從上次暫停的地方繼續執行（n -= 1）
# - n 變為 0
# - while 迴圈條件不滿足，跳出迴圈
# - 執行 print("Done!")
# - 函數結束，擲出 StopIteration
try:
    next(c)
except StopIteration:
    print("StopIteration!")


# ========== 3. 無限生成器 ==========
# 生成器可以無限延續
# 因為使用延遲計算，所以不會佔用大量記憶體


def fibonacci():
    """
    費波那契數列生成器

    費波那契數列：0, 1, 1, 2, 3, 5, 8, 13, ...
    規則：每個數字是前兩個數字的和

    這個函數會無限迴圈，不斷生成費波那契數列的下一個數字
    我們可以取任意多個值，而不是限制在某個上限
    """
    a, b = 0, 1
    while True:
        yield a
        # 同時更新兩個變數：a 變為 b，b 變為 a+b
        a, b = b, a + b


print("\n--- Fibonacci 生成器 ---")
fib = fibonacci()
# 因為費波那契生成器是無限的，我們用 range(10) 只取前 10 個值
for i in range(10):
    print(next(fib), end=" ")
print()


# ========== 4. yield from 語法 ==========
# yield from 用於將一個可迭代物件的所有元素委託給生成器
# 相當於：for x in iterable: yield x


def chain_iter(*iterables):
    """
    串聯多個可迭代物件

    yield from 語句：
    - 逐一委託給 iterables 中的每個可迭代物件
    - 相當於：
      for it in iterables:
          for item in it:
              yield item
    """
    for it in iterables:
        yield from it  # 委託給可迭代物件 it


print("\n--- yield from 用法 ---")
result = list(chain_iter([1, 2], [3, 4], [5, 6]))
print(f"chain_iter: {result}")


# ========== 5. 生成器在樹遍歷中的應用 ==========
# 生成器特別適合遞迴遍歷複雜的資料結構


class Node:
    """樹的節點"""

    def __init__(self, value):
        self.value = value  # 節點的值
        self.children = []  # 子節點列表

    def add_child(self, node):
        """添加子節點"""
        self.children.append(node)

    def __iter__(self):
        """使節點本身可迭代，返回子節點"""
        return iter(self.children)

    def depth_first(self):
        """
        深度優先遍歷

        深度優先遍歷（DFS）的訪問順序：
        1. 訪問根節點
        2. 遞迴訪問第一個子樹的所有節點
        3. 遞迴訪問第二個子樹的所有節點
        4. ...依此類推

        使用生成器的好處：
        - 可以邊遍歷邊處理節點
        - 不需要一次性返回所有節點（節省記憶體）
        """
        yield self  # 先返回當前節點
        for child in self:
            # yield from child.depth_first() 會：
            # 1. 呼叫 child.depth_first()，得到一個生成器
            # 2. 將該生成器的所有值委託出去
            yield from child.depth_first()


print("\n--- 樹的深度優先遍歷 ---")
# 建立樹的結構：
#       0
#      / \
#     1   2
#    / \
#   3   4

root = Node(0)
root.add_child(Node(1))
root.add_child(Node(2))
root.children[0].add_child(Node(3))
root.children[0].add_child(Node(4))

# 深度優先遍歷的訪問順序：0 -> 1 -> 3 -> 4 -> 2
for node in root.depth_first():
    print(node.value, end=" ")
print()


# ========== 6. 生成器在列表攤平中的應用 ==========
# 另一個常見的遞迴應用：將巢狀列表攤平成單層列表


def flatten(items):
    """
    遞迴地攤平巢狀序列

    邏輯：
    - 對於 items 中的每個元素 x：
      - 如果 x 是可迭代的（有 __iter__）且不是字串，則遞迴攤平它
      - 否則，直接 yield x

    為什麼要特別檢查 not isinstance(x, str)？
    - 字串也是可迭代的（可以迭代每個字元）
    - 但我們希望將字串作為原子元素，不要將它拆分成字元
    """
    for x in items:
        # 檢查 x 是否是可迭代的（且不是字串）
        if hasattr(x, "__iter__") and not isinstance(x, str):
            # 遞迴攤平：yield from flatten(x)
            yield from flatten(x)
        else:
            # 原子元素，直接返回
            yield x


print("\n--- 巢狀序列攤平 ---")
nested = [1, [2, [3, 4]], 5]
print(f"展開: {list(flatten(nested))}")
