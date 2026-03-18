import unittest
from solution_948 import solve


class TestFakeCoin(unittest.TestCase):
    """
    這是一個針對「找出假幣」問題的單元測試。
    測試目標為驗證解題函式的正確性，確保各種邊界情況及一般情況下都能正確返回結果。
    """

    def test_single_fake_lighter(self):
        # 假設 1 號是較輕的假幣
        # 天平測試: 左邊 [1] 右邊 [2]，結果為 '<' (1比2輕)
        # 天平測試: 左邊 [2] 右邊 [3]，結果為 '=' (2跟3一樣重)
        weighings = [(1, [1], [2], "<"), (1, [2], [3], "=")]
        self.assertEqual(solve(3, 2, weighings), 1)

    def test_single_fake_heavier(self):
        # 假設 3 號是較重的假幣
        # 左邊 [1] 右邊 [3]，結果為 '<' (1比3輕)
        # 左邊 [1] 右邊 [2]，結果為 '=' (1跟2一樣重)
        weighings = [(1, [1], [3], "<"), (1, [1], [2], "=")]
        self.assertEqual(solve(3, 2, weighings), 3)

    def test_cannot_determine(self):
        # 測試無法確定的情況
        # 如果只有 3 枚硬幣，只秤了一次且結果為 '=' (1和2一樣重)
        # 則 3 號最有可能是假幣，但不知道它是輕還是重。
        # 根據題目，若是能明確找出是哪一枚（即使不知輕重）也應該返回。
        # 等等，如果 1=2，3 可能是較輕或較重，總共就只有 3 是假幣。
        # 但如果有 4 枚硬幣，1=2，那 3 和 4 都有可能，就無法確定。
        weighings = [(1, [1], [2], "=")]
        # N=4, 無法確定是 3 還是 4
        self.assertEqual(solve(4, 1, weighings), 0)
        # N=3, 假幣一定是 3 (雖然不知道輕重，但只有它沒秤過)
        self.assertEqual(solve(3, 1, weighings), 3)

    def test_multiple_inequalities(self):
        # 多次不平衡秤重
        # 5枚硬幣，1號較輕
        # [1, 2] < [3, 4]
        # [1, 3] < [2, 5]
        # 交集：1 必須在較輕的左邊 (因為兩次都在左邊且小於)
        weighings = [(2, [1, 2], [3, 4], "<"), (2, [1, 3], [2, 5], "<")]
        self.assertEqual(solve(5, 2, weighings), 1)


if __name__ == "__main__":
    # 執行測試並保留紀錄
    with open("test_record_948.log", "w", encoding="utf-8") as f:
        runner = unittest.TextTestRunner(stream=f, verbosity=2)
        unittest.main(argv=[""], testRunner=runner, exit=False)
