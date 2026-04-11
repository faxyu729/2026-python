"""
P5 - 遊戲流程
實現 BigTwoGame 類別的遊戲邏輯
"""

from game.models_p1 import Deck, Player, SUIT_SYMBOLS, RANK_SYMBOLS
from game.classifier_p2 import HandClassifier
from game.finder_p3 import HandFinder
from game.ai_p4 import AIStrategy


def format_cards(cards):
    """Format cards for display"""
    suit_names = {0: "C", 1: "D", 2: "H", 3: "S"}  # Clubs, Diamonds, Hearts, Spades
    return ", ".join(
        [f"{RANK_SYMBOLS.get(c.rank, '?')}{suit_names.get(c.suit, '?')}" for c in cards]
    )


class BigTwoGame:
    """大老二遊戲"""

    def __init__(self):
        """初始化遊戲"""
        self.deck = None
        self.players = []
        self.current_player = 0
        self.last_play = None
        self.last_player_name = None
        self.last_player_index = None  # Track who last played
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

        # 列印遊戲開始信息
        print("=" * 60)
        print("Big Two Game Started!")
        print("=" * 60)
        for i, player in enumerate(self.players):
            is_current = " (First Player)" if i == self.current_player else ""
            print(f"Player {i}: {player.name} - {len(player.hand)} cards{is_current}")
        print("=" * 60)
        print()

    def play(self, player_or_cards, cards=None):
        """
        玩家出牌

        Args:
            player_or_cards: 玩家物件 或 要出的牌列表
            cards: 要出的牌 (如果第一個參數是玩家物件)

        Returns:
            bool: 是否成功出牌
        """
        # 處理兩種調用方式: play(player, cards) 或 play(cards)
        if cards is None:
            # play(cards) 模式 - 從當前玩家推斷
            cards = player_or_cards
            player = self.get_current_player()
        else:
            # play(player, cards) 模式
            player = player_or_cards

        if not self._is_valid_play(cards):
            return False

        # 移除手牌
        player.play_cards(cards)

        # 設定為上家出牌
        self.last_play = cards
        self.pass_count = 0

        # 檢查獲勝
        self.check_winner()

        # 列印出牌信息
        cards_display = format_cards(cards)
        print(
            f"[{player.name}] plays: {cards_display} (remaining {len(player.hand)} cards)"
        )

        # 記錄出牌者的名字和索引
        self.last_player_name = player.name
        self.last_player_index = self.current_player

        # 輪到下位
        self.next_turn()

        return True

    def pass_(self, player=None):
        """
        玩家過牌

        Args:
            player: 玩家物件 (可選，不提供則使用當前玩家)

        Returns:
            bool: 是否成功過牌
        """
        if player is None:
            player = self.get_current_player()

        self.pass_count += 1

        # 檢查回合重置
        round_was_reset = self.pass_count >= 3
        self.check_round_reset()

        # 只在回合重置時列印，表示新一輪開始
        if self.pass_count == 0:
            print(f"[{player.name}] passes - New round started!")

        # 輪到下位（但如果剛重置回合，不再跳過，因為已經回到最後出牌者）
        if not round_was_reset:
            self.next_turn()

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
            self.last_player_name = None
            self.pass_count = 0
            # 回到最後出牌者開始新一輪
            self.current_player = self.last_player_index

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
        player = self.get_current_player()
        valid_plays = HandFinder.get_all_valid_plays(player.hand, self.last_play)

        if valid_plays:
            best_play = AIStrategy.select_best(
                valid_plays, player.hand, self.last_play is None
            )
            if best_play:
                return self.play(best_play)

        return self.pass_()
