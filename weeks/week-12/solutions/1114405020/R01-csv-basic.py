# R01. CSV 基礎讀寫（6.1）
# 本檔示範 csv.reader、csv.writer、csv.DictReader、csv.DictWriter 的基本用法。
# 版本重點：把每段流程拆成清楚步驟，讓你知道「現在在做什麼、為什麼這樣做、做完會得到什麼」。

import csv
import io

# ── 範例資料（用字串模擬 CSV 檔案內容）────────────────────
# 實務上 CSV 常來自檔案，但這裡先用字串示範，方便在不依賴外部檔案的情況下觀察結果。
# 第一列通常是標頭（欄位名稱），後面每一列是實際資料。
# 你可以把它想像成一個「尚未被解析的原始文字檔內容」。
raw = """Symbol,Price,Date,Time,Change,Volume
AA,39.48,6/11/2007,9:36am,-0.18,181800
AIG,71.38,6/11/2007,9:36am,-0.15,195500
AXP,62.58,6/11/2007,9:36am,-0.46,935000
"""

# ── 步驟 1：用 csv.reader 讀取（每列 -> list）─────────────
# 目的：先看最基礎的 CSV 讀法，理解「CSV 其實就是一列一列的字串」。
# 作法：先把 raw 交給 StringIO 轉成類檔案物件，再交給 csv.reader。
# 結果：reader 會逐列吐出 list；每個欄位先以字串形式存在。
print("=== csv.reader ===")
# Step 1-1. 建立類檔案物件：讓 csv 模組可用「像讀檔案一樣」的方式讀字串。
f = io.StringIO(raw)
# Step 1-2. 建立 reader 迭代器：每次迴圈會拿到一列（list）。
reader = csv.reader(f)
# next(reader) 會先讀出第一列，因此這一列就會被當作欄位標頭來保存。
# 之後迴圈只處理真正的資料列。
# Step 1-3. 取出標頭列。
headers = next(reader)
print("標頭：", headers)
# Step 1-4. 逐列印出資料列，觀察 row 的型別與內容。
for row in reader:
    print(row)

# ── 步驟 2：用 csv.DictReader 讀取（每列 -> dict）──────────
# 目的：避免用索引位置存取欄位（例如 row[3]），改用欄位名稱存取更直覺。
# 作法：把同一份 raw 再讀一次，改用 DictReader。
# 結果：每列都會變成 dict，key 來自標頭列（Symbol、Price...）。
print("\n=== csv.DictReader ===")
# Step 2-1. 重新建立 StringIO；因為上一段已讀到檔尾，需重建新的讀取來源。
f = io.StringIO(raw)
# Step 2-2. 逐列讀出 dict，直接用欄位名稱取值。
for row in csv.DictReader(f):
    # row 是一個 dict，所以可以直接用欄位名稱取值。
    # 這裡用格式化輸出，讓欄位排列更整齊，方便觀察。
    print(f"{row['Symbol']:5s}  價格={row['Price']:>6s}  漲跌={row['Change']}")

# ── 步驟 3：用 csv.writer 寫出（list -> CSV）──────────────
# 目的：把 Python 資料寫成標準 CSV 文字格式。
# 作法：建立輸出用 StringIO，再用 writerow() 一列一列寫入。
# 結果：output.getvalue() 可拿到完整 CSV 內容。
print("\n=== csv.writer ===")
# Step 3-1. 建立輸出緩衝區（記憶體中的文字檔）。
output = io.StringIO()
# Step 3-2. 建立 writer，負責把資料列轉成 CSV 格式。
writer = csv.writer(output)
# writerow() 一次寫入一列；傳入 list、tuple 等可迭代資料即可。
# Step 3-3. 先寫標頭列，再寫資料列。
writer.writerow(["Symbol", "Price", "Change"])
writer.writerow(["AA", 39.48, -0.18])
writer.writerow(["AIG", 71.38, -0.15])
# getvalue() 會把 StringIO 目前累積的內容整段取出，方便檢查輸出結果。
# Step 3-4. 印出結果，確認是否為你預期的 CSV 格式。
print(output.getvalue())

# ── 步驟 4：用 csv.DictWriter 寫出（dict -> CSV）──────────
# 目的：資料若本來就是 dict，直接用欄位名稱寫出可讀性更好。
# 作法：先定義 fieldnames（欄位順序），再寫 header 與每筆 dict。
# 結果：不用記欄位索引，只要 key 對上欄位名稱即可。
print("=== csv.DictWriter ===")
# Step 4-1. 建立新的輸出緩衝區，避免和前一段內容混在一起。
output = io.StringIO()
# Step 4-2. 定義欄位順序；輸出 CSV 時會依這個順序排列。
fieldnames = ["Symbol", "Price", "Change"]
writer = csv.DictWriter(output, fieldnames=fieldnames)
# writeheader() 會依照 fieldnames 自動輸出第一列標頭。
# Step 4-3. 先寫表頭。
writer.writeheader()
# writerow() 接受 dict，key 會對應到欄位名稱。
# Step 4-4. 寫入每筆 dict 資料。
writer.writerow({"Symbol": "AA",  "Price": 39.48, "Change": -0.18})
writer.writerow({"Symbol": "AIG", "Price": 71.38, "Change": -0.15})
# Step 4-5. 印出最終 CSV 字串。
print(output.getvalue())

# ── 常用參數補充說明 ─────────────────────────────────────
# delimiter='\t'         → 指定分隔符號為 Tab，可用來處理 TSV 檔案。
# quotechar='"'          → 指定欄位包覆用的引號字元。
# quoting=csv.QUOTE_ALL   → 讓每個欄位都加上引號，常用於需要更嚴格輸出格式的情境。
# 小提醒：CSV 預設把所有欄位先當字串讀入；如果要做數值運算，通常要自行轉型（例如 float/int）。
