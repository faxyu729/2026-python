import unittest

from robot_core import RobotState, run_commands, turn_left, turn_right


class TestRobotCore(unittest.TestCase):
    """核心規則測試：方向旋轉、越界、非法指令。"""

    def test_turn_left_from_north_is_west(self):
        self.assertEqual(turn_left("N"), "W")

    def test_turn_right_from_north_is_east(self):
        self.assertEqual(turn_right("N"), "E")

    def test_four_right_turns_back_to_original(self):
        d = "N"
        for _ in range(4):
            d = turn_right(d)
        self.assertEqual(d, "N")

    def test_forward_inside_boundary_not_lost(self):
        state = RobotState(0, 0, "N")
        scents = set()
        result = run_commands(state, "F", 5, 3, scents)
        self.assertEqual((result.x, result.y, result.direction, result.lost), (0, 1, "N", False))

    def test_forward_outside_boundary_becomes_lost(self):
        state = RobotState(5, 3, "N")
        scents = set()
        result = run_commands(state, "F", 5, 3, scents)
        self.assertTrue(result.lost)
        self.assertEqual((result.x, result.y, result.direction), (5, 3, "N"))

    def test_lost_robot_stops_processing_remaining_commands(self):
        state = RobotState(5, 3, "N")
        scents = set()
        result = run_commands(state, "FRF", 5, 3, scents)
        self.assertTrue(result.lost)
        self.assertEqual((result.x, result.y, result.direction), (5, 3, "N"))

    def test_invalid_command_raises_value_error(self):
        state = RobotState(0, 0, "N")
        scents = set()
        with self.assertRaises(ValueError):
            run_commands(state, "FX", 5, 3, scents, invalid_policy="raise")


if __name__ == "__main__":
    unittest.main()
