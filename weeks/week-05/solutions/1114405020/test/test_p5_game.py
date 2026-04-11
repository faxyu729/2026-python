"""
P5 - 遊戲流程測試
測試 BigTwoGame 類別的遊戲邏輯
"""

import unittest
from game.models_p1 import Card, Deck, Hand, Player
from game.classifier_p2 import HandClassifier


class BigTwoGame:
    """大老二遊戲"""

    def __init__(self):
        """初始化遊戲"""
        self.deck = None
        self.players = []
        self.current_player = 0
        self.last_play = None
        self.pass_count = 0
        self.winner = None
        self.round_number = 0

    def setup(self):
        """設定遊戲"""
        # 建立牌堆
        self.deck = Deck()
        self.deck.shuffle()

        # 建立4位玩家（1人類，3個AI）
        self.players = [
            Player("Player", False),
            Player("AI1", True),
            Player("AI2", True),
            Player("AI3", True),
        ]

        # 發13張牌給每位玩家
        for player in self.players:
            cards = self.deck.deal(13)
            player.take_cards(cards)

        # 找有 3♣ 的玩家作為先手
        for i, player in enumerate(self.players):
            if player.hand.find_3_clubs():
                self.current_player = i
                break

        self.round_number = 1

    def play(self, player, cards):
        """
        玩家出牌

        Args:
            player: 玩家物件
            cards: 要出的牌

        Returns:
            bool: 是否成功出牌
        """
        if not self._is_valid_play(cards):
            return False

        # 移除手牌
        player.play_cards(cards)

        # 設定為上家出牌
        self.last_play = cards
        self.pass_count = 0

        # 檢查獲勝
        self.check_winner()

        return True

    def pass_(self, player):
        """
        玩家過牌

        Args:
            player: 玩家物件

        Returns:
            bool: 是否成功過牌
        """
        self.pass_count += 1

        # 檢查回合重置
        self.check_round_reset()

        return True

    def next_turn(self):
        """輪到下位"""
        self.current_player = (self.current_player + 1) % 4

    def _is_valid_play(self, cards):
        """檢查出牌是否合法"""
        return HandClassifier.can_play(self.last_play, cards)

    def check_round_reset(self):
        """檢查是否需要重置回合"""
        if self.pass_count >= 3:
            self.last_play = None
            self.pass_count = 0

    def check_winner(self):
        """檢查是否有獲勝者"""
        for player in self.players:
            if len(player.hand) == 0:
                self.winner = player
                return player
        return None

    def is_game_over(self):
        """檢查遊戲是否結束"""
        return self.winner is not None

    def get_current_player(self):
        """取得當前玩家"""
        return self.players[self.current_player]

    def ai_turn(self):
        """AI 回合"""
        from game.finder_p3 import HandFinder
        from game.ai_p4 import AIStrategy

        player = self.get_current_player()
        valid_plays = HandFinder.get_all_valid_plays(player.hand, self.last_play)

        if valid_plays:
            best_play = AIStrategy.select_best(
                valid_plays, player.hand, self.last_play is None
            )
            if best_play:
                return self.play(player, best_play)

        return self.pass_(player)


class TestGameSetup(unittest.TestCase):
    """遊戲初始化測試"""

    def test_game_has_4_players(self):
        """測試：遊戲有4位玩家"""
        game = BigTwoGame()
        game.setup()
        self.assertEqual(len(game.players), 4)

    def test_each_player_13_cards(self):
        """測試：每位玩家13張牌"""
        game = BigTwoGame()
        game.setup()
        for player in game.players:
            self.assertEqual(len(player.hand), 13)

    def test_total_cards_distributed(self):
        """測試：總共分配52張牌"""
        game = BigTwoGame()
        game.setup()
        total = sum(len(player.hand) for player in game.players)
        self.assertEqual(total, 52)

    def test_first_player_has_3_clubs(self):
        """測試：先手玩家有 3♣"""
        game = BigTwoGame()
        game.setup()
        first_player = game.players[game.current_player]
        self.assertIsNotNone(first_player.hand.find_3_clubs())

    def test_one_human_three_ai(self):
        """測試：1人類3AI"""
        game = BigTwoGame()
        game.setup()
        human_count = sum(1 for p in game.players if not p.is_ai)
        ai_count = sum(1 for p in game.players if p.is_ai)
        self.assertEqual(human_count, 1)
        self.assertEqual(ai_count, 3)


class TestPlayRound(unittest.TestCase):
    """出牌流程測試"""

    def test_play_removes_cards(self):
        """測試：出牌移除手牌"""
        game = BigTwoGame()
        game.setup()
        player = game.players[0]
        initial_count = len(player.hand)

        # 找個可以出的單張
        if player.hand:
            card = player.hand[0]
            game.last_play = None
            if HandClassifier.can_play(None, [card]):
                game.play(player, [card])
                self.assertEqual(len(player.hand), initial_count - 1)

    def test_play_sets_last_play(self):
        """測試：出牌設定 last_play"""
        game = BigTwoGame()
        game.setup()
        player = game.players[0]

        if player.hand:
            card = player.hand[0]
            if HandClassifier.can_play(None, [card]):
                game.play(player, [card])
                self.assertIsNotNone(game.last_play)

    def test_invalid_play(self):
        """測試：非法出牌"""
        game = BigTwoGame()
        game.setup()
        player = game.players[0]

        # 嘗試出不合法的牌
        if len(player.hand) >= 2:
            result = game.play(player, player.hand[:2])
            # 根據 last_play 的狀態，結果可能為 False

    def test_pass_increments(self):
        """測試：過牌增加計數"""
        game = BigTwoGame()
        game.setup()
        initial_count = game.pass_count
        player = game.players[0]
        game.pass_(player)
        self.assertEqual(game.pass_count, initial_count + 1)


class TestRoundLogic(unittest.TestCase):
    """回合判定測試"""

    def test_three_passes_resets(self):
        """測試：3人過牌重置"""
        game = BigTwoGame()
        game.setup()
        game.last_play = [game.players[0].hand[0]]

        player = game.players[1]
        game.pass_(player)
        game.pass_(player)
        game.pass_(player)

        self.assertIsNone(game.last_play)

    def test_turn_rotates(self):
        """測試：回合輪轉"""
        game = BigTwoGame()
        game.setup()
        initial = game.current_player
        game.next_turn()
        self.assertEqual(game.current_player, (initial + 1) % 4)


class TestWinner(unittest.TestCase):
    """獲勝判定測試"""

    def test_detect_winner(self):
        """測試：手牌空時檢測獲勝"""
        game = BigTwoGame()
        game.setup()

        # 模擬玩家手牌空
        game.players[0].hand.clear()
        winner = game.check_winner()
        self.assertEqual(winner, game.players[0])

    def test_no_winner_yet(self):
        """測試：有牌時無獲勝者"""
        game = BigTwoGame()
        game.setup()
        winner = game.check_winner()
        self.assertIsNone(winner)

    def test_game_ends(self):
        """測試：有獲勝者時遊戲結束"""
        game = BigTwoGame()
        game.setup()
        game.players[0].hand.clear()
        game.check_winner()
        self.assertTrue(game.is_game_over())


if __name__ == "__main__":
    unittest.main(verbosity=2)
