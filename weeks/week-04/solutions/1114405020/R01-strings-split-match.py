# R01. 字串分割與匹配（2.1–2.3）
# 這支程式示範了三個極度常用的字串處理技巧：
# 1. 使用正則表達式 (Regex) 處理多種分隔符號的字串分割
# 2. 檢查字串的開頭與結尾
# 3. 使用類似作業系統終端機 (Shell) 的萬用字元 (Wildcard) 來匹配字串

import re
from fnmatch import fnmatch, fnmatchcase

# ── 2.1 多界定符分割 (re.split) ──────────────────────────────────
# 情境：如果字串裡面混雜了逗號 (,)、分號 (;) 還有空白，用一般字串的 .split() 會很痛苦。
# 解法：使用 re.split() 搭配正則表達式！
line = "asdf fjdk; afed, fjek,asdf, foo"

# 正則表達式解說：r"[;,\s]\s*"
# [;,\s] 代表「遇到分號、逗號或空白字元 (空格/Tab)」的其中一個就算分隔符。
# \s*    代表「後面可以跟著零個或多個空白字元」，這樣就能把緊接在逗號後面的空白一起吃掉，才不會切出空白字串。
print("多分隔符分割：", re.split(r"[;,\s]\s*", line))
# 輸出：['asdf', 'fjdk', 'afed', 'fjek', 'asdf', 'foo']

# 非捕獲分組 (Non-capturing group)： (?:...)
# 如果你用括號 (...) 包住正則條件，re.split 會「連同分隔符號一起保留在結果串列中」。
# 但如果你加上了 ?: 變成 (?:...)，它就會「分組用，但不保留」，出來的結果跟上面一樣乾淨。
print("非捕獲分組：", re.split(r"(?:,|;|\s)\s*", line))
# 輸出：['asdf', 'fjdk', 'afed', 'fjek', 'asdf', 'foo']


# ── 2.2 開頭/結尾匹配 (startswith / endswith) ────────────────────────────────
# 這是 Python 內建最好用的字串方法之一，不需要動用殺雞焉用牛刀的正規表達式。
filename = "spam.txt"
print("是否以 .txt 結尾？", filename.endswith(".txt"))  # 輸出：True
print("是否以 file: 開頭？", filename.startswith("file:"))  # 輸出：False

# 💡 隱藏神技：同時檢查「多種」後綴或開頭
# 大多數人會寫一堆 or (if name.endswith('.c') or name.endswith('.h'))
# 但其實 endswith 和 startswith 允許你直接傳入一個「元組 (Tuple)」！
# 注意：只能傳入 Tuple，如果你傳 List 會噴錯 (TypeError)！
filenames = ["Makefile", "foo.c", "bar.py", "spam.c", "spam.h"]
# 找出所有 C 語言相關檔案 (.c 和 .h)
c_files = [name for name in filenames if name.endswith((".c", ".h"))]
print("找出多種副檔名：", c_files)
# 輸出：['foo.c', 'spam.c', 'spam.h']


# ── 2.3 Shell 通配符匹配 (fnmatch) ─────────────────────────────
# fnmatch 提供了一種比正則表達式 (Regex) 更簡單、更直覺的匹配方式。
# 它使用的是我們在終端機 (cmd/bash) 裡找檔案時用的那套規則，例如 `*` 代表任意字元，`?` 代表單一字元。

# `*.txt` 代表「只要結尾是 .txt 的都算數」
print("匹配 *.txt：", fnmatch("foo.txt", "*.txt"))  # 輸出：True

# `Dat[0-9]*` 代表「以 Dat 開頭，接著一個 0-9 的數字，後面隨便接什麼都可以」
print("匹配 Dat[0-9]*：", fnmatch("Dat45.csv", "Dat[0-9]*"))  # 輸出：True

# ⚠️ 大小寫區分的問題：
# fnmatch() 的行為會跟著你目前的「作業系統」而改變！
# 在 Windows 上它不分大小寫，但在 Mac/Linux 上會分大小寫。
# 如果你想要程式在所有系統上的行為一致（強制區分大小寫），請使用 fnmatchcase()！
print(
    "強制區分大小寫：", fnmatchcase("foo.txt", "*.TXT")
)  # 輸出：False (因為小寫 txt 不等於大寫 TXT)

# 實戰應用：在一堆地址中，找出所有以 " ST" (Street) 結尾的地址
addresses = ["5412 N CLARK ST", "1060 W ADDISON ST", "1039 W GRANVILLE AVE"]
street_addresses = [a for a in addresses if fnmatchcase(a, "* ST")]
print("尋找 ST 結尾地址：", street_addresses)
# 輸出：['5412 N CLARK ST', '1060 W ADDISON ST']
