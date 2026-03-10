def parse_input(input_data):
    lines = input_data.strip().split('\n')
    if not lines:
        return 0, 0, []
    
    first_line = lines[0].split()
    n, k = int(first_line[0]), int(first_line[1])
    
    students = []
    for line in lines[1:]:
        parts = line.split()
        name, score, age = parts[0], int(parts[1]), int(parts[2])
        students.append((name, score, age))
    
    return n, k, students

def sort_students(students):
    return sorted(students, key=lambda x: (-x[1], x[2], x[0]))

def format_output(top_students):
    return [f"{name} {score} {age}" for name, score, age in top_students]

def student_ranking(input_data):
    n, k, students = parse_input(input_data)
    sorted_students = sort_students(students)
    top_k = sorted_students[:k]
    return format_output(top_k)
