# U03. 文字 vs 位元組、編碼觀念（5.1 encoding / 5.4）
# Bloom: Understand — 能解釋什麼時候用 'rb'、為什麼要指定 encoding

from pathlib import Path

# ── 5.4 二進位讀寫：圖片、zip、任何非文字 ───────────────
# 檔案有兩種常見處理方式：
# 1) 文字模式（text mode）：處理 str，會涉及編碼/解碼
# 2) 二進位模式（binary mode）：處理 bytes，不做編碼轉換
#
# 這段示範二進位模式。先造一個「假 PNG」：
# 只寫 PNG 檔案最前面的 8 bytes（magic number），
# 用來識別檔案格式是否為 PNG。
magic = bytes([0x89, 0x50, 0x4E, 0x47, 0x0D, 0x0A, 0x1A, 0x0A])
# write_bytes() 會直接把 bytes 寫進檔案，
# 不需要也不能指定文字編碼。
Path("fake.png").write_bytes(magic)

# 讀回前 8 bytes，對照 PNG 檔頭
# 以 "rb" 開檔：read binary，回傳型別是 bytes。
with open("fake.png", "rb") as f:
    head = f.read(8)
print(head)           # b'\x89PNG\r\n\x1a\n'
print(head == magic)  # True

# bytes 可逐位元組迭代（每一格是 0~255 的 int，不是字串）
# 這跟 str 逐字元迭代（拿到字元）是不同概念。
for b in head[:4]:
    print(b, hex(b))

# ── 文字 vs 位元組的型別差 ─────────────────────────────
s = "你好"
# encode("utf-8")：把「文字(str)」轉成「位元組(bytes)」。
# 常見用途：
# - 網路傳輸（socket/http）
# - 寫入二進位檔案
# - 與只接受 bytes 的 API 溝通
b = s.encode("utf-8")   # str -> bytes
print(s, type(s))       # <class 'str'>
print(b, type(b))       # <class 'bytes'>
# decode("utf-8")：把 bytes 還原成 str。
# encode 與 decode 要用同一種編碼，才不會亂碼或錯誤。
print(b.decode("utf-8"))  # bytes -> str

# ── 5.1 encoding 參數：寫錯會爛掉 ──────────────────────
# write_text(..., encoding="utf-8")：
# 明確指定輸出編碼，避免不同作業系統/環境預設值不同造成問題。
Path("zh.txt").write_text("中文測試\n", encoding="utf-8")

# 正常：用 utf-8 讀 utf-8 寫的檔
print(Path("zh.txt").read_text(encoding="utf-8"))

# 故意弄錯：用 big5 解 utf-8 → UnicodeDecodeError
# 核心觀念：
# - 檔案本體只有 bytes
# - 解碼時你必須告訴 Python 這些 bytes 應該用哪種規則解讀
# - 若規則不對（例如 utf-8 檔用 big5 解），就可能拋出解碼例外
try:
    print(Path("zh.txt").read_text(encoding="big5"))
except UnicodeDecodeError as e:
    # 捕捉解碼失敗，讓錯誤示範可被清楚觀察。
    print("解碼錯誤:", e)

# 小結：
# - 文字檔：用 'rt'/'wt'（或 read_text/write_text），並明示 encoding='utf-8'
# - 二進位檔（png/zip/pickle/...）：用 'rb'/'wb'，處理 bytes，不談 encoding
# - 判斷口訣：
#   看到「可閱讀文字」通常走 str + encoding；
#   看到「原始資料格式」通常走 bytes + binary mode。
