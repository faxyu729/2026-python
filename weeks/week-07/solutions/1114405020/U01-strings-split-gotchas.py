# U01. 字串分割與匹配的陷阱（2.1–2.11）
# 本程式展示字串操作中的常見坑點：
# 1. 捕獲分組保留分隔符 / 2. startswith 必須傳 tuple / 3. strip 只處理頭尾

import re

# ── 捕獲分組保留分隔符（2.1）─────────────────────────
# 問題：re.split() 使用捕獲分組 (...) 會將分隔符也保留在結果中
# 這有助於重建原始文本或分析文本結構

line = "asdf fjdk; afed, fjek,asdf, foo"
# re.split(r"(;|,|\s)\s*", line) 將分隔符放在括號內（捕獲分組）
# 分隔符包括：; 或 , 或空白字元，後面可能還有空白（\s*）
fields = re.split(r"(;|,|\s)\s*", line)
# 結果：['asdf', ' ', 'fjdk', ';', 'afed', ',', 'fjek', ',', 'asdf', ',', 'foo']
# 注意：偶數索引 (0,2,4...) 是實際值，奇數索引 (1,3,5...) 是分隔符

values = fields[::2]  # 偶數索引 = 實際值（[::2] 是步長為2的切片）
delimiters = fields[1::2] + [""]  # 奇數索引 = 分隔符，最後加空字串以對齐
# 重建：透過 zip() 配對每個值與其對應的分隔符，然後用 "".join() 連接
rebuilt = "".join(v + d for v, d in zip(values, delimiters))
print(rebuilt)  # 'asdf fjdk;afed,fjek,asdf,foo'（分隔符位置保留）

# ── startswith 必須傳 tuple（2.2）────────────────────
# 問題：startswith() 的第一個參數必須是字串或 tuple，不能是 list
# 常見錯誤：傳入 list 會導致 TypeError

url = "http://www.python.org"
choices = ["http:", "ftp:"]  # 這是 list

# ❌ 錯誤做法：直接傳 list
try:
    result = url.startswith(choices)  # type: ignore[arg-type]
except TypeError as e:
    # 會觸發：TypeError: startswith first arg must be str or a tuple of str, not list
    print(f"TypeError: {e}")  # 不能傳 list！

# ✓ 正確做法：將 list 轉換為 tuple
print(url.startswith(tuple(choices)))  # True（轉成 tuple 才行）

# ── strip 只處理頭尾，不處理中間（2.11）──────────────
# 問題：strip() 只移除字串開頭與結尾的空白，中間的空白保持不變
# 這與許多人期望的「移除所有空白」不同

s = "  hello     world  "

# ❌ 問題 1：strip() 只清理頭尾
print(repr(s.strip()))  # 'hello     world'（中間多餘空白還在）

# ❌ 問題 2：replace(" ", "") 會移除所有空白，包括單詞間的空白
print(repr(s.replace(" ", "")))  # 'helloworld'（過頭，連詞間空白也消）

# ✓ 正確做法：先 strip()，再用 re.sub() 將多個空白壓縮成一個
# re.sub(r"\s+", " ", ...) 將一個或多個空白字元替換為單一空格
print(repr(re.sub(r"\s+", " ", s.strip())))  # 'hello world'（正確）

# 補充：生成器逐行清理（高效，不預載入記憶體）
# 當處理大量行時，使用生成器表達式比一次性載入更節省記憶體
lines = ["  apple  \n", "  banana  \n"]
for line in (l.strip() for l in lines):  # 生成器表達式：(l.strip() for l in lines)
    # l.strip() 移除每行的頭尾空白（包括換行符 \n）
    print(line)  # apple、banana
