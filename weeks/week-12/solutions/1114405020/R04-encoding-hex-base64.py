# R04. 十六進位與 Base64 編碼解碼（6.9–6.10）
# 本檔示範二進位資料常見的兩種表示法：Hex 與 Base64。
# 版本重點：用步驟化註解拆解每一步，並明確標示資料型別如何變化。

import binascii
import base64

# ── 步驟 0：準備原始位元組資料（bytes）────────────────────
# 目的：先有一段 bytes，才能示範如何轉成 Hex/Base64。
# 作法：建立一個 bytes 常值，內容包含 ASCII 與 UTF-8 中文位元組。
# 結果：data 的型別是 bytes，不是 str。
data = b"Hello, \xe4\xb8\x96\xe7\x95\x8c"   # "Hello, 世界" in UTF-8

# ── 步驟 1：Hex 編碼（bytes -> hex）──────────────────────
# 目的：把 bytes 轉成較易讀、可印出的十六進位表示。
# 作法：分別示範 binascii.b2a_hex() 與 bytes.hex()。
# 結果：兩者內容等價，但回傳型別不同。

# 子步驟 1-1：使用 binascii.b2a_hex()
# 輸入：bytes
# 輸出：bytes（內容是十六進位字元，例如 b'48656c...'）
hex_str = binascii.b2a_hex(data)
print("b2a_hex：", hex_str)                   # b'48656c6c6f2c ...'

# 子步驟 1-2：使用 bytes.hex()
# 輸入：bytes
# 輸出：str（內容是十六進位字元，例如 '48656c...'）
hex_str2 = data.hex()                         # Python 3.5+ 內建方法
print(".hex()：", hex_str2)

# ── 步驟 2：Hex 解碼（hex -> bytes）──────────────────────
# 目的：把剛才的十六進位表示還原成原始 bytes。
# 作法：對應使用 a2b_hex() 與 bytes.fromhex()。
# 結果：restored / restored2 應該都會回到與 data 相同的 bytes。

# 子步驟 2-1：把 b2a_hex() 的結果還原回 bytes
restored = binascii.a2b_hex(hex_str)
print("a2b_hex：", restored)

# 子步驟 2-2：把 .hex() 的字串結果還原回 bytes
restored2 = bytes.fromhex(hex_str2)           # Python 3.5+
print("fromhex：", restored2)

# 子步驟 2-3：驗證還原是否正確（Round-trip check）
# 如果不相等，assert 會拋錯，代表編碼/解碼流程有問題。
assert restored == data     # 確認一致
assert restored2 == data    # 再確認一次另一種 API 的還原結果

# ── 步驟 3：準備 Base64 測試資料 ─────────────────────────
# 目的：用一段乾淨的 ASCII bytes 示範 Base64 流程。
# 結果：msg 型別為 bytes。
msg = b"Python Cookbook"

# ── 步驟 4：Base64 編碼與解碼 ───────────────────────────
# 目的：示範如何把 bytes 轉成 Base64，再從 Base64 還原。
# 作法：先 b64encode()，再 b64decode()。
# 結果：decoded 應與 msg 完全一致。

# 子步驟 4-1：Base64 編碼
# 輸入：bytes
# 輸出：bytes（只含 Base64 字元集）
encoded = base64.b64encode(msg)
print("\nb64encode：", encoded)               # b'UHl0aG9uIENvb2tib29r'

# 子步驟 4-2：Base64 解碼
# 輸入：Base64 bytes
# 輸出：原始 bytes
decoded = base64.b64decode(encoded)
print("b64decode：", decoded)                 # b'Python Cookbook'

# 子步驟 4-3：驗證 Base64 還原結果
assert decoded == msg

# ── 步驟 5：URL-safe Base64 ─────────────────────────────
# 目的：在網址、檔名等情境避免使用 + / 這些可能造成語意衝突的字元。
# 作法：使用 urlsafe_b64encode()，將 + / 替換為 - _。
# 結果：得到更適合 URL 傳遞的 Base64 表示。
url_encoded = base64.urlsafe_b64encode(msg)
print("urlsafe：  ", url_encoded)

# ── 步驟 6：應用場景與重點比較 ───────────────────────────
# 目的：理解何時該選 Hex、何時該選 Base64。
# Hex    → 可讀性高，長度約為原始資料 2 倍，常見於 hash / MAC 位址 / 除錯輸出。
# Base64 → 長度約為原始資料 1.33 倍，常見於 email 附件、HTTP 認證、JWT。
# 關鍵觀念：兩者都是編碼（表示方式），不是加密；拿到資料的人可直接還原。
