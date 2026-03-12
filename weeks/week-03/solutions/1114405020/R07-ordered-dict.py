# R7. OrderedDict（1.7）

from collections import OrderedDict
import json

# OrderedDict 是「會記住鍵加入順序」的字典型別。
# 在較舊的 Python 版本中，若你很在意鍵的輸出順序，
# 常用 OrderedDict 來明確表達「順序是資料的一部分」。
d = OrderedDict()

# 依序加入兩個鍵。
# 目前順序是：foo -> bar。
d['foo'] = 1; d['bar'] = 2

# 印出 OrderedDict 內容，可看到它保留了插入順序。
print("有序字典的內容:", d)

# json.dumps 會把字典物件轉成 JSON 字串。
# 因為 d 是有序的，所以輸出的鍵順序也會依照 foo、bar。
# 這在你需要「固定欄位順序」輸出時很有幫助。
json_result = json.dumps(d)
print("轉成 JSON 字串後:", json_result)
