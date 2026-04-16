# Remember（記憶）- enumerate() 和 zip()
# 本文件展示了兩個實用的迭代工具函數：
# 1. enumerate() - 在迭代時同時獲得索引和元素
# 2. zip() - 將多個序列配對迭代

# ========== enumerate() 函數 ==========
# enumerate(序列) 會返回一個迭代器，每次返回 (索引, 元素) 的元組
# 預設索引從 0 開始

colors = ["red", "green", "blue"]

print("--- enumerate() 基本用法 ---")
# enumerate() 返回 (索引, 顏色) 的元組
# 索引從 0 開始計算
for i, color in enumerate(colors):
    print(f"{i}: {color}")

print("\n--- enumerate(start=1) ---")
# 使用 start 參數可以改變索引的起始值
# 這在處理需要 1-based 索引的情況很有用（例如行號、序號等）
for i, color in enumerate(colors, 1):
    print(f"第{i}個: {color}")

print("\n--- enumerate with 檔案 ---")
# 實際應用：處理檔案時，經常需要記錄行號
# 使用 enumerate(lines, 1) 可以得到 1-based 的行號
lines = ["line1", "line2", "line3"]
for lineno, line in enumerate(lines, 1):
    print(f"行 {lineno}: {line}")

# ========== zip() 函數 ==========
# zip() 將多個序列中相同位置的元素配對
# 返回一個迭代器，每次返回由各序列對應元素組成的元組

print("\n--- zip() 基本用法 ---")
# zip(列表1, 列表2) 會同時迭代兩個列表
# 返回 (列表1的元素, 列表2的元素) 的元組
names = ["Alice", "Bob", "Carol"]
scores = [90, 85, 92]
for name, score in zip(names, scores):
    print(f"{name}: {score}")

print("\n--- zip() 多個序列 ---")
# zip() 可以處理多個序列
# 會同時從所有序列中取出相同位置的元素
a = [1, 2, 3]
b = [10, 20, 30]
c = [100, 200, 300]
for x, y, z in zip(a, b, c):
    print(f"{x} + {y} + {z} = {x + y + z}")

print("\n--- zip() 長度不同 ---")
# 當序列長度不同時，zip() 會在最短序列結束時停止
# 這可能導致較長序列的元素被忽略
x = [1, 2]
y = ["a", "b", "c"]
print(f"list(zip(x, y)): {list(zip(x, y))}")
# 結果：[(1, 'a'), (2, 'b')]，'c' 被忽略了

# 使用 zip_longest() 可以填充缺失的元素
from itertools import zip_longest

print(f"zip_longest: {list(zip_longest(x, y, fillvalue=0))}")
# 結果：[(1, 'a'), (2, 'b'), (0, 'c')]，缺失的值用 fillvalue 補充

print("\n--- 建立字典 ---")
# zip() 的常見應用：將鍵和值配對來建立字典
keys = ["name", "age", "city"]
values = ["John", "30", "NYC"]
d = dict(zip(keys, values))
print(f"dict: {d}")
