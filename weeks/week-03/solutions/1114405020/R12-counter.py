# R12. Counter 統計 + most_common（1.12）

from collections import Counter

# words 是要統計出現次數的字串串列。
# 其中 look 出現 2 次，其餘先各 1 次。
words = ['look', 'into', 'my', 'eyes', 'look']

# Counter 可以把「元素 -> 次數」快速統計出來，
# 結果像是一個特化過的字典。
# 例如：Counter({'look': 2, 'into': 1, 'my': 1, 'eyes': 1})
word_counts = Counter(words)

# most_common(n) 會回傳前 n 個最高頻元素，格式是：
# [(元素, 次數), (元素, 次數), ...]
# 這行會得到出現次數最高的前 3 名。
top_three = word_counts.most_common(3)

# update(iterable) 會把新資料再累加進既有計數。
# 這裡又加入兩個 'eyes'，所以 eyes 的次數會增加 2。
word_counts.update(['eyes', 'eyes'])

# 補充觀念：
# Counter 常見用途包括：文字詞頻統計、投票計票、事件出現次數分析。
