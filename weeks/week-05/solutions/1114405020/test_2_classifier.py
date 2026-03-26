import unittest
from game.models import Card
from game.classifier import CardType, HandClassifier


class TestCardType(unittest.TestCase):
    """測試 CardType 列舉"""

    def test_cardtype_values(self):
        """測試：CardType 列舉值正確"""
        self.assertEqual(CardType.SINGLE.value, 1)
        self.assertEqual(CardType.PAIR.value, 2)
        self.assertEqual(CardType.TRIPLE.value, 3)
        self.assertEqual(CardType.STRAIGHT.value, 4)
        self.assertEqual(CardType.FLUSH.value, 5)
        self.assertEqual(CardType.FULL_HOUSE.value, 6)
        self.assertEqual(CardType.FOUR_OF_A_KIND.value, 7)
        self.assertEqual(CardType.STRAIGHT_FLUSH.value, 8)


class TestSingleCardClassification(unittest.TestCase):
    """測試單張牌分類"""

    def test_classify_single_ace(self):
        """測試：分類 ♠A"""
        cards = [Card(14, 3)]
        result = HandClassifier.classify(cards)
        self.assertEqual(result, (CardType.SINGLE, 14, 3))

    def test_classify_single_two(self):
        """測試：分類 ♣2"""
        cards = [Card(15, 0)]
        result = HandClassifier.classify(cards)
        self.assertEqual(result, (CardType.SINGLE, 15, 0))

    def test_classify_single_three(self):
        """測試：分類 ♣3"""
        cards = [Card(3, 0)]
        result = HandClassifier.classify(cards)
        self.assertEqual(result, (CardType.SINGLE, 3, 0))


class TestPairClassification(unittest.TestCase):
    """測試對子分類"""

    def test_classify_pair(self):
        """測試：分類對A（♠A,♥A）"""
        cards = [Card(14, 3), Card(14, 2)]
        result = HandClassifier.classify(cards)
        self.assertEqual(result, (CardType.PAIR, 14, 3))

    def test_classify_pair_diff_rank(self):
        """測試：兩張不同數字的牌（♠A,♠K）返回 None"""
        cards = [Card(14, 3), Card(13, 3)]
        result = HandClassifier.classify(cards)
        self.assertIsNone(result)

    def test_classify_pair_from_three(self):
        """測試：從三張牌中提取對子"""
        cards = [Card(14, 3), Card(14, 2), Card(14, 1)]
        # 只取前兩張
        result = HandClassifier.classify(cards[:2])
        self.assertEqual(result, (CardType.PAIR, 14, 3))


class TestTripleClassification(unittest.TestCase):
    """測試三條分類"""

    def test_classify_triple(self):
        """測試：分類三A（♠A,♥A,♦A）"""
        cards = [Card(14, 3), Card(14, 2), Card(14, 1)]
        result = HandClassifier.classify(cards)
        self.assertEqual(result, (CardType.TRIPLE, 14, 3))

    def test_classify_triple_not_enough(self):
        """測試：兩張牌無法構成三條"""
        cards = [Card(14, 3), Card(14, 2)]
        result = HandClassifier.classify(cards)
        # 兩張牌會被分類為對子，不是三條
        self.assertNotEqual(result, (CardType.TRIPLE, 14, 0))


class TestFiveCardClassification(unittest.TestCase):
    """測試五張牌型分類"""

    def test_classify_straight(self):
        """測試：分類順子（3♣,4♦,5♥,6♠,7♣）"""
        cards = [Card(3, 0), Card(4, 1), Card(5, 2), Card(6, 3), Card(7, 0)]
        result = HandClassifier.classify(cards)
        self.assertEqual(result, (CardType.STRAIGHT, 7, 0))

    def test_classify_straight_ace_low(self):
        """測試：分類低順（A♣,2♦,3♥,4♠,5♣）- A當1"""
        cards = [Card(14, 0), Card(15, 1), Card(3, 2), Card(4, 3), Card(5, 0)]
        result = HandClassifier.classify(cards)
        # 修正：此牌型應該是 (STRAIGHT, 5, 0)，而不是用 A 的值
        self.assertEqual(result, (CardType.STRAIGHT, 5, 0))

    def test_classify_flush(self):
        """測試：分類同花（♣3,♣5,♣7,♣9,♣J）"""
        cards = [Card(3, 0), Card(5, 0), Card(7, 0), Card(9, 0), Card(11, 0)]
        result = HandClassifier.classify(cards)
        self.assertEqual(result, (CardType.FLUSH, 11, 0))

    def test_classify_full_house(self):
        """測試：分類葫蘆（♠A,♥A,♦A,♣2,♦2）"""
        cards = [Card(14, 3), Card(14, 2), Card(14, 1), Card(15, 0), Card(15, 1)]
        result = HandClassifier.classify(cards)
        self.assertEqual(result, (CardType.FULL_HOUSE, 14, 0))

    def test_classify_four_of_a_kind(self):
        """測試：分類四條（♠A,♥A,♦A,♣A,♦3）"""
        cards = [Card(14, 3), Card(14, 2), Card(14, 1), Card(14, 0), Card(3, 1)]
        result = HandClassifier.classify(cards)
        self.assertEqual(result, (CardType.FOUR_OF_A_KIND, 14, 0))

    def test_classify_straight_flush(self):
        """測試：分類順子同花（♣3,♣4,♣5,♣6,♣7）"""
        cards = [Card(3, 0), Card(4, 0), Card(5, 0), Card(6, 0), Card(7, 0)]
        result = HandClassifier.classify(cards)
        self.assertEqual(result, (CardType.STRAIGHT_FLUSH, 7, 0))


