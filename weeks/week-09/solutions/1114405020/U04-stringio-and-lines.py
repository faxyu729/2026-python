# U04. 類檔案物件 StringIO 與逐行處理（5.6 / 5.1 逐行）
# Bloom: Understand — 知道 file-like 是鴨子型別，能把記憶體當檔案用

import io
from pathlib import Path

# ── 5.6 StringIO：記憶體裡的「假檔案」 ─────────────────
# io.StringIO() 會建立一個「文字型」的記憶體緩衝區，
# 介面看起來像檔案（可 write/read/seek），但資料存在 RAM 中。
#
# 適用情境：
# - 單元測試：不想真的寫入磁碟
# - 暫存文字內容：後續再一次取得完整字串
# - 要餵給只接受 file-like 物件的函式
buf = io.StringIO()
# print(..., file=buf) 代表把輸出導向到 buf，
# 不會印在終端機，而是累積在記憶體中。
print("第一行", file=buf)
print("第二行", file=buf)
print("第三行", file=buf)

# 取出整段字串
# getvalue()：把目前緩衝區所有內容一次取回成 str。
text = buf.getvalue()
print("---StringIO 內容---")
print(text)

# 也能當讀檔用：seek 回開頭再逐行讀
# 寫完後游標通常在尾端；若要從頭讀，必須先 seek(0)。
# 這個觀念和一般檔案物件完全相同。
buf.seek(0)
# enumerate(buf, 1) 會在逐行迭代時同時給行號（從 1 開始）。
for i, line in enumerate(buf, 1):
    # 每行通常帶有尾端換行，rstrip() 可移除顯示上的多餘空白。
    print(i, line.rstrip())

# 為什麼有用？任何收 file-like 的 API（csv、json、logging）
# 都能塞 StringIO，不必真的寫到磁碟、方便測試。
import csv
mem = io.StringIO()
# csv.writer 只要求目標物件具備 .write() 等檔案介面，
# 因此 StringIO 可直接當成「記憶體中的 CSV 檔案」。
writer = csv.writer(mem)
writer.writerow(["name", "score"])
writer.writerow(["alice", 90])
print("---CSV in memory---")
print(mem.getvalue())

# ── 5.1 延伸：逐行處理檔案（大檔友善） ─────────────────
# 先造一個多行檔
src = Path("poem.txt")
# write_text() 直接把文字寫入檔案；
# 這裡刻意放入空白行，後面用來示範過濾。
src.write_text("床前明月光\n\n疑是地上霜\n\n舉頭望明月\n低頭思故鄉\n", encoding="utf-8")

# 任務：過濾空行、加上行號、寫到新檔
dst = Path("poem_numbered.txt")
# 同時開兩個檔案：
# - fin: 讀取來源檔（rt）
# - fout: 寫入目標檔（wt）
# 以反斜線續行只是排版技巧，讓 with 區塊更易讀。
with open(src, "rt", encoding="utf-8") as fin, \
     open(dst, "wt", encoding="utf-8") as fout:
    # n 只統計「有效內容行」，所以空行不會編號。
    n = 0
    for line in fin:               # 逐行：一次只讀一行到記憶體
        # 移除每行尾端換行，方便做空行判斷與格式化輸出。
        line = line.rstrip()
        # 空字串代表原本是空行（或只有空白被去除後變空），直接跳過。
        if not line:
            continue               # 跳過空行
        # 只有非空行才遞增編號。
        n += 1
        # {n:02d} 表示至少兩位數，不足前補 0：
        # 1 -> 01, 2 -> 02，有助於對齊與閱讀。
        print(f"{n:02d}. {line}", file=fout)

print("---加行號後---")
# 最後讀回結果檢查，確認空行已被過濾且行號正確。
print(dst.read_text(encoding="utf-8"))
