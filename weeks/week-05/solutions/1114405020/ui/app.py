"""
大老二遊戲 - 主應用程序
"""

import pygame
from typing import List, Optional
from game.game_p5 import BigTwoGame

# 嘗試導入 PIL，如果不可用則使用純 pygame 渲染
try:
    from PIL import Image, ImageDraw, ImageFont

    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False


class BigTwoApp:
    """大老二遊戲應用程序"""

    def __init__(self):
        """初始化應用程序"""
        pygame.init()

        self.screen_width = 1050
        self.screen_height = 550
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("大老二 - 撲克牌遊戲")
        self.clock = pygame.time.Clock()

        self.game = BigTwoGame()
        self.game.setup()

        self.running = True
        self.selected_cards = []
        self.message = ""
        self.message_time = 0
        self.show_rules = False
        self.ai_move_delay = 0  # Add delay for AI moves

        # 字體 - pygame 字體用於ASCII字符
        self.font_large = pygame.font.Font(None, 36)
        self.font_medium = pygame.font.Font(None, 22)
        self.font_small = pygame.font.Font(None, 16)

        # 嘗試加載中文字體
        self.font_chinese_large = None
        self.font_chinese_medium = None
        self.font_chinese_small = None
        self.font_chinese_tiny = None
        self.font_chinese_suit = None

        # Arial font for suit symbols (Arial supports Unicode suit symbols)
        self.font_suit_arial = pygame.font.SysFont("arial", 24)
        self.font_suit_arial_small = pygame.font.SysFont("arial", 12)

        try:
            # 使用 SimSun 字體用於中文
            font_path = "C:\\Windows\\Fonts\\SimSun.ttc"
            self.font_chinese_large = pygame.font.Font(font_path, 32)
            self.font_chinese_medium = pygame.font.Font(font_path, 20)
            self.font_chinese_small = pygame.font.Font(font_path, 16)
            self.font_chinese_tiny = pygame.font.Font(font_path, 12)
            self.font_chinese_suit = pygame.font.Font(font_path, 24)
        except:
            # 如果加载失败，使用默認字體
            pass

        # 初始化 PIL 字體用於 Unicode 字符（备用）
        self.pil_font_large = None
        self.pil_font_medium = None
        self.pil_font_small = None
        self.pil_font_suit = None

        if PIL_AVAILABLE:
            try:
                # 嘗試使用中文字體（宋體）
                font_path = "C:\\Windows\\Fonts\\SimSun.ttc"
                try:
                    self.pil_font_large = ImageFont.truetype(font_path, 36)
                    self.pil_font_medium = ImageFont.truetype(font_path, 22)
                    self.pil_font_small = ImageFont.truetype(font_path, 16)
                    self.pil_font_suit = ImageFont.truetype(font_path, 56)
                except:
                    # 回退到Arial
                    font_path = "C:\\Windows\\Fonts\\arial.ttf"
                    self.pil_font_large = ImageFont.truetype(font_path, 36)
                    self.pil_font_medium = ImageFont.truetype(font_path, 22)
                    self.pil_font_small = ImageFont.truetype(font_path, 16)
                    self.pil_font_suit = ImageFont.truetype(font_path, 56)
            except:
                try:
                    # 回退到預設字體
                    self.pil_font_large = ImageFont.load_default()
                    self.pil_font_medium = ImageFont.load_default()
                    self.pil_font_small = ImageFont.load_default()
                    self.pil_font_suit = ImageFont.load_default()
                except:
                    pass

    def format_cards_for_display(self, cards):
        """Format cards with suit symbols for display"""
        suit_symbols = {0: "♣", 1: "♦", 2: "♥", 3: "♠"}
        rank_names = {
            3: "3",
            4: "4",
            5: "5",
            6: "6",
            7: "7",
            8: "8",
            9: "9",
            10: "10",
            11: "J",
            12: "Q",
            13: "K",
            14: "A",
            15: "2",
        }
        return " ".join(
            [
                f"{rank_names.get(c.rank, '?')}{suit_symbols.get(c.suit, '?')}"
                for c in cards
            ]
        )

    def pil_render_text(self, text, font, color=(255, 255, 255)):
        """使用適當的字體渲染文本，優先使用 pygame 中文字體"""
        # 檢查是否包含花色符號
        has_suit_symbols = any(c in "♣♦♥♠" for c in text)

        # 如果包含花色符號，需要用不同的方式處理
        if has_suit_symbols:
            # 用 pygame Arial 字體直接渲染（支持 Unicode）
            if self.font_suit_arial:
                try:
                    return self.font_suit_arial.render(text, True, color)
                except:
                    pass

        # 首先嘗試用 pygame 中文字體
        if self.font_chinese_large is not None:
            # 檢查是否是中文
            has_chinese = any(ord(c) > 0x4E00 for c in text)
            if has_chinese:
                # 根據字體大小選擇合適的 pygame 中文字體
                if font == self.pil_font_large:
                    return self.font_chinese_large.render(text, True, color)
                elif font == self.pil_font_medium:
                    return self.font_chinese_medium.render(text, True, color)
                elif font == self.pil_font_small:
                    return self.font_chinese_small.render(text, True, color)

        # 使用 PIL 渲染（如果可用）
        if PIL_AVAILABLE and font:
            try:
                pil_image = Image.new("RGBA", (300, 50), (0, 0, 0, 0))
                draw = ImageDraw.Draw(pil_image)
                draw.text((0, 0), text, font=font, fill=color)

                # 轉換為 pygame Surface
                mode = pil_image.mode
                size = pil_image.size
                data = pil_image.tobytes()
                return pygame.image.fromstring(data, size, mode)
            except:
                pass

        # 最後回退到預設渲染
        return self.font_large.render(text, True, color)

    def run(self):
        """運行遊戲"""
        print("=" * 60)
        print("    大老二 - 撲克牌遊戲")
        print("=" * 60)
        print()
        print("Controls:")
        print("  • Click card to select")
        print("  • Enter or 'Play' button: play cards")
        print("  • P or 'Pass' button: pass")
        print("  • R key: view rules")
        print("  • ESC: quit")
        print("=" * 60 + "\n")

        while self.running and not self.game.is_game_over():
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_mouse_click(event.pos)
                elif event.type == pygame.KEYDOWN:
                    self.handle_key_press(event.key)

            self.update()
            self.render()
            self.clock.tick(30)

        pygame.quit()
        if self.game.winner:
            print(f"\nGame Over! {self.game.winner.name} wins!")
        print("Thank you for playing!")

    def handle_mouse_click(self, pos):
        """處理滑鼠點擊"""
        x, y = pos

        if self.show_rules:
            self.show_rules = False
            return

        # 檢查是否點擊了卡牌
        hand = self.game.players[0].hand
        for i, card in enumerate(hand):
            card_x = 100 + i * 65
            card_y = self.screen_height - 180
            card_rect = pygame.Rect(card_x, card_y, 70, 100)
            if card_rect.collidepoint(x, y):
                if card in self.selected_cards:
                    self.selected_cards.remove(card)
                else:
                    self.selected_cards.append(card)
                return

        # 檢查是否點擊了按鈕
        button_y = self.screen_height - 45

        # 出牌按鈕
        if pygame.Rect(220, button_y, 140, 40).collidepoint(x, y):
            self.play_selected_cards()
            return

        # 跳過按鈕
        if pygame.Rect(380, button_y, 140, 40).collidepoint(x, y):
            self.pass_turn()
            return

        # 重新開始按鈕
        if pygame.Rect(540, button_y, 140, 40).collidepoint(x, y):
            self.restart_game()
            return

    def handle_key_press(self, key):
        """處理鍵盤按鍵"""
        if key == pygame.K_ESCAPE:
            self.running = False
        elif key == pygame.K_RETURN:
            if not self.show_rules:
                self.play_selected_cards()
        elif key == pygame.K_r:
            self.show_rules = not self.show_rules
        elif key == pygame.K_p:
            if not self.show_rules:
                self.pass_turn()

    def play_selected_cards(self):
        """出牌"""
        if not self.selected_cards:
            self.message = "請選擇卡牌！"
            self.message_time = 30
            return

        current_idx = self.game.current_player
        if current_idx != 0:
            self.message = "現在不是您的回合！"
            self.message_time = 30
            return

        self.game.play(self.selected_cards)
        self.selected_cards = []
        self.message = ""

    def pass_turn(self):
        """跳過"""
        current_idx = self.game.current_player
        if current_idx != 0:
            self.message = "現在不是您的回合！"
            self.message_time = 30
            return

        self.game.pass_()
        self.selected_cards = []
        self.message = ""

    def restart_game(self):
        """重新開始"""
        self.game = BigTwoGame()
        self.game.setup()
        self.selected_cards = []
        self.message = "遊戲已重新開始！"
        self.message_time = 60

    def update(self):
        """更新遊戲狀態"""
        if self.message_time > 0:
            self.message_time -= 1
        else:
            self.message = ""

        # Handle AI player turns with delay
        if self.ai_move_delay > 0:
            self.ai_move_delay -= 1
        else:
            current_idx = self.game.current_player
            if isinstance(current_idx, int) and 0 <= current_idx < len(
                self.game.players
            ):
                # If it's not the human player (player 0), let AI make a move
                if current_idx != 0:
                    self.game.ai_turn()
                    self.ai_move_delay = 30  # Add 1 second delay (30 frames at 30 FPS)

    def render(self):
        """渲染遊戲"""
        self.screen.fill((108, 142, 168))

        if self.show_rules:
            self.render_rules_page()
        else:
            self.render_game()

        pygame.display.flip()

    def render_game(self):
        """渲染遊戲主畫面"""
        self.render_left_panel()
        self.render_center_game()
        self.render_right_panel()

    def render_left_panel(self):
        """左側面板：遊戲規則"""
        x_start = 15
        y_start = 50
        line_height = 18

        title_text = "遊戲規則"
        title_surf = self.pil_render_text(
            title_text, self.pil_font_large, (255, 255, 100)
        )
        self.screen.blit(title_surf, (x_start, y_start))

        rules_text = [
            "",
            "出牌類型：",
            "- 單張",
            "- 對子（2張）",
            "- 三條",
            "- 炸彈（4張）",
            "- 順子（5+張）",
            "- 雙順（3+對）",
            "",
            "牌級順序：",
            "3<4<5<6<7<8<9<10",
            "<J<Q<K<A<2",
        ]

        y_offset = y_start + 40
        for rule in rules_text:
            if rule:
                # 使用较小的字体来节省空间
                if self.font_chinese_tiny is not None:
                    text_surf = self.font_chinese_tiny.render(
                        rule, True, (255, 255, 255)
                    )
                else:
                    text_surf = self.pil_render_text(
                        rule, self.pil_font_small, (255, 255, 255)
                    )
                self.screen.blit(text_surf, (x_start, y_offset))
            y_offset += line_height

    def render_center_game(self):
        """中央遊戲區域"""
        title_text = "大老二撲克牌遊戲"
        title_surf = self.pil_render_text(
            title_text, self.pil_font_large, (255, 255, 255)
        )
        title_x = self.screen_width // 2 - title_surf.get_width() // 2
        self.screen.blit(title_surf, (title_x, 15))

        # Current player info
        current_idx = self.game.current_player
        if isinstance(current_idx, int) and 0 <= current_idx < len(self.game.players):
            current = self.game.players[current_idx]
            current_text = f"Current: {current.name}"
            current_surf = self.pil_render_text(
                current_text, self.pil_font_medium, (255, 200, 100)
            )
            self.screen.blit(current_surf, (350, 50))

        # Last play info with card display
        if self.game.last_play:
            last_play_display = self.format_cards_for_display(self.game.last_play)
            last_play_str = f"Last play: {last_play_display}"
            last_text = self.pil_render_text(
                last_play_str, self.pil_font_small, (200, 200, 200)
            )
            self.screen.blit(last_text, (350, 80))

            # Show who played it
            if hasattr(self.game, "last_player_name"):
                who_played = f"by {self.game.last_player_name}"
                who_text = self.pil_render_text(
                    who_played, self.pil_font_small, (180, 180, 180)
                )
                self.screen.blit(who_text, (350, 100))
        else:
            no_play_text = self.pil_render_text(
                "Last play: None (new round)", self.pil_font_small, (180, 180, 180)
            )
            self.screen.blit(no_play_text, (350, 80))

        # Pass count info
        pass_count_text = f"Passes: {self.game.pass_count}/3"
        pass_text = self.pil_render_text(
            pass_count_text, self.pil_font_small, (200, 150, 150)
        )
        self.screen.blit(pass_text, (350, 120))

        self.render_player_hand()
        self.render_buttons()

        if self.message:
            self.render_message()

        if self.game.is_game_over() and self.game.winner:
            winner_text = f"Game Over! {self.game.winner.name} wins!"
            winner_surf = self.pil_render_text(
                winner_text, self.pil_font_large, (255, 200, 100)
            )
            winner_x = self.screen_width // 2 - winner_surf.get_width() // 2
            self.screen.blit(winner_surf, (winner_x, 300))

    def render_right_panel(self):
        """右側面板：其他玩家"""
        panel_x = self.screen_width - 190
        y_start = 50

        title = self.pil_render_text("Players", self.pil_font_medium, (255, 255, 100))
        self.screen.blit(title, (panel_x, y_start))

        y_offset = y_start + 40
        current_idx = self.game.current_player

        for i, player in enumerate(self.game.players):
            # Display all players
            player_info = f"{player.name}: {len(player.hand)} cards"

            if isinstance(current_idx, int) and current_idx == i:
                color = (255, 200, 0)
                player_info += " *"  # Mark current player
            else:
                color = (255, 255, 255)

            text = self.pil_render_text(player_info, self.pil_font_small, color)
            self.screen.blit(text, (panel_x, y_offset))
            y_offset += 30

    def render_player_hand(self):
        """渲染玩家手牌"""
        hand = self.game.players[0].hand
        hand_y = self.screen_height - 180
        hand_x_start = 100
        card_spacing = 65

        label = self.pil_render_text("你的手牌:", self.pil_font_small, (255, 255, 100))
        self.screen.blit(label, (hand_x_start, hand_y - 35))

        for i, card in enumerate(hand):
            card_x = hand_x_start + i * card_spacing
            is_selected = card in self.selected_cards
            self.draw_card(card, card_x, hand_y, selected=is_selected)

    def draw_card(self, card, x, y, selected=False):
        """繪製卡牌"""
        w, h = 70, 100

        if selected:
            bg_color = (150, 200, 255)
        else:
            bg_color = (255, 255, 255)

        rect = pygame.Rect(x, y, w, h)
        pygame.draw.rect(self.screen, bg_color, rect)
        pygame.draw.rect(self.screen, (0, 0, 0), rect, 2)

        suit_map = {0: "♣", 1: "♦", 2: "♥", 3: "♠"}
        rank_map = {
            2: "3",
            3: "4",
            4: "5",
            5: "6",
            6: "7",
            7: "8",
            8: "9",
            9: "10",
            10: "J",
            11: "Q",
            12: "K",
            13: "A",
            14: "A",
            15: "2",
        }

        suit_sym = suit_map.get(card.suit, "?")
        rank_sym = rank_map.get(card.rank, "?")

        if card.suit in [1, 2]:
            suit_color = (255, 0, 0)
        else:
            suit_color = (0, 0, 0)

        # 花色符號（上）- 使用 Arial 字體（支持 Unicode 花色符號）
        suit_surf = self.font_suit_arial.render(suit_sym, True, suit_color)
        suit_rect = suit_surf.get_rect(topleft=(x + 3, y + 3))
        self.screen.blit(suit_surf, suit_rect)

        # 點數（中）- 使用 pygame 字体
        rank_surf = self.font_chinese_medium.render(rank_sym, True, (0, 0, 0))
        rank_rect = rank_surf.get_rect(center=(x + w // 2, y + h // 2))
        self.screen.blit(rank_surf, rank_rect)

        # 花色符號（下）- 使用 Arial 字體（支持 Unicode 花色符號）
        suit_surf_small = self.font_suit_arial_small.render(suit_sym, True, suit_color)
        # Position from bottom-right but keep inside card bounds (70 wide x 100 tall)
        suit_rect_small = suit_surf_small.get_rect(bottomright=(x + w - 8, y + h - 5))
        self.screen.blit(suit_surf_small, suit_rect_small)

    def render_buttons(self):
        """渲染按鈕"""
        button_y = self.screen_height - 45
        button_width = 140
        button_height = 40

        buttons = [
            (220, "出牌(Enter)"),
            (380, "跳過(P)"),
            (540, "重新開始"),
        ]

        for x, label in buttons:
            button_rect = pygame.Rect(x, button_y, button_width, button_height)
            pygame.draw.rect(self.screen, (70, 130, 180), button_rect)
            pygame.draw.rect(self.screen, (255, 255, 255), button_rect, 2)

            # 使用更小的字体
            if self.font_chinese_tiny is not None:
                text = self.font_chinese_tiny.render(label, True, (255, 255, 255))
            else:
                text = self.pil_render_text(label, self.pil_font_small, (255, 255, 255))

            text_rect = text.get_rect(
                center=(x + button_width // 2, button_y + button_height // 2)
            )
            self.screen.blit(text, text_rect)

    def render_message(self):
        """渲染消息"""
        if not self.message:
            return

        msg_surf = self.pil_render_text(
            self.message, self.pil_font_small, (255, 100, 100)
        )
        msg_x = self.screen_width // 2 - msg_surf.get_width() // 2
        self.screen.blit(msg_surf, (msg_x, 250))

    def render_rules_page(self):
        """渲染規則頁面"""
        self.screen.fill((108, 142, 168))

        title = self.pil_render_text("遊戲規則", self.pil_font_large, (255, 255, 100))
        title_x = self.screen_width // 2 - title.get_width() // 2
        self.screen.blit(title, (title_x, 20))

        rules = [
            "遊戲目標：最快清空手牌的玩家獲勝",
            "",
            "出牌規則：",
            "1. 持有梅花3的玩家先出",
            "2. 可以出單張、對子、三條、炸彈（4張相同）、順子、雙順",
            "3. 每次出牌必須比上一輪更大",
            "4. 如果無法出更大的牌，可以跳過",
            "5. 當所有玩家都跳過時，出牌者開始新的一輪",
            "",
            "牌級順序（從小到大）：",
            "3 < 4 < 5 < 6 < 7 < 8 < 9 < 10 < J < Q < K < A < 2",
            "",
            "特殊規則：",
            "- 炸彈（4張相同的牌）可以打任何牌型",
            "- 雙2是最大的組合",
            "",
            "按 ESC 返回遊戲",
        ]

        y_offset = 70
        for rule in rules:
            if rule:
                rule_surf = self.pil_render_text(
                    rule, self.pil_font_small, (255, 255, 255)
                )
                x = (self.screen_width - rule_surf.get_width()) // 2
                self.screen.blit(rule_surf, (x, y_offset))
            y_offset += 26
