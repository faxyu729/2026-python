from collections import defaultdict, Counter

def parse_logs(lines):
    user_counts = defaultdict(int)
    action_counts = Counter()
    
    for line in lines:
        user, action = line.split()
        user_counts[user] += 1
        action_counts[action] += 1
    
    return user_counts, action_counts

def get_sorted_user_counts(user_counts):
    sorted_users = sorted(user_counts.items(), key=lambda x: (-x[1], x[0]))
    return [f"{user} {count}" for user, count in sorted_users]

def get_top_action(action_counts):
    if action_counts:
        top_action = action_counts.most_common(1)[0]
        return f"{top_action[0]} {top_action[1]}"
    else:
        return "N/A 0"

def log_summary(input_data):
    lines = input_data.strip().split('\n')
    if not lines:
        return {
            "user_counts": [],
            "top_action": "N/A 0"
        }
    
    m = int(lines[0])
    if m == 0:
        return {
            "user_counts": [],
            "top_action": "N/A 0"
        }
    
    user_counts, action_counts = parse_logs(lines[1:])
    
    user_counts_list = get_sorted_user_counts(user_counts)
    top_action_str = get_top_action(action_counts)
    
    return {
        "user_counts": user_counts_list,
        "top_action": top_action_str
    }
