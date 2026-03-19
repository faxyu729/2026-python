from collections import defaultdict, Counter


def parse_logs(lines):
    """
    解析日誌行，統計每位使用者的操作次數，以及各種操作的總次數。

    Args:
        lines (list): 包含 'user action' 格式字串的串列。

    Returns:
        tuple: (user_counts, action_counts)
               user_counts 為紀錄使用者操作次數的 defaultdict。
               action_counts 為紀錄各種操作次數的 Counter。
    """
    user_counts = defaultdict(int)
    action_counts = Counter()

    for line in lines:
        if not line.strip():
            continue
        user, action = line.split()
        user_counts[user] += 1
        action_counts[action] += 1

    return user_counts, action_counts


def get_sorted_user_counts(user_counts):
    """
    將使用者的操作次數排序（按次數降冪，次數相同則按使用者名稱升冪）。

    Args:
        user_counts (dict): 使用者操作次數的字典。

    Returns:
        list: 格式化後的使用者次數清單。
    """
    sorted_users = sorted(user_counts.items(), key=lambda x: (-x[1], x[0]))
    return [f"{user} {count}" for user, count in sorted_users]


def get_top_action(action_counts):
    """
    取得出現最多次的操作及其次數。

    Args:
        action_counts (Counter): 記錄操作次數的 Counter。

    Returns:
        str: 格式為 'action count' 的字串。若無操作則回傳 'N/A 0'。
    """
    if action_counts:
        # 注意：Counter的most_common會回傳包含(元素, 次數)的list
        # 若有多個最高次數，這裡僅簡單取第一個。如需進階排序，可以再調整。
        top_action = action_counts.most_common(1)[0]
        return f"{top_action[0]} {top_action[1]}"
    else:
        return "N/A 0"


def log_summary(input_data):
    """
    統計日誌資料並回傳使用者的操作次數排序，以及最常出現的操作。

    Args:
        input_data (str): 原始的日誌輸入資料，首行為日誌筆數。

    Returns:
        dict: 包含 'user_counts' (list) 和 'top_action' (str) 的字典。
    """
    lines = input_data.strip().split("\n")
    if not lines:
        return {"user_counts": [], "top_action": "N/A 0"}

    m = int(lines[0])
    if m == 0:
        return {"user_counts": [], "top_action": "N/A 0"}

    user_counts, action_counts = parse_logs(lines[1:])

    user_counts_list = get_sorted_user_counts(user_counts)
    top_action_str = get_top_action(action_counts)

    return {"user_counts": user_counts_list, "top_action": top_action_str}
