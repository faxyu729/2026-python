# R1. 序列解包（1.1）

# 先建立一個 tuple（不可變序列），內容有兩個元素。
p = (4, 5)

# 序列解包（unpacking）：
# 右邊序列的第 1 個值給 x，第 2 個值給 y。
# 所以執行後：x = 4, y = 5。
# 重要規則：左邊變數數量要和右邊元素數量一致，否則會拋出 ValueError。
x, y = p

# 這是一個 list（可變序列），第四個元素本身又是一個 tuple。
# 結構可想成：
# ['ACME', 50, 91.1, (2012, 12, 21)]
data = ['ACME', 50, 91.1, (2012, 12, 21)]

# 一般解包：照位置把資料拆給對應變數。
# name='ACME', shares=50, price=91.1, date=(2012, 12, 21)
name, shares, price, date = data

# 巢狀解包：不只把第四個欄位取出，還直接把 (year, mon, day) 再拆開。
# 這樣可以少寫像 date[0], date[1], date[2] 這種索引存取。
# 執行後：year=2012, mon=12, day=21。
name, shares, price, (year, mon, day) = data

# 丟棄不需要的值（占位）
# 慣例上用底線 _ 表示「這個值我不會用到」。
# 這行只保留 shares 與 price，第一個與第四個欄位都忽略。
# 注意：_ 仍然是一個合法變數名稱，只是程式風格上拿來當占位符。
_, shares, price, _ = data
