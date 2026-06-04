import unittest

from square_counter import count_squares


class TestCountSquares(unittest.TestCase):
    def test_basic_range(self):
        self.assertEqual(count_squares(1, 10), 3)

    def test_edge_single_point_square(self):
        self.assertEqual(count_squares(4, 4), 1)

    def test_edge_single_point_non_square(self):
        self.assertEqual(count_squares(2, 2), 0)

    def test_edge_negative_to_positive(self):
        self.assertEqual(count_squares(-5, 5), 3)

    def test_invalid_input_raises(self):
        with self.assertRaises(ValueError):
            count_squares(5, 2)


if __name__ == "__main__":
    unittest.main()