class TestHandComparison(unittest.TestCase):
    """測試牌型比較"""

    def test_compare_single_rank(self):
        """測試：單張比較 - ♠A vs ♠K"""
        play1 = [Card(14, 3)]
        play2 = [Card(13, 3)]
        result = HandClassifier.compare(play1, play2)
        self.assertEqual(result, 1)

    def test_compare_single_suit(self):
        """測試：單張比較 - ♠A vs ♥A（同數字比花色）"""
        play1 = [Card(14, 3)]
        play2 = [Card(14, 2)]
        result = HandClassifier.compare(play1, play2)
        self.assertEqual(result, 1)

    def test_compare_pair_rank(self):
        """測試：對子比較 - 對A vs 對K"""
        play1 = [Card(14, 3), Card(14, 2)]
        play2 = [Card(13, 3), Card(13, 2)]
        result = HandClassifier.compare(play1, play2)
        self.assertEqual(result, 1)

    def test_compare_pair_suit(self):
        """測試：對子比較 - (♠♥A) vs (♦♣A)"""
        play1 = [Card(14, 3), Card(14, 2)]
        play2 = [Card(14, 1), Card(14, 0)]
        result = HandClassifier.compare(play1, play2)
        self.assertEqual(result, 1)

    def test_compare_different_type(self):
        """測試：不同牌型比較 - 對子 vs 單張"""
        play1 = [Card(5, 3), Card(5, 2)]
        play2 = [Card(14, 3)]
        result = HandClassifier.compare(play1, play2)
        self.assertEqual(result, 1)

    def test_compare_flush_vs_straight(self):
        """測試：不同五張牌型比較 - 同花 vs 順子"""
        play1 = [Card(3, 0), Card(5, 0), Card(7, 0), Card(9, 0), Card(11, 0)]
        play2 = [Card(3, 0), Card(4, 1), Card(5, 2), Card(6, 3), Card(7, 0)]
        result = HandClassifier.compare(play1, play2)
        self.assertEqual(result, 1)

    def test_compare_equal(self):
        """測試：相同牌型比較"""
        play1 = [Card(14, 3)]
        play2 = [Card(14, 3)]
        result = HandClassifier.compare(play1, play2)
        self.assertEqual(result, 0)


class TestLegality(unittest.TestCase):
    """測試合法性檢查"""

    def test_can_play_first_3clubs(self):
        """測試：第一張牌必須是 ♣3"""
        cards = [Card(3, 0)]
        can_play = HandClassifier.can_play(None, cards)
        self.assertTrue(can_play)

    def test_can_play_first_not_3clubs(self):
        """測試：第一張牌不是 ♣3 不合法"""
        cards = [Card(14, 3)]
        can_play = HandClassifier.can_play(None, cards)
        self.assertFalse(can_play)

    def test_can_play_same_type_stronger(self):
        """測試：同牌型且更強可以出牌"""
        last = [Card(5, 3), Card(5, 2)]
        current = [Card(6, 3), Card(6, 2)]
        can_play = HandClassifier.can_play(last, current)
        self.assertTrue(can_play)

    def test_can_play_same_type_weaker(self):
        """測試：同牌型但較弱不能出牌"""
        last = [Card(10, 3), Card(10, 2)]
        current = [Card(5, 3), Card(5, 2)]
        can_play = HandClassifier.can_play(last, current)
        self.assertFalse(can_play)

    def test_can_play_diff_type(self):
        """測試：不同牌型不能出牌"""
        last = [Card(5, 3), Card(5, 2)]
        current = [Card(6, 3)]
        can_play = HandClassifier.can_play(last, current)
        self.assertFalse(can_play)


if __name__ == "__main__":
    unittest.main(verbosity=2)
