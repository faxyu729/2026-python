# R03. 字串清理、對齊、拼接與格式化（2.11–2.16）
# 這支程式示範了日常開發中最常用到的各種字串「排版與整理」技巧。
# 學會這些，你就不需要自己寫一堆 for 迴圈來補空白、去空白或排版了！

import textwrap

# ── 2.11 清理字元 (strip) ─────────────────────────────────────
# strip() 就像是字串的「除毛刀」，預設會把字串【頭尾兩端】的空白、換行(\n) 全部削掉。
s = "  hello world \n"

# repr() 是用來把字串加上引號印出來，方便我們看清楚頭尾的空白還在不在。
print("去除兩端空白:", repr(s.strip()))  # 結果: 'hello world'
print("只去除左端空白:", repr(s.lstrip()))  # 結果: 'hello world \n'

# 進階用法：你不只能去空白，還能指定要去掉的符號！
# 這裡傳入 "-="，代表只要頭尾碰到減號或是等號，通通砍掉。
print("去除指定符號:", "-----hello=====".strip("-="))  # 結果: 'hello'


# ── 2.13 字串對齊 (ljust, rjust, center) ─────────────────────────────────────
# 這些方法可以幫你輕鬆做出報表、表格那樣整齊的輸出效果。
text = "Hello World"

print("\n靠左對齊(補滿20格):", repr(text.ljust(20)))  # 'Hello World         '
print("靠右對齊(補滿20格):", repr(text.rjust(20)))  # '         Hello World'

# 你還可以指定「拿什麼符號來補空白」
print("置中對齊(用*補滿):", text.center(20, "*"))  # '****Hello World*****'

# 另一個超強的內建函數 format()，它支援更簡潔的對齊符號：
# < 代表靠左，> 代表靠右，^ 代表置中。
print("使用 format 置中:", format(text, "^20"))  # '    Hello World     '

# 最常用的數字對齊與小數點控制： >10.2f
# >10 代表總共佔 10 格並靠右， .2f 代表浮點數保留兩位小數。
print("數字排版:", format(1.2345, ">10.2f"))  # '      1.23'


# ── 2.14 合併拼接 (join) ─────────────────────────────────────
# 如果你要把一個陣列裡面的字串接起來，【千萬不要用 + 號在迴圈裡加】！
# 因為字串是不可變的，每次 + 都會產生新字串，效能非常差。請一律使用 join()。
parts = ["Is", "Chicago", "Not", "Chicago?"]

print("\n用空白拼接:", " ".join(parts))  # 'Is Chicago Not Chicago?'
print("用逗號拼接:", ",".join(parts))  # 'Is,Chicago,Not,Chicago?'

# 如果陣列裡面混了數字怎麼辦？join 只吃字串！
# 神招：在 join 裡面塞一個生成器 (Generator)，自動把它們轉成 str。
data = ["ACME", 50, 91.1]
print("包含數字的拼接:", ",".join(str(d) for d in data))  # 'ACME,50,91.1'


# ── 2.15 插入變量 (format / f-string) ─────────────────────────────────────
name, n = "Guido", 37

# 老派作法一：使用 .format()
s = "{name} has {n} messages."
print("\n用 format:", s.format(name=name, n=n))

# 老派作法二：使用 format_map 搭配 vars()
# vars() 會把目前環境中所有的變數打包成一個字典，自動對應填入。
print("用 format_map:", s.format_map(vars()))

# 👑 現代最佳實踐 (Python 3.6+)： f-string
# 在字串前面加個 f，就可以直接把變數寫在括號 {} 裡面，可讀性最高、執行速度最快！
print("用 f-string (推薦):", f"{name} has {n} messages.")


# ── 2.16 指定列寬 (textwrap) ─────────────────────────────────────
# 當你有超級長的一行字串，想要把它變成「每行不超過 N 個字元」的文章排版時使用。
long_s = (
    "Look into my eyes, look into my eyes, the eyes, "
    "not around the eyes, look into my eyes, you're under."
)

print("\n【限制寬度排版 (每行最多40字)】")
# fill() 會幫你把長字串依照空格切斷換行，保證不會把單字切成兩半。
print(textwrap.fill(long_s, 40))

print("\n【限制寬度排版 (第一行縮排)】")
# initial_indent 可以幫你自動在第一段加上縮排空白。
print(textwrap.fill(long_s, 40, initial_indent="    "))
