import unittest
import sys
from pathlib import Path

# 添加上層目錄到 path，以便導入 task1_csv_to_json
sys.path.insert(0, str(Path(__file__).parent.parent))

from task1_csv_to_json import filter_by_admission, count_by_dept, extract_student_info


class TestTask1(unittest.TestCase):
    """Task 1 測試類"""
    
    def setUp(self):
        """設定測試資料"""
        self.sample_rows = [
            {"入學方式": "聯合登記分發", "系所名稱": "資訊系", "學號": "1131001", "畢業學校": "X高中", "郵遞區號": "100"},
            {"入學方式": "聯合登記分發", "系所名稱": "電機系", "學號": "1131002", "畢業學校": "Y高中", "郵遞區號": "101"},
            {"入學方式": "聯合登記分發", "系所名稱": "資訊系", "學號": "1131003", "畢業學校": "Z高中", "郵遞區號": "102"},
            {"入學方式": "繁星推甄", "系所名稱": "機械系", "學號": "1131004", "畢業學校": "A高中", "郵遞區號": "103"},
            {"入學方式": "個人申請", "系所名稱": "電子系", "學號": "1131005", "畢業學校": "B高中", "郵遞區號": "104"},
        ]
    
    def test_filter_keeps_correct_rows(self):
        """測試：過濾後的列入學方式全為「聯合登記分發」"""
        result = filter_by_admission(self.sample_rows, "聯合登記分發")
        self.assertEqual(len(result), 3)
        for row in result:
            self.assertEqual(row["入學方式"], "聯合登記分發")
    
    def test_filter_removes_others(self):
        """測試：其他入學方式的列不出現在結果中"""
        result = filter_by_admission(self.sample_rows, "聯合登記分發")
        dept_list = [row["系所名稱"] for row in result]
        self.assertNotIn("機械系", dept_list)  # 繁星推甄系所不應該出現
        self.assertNotIn("電子系", dept_list)  # 個人申請系所不應該出現
    
    def test_filter_empty_input(self):
        """測試：空 list 輸入時回傳空 list"""
        result = filter_by_admission([], "聯合登記分發")
        self.assertEqual(result, [])
    
    def test_count_by_dept_correct(self):
        """測試：已知資料的系所統計結果正確"""
        filtered = filter_by_admission(self.sample_rows, "聯合登記分發")
        result = count_by_dept(filtered)
        self.assertEqual(result["資訊系"], 2)
        self.assertEqual(result["電機系"], 1)
        self.assertEqual(len(result), 2)
    
    def test_count_by_dept_empty(self):
        """測試：空輸入時回傳空 dict"""
        result = count_by_dept([])
        self.assertEqual(result, {})
    
    def test_extract_student_info_fields(self):
        """測試：提取的學生資訊包含正確的欄位"""
        result = extract_student_info(self.sample_rows[:1])
        self.assertEqual(len(result), 1)
        student = result[0]
        self.assertIn("學號", student)
        self.assertIn("系所名稱", student)
        self.assertIn("畢業學校", student)
        self.assertIn("郵遞區號", student)
    
    def test_filter_multiple_methods(self):
        """測試：不同入學方式的過濾"""
        result_1 = filter_by_admission(self.sample_rows, "繁星推甄")
        self.assertEqual(len(result_1), 1)
        self.assertEqual(result_1[0]["系所名稱"], "機械系")
        
        result_2 = filter_by_admission(self.sample_rows, "個人申請")
        self.assertEqual(len(result_2), 1)
        self.assertEqual(result_2[0]["系所名稱"], "電子系")
    
    def test_count_single_dept(self):
        """測試：僅有一個系所的統計"""
        single_dept = [
            {"入學方式": "聯合登記分發", "系所名稱": "資訊系"},
            {"入學方式": "聯合登記分發", "系所名稱": "資訊系"},
        ]
        result = count_by_dept(single_dept)
        self.assertEqual(result["資訊系"], 2)
        self.assertEqual(len(result), 1)


if __name__ == '__main__':
    unittest.main()
