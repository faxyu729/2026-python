# U02. 正則表達式進階技巧（2.4–2.6）
# 本程式展示 regex 進階用法：
# 1. 預編譯提升效能 / 2. sub() 搭配回呼函數 / 3. 保持大小寫一致的替換

import re
import timeit
from calendar import month_abbr

# ── 預編譯效能（2.4）──────────────────────────────────
# 問題：重複使用相同的正則表達式時，每次都需要編譯，浪費效能
# 解決：使用 re.compile() 預先編譯，重複使用時會更快
text = "Today is 11/27/2012. PyCon starts 3/13/2013."
datepat = re.compile(r"(\d+)/(\d+)/(\d+)")  # 預編譯日期格式：MM/DD/YYYY
# 正則表達式說明：
#   (\d+)   = 捕獲分組 1：一個或多個數字（月份）
#   (\d+)   = 捕獲分組 2：一個或多個數字（日期）
#   (\d+)   = 捕獲分組 3：一個或多個數字（年份）


def using_module(text=text):
    # ❌ 效能較差：每次呼叫都要編譯正則表達式
    return re.findall(r"(\d+)/(\d+)/(\d+)", text)


def using_compiled():
    # ✓ 效能較佳：使用預編譯的正則表達式物件
    return datepat.findall(text)


# 效能測試：比較兩種方法的耗時（各執行 50,000 次）
t1 = timeit.timeit(using_module, number=50_000)
t2 = timeit.timeit(using_compiled, number=50_000)
print(f"直接呼叫: {t1:.3f}s  預編譯: {t2:.3f}s")
# 預編譯通常快 2-3 倍，且頻繁使用時優勢更明顯


# ── sub 回呼函數（2.5）────────────────────────────────
# 問題：簡單的字串替換無法滿足複雜的轉換需求
# 解決：使用回呼函數 (callback)，在 sub() 中接收 Match 物件並動態生成替換文本


def change_date(m: re.Match) -> str:
    # 參數 m 是 re.Match 物件，包含此次匹配的所有捕獲分組
    mon_name = month_abbr[
        int(m.group(1))
    ]  # month_abbr[1]='Jan', month_abbr[11]='Nov' 等
    # m.group(1) = 月份（作為整數）
    # m.group(2) = 日期
    # m.group(3) = 年份
    return f"{m.group(2)} {mon_name} {m.group(3)}"
    # 輸出格式：DD Mon YYYY（例如 27 Nov 2012）


# sub(pattern, repl, string) 中 repl 可以是函數
# 每次找到匹配時，就呼叫函數並傳入 Match 物件
print(datepat.sub(change_date, text))
# 'Today is 27 Nov 2012. PyCon starts 13 Mar 2013.'


# ── 保持大小寫一致的替換（2.6）───────────────────────
# 問題：簡單替換會破壞原始文本的大小寫模式
# 例如：要把 "python" 改為 "snake"，但要保持原文的大小寫（PYTHON→SNAKE, python→snake）
# 解決：使用高階函數 (higher-order function)，返回一個適應大小寫的替換函數


def matchcase(word: str):
    # 高階函數：接收要替換的字詞，返回一個替換函數
    def replace(m: re.Match) -> str:
        # 此函數會被 re.sub() 作為回呼函數呼叫
        t = m.group()  # 取得匹配的原文文本（例如 "PYTHON", "python", "Python"）

        if t.isupper():
            # 如果原文全部大寫，則返回大寫的替換詞
            return word.upper()  # word="snake" → "SNAKE"

        if t.islower():
            # 如果原文全部小寫，則返回小寫的替換詞
            return word.lower()  # word="snake" → "snake"

        if t[0].isupper():
            # 如果原文首字母大寫（駝峰），則返回首字母大寫的替換詞
            return word.capitalize()  # word="snake" → "Snake"

        # 其他情況直接返回替換詞（預設為小寫）
        return word

    return replace  # 返回替換函數


s = "UPPER PYTHON, lower python, Mixed Python"
# re.sub(pattern, repl, string, flags=...)
# flags=re.IGNORECASE 使搜尋不區分大小寫，可匹配 "PYTHON", "python", "Python"
print(re.sub("python", matchcase("snake"), s, flags=re.IGNORECASE))
# 'UPPER SNAKE, lower snake, Mixed Snake'
# 解釋：
#   - "PYTHON" 匹配 → 全大寫 → 返回 "SNAKE"
#   - "python"  匹配 → 全小寫 → 返回 "snake"
#   - "Python"  匹配 → 首大寫 → 返回 "Snake"
