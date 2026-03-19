def parse_input(input_data):
    """
    解析輸入資料，取得學生數量 n、需要取出的前 k 名，以及所有學生的詳細資料。

    Args:
        input_data (str): 包含多行字串的輸入資料。

    Returns:
        tuple: (n, k, students) 包含學生數 (int)、提取名額 (int) 及學生清單 (list of tuples)。
    """
    lines = input_data.strip().split("\n")
    if not lines or not lines[0]:
        return 0, 0, []

    first_line = lines[0].split()
    n, k = int(first_line[0]), int(first_line[1])

    students = []
    for line in lines[1:]:
        if not line.strip():
            continue
        parts = line.split()
        name, score, age = parts[0], int(parts[1]), int(parts[2])
        students.append((name, score, age))

    return n, k, students


def sort_students(students):
    """
    依據成績（降冪）、年齡（升冪）、姓名（升冪）對學生進行排序。

    Args:
        students (list): 學生資料的串列，每個元素為 (name, score, age)。

    Returns:
        list: 排序後的學生清單。
    """
    return sorted(students, key=lambda x: (-x[1], x[2], x[0]))


def format_output(top_students):
    """
    格式化輸出的學生資料。

    Args:
        top_students (list): 排序並擷取後的學生清單。

    Returns:
        list: 每位學生資訊的字串串列。
    """
    return [f"{name} {score} {age}" for name, score, age in top_students]


def student_ranking(input_data):
    """
    執行學生排序流程，並回傳前 k 名學生的資料。

    Args:
        input_data (str): 原始輸入資料。

    Returns:
        list: 包含前 k 名學生資訊字串的串列。
    """
    n, k, students = parse_input(input_data)
    sorted_students = sort_students(students)
    top_k = sorted_students[:k]
    return format_output(top_k)
