# R02. 正則表達式：搜尋、替換、旗標（2.4–2.8）
# 這支程式是 Python 正則表達式 (Regular Expression, Regex) 的精華大補帖！
# 涵蓋了從基本的搜尋、替換，到進階的非貪婪模式、多行匹配等重要觀念。

import re

# ── 2.4 匹配和搜尋 (findall / match / finditer) ──────────────────
text = "Today is 11/27/2012. PyCon starts 3/13/2013."

# 使用 re.compile() 先將正則規則「編譯」起來。
# 這樣做的好處是：如果這個規則會被重複使用很多次，先編譯可以大幅提升效能！
# r"..." 的 r 代表 Raw String，意思是「裡面的反斜線 \ 不要當作跳脫字元」，寫 Regex 必加！
# (\d+) 代表一個群組 (Group)，裡面可以匹配 1 個以上的數字 (\d 是數字，+ 是一次以上)
datepat = re.compile(r"(\d+)/(\d+)/(\d+)")

# findall() 會找出所有符合的結果。
# 因為我們有加括號 () 做群組，所以它回傳的會是 Tuple 組成的 List。
print("findall 尋找所有:", datepat.findall(text))
# 輸出: [('11', '27', '2012'), ('3', '13', '2013')]

# match() 只會從字串的「最開頭」開始找，如果開頭不符合就直接回傳 None。
m = datepat.match("11/27/2012")
assert m is not None
# group(0) 代表「完整匹配到的字串」，groups() 代表「括號裡面的群組內容」
print("match 取值:", m.group(0), m.groups())  # 輸出: '11/27/2012' ('11', '27', '2012')

# finditer() 跟 findall 很像，但它回傳的是一個迭代器 (Iterator)。
# 這樣可以搭配 for 迴圈，一個一個拿出來處理，非常省記憶體。
print("finditer 巡覽結果:")
for m in datepat.finditer(text):
    month, day, year = m.groups()
    print(f"-> 轉換格式: {year}-{month}-{day}")


# ── 2.5 搜尋和替換 (sub / subn) ───────────────────────────────────
# re.sub() 可以用來替換字串。
# 神奇語法 r"\3-\1-\2"： \3 代表把第三個群組(年)搬到前面，\1 是月，\2 是日。
print("\n字串替換 (數字分組):", re.sub(r"(\d+)/(\d+)/(\d+)", r"\3-\1-\2", text))
# 輸出: 'Today is 2012-11-27. PyCon starts 2013-3-13.'

# 如果分組太多，用數字 \1 \2 容易搞混，可以使用「命名群組 (Named Group)」！
# 語法：(?P<名字>規則)，替換時使用 \g<名字>
print(
    "字串替換 (命名分組):",
    re.sub(
        r"(?P<month>\d+)/(?P<day>\d+)/(?P<year>\d+)",
        r"\g<year>-\g<month>-\g<day>",
        text,
    ),
)

# re.subn() 也是替換，但它會多回傳一個「替換了幾次」的數字。
newtext, n = re.subn(r"(\d+)/(\d+)/(\d+)", r"\3-\1-\2", text)
print(f"替換完成，共替換了 {n} 次")  # 輸出: 替換了 2 次


# ── 2.6 忽略大小寫 (IGNORECASE) ───────────────────────────────────
s = "UPPER PYTHON, lower python, Mixed Python"
# 加上 flags=re.IGNORECASE，不管是大寫、小寫還是混寫，通通抓出來！
print("\n忽略大小寫匹配:", re.findall("python", s, flags=re.IGNORECASE))
# 輸出: ['PYTHON', 'python', 'Python']


# ── 2.7 非貪婪 (最短匹配) ────────────────────────────
# 這是 Regex 裡最容易踩坑的地方！
text2 = 'Computer says "no." Phone says "yes."'

# 貪婪模式 (Greedy)：預設的 .* 會盡可能「吃掉最多」的字元。
# 所以它會從第一個引號，直接吃到最後面那句的引號，中間的東西全吃掉了！
print("貪婪模式:", re.compile(r'"(.*)"').findall(text2))
# 輸出: ['no." Phone says "yes.'] (抓錯了！)

# 非貪婪模式 (Non-greedy)：在 * 後面加上一個問號 ? 變成 .*?
# 這代表「吃得越少越好」，只要碰到下一個條件 (也就是引號) 就馬上停止！
print("非貪婪模式:", re.compile(r'"(.*?)"').findall(text2))
# 輸出: ['no.', 'yes.'] (完美命中！)


# ── 2.8 多行匹配 (DOTALL) ────────────────────────────
code = "/* this is a\nmultiline comment */"

# 在 Regex 裡，. (點) 預設可以匹配任何字元，【唯獨不包含換行符號 \n】！
# 所以如果是跨行的註解，普通的 .*? 會在第一行尾巴就停下來，導致匹配失敗。
# 解法：加上 re.DOTALL 旗標！這會讓 . 威力升級，連 \n 都吃得下去！
print("多行匹配:", re.compile(r"/\*(.*?)\*/", flags=re.DOTALL).findall(code))
# 輸出: [' this is a\nmultiline comment ']
