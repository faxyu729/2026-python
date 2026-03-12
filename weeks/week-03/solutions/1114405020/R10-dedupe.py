# R10. 去重且保序（1.10）

# 這個函式用來「去除重複值，並保留第一次出現的順序」。
# 核心技巧：
# 1) 用 seen（集合）記錄「已看過」的值，集合查找是 O(1) 平均時間。
# 2) 用 yield 逐筆產生結果，呼叫端可視需要轉成 list 或繼續串流處理。
def dedupe(items):
    # seen 用來追蹤已出現過的元素。
    seen = set()

    # 依原始順序走訪每個元素。
    for item in items:
        # 若目前元素還沒看過，才輸出。
        if item not in seen:
            # 先回傳這個「第一次出現」的元素。
            yield item

            # 再把它標記為已看過，後續重複值就會被略過。
            seen.add(item)


# 進階版：支援 key 函式，讓你決定「怎樣才算重複」。
# 適合元素本身不可雜湊（例如 dict）或你只想用部分欄位判斷重複時。
def dedupe2(items, key=None):
    seen = set()
    for item in items:
        # 若有提供 key，就用 key(item) 當比較基準；
        # 否則直接用 item 本身比較。
        val = item if key is None else key(item)

        # 只有當比較基準 val 首次出現時，才輸出原始 item。
        if val not in seen:
            yield item
            seen.add(val)


# 範例 1：一般數字去重。
# 原始順序是 [1, 5, 2, 1, 9, 1, 5, 10]
# 去重後會保留首次出現順序，變成 [1, 5, 2, 9, 10]。
numbers = [1, 5, 2, 1, 9, 1, 5, 10]
unique_numbers = list(dedupe(numbers))
print("原始數字串列:", numbers)
print("去除重複且保留原順序後:", unique_numbers)

# 範例 2：字典去重。
# dict 本身不能直接放進 set（不可雜湊），所以改用 key 取出可比較的 tuple。
records = [
    {'x': 1, 'y': 2},
    {'x': 1, 'y': 3},
    {'x': 1, 'y': 2},
    {'x': 2, 'y': 4},
]

# 這裡用 (x, y) 當去重依據：
# 代表只要 x 和 y 都相同，就視為重複資料。
unique_records = list(dedupe2(records, key=lambda item: (item['x'], item['y'])))
print("原始字典串列:", records)
print("依照 x 和 y 去除重複後:", unique_records)
