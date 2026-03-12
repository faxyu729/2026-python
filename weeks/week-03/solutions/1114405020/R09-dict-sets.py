# R9. 兩字典相同點：keys/items 集合運算（1.9）

# 兩個示範字典：
# a 與 b 有部分相同鍵（x, y），也有各自獨有鍵（z 與 w）。
a = {'x': 1, 'y': 2, 'z': 3}
b = {'w': 10, 'x': 11, 'y': 2}

# dict_keys 物件可以做集合運算。
# a.keys() & b.keys() 是交集：同時出現在 a、b 的鍵。
same_keys = a.keys() & b.keys()

# a.keys() - b.keys() 是差集：只在 a 出現、不在 b 出現的鍵。
only_in_a = a.keys() - b.keys()

# items() 會得到 (key, value) 配對，
# 做交集時必須 key 和 value 都一樣才算相同。
# 例如 ('y', 2) 會被視為共同項目；
# 但 x 的值不同（1 vs 11），所以 ('x', 1) 和 ('x', 11) 不會相同。
same_items = a.items() & b.items()

print("字典 a 的內容:", a)
print("字典 b 的內容:", b)
print("兩個字典共同擁有的鍵:", same_keys)
print("只在字典 a 中出現的鍵:", only_in_a)
print("兩個字典完全相同的鍵值配對:", same_items)

# 字典推導式（dict comprehension）：
# 從 a 挑選鍵來建立新字典 c。
# 這裡用 a.keys() - {'z', 'w'} 表示把 z、w 排除。
# 因為 w 本來就不在 a，實際上會排掉的是 z，
# 所以 c 會留下 x 與 y 對應的資料。
c = {k: a[k] for k in a.keys() - {'z', 'w'}}
print("排除 z 和 w 後建立的新字典:", c)
