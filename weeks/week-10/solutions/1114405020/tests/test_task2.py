import unittest
import xml.etree.ElementTree as ET
import sys
from pathlib import Path

# 添加上層目錄到 path，以便導入 task2_json_to_xml
sys.path.insert(0, str(Path(__file__).parent.parent))

from task2_json_to_xml import build_xml_tree


class TestTask2(unittest.TestCase):
    """Task 2 測試類"""
    
    def setUp(self):
        """設定測試資料"""
        self.sample_data = {
            "來源": "113年新生資料庫",
            "入學方式篩選": "聯合登記分發",
            "總人數": 3,
            "系所統計": {
                "資訊系": 2,
                "電機系": 1
            },
            "學生清單": [
                {
                    "學號": "1131001",
                    "系所名稱": "資訊系",
                    "畢業學校": "X高中",
                    "郵遞區號": "100"
                },
                {
                    "學號": "1131002",
                    "系所名稱": "電機系",
                    "畢業學校": "Y高中",
                    "郵遞區號": "101"
                },
                {
                    "學號": "1131003",
                    "系所名稱": "資訊系",
                    "畢業學校": "Z高中",
                    "郵遞區號": "102"
                }
            ]
        }
    
    def test_root_tag_and_attrs(self):
        """測試：根標籤為 students，total 屬性正確"""
        root = build_xml_tree(self.sample_data)
        self.assertEqual(root.tag, "students")
        self.assertEqual(root.get("source"), "113年新生資料庫")
        self.assertEqual(root.get("total"), "3")
    
    def test_student_count_matches(self):
        """測試：XML 中 <student> 數量與 JSON 學生清單一致"""
        root = build_xml_tree(self.sample_data)
        students = root.findall("student")
        self.assertEqual(len(students), 3)
    
    def test_student_attrs_exist(self):
        """測試：每個 <student> 包含 id、dept、school、zip 屬性"""
        root = build_xml_tree(self.sample_data)
        students = root.findall("student")
        for student in students:
            self.assertIsNotNone(student.get("id"))
            self.assertIsNotNone(student.get("dept"))
            self.assertIsNotNone(student.get("school"))
            self.assertIsNotNone(student.get("zip"))
    
    def test_empty_student_list(self):
        """測試：學生清單為空時，total 屬性為 0"""
        empty_data = {
            "來源": "113年新生資料庫",
            "總人數": 0,
            "學生清單": []
        }
        root = build_xml_tree(empty_data)
        self.assertEqual(root.get("total"), "0")
        students = root.findall("student")
        self.assertEqual(len(students), 0)
    
    def test_xml_is_valid(self):
        """測試：輸出的 XML 字串可被 ET.fromstring() 正常解析"""
        root = build_xml_tree(self.sample_data)
        xml_str = ET.tostring(root, encoding='unicode')
        
        # 應該能正常解析
        try:
            parsed = ET.fromstring(xml_str)
            self.assertEqual(parsed.tag, "students")
        except ET.ParseError:
            self.fail("XML 解析失敗")
    
    def test_student_data_accuracy(self):
        """測試：XML 中的學生資料與輸入資料一致"""
        root = build_xml_tree(self.sample_data)
        students = root.findall("student")
        
        # 檢查第一個學生
        self.assertEqual(students[0].get("id"), "1131001")
        self.assertEqual(students[0].get("dept"), "資訊系")
        self.assertEqual(students[0].get("school"), "X高中")
        self.assertEqual(students[0].get("zip"), "100")
    
    def test_root_attrs_with_empty_source(self):
        """測試：當 source 為空時的處理"""
        data = {
            "總人數": 1,
            "學生清單": [
                {"學號": "001", "系所名稱": "系", "畢業學校": "校", "郵遞區號": "0"}
            ]
        }
        root = build_xml_tree(data)
        self.assertEqual(root.get("source"), "")
        self.assertEqual(root.get("total"), "1")
    
    def test_xml_with_special_characters(self):
        """測試：XML 中處理特殊字元（中文）"""
        data = {
            "來源": "113年新生資料庫",
            "總人數": 1,
            "學生清單": [
                {
                    "學號": "1131001",
                    "系所名稱": "資訊工程系",
                    "畢業學校": "國立中興高級中學",
                    "郵遞區號": "402"
                }
            ]
        }
        root = build_xml_tree(data)
        xml_str = ET.tostring(root, encoding='unicode')
        
        # 應該能正常解析中文
        try:
            parsed = ET.fromstring(xml_str)
            student = parsed.find("student")
            self.assertEqual(student.get("dept"), "資訊工程系")
        except ET.ParseError:
            self.fail("XML 處理中文失敗")


if __name__ == '__main__':
    unittest.main()
