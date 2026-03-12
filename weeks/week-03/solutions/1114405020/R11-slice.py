# R11. 命名切片 slice（1.11）

# 這是一筆固定欄寬（fixed-width）的文字資料。
# 想像成一列報表：某些位置放股數、某些位置放價格，
# 其他位置可能是空白或填充字元（這裡用 . 示意）。
record = '....................100 .......513.25 ..........'

# slice(start, stop) 代表從 start 切到 stop-1（stop 不包含）。
# 這裡把「股數」欄位命名成 SHARES，避免直接寫神祕數字索引。
SHARES = slice(20, 23)

# 同理，把「價格」欄位命名成 PRICE。
# 命名切片的優點：
# 1) 可讀性高（知道這段索引代表什麼欄位）
# 2) 後續維護時只改這裡，不用到處找硬編索引
PRICE = slice(31, 37)

# record[SHARES] 會取出 '100'（字串）
# record[PRICE] 會取出 '513.25'（字串）
# 再分別轉成 int / float 後相乘，得到總成本。
cost = int(record[SHARES]) * float(record[PRICE])
