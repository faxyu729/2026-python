import unittest

from robot_core import RobotState, run_commands


class TestRobotScent(unittest.TestCase):
    """scent 規則測試：相同位置與方向才會忽略危險前進。"""

    def test_first_robot_leaves_scent_after_lost(self):
        state = RobotState(5, 3, "N")
        scents = set()
        result = run_commands(state, "F", 5, 3, scents)
        self.assertTrue(result.lost)
        self.assertIn((5, 3, "N"), scents)

    def test_second_robot_ignores_dangerous_forward_on_same_scent(self):
        scents = {(5, 3, "N")}
        state = RobotState(5, 3, "N")
        result = run_commands(state, "F", 5, 3, scents)
        self.assertFalse(result.lost)
        self.assertEqual((result.x, result.y, result.direction), (5, 3, "N"))

    def test_same_cell_different_direction_should_not_share_scent(self):
        scents = {(5, 3, "N")}
        state = RobotState(5, 3, "E")
        result = run_commands(state, "F", 5, 3, scents)
        self.assertTrue(result.lost)

    def test_ignore_scent_and_continue_following_commands(self):
        scents = {(5, 3, "N")}
        state = RobotState(5, 3, "N")
        result = run_commands(state, "FRF", 5, 3, scents)
        self.assertEqual((result.x, result.y, result.direction, result.lost), (5, 3, "E", True))


if __name__ == "__main__":
    unittest.main()
