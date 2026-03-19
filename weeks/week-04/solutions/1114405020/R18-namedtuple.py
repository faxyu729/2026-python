# R18. 具名元組 namedtuple（1.18）
# namedtuple 是一種可以像字典一樣有名字 (key)，但又保留了元組 (tuple) 特性（輕量、不可變）的資料結構。
# 當你想建立一個簡單的類別 (Class) 來儲存資料，但又不想寫一大串 Class 程式碼時，這會是你的救星！

from collections import namedtuple

# ---------------------------------------------------------
# 範例一：基本的 namedtuple 建立與取值
# ---------------------------------------------------------
# 建立一個名為 'Subscriber' 的具名元組，並定義它有兩個屬性欄位：'addr' 和 'joined'
# (通常變數名稱與第一個參數的字串名稱會保持一致)
Subscriber = namedtuple("Subscriber", ["addr", "joined"])

# 接著我們就可以像呼叫類別 (Class) 的建構子一樣，建立一筆資料實體
sub = Subscriber("jonesy@example.com", "2012-10-19")

# 💡 namedtuple 的最大優點：
# 我們不再需要用難記的索引值 `sub[0]` 來取值，可以直接用 `.屬性名稱` 的方式來存取資料！
# 這讓程式碼的「可讀性」大幅提升。
# 例如，這裡可以直接取得 email 地址：
print(sub.addr)  # 結果會是：'jonesy@example.com'


# ---------------------------------------------------------
# 範例二：修改 namedtuple 內的值 (使用 _replace)
# ---------------------------------------------------------
# 建立一個 'Stock' 股票紀錄的資料結構，包含名稱、股數、價格
Stock = namedtuple("Stock", ["name", "shares", "price"])
s = Stock("ACME", 100, 123.45)

# ⚠️ 注意：因為它是「元組 (Tuple)」，所以它具有「不可變 (Immutable)」的特性！
# 你不能直接做這件事： s.shares = 75  <-- 會發生 AttributeError 錯誤！

# 如果你真的需要更新裡面的某個數值，你必須使用內建的 `_replace()` 方法。
# `_replace()` 會產生一個「全新的」namedtuple 實體，並替換掉你指定的欄位，
# 原本的實體不會被改變，所以通常我們會把新的結果重新指派回變數 `s`。
s = s._replace(shares=75)
# 此時的 s 變成了：Stock(name='ACME', shares=75, price=123.45)
