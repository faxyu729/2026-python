import csv
import json
import functools
import time
from collections import Counter
from pathlib import Path


def timeit(func):
    """計時裝飾器：量測函式執行時間"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        print(f"[timeit] {func.__name__} 耗時 {elapsed:.6f}s")
        return result
    return wrapper


@timeit
def read_csv(filepath: str) -> list[dict]:
    """讀取 CSV 檔案，回傳所有列的 list"""
    rows = []
    with open(filepath, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(row)
    return rows


def filter_by_admission(rows: list[dict], method: str) -> list[dict]:
    """按入學方式過濾學生資料"""
    return [r for r in rows if r.get("入學方式") == method]


def count_by_dept(rows: list[dict]) -> dict:
    """統計各系所的學生人數"""
    if not rows:
        return {}
    dept_names = [r.get("系所名稱", "") for r in rows]
    return dict(Counter(dept_names))


def extract_student_info(rows: list[dict]) -> list[dict]:
    """提取需要的學生資訊"""
    students = []
    for row in rows:
        student = {
            "學號": row.get("學號", ""),
            "系所名稱": row.get("系所名稱", ""),
            "畢業學校": row.get("畢業學校", ""),
            "郵遞區號": row.get("郵遞區號", ""),
        }
        students.append(student)
    return students


@timeit
def write_json(data: dict, filepath: str) -> None:
    """將資料寫出為 JSON 檔案"""
    # 確保目錄存在
    Path(filepath).parent.mkdir(parents=True, exist_ok=True)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def main():
    # 讀取 CSV 檔案
    csv_path = r"E:\python\week 10\2026-python\assets\stu-data\113年新生資料庫.csv"
    rows = read_csv(csv_path)
    
    # 過濾入學方式
    admission_method = "聯合登記分發"
    filtered_rows = filter_by_admission(rows, admission_method)
    
    # 統計系所人數
    dept_stats = count_by_dept(filtered_rows)
    
    # 提取學生資訊
    student_list = extract_student_info(filtered_rows)
    
    # 準備輸出資料
    output_data = {
        "來源": "113年新生資料庫",
        "入學方式篩選": admission_method,
        "總人數": len(filtered_rows),
        "系所統計": dept_stats,
        "學生清單": student_list
    }
    
    # 寫出 JSON
    json_path = r"E:\python\week 10\2026-python\weeks\week-10\solutions\1114405020\output\students.json"
    write_json(output_data, json_path)
    
    print("Processing completed!")
    print(f"  Filter: admission_method = '{admission_method}'")
    print(f"  Total students: {len(filtered_rows)}")
    print(f"  Departments: {len(dept_stats)}")
    print(f"  Output file: {json_path}")


if __name__ == "__main__":
    main()
