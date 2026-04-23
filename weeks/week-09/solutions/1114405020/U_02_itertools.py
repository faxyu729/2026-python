# Understand（理解）- itertools 工具函數

# 從 itertools 匯入常用工具：
# - islice: 針對「可迭代物件」做切片（不一定要先轉成 list）
# - dropwhile: 只要條件為 True 就持續丟棄前面的元素，直到第一次 False 後全部保留
# - takewhile: 只要條件為 True 就持續取元素，遇到第一次 False 立刻停止
# - chain: 把多個可迭代物件接成一條序列
# - permutations: 產生排列（順序有差）
# - combinations: 產生組合（順序無差）
from itertools import islice, dropwhile, takewhile, chain, permutations, combinations

print("--- islice() 切片 ---")


def count(n):
    # 這是一個「無限生成器」：從 n 開始一路遞增。
    # 使用 yield 可以每次產出一個值，保留函式狀態，下一次再從中斷處繼續。
    # 與一次建立超大清單相比，生成器更省記憶體。
    i = n
    while True:
        yield i
        i += 1


c = count(0)
# islice(c, 5, 10) 的語意：
# - 跳過前 5 個值（索引 0~4）
# - 取到索引 10 前（即 5~9），所以總共 5 個元素
# 注意：c 是生成器，被取用後游標會前進，之後再用 c 位置會改變。
result = list(islice(c, 5, 10))
print(f"islice(c, 5, 10): {result}")

print("\n--- dropwhile() 條件跳過 ---")
nums = [1, 3, 5, 2, 4, 6]
# dropwhile(lambda x: x < 5, nums) 的行為：
# 1) 從頭開始檢查，1<5 與 3<5 都成立，因此先丟棄
# 2) 到 5 時條件不成立（5<5 為 False），從這一刻起「後面全部保留」
# 3) 即使後面有 2、4 仍小於 5，也不再丟棄
result = list(dropwhile(lambda x: x < 5, nums))
print(f"dropwhile(x<5, {nums}): {result}")

print("\n--- takewhile() 條件取用 ---")
# takewhile(lambda x: x < 5, nums) 的行為：
# 1) 從頭開始取，1<5、3<5 成立所以保留
# 2) 遇到 5 時條件失敗，立刻停止，不再往後看
# 3) 所以結果只會是前面連續符合條件的區段
result = list(takewhile(lambda x: x < 5, nums))

print(f"takewhile(x<5, {nums}): {result}")
#if x < 5:
#   return Ture
#else:
#   return False
print("\n--- chain() 串聯 ---")
a = [1, 2]
b = [3, 4]
c = [5]
# chain(a, b, c) 會依序走訪 a -> b -> c，
# 像把三段資料接成一條資料流，不需先手動相加或合併。
print(f"chain(a, b, c): {list(chain(a, b, c))}")

print("\n--- permutations() 排列 ---")
items = ["a", "b", "c"]
print(f"permutations(items):")
# permutations(items) 預設取全部長度（r=len(items)），
# 產生所有可能順序，元素不可重複使用。
# 例如 ('a','b','c') 與 ('b','a','c') 視為不同結果。
for p in permutations(items):
    print(f"  {p}")

print(f"permutations(items, 2):")
# permutations(items, 2) 表示從 3 個元素中「依序」挑 2 個，
# 例如 ('a','b') 與 ('b','a') 仍是不同排列。
for p in permutations(items, 2):
    print(f"  {p}")

print("\n--- combinations() 組合 ---")
print(f"combinations(items, 2):")
# combinations(items, 2) 表示挑 2 個元素的所有組合，
# 與排列不同，組合不看順序：('a','b') 和 ('b','a') 視為同一組。
for c in combinations(items, 2):
    print(f"  {c}")

print("\n--- 組合應用：密碼窮舉 ---")
chars = ["A", "B", "1"]
print("2位數密碼:")
# 這裡用 permutations(chars, 2) 產生「不重複字元」的兩位密碼。
# 因為是排列，所以 AB 與 BA 會同時出現。
for p in permutations(chars, 2):
    print(f"  {''.join(p)}")

print("2位數密碼（可重複）:")
from itertools import combinations_with_replacement

# combinations_with_replacement(chars, 2) 允許重複元素，
# 例如 AA 可出現；但它是「組合」概念，不看順序，
# 所以 AB 會出現一次，不會同時有 BA。
for p in combinations_with_replacement(chars, 2):
    print(f"  {''.join(p)}")
