# R02. JSON 基礎讀寫（6.2）
# 本檔示範 json.loads、json.dumps、json.load、json.dump 的基本用法。
# 版本重點：用步驟化註解說明每一步「為何做、怎麼做、做完得到什麼」。
# 強化重點：每個步驟都會補上型別變化，幫助你建立 JSON 與 Python 物件的對應直覺。

import json

# ── 步驟 0：準備一筆 Python 物件資料 ──────────────────────
# 目的：先有一份記憶體中的資料，後續才能示範 JSON 的轉換流程。
# 作法：建立一個 dict，其中包含字串、整數、清單等常見型別。
# 結果：data 是 Python 物件，不是 JSON 字串。
# 觀察：此時資料仍可直接用 data["name"]、data["scores"][0] 這種 Python 方式存取。
data = {"name": "Alice", "age": 30, "scores": [95, 87, 92]}

# ── 步驟 1：序列化（Python -> JSON 字串）───────────────
# 目的：把 Python 物件轉為可傳輸、可儲存的 JSON 文字。
# 作法：使用 json.dumps(data)。
# 結果：s 的型別是 str，內容長得像 JSON。
# 子步驟 1-0：先做最基本的序列化，不加任何格式化參數。
s = json.dumps(data)
# 子步驟 1-1：印出型別與內容，確認確實已從 dict 變成 str。
print(type(s), s)

# Step 1-2：美化輸出版本
# 目的：讓 JSON 更好閱讀、較適合教學與除錯。
# 作法：indent=4 產生縮排，sort_keys=True 讓欄位排序固定。
# 結果：s_pretty 仍是字串，但版面比較整齊。
# 觀察：這只改變顯示格式，不改變資料語意。
s_pretty = json.dumps(data, indent=4, sort_keys=True)
print(s_pretty)

# ── 步驟 2：反序列化（JSON 字串 -> Python）──────────────
# 目的：把 JSON 文字還原回 Python 可操作的資料結構。
# 作法：使用 json.loads(s)。
# 結果：obj 會回到 dict，可直接用 key 取值。
# 子步驟 2-0：把剛才序列化的 s 還原。
obj = json.loads(s)
# 子步驟 2-1：印出型別與欄位，確認 str 已還原為 dict。
print(type(obj), obj["name"])

# ── 步驟 3：檔案 I/O（寫入與讀回）────────────────────────
# 目的：示範真實情境中 JSON 檔的存取流程。
# 作法：先 dump 到檔案，再 load 回記憶體。
# 結果：可確認「寫出去」與「讀回來」的資料一致。
# 觀察：dumps/loads 是字串層級；dump/load 是檔案層級，兩者概念相同。

# Step 3-1：寫出到檔案
# json.dump() 與 dumps() 概念相同，但 dump() 直接把 JSON 輸出到檔案物件。
# ensure_ascii=False 可保留中文原字，不轉成 \uXXXX 跳脫序列。
# 子步驟 3-1a：以寫入模式開啟檔案。
# 子步驟 3-1b：把 data 以 JSON 格式寫入檔案。
with open("/tmp/data.json", "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

# Step 3-2：從檔案讀入
# json.load() 會把檔案中的 JSON 內容直接轉成 Python 物件。
# 子步驟 3-2a：以讀取模式開啟同一檔案。
# 子步驟 3-2b：把 JSON 檔內容反序列化成 Python 物件。
with open("/tmp/data.json", "r", encoding="utf-8") as f:
    loaded = json.load(f)
# 子步驟 3-2c：印出 loaded，比對是否與原始 data 結構一致。
print(loaded)

# ── 步驟 4：理解型別對應規則 ────────────────────────────
# 目的：知道 Python 各型別會如何映射到 JSON，避免轉換後型別誤判。
# 作法：先看對照表，再做一個混合型別的小例子。
# 結果：可直覺預測 dumps / loads 的資料形狀。
# 觀察：JSON 沒有 tuple、set、datetime 等型別，這些型別通常需要自行轉換策略。
# Python dict   → JSON object  {}
# Python list   → JSON array   []
# Python str    → JSON string  ""
# Python int    → JSON number
# Python float  → JSON number
# Python True   → JSON true
# Python None   → JSON null

# Step 4-1：混合型別示範
# 這裡會看到 True -> true、None -> null 的轉換。
# 子步驟 4-1a：先建立混合型別清單。
# 子步驟 4-1b：序列化後觀察布林值與空值在 JSON 中的表示。
print(json.dumps([1, True, None, "hello"]))
# [1, true, null, "hello"]

# ── 步驟 5：中文顯示設定（ensure_ascii）──────────────────
# 目的：控制 JSON 輸出時，中文要直接顯示還是用跳脫字元表示。
# 作法：比較 ensure_ascii=False 與 ensure_ascii=True 的輸出差異。
# 結果：False 會保留中文；True 會轉成跳脫格式。
# 子步驟 5-0：準備含中文欄位與值的資料。
record = {"城市": "澎湖", "人口": 100000}
# 子步驟 5-1：False，直接顯示中文。
print(json.dumps(record, ensure_ascii=False))   # 會直接顯示中文
# 子步驟 5-2：True，將中文轉成跳脫格式。
print(json.dumps(record, ensure_ascii=True))    # 會將中文轉成跳脫格式

# 補充：學習順序建議
# 1. 先熟悉 dumps/loads（字串層級）
# 2. 再學 dump/load（檔案層級）
# 3. 最後再調整 indent、sort_keys、ensure_ascii 等輸出選項
# 4. 每做完一段就印 type(...)，確認自己真的理解型別是否改變
