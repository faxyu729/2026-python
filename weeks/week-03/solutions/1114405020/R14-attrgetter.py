# R14. 物件排序 attrgetter（1.14）

from operator import attrgetter


# 這裡先定義一個簡單的類別 User。
# 每個 User 物件都有一個 user_id 屬性。
class User:
    # 建構子：建立物件時，把傳入的 user_id 存到實例屬性。
    def __init__(self, user_id):
        self.user_id = user_id


# users 是「物件列表」，裡面放的是 User 實例，不是 dict。
users = [User(23), User(3), User(99)]

# attrgetter('user_id') 會建立一個取值函式：
# 當 sorted 逐一讀取 users 的元素時，
# 會去拿每個物件的 .user_id 當排序依據。
# 因此排序規則是依照 user_id 由小到大。
# 排序結果的順序會是：User(3), User(23), User(99)。
users_sorted = sorted(users, key=attrgetter('user_id'))

# 補充：
# 1) sorted 不會改動原本的 users，而是回傳新列表。
# 2) 如果想原地排序，可使用 users.sort(key=attrgetter('user_id'))。
