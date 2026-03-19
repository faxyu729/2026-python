import unittest
from task2_student_ranking import student_ranking

class TestStudentRanking(unittest.TestCase):
    def test_normal_case(self):
        input_data = """6 3
amy 88 20
bob 88 19
zoe 92 21
ian 88 19
leo 75 20
eva 92 20"""
        expected = [
            "eva 92 20",
            "zoe 92 21",
            "bob 88 19"
        ]
        self.assertEqual(student_ranking(input_data), expected)

    def test_k_zero(self):
        input_data = """3 0
a 90 20
b 80 21
c 70 22"""
        expected = []
        self.assertEqual(student_ranking(input_data), expected)

    def test_tie_breaking(self):
        input_data = """4 4
bob 88 19
ian 88 19
amy 88 20
zoe 88 21"""
        expected = [
            "bob 88 19",
            "ian 88 19",
            "amy 88 20",
            "zoe 88 21"
        ]
        self.assertEqual(student_ranking(input_data), expected)

if __name__ == '__main__':
    unittest.main()
