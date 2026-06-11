import unittest
import io
import sys
from contextlib import redirect_stdout

from timing import timeit


class TestTimeit(unittest.TestCase):
    def test_returns_original_result(self):
        @timeit
        def add(a, b):
            return a + b

        self.assertEqual(add(2, 3), 5)
        self.assertEqual(add(-1, 1), 0)

        @timeit
        def greet(name):
            return f"Hello, {name}!"

        self.assertEqual(greet("Alice"), "Hello, Alice!")

    def test_preserves_function_metadata(self):
        @timeit
        def add(a, b):
            """Return the sum of a and b."""
            return a + b

        self.assertEqual(add.__name__, "add")
        self.assertEqual(add.__doc__, "Return the sum of a and b.")

    def test_records_elapsed_time(self):
        @timeit
        def add(a, b):
            return a + b

        add(1, 2)
        self.assertIsInstance(add.last_elapsed, float)
        self.assertGreaterEqual(add.last_elapsed, 0)
        self.assertEqual(len(add.records), 1)

        add(3, 4)
        self.assertEqual(len(add.records), 2)
        self.assertIsInstance(add.records[0], float)
        self.assertIsInstance(add.records[1], float)

    def test_records_on_exception(self):
        @timeit
        def div(a, b):
            return a / b

        with self.assertRaises(ZeroDivisionError):
            div(1, 0)

        self.assertIsInstance(div.last_elapsed, float)
        self.assertGreaterEqual(div.last_elapsed, 0)
        self.assertEqual(len(div.records), 1)

    def test_no_print(self):
        @timeit
        def add(a, b):
            return a + b

        buf = io.StringIO()
        with redirect_stdout(buf):
            add(1, 2)

        self.assertEqual(buf.getvalue(), "")

    def test_records_multiple_calls_accumulate(self):
        @timeit
        def add(a, b):
            return a + b

        for i in range(5):
            add(i, i + 1)

        self.assertEqual(len(add.records), 5)
        for t in add.records:
            self.assertIsInstance(t, float)
            self.assertGreaterEqual(t, 0)


if __name__ == "__main__":
    unittest.main()
