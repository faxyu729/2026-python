# R04. 位元組字串操作（2.20）
# bytes / bytearray 支援大部分字串方法，但有幾個重要差異

import re

# 建立 bytes 物件時，前面要加 b。
# 這代表內容是「位元組序列」，常見於檔案 I/O、網路封包、編碼轉換情境。
data = b"Hello World"
# 切片行為和一般字串很像，回傳的仍是 bytes。
print(data[0:5])  # b'Hello'
# startswith 也可用在 bytes，但比對目標必須也是 bytes。
print(data.startswith(b"Hello"))  # True
# split 預設會用空白切割，回傳 list[bytes]。
print(data.split())  # [b'Hello', b'World']
# replace 會回傳新 bytes，不會就地修改原本 data。
print(data.replace(b"Hello", b"Hello Cruel"))  # b'Hello Cruel World'

# 正則表達式也必須使用 bytes 模式
raw = b"FOO:BAR,SPAM"
# 注意這裡 pattern 要寫成 rb"..."（raw bytes pattern），
# 如果寫成一般字串 pattern，會和 bytes 資料型別不相容。
print(re.split(rb"[:,]", raw))  # [b'FOO', b'BAR', b'SPAM']

# 差異 1：索引回傳整數而非字元
a = "Hello"
b = b"Hello"
# str 索引會回傳單一字元（型別是 str）。
print(a[0])  # 'H'（字元）
# bytes 索引會回傳 0~255 的整數（對應該位元組的數值）。
# 這也是為什麼 b[0] 會是 72，而不是 'H'。
print(b[0])  # 72（整數，即 ord('H')）

# 差異 2：不能直接用 format()，需先編碼
# format() 產生的是 str（文字）；若要得到 bytes，需再 encode。
# 這裡使用 ASCII 編碼，因為內容都是英數與空白，最安全直觀。
formatted = "{:10s} {:10d}".format("ACME", 100).encode("ascii")
print(formatted)  # b'ACME            100'
