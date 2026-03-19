# R15. 分組 groupby（1.15）

# 引入 groupby 模組，用於將迭代器中相鄰且相同的元素分組
from itertools import groupby

# 引入 itemgetter，這是一個方便取得字典或物件中特定鍵值的工具
from operator import itemgetter

# 建立一個包含多個字典的串列 (List of Dictionaries)
# 這裡模擬的是一些具有日期 (date) 與地址 (address) 的資料紀錄
rows = [
    {"date": "07/01/2012", "address": "..."},
    {"date": "07/02/2012", "address": "..."},
]

# 【非常重要】：在使用 groupby 之前，必須先將資料進行「排序 (sort)」！
# 因為 groupby 只會將「相鄰」且「鍵值相同」的項目分在一起。
# 如果相同的日期散落在不同的位置，groupby 會把它們分成不同組。
# 這裡使用 itemgetter('date')，代表我們依據每個字典裡的 'date' 鍵值來進行排序。
rows.sort(key=itemgetter("date"))

# 使用 groupby 對排序後的串列進行分組
# - 第一個參數：要被分組的資料 (這裡是 rows)
# - 第二個參數 key：指定分組的依據 (同樣使用 itemgetter('date')，依日期分組)
#
# groupby 每次迴圈會回傳兩個東西：
# 1. date: 分組的鍵值 (例如 '07/01/2012')
# 2. items: 一個迭代器 (iterator)，裡面包含了所有該群組底下的原始資料項目
for date, items in groupby(rows, key=itemgetter("date")):
    # 印出當前的分組日期 (選作，方便觀察結果)
    # print("日期：", date)

    # 遍歷該群組底下的每一筆資料
    for i in items:
        # i 是一個字典，例如 {'date': '07/01/2012', 'address': '...'}
        # 在這裡可以對群組內的資料進行操作
        pass
        # print("  資料內容：", i)
