# U03. 字串格式化效能與陷阱（2.14–2.20）
# 本程式展示字串操作的效能問題與常見陷阱：
# 1. join 效能優於 + / 2. format_map 的缺失鍵處理 / 3. bytes 索引差異

import timeit

# ── join 效能優於 + （2.14）──────────────────────────
# 問題：使用 + 串接多個字串時，每次都建立新物件，時間複雜度為 O(n²)
# 解決：使用 join() 一次分配記憶體，時間複雜度為 O(n)，快 10-100 倍

parts = [f"item{i}" for i in range(1000)]  # 建立 1000 個字串的列表


def bad_concat():
    # ❌ 不好的做法：用 += 串接
    s = ""
    for p in parts:
        s += p  # 每次執行 += 時，Python 都要建立新字串物件
        # 第 1 次：s = "item0"（複製 "item0"，1 個字元）
        # 第 2 次：s = "item0item1"（複製 "item0item1"，13 個字元）
        # ...依此類推，最後複製整個字串，總成本 = O(n²)
    return s


def good_join():
    # ✓ 好的做法：用 join() 串接
    return "".join(parts)  # 一次分配所需記憶體，複製所有部分，O(n)


# 效能測試：比較兩種方法的耗時（各執行 500 次）
t1 = timeit.timeit(bad_concat, number=500)
t2 = timeit.timeit(good_join, number=500)
print(f"+串接: {t1:.3f}s  join: {t2:.3f}s")
# 通常 join 會快 10-100 倍，取決於字串數量和總長度


# ── format_map 處理缺失鍵（2.15）─────────────────────
# 問題：format() 如果鍵不存在會拋出 KeyError 例外
# 解決：自訂 dict 子類，覆寫 __missing__() 方法，缺失時返回預設值


class SafeSub(dict):
    # SafeSub 繼承 dict，並覆寫 __missing__() 方法
    # 當字典中找不到指定的鍵時，__missing__() 會被自動呼叫

    def __missing__(self, key: str) -> str:
        # key：format 字串中尋找的鍵名
        # 返回：用大括號包圍的鍵名，保留在輸出中
        return "{" + key + "}"  # 例如找不到 'n'，則返回 "{n}"


# 示例：使用 vars() 取得當前局部變數字典
name = "Guido"  # 存在於變數
s = "{name} has {n} messages."  # {name} 存在，{n} 不存在

# format_map() 比 format() 的優點：直接接收字典，不需複製
print(s.format_map(SafeSub(vars())))
# 'Guido has {n} messages.'（n 不存在，但不拋出例外，保留 {n}）
#
# 說明：
#   - vars() 在此作用域中傳回 {'name': 'Guido', 's': '...'}
#   - SafeSub 包裝此字典，使其具備缺失鍵容錯功能
#   - format_map() 找到 'name'，但找不到 'n'，呼叫 __missing__('n')
#   - 返回 "{n}"，保留在輸出字串中


# ── bytes 索引回傳整數（2.20）────────────────────────
# 問題：bytes 和 str 的索引行為不同，容易混淆
# str 索引傳回字元（字串），bytes 索引傳回整數（該位元組的值）

a = "Hello"  # 字串
b = b"Hello"  # 位元組字串

# 索引行為差異
print(a[0])  # 'H'（傳回字元，型態為 str）
print(b[0])  # 72（傳回整數，72 = ord('H')，該位元組的 ASCII 值）
#
# 說明：
#   - str[0] 傳回 str 型態的單一字元
#   - bytes[0] 傳回 int 型態的 0-255 整數值
#   - 這是因為 bytes 表示原始二進位資料，不一定是文字

# ── bytes 格式化的注意事項 ────────────────────────────
# 問題：bytes 不支援 format()，必須先用 str 格式化，再 encode 轉換
# ❌ 錯誤做法：b"...{:10s}...".format("ACME")  → TypeError

# ✓ 正確做法：先用字串格式化，再編碼為 bytes
formatted = "{:10s} {:5d}".format("ACME", 100)
# 說明：
#   "{:10s}" = 字串，寬度 10（右對齐，左邊補空白）
#   "{:5d}"  = 整數，寬度 5
#   結果：'ACME            100'（ACME 佔 4 個字元，補 6 個空格）

result = formatted.encode("ascii")  # 轉換為 bytes
print(result)
# b'ACME            100'
