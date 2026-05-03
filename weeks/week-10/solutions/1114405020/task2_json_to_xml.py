import json
import functools
import time
import xml.etree.ElementTree as ET
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
def read_json(filepath: str) -> dict:
    """讀取 JSON 檔案，回傳 dict"""
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data


def build_xml_tree(data: dict) -> ET.Element:
    """建構 ElementTree 結構，回傳根節點"""
    # 建立根節點
    root = ET.Element("students")
    root.set("source", data.get("來源", ""))
    root.set("total", str(data.get("總人數", 0)))
    
    # 添加每個學生的節點
    students = data.get("學生清單", [])
    for student in students:
        student_elem = ET.SubElement(root, "student")
        student_elem.set("id", student.get("學號", ""))
        student_elem.set("dept", student.get("系所名稱", ""))
        student_elem.set("school", student.get("畢業學校", ""))
        student_elem.set("zip", student.get("郵遞區號", ""))
    
    return root


@timeit
def write_xml(data: dict, filepath: str) -> None:
    """將 dict 轉換為 XML 並寫出"""
    # 建構 XML 樹
    root = build_xml_tree(data)
    
    # 建立 ElementTree 物件
    tree = ET.ElementTree(root)
    
    # 確保目錄存在
    Path(filepath).parent.mkdir(parents=True, exist_ok=True)
    
    # 寫出 XML 檔案（含 XML 宣告）
    tree.write(filepath, encoding='utf-8', xml_declaration=True)


def main():
    # 讀取 JSON 檔案
    json_path = r"E:\python\week 10\2026-python\weeks\week-10\solutions\1114405020\output\students.json"
    data = read_json(json_path)
    
    # 寫出 XML
    xml_path = r"E:\python\week 10\2026-python\weeks\week-10\solutions\1114405020\output\students.xml"
    write_xml(data, xml_path)
    
    print("XML conversion completed!")
    print(f"  Total students: {data.get('總人數', 0)}")
    print(f"  Output file: {xml_path}")


if __name__ == "__main__":
    main()
