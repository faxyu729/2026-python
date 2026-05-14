# R05. 資料統計與累加（6.13）
# 本檔示範 collections 裡幾個很常用的工具：Counter、defaultdict、namedtuple。
# 版本重點：改為步驟化註解，逐步說明每段的目的、作法、結果與資料流。

from collections import Counter, defaultdict, namedtuple

# ── 步驟 0：準備待統計資料 ──────────────────────────────
# 目的：先建立一份可計數的樣本資料。
# 作法：用清單裝多個字串，故意放入重複值。
# 結果：後續可觀察每個元素被統計出現的次數。
words = ["apple", "banana", "apple", "cherry", "banana", "apple"]

# ── 步驟 1：Counter 計數與排序 ──────────────────────────
# 目的：快速統計每個元素出現次數，並取出前幾名。
# 作法：先 Counter(words)，再使用 most_common(n)。
# 結果：得到類似 dict 的計數映射，並可依次數排序查看熱門元素。
# 子步驟 1-1：建立計數器物件。
cnt = Counter(words)
# Counter 會自動把相同元素的次數累加，回傳結果類似字典。
print("Counter：", cnt)
# most_common(n) 會依出現次數由高到低排序，取出前 n 名。
# 子步驟 1-2：查看前 2 名常見元素。
print("最多出現：", cnt.most_common(2))      # [('apple', 3), ('banana', 2)]

# 子步驟 1-3：合併不同批次統計結果。
# Counter 彼此可以直接相加，方便把多來源資料的計數整合。
extra = Counter(["banana", "cherry"])
print("合併：", cnt + extra)

# ── 步驟 2：defaultdict(list) 做分組 ────────────────────
# 目的：把同一類別資料自動收集到同一個清單。
# 作法：defaultdict(list) + 迴圈 append。
# 結果：每個 dept 對應一個成員清單，不需手動判斷 key 是否存在。
# 觀察：如果使用一般 dict，通常要先 if key not in dict 再初始化空 list。

# 子步驟 2-1：準備「系所, 姓名」資料。
records = [
    ("系資", "Alice"),
    ("電子", "Bob"),
    ("系資", "Carol"),
    ("電子", "David"),
    ("系資", "Eve"),
]

# 子步驟 2-2：建立分組容器，預設值為空 list。
by_dept = defaultdict(list)
for dept, name in records:
    # 因為預設值是 list，所以第一次遇到某系所時會自動建立空清單。
    # 之後就能直接 append，不需要先檢查 key 是否存在。
    by_dept[dept].append(name)

# 子步驟 2-3：輸出分組結果，確認同系資料有被聚合。
print("\ndefaultdict：")
for dept, members in by_dept.items():
    # items() 會同時取出 key 與 value，方便逐組輸出。
    print(f"  {dept}: {members}")

# ── 步驟 3：defaultdict(int) 做累加 ─────────────────────
# 目的：統計每個人的總分。
# 作法：defaultdict(int) 讓新 key 預設為 0，再用 += 累加。
# 結果：不用手動初始化分數，程式更精簡。
# 子步驟 3-1：建立「姓名, 分數」樣本資料。
score_sum = defaultdict(int)
scores = [("Alice", 90), ("Bob", 80), ("Alice", 85), ("Bob", 70)]

# 子步驟 3-2：逐筆累加總分。
for name, score in scores:
    # 第一次出現某個名字時，score_sum[name] 會先是 0，接著再把分數加上去。
    score_sum[name] += score

# 子步驟 3-3：印出最終總分。
# 轉成一般 dict 只是為了顯示時更直觀，避免印出 defaultdict(...) 的形式。
print("\n各人總分：", dict(score_sum))

# ── 步驟 4：namedtuple 建立可讀資料結構 ─────────────────
# 目的：保留 tuple 的輕量特性，同時提升欄位可讀性。
# 作法：先定義 Stock 型別，再建立一筆實例資料。
# 結果：可用 s.symbol、s.price 這種屬性式存取，而非 s[0]、s[1]。
# 子步驟 4-1：定義具名欄位。
Stock = namedtuple("Stock", ["symbol", "price", "change"])
# 子步驟 4-2：建立資料實例。
s = Stock("AA", 39.48, -0.18)
# 取值時可以直接用屬性名稱，不必記住第幾個欄位代表什麼。
print(f"\n{s.symbol}: ${s.price}  漲跌 {s.change}")

# ── 步驟 5：綜合應用（分組後計算平均）───────────────────
# 目的：整合前面觀念，從 list of dict 做實際統計。
# 作法：先以 dept 分組收集 score，再逐組計算平均值。
# 結果：可得到每個系所的平均分數。
# 子步驟 5-1：準備來源資料（常見於 CSV/JSON 讀入後）。
data = [
    {"dept": "系資", "score": 85},
    {"dept": "電子", "score": 78},
    {"dept": "系資", "score": 92},
    {"dept": "電子", "score": 88},
]

# 子步驟 5-2：用 defaultdict(list) 收集每系分數。
dept_scores = defaultdict(list)
for row in data:
    # 先用 dept 當分組 key，再把 score 收集到對應清單中。
    dept_scores[row["dept"]].append(row["score"])

# 子步驟 5-3：逐組計算平均並輸出。
print("\n各系平均：")
for dept, scores in dept_scores.items():
    # 平均分數 = 總和 / 筆數
    avg = sum(scores) / len(scores)
    print(f"  {dept}: {avg:.1f}")

# 補充：學習路徑建議
# 1. 先熟悉 Counter（最直觀的計數）
# 2. 再學 defaultdict(list/int)（分組與累加）
# 3. 最後用 namedtuple 提升資料可讀性，並練習整合成完整統計流程
