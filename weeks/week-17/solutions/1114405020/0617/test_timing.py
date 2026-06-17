import unittest
from timing import timeit

class TestTimeit(unittest.TestCase):
    def test_basic_functionality(self):
        """測試回傳值不變、records 數量正確且 last_elapsed 為平均值"""
        @timeit(repeat=3)
        def add(a, b):
            """Add two numbers"""
            return a + b
        
        result = add(1, 2)
        self.assertEqual(result, 3)
        self.assertEqual(len(add.records), 3)
        self.assertIsInstance(add.records[0], float)
        self.assertAlmostEqual(add.last_elapsed, sum(add.records) / 3)

    def test_metadata_preservation(self):
        """測試 __name__ 與 __doc__ 是否被保留"""
        @timeit()
        def my_func():
            """Test docstring"""
            pass
        
        self.assertEqual(my_func.__name__, "my_func")
        self.assertEqual(my_func.__doc__, "Test docstring")

    def test_repeat_one(self):
        """Edge Case: repeat=1"""
        @timeit(repeat=1)
        def fast_func():
            return True
        
        fast_func()
        self.assertEqual(len(fast_func.records), 1)
        self.assertEqual(fast_func.last_elapsed, fast_func.records[0])

    def test_invalid_repeat(self):
        """Edge Case: repeat < 1 應拋出 ValueError"""
        with self.assertRaises(ValueError):
            @timeit(repeat=0)
            def fail_func():
                pass
            fail_func()

    def test_no_return_value(self):
        """Edge Case: 被裝飾函式沒有回傳值"""
        @timeit()
        def no_ret():
            pass
        
        result = no_ret()
        self.assertIsNone(result)
        self.assertTrue(len(no_ret.records) > 0)

if __name__ == "__main__":
    unittest.main()
