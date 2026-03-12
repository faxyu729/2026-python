# R13. 字典列表排序 itemgetter（1.13）

from operator import itemgetter

# rows 是「字典組成的串列」，每個字典代表一筆資料。
# fname: 名字
# uid: 使用者編號
rows = [
	{'fname': 'Brian', 'uid': 1003},
	{'fname': 'John', 'uid': 1001},
]

# itemgetter('fname') 會建立一個函式：
# 當它拿到一個字典時，會回傳該字典的 'fname' 值。
# sorted(..., key=...) 會依據這個 key 值進行排序。
# 這行的意思：依照名字字母順序排序。
rows_by_name = sorted(rows, key=itemgetter('fname'))

# 依照 uid（數字）由小到大排序。
rows_by_uid = sorted(rows, key=itemgetter('uid'))

# itemgetter('uid', 'fname') 會回傳一個 tuple： (uid, fname)
# 排序時會先比 uid；若 uid 相同，才比 fname。
# 這是多欄位排序的常見寫法。
rows_by_uid_then_name = sorted(rows, key=itemgetter('uid', 'fname'))
