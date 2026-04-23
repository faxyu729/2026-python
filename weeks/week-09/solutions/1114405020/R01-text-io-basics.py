# R01. 文本 I/O 基本式（5.1 / 5.2 / 5.3 / 5.17）
# Bloom: Remember — 會叫出 open/print 的基本參數

from pathlib import Path
# Path 用來表示檔案路徑，寫法比字串更直覺，
# 也方便跨平台（Windows/macOS/Linux）處理路徑。
# 常見模式字元：
# - w: write，寫入（若檔案存在會覆蓋）
# - a: append，附加（保留舊內容，從尾端加上新內容）
# - r: read，讀取
# - t: text，文字模式（預設就是 t）

# ── 5.1 讀寫文本檔 ─────────────────────────────────────
# 寫入：mode='wt'（w + t）
# - 使用 UTF-8 編碼，避免中文出現亂碼
# - 建議明確指定 encoding，讓不同電腦行為一致
path = Path("hello.txt")
# with 區塊的好處：區塊結束後會自動 close()，
# 就算中間發生例外，也能安全關檔。
with open(path, "wt", encoding="utf-8") as f:
    # write() 會把字串原樣寫入檔案，不會自動補換行，
    # 所以若要換行，要自己加上 \n。
    f.write("你好，Python\n")
    f.write("第二行\n")

# 讀回：一次讀完 vs 逐行讀
with open(path, "rt", encoding="utf-8") as f:
    # f.read()：一次把整個檔案讀成一個字串。
    # 適合小檔案；若檔案很大會占用較多記憶體。
    print(f.read())

with open(path, "rt", encoding="utf-8") as f:
    # 逐行迭代：每次只處理一行，較省記憶體，
    # 是處理大檔案時最常見的寫法。
    for line in f:
        # 每行通常尾端含有換行符 \n，
        # 用 rstrip() 去掉尾端空白與換行，輸出更乾淨。
        print(line.rstrip())

# ── 5.2 print 導向檔案 ─────────────────────────────────
with open("log.txt", "wt", encoding="utf-8") as f:
    # print(..., file=f) 可把輸出導向檔案，而不是終端機。
    print("登入成功", file=f)
    print("使用者:", "alice", file=f)
# print 重要參數：
# - *values: 一個或多個要輸出的值
# - sep: 多個值之間的分隔字串（預設空白）
# - end: 結尾字串（預設 \n）
# - file: 輸出目的地（預設 sys.stdout，這裡改為檔案）

# ── 5.3 調整分隔符與行終止符 ───────────────────────────
fruits = ["apple", "banana", "cherry"]
with open("fruits.csv", "wt", encoding="utf-8") as f:
    # *fruits 會把串列拆成多個位置參數，
    # 再透過 sep="," 串成 CSV 風格的一行。
    print(*fruits, sep=",", end="\n", file=f)
# CSV（Comma-Separated Values）：
# 用逗號分隔欄位，常用於表格資料交換。

# end='' 可避免多一個換行
with open("fruits.csv", "at", encoding="utf-8") as f:
    # 先輸出 date 並以逗號結尾，不換行。
    print("date", end=",", file=f)
    # 再接著把日期寫完，形成同一行的第二個欄位。
    print("2026-04-23", file=f)
# at 模式：append + text，在檔尾附加內容，不覆蓋舊資料。
# end=","：把一筆輸出接在同一行下一欄，常見於手動拼 CSV。

# Path.read_text() 是快速讀完整文字檔的便捷方法。
# 適合小檔案，因為會一次載入到記憶體。
print(Path("fruits.csv").read_text(encoding="utf-8"))
# apple,banana,cherry
# date,2026-04-23

# ── 5.17 文字模式 vs 位元組模式提醒 ────────────────────
# 重要型別規則：
# - 'wt'（文字模式）要寫入 str
# - 'wb'（位元組模式）要寫入 bytes
# 若模式與資料型別不相符，會拋出 TypeError。
try:
    with open("bad.txt", "wt", encoding="utf-8") as f:
        # 這行故意示範錯誤：在文字模式下寫 bytes。
        f.write(b"bytes in text mode")
except TypeError as e:
    # 捕捉錯誤並印出訊息，讓學習者知道錯在哪裡。
    print("錯誤示範:", e)
