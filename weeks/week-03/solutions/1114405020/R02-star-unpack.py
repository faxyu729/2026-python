# R2. 解包數量不固定：星號解包（1.2）


# 這個函式要做的事：
# 從一串成績中「忽略第一個與最後一個」，只計算中間成績平均。
# 例如某些評分情境會去掉最高/最低或頭尾值。
def drop_first_last(grades):
    # 星號解包（extended unpacking）：
    # first  接第一個元素
    # middle 接中間所有元素（注意：一定是 list）
    # last   接最後一個元素
    # 這種寫法適合「頭尾固定、中間數量不固定」的資料。
    first, *middle, last = grades

    # middle 是要計算平均的主要資料來源。
    # 若 middle 為空，len(middle) 會是 0，會導致除以 0 錯誤。
    # 這個範例假設傳入資料至少有 3 筆（first/middle/last 才有意義）。
    return sum(middle) / len(middle)


# 這是一筆含有「姓名、Email、多個電話」的資料。
record = ('Dave', 'dave@example.com', '773-555-1212', '847-555-1212')

# 前兩個欄位固定拆給 name 與 email，
# 剩下全部欄位都交給 phone_numbers（結果會是 list）。
# 就算只有一支電話，phone_numbers 也會是 list（例如 ['773-...']）。
name, email, *phone_numbers = record


# 星號也可以放在前面：
# trailing 接前面所有元素，current 接最後一個元素。
# 常用在「最後一筆是目前值，其餘是歷史值」的情境。
*trailing, current = [10, 8, 7, 1, 9, 5, 10, 3]
