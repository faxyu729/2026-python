"""
大老二遊戲 - 主應用程序
"""

import pygame
from typing import List, Optional
from PIL import Image, ImageDraw, ImageFont
from game.game_p5 import BigTwoGame


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
        self.message = "遊戲已開始！"
        self.message_time = 0
        self.show_rules = False
        self.selected_cards = []

        # 字體
        self.font_large = pygame.font.Font(None, 28)
        self.font_medium = pygame.font.Font(None, 16)
        self.font_small = pygame.font.Font(None, 12)
        
        # 初始化 PIL 字體用於 Unicode 字符
        try:
            # 嘗試使用系統字體來渲染中文和符號
            self.pil_font_large = ImageFont.truetype("arial.ttf", 28)
            self.pil_font_medium = ImageFont.truetype("arial.ttf", 16)
            self.pil_font_small = ImageFont.truetype("arial.ttf", 12)
            self.pil_font_suit = ImageFont.truetype("arial.ttf", 40)
        except:
            # 如果找不到字體，使用預設字體
            self.pil_font_large = ImageFont.load_default()
            self.pil_font_medium = ImageFont.load_default()
            self.pil_font_small = ImageFont.load_default()
            self.pil_font_suit = ImageFont.load_default()

    def pil_render_text(self, text, font, color=(255, 255, 255), bg_color=None):
        """使用 PIL 渲染文本，支援 Unicode 字符"""
        # 建立暫時圖像
        size = font.getbbox(text)
        width = size[2] - size[0] + 4
        height = size[3] - size[1] + 4

        img = Image.new("RGBA", (width, height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)

        # 繪製文本
        draw.text((2, 2), text, font=font, fill=color)

        # 轉換為 pygame 表面
        mode = img.mode
        size = img.size
        data = img.tobytes()

        return pygame.image.fromstring(data, size, mode)

    def run(self):
        """主遊戲迴圈"""
        print("=" * 60)
        print("Big Two Card Game")
        print("=" * 60)
        print("Game window opened! (1050x550)")
        print("\nControls:")
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

            # 更新遊戲邏輯
            self.update()

            # 渲染
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
            card_y = self.screen_height - 140
            card_rect = pygame.Rect(card_x, card_y, 70, 100)
            if card_rect.collidepoint(x, y):
                if card in self.selected_cards:
                    self.selected_cards.remove(card)
                else:
                    self.selected_cards.append(card)
                return

        # 檢查是否點擊了按鈕
        button_y = self.screen_height - 40

        # 出牌按鈕
        if pygame.Rect(240, button_y, 120, 35).collidepoint(x, y):
            self.play_selected_cards()
            return

        # 過牌按鈕
        if pygame.Rect(380, button_y, 120, 35).collidepoint(x, y):
            self.pass_turn()
            return

        # 重新開始按鈕
        if pygame.Rect(530, button_y, 120, 35).collidepoint(x, y):
            self.restart_game()
            return

    def handle_key_press(self, key):
        """處理按鍵"""
        if key == pygame.K_ESCAPE:
            self.running = False
        elif key == pygame.K_r:
            self.show_rules = not self.show_rules
        elif key == pygame.K_RETURN:
            if not self.show_rules:
                self.play_selected_cards()
        elif key == pygame.K_p:
            if not self.show_rules:
                self.pass_turn()

     def play_selected_cards(self):
         """出牌"""
         if not self.selected_cards:
             self.message = "請選擇卡牌！"
             self.message_time = 60
             return

         try:
             success = self.game.play(self.selected_cards)
             if success:
                 self.selected_cards = []
                 self.message = "出牌成功！"
                 self.message_time = 60
             else:
                 self.message = "非法出牌！"
                 self.message_time = 60
         except Exception as e:
             self.message = f"錯誤：{str(e)}"
             self.message_time = 60

     def pass_turn(self):
         """過牌"""
         try:
             self.game.pass_()
             self.selected_cards = []
             self.message = "已跳過"
             self.message_time = 60
         except Exception as e:
             self.message = "跳過失敗"
             self.message_time = 60

    def restart_game(self):
        """重新開始"""
        self.game = BigTwoGame()
        self.game.setup()
        self.selected_cards = []
         self.message = "遊戲已重新開始！"
        self.message_time = 60

    def update(self):
        """更新遊戲狀態"""
        # 更新訊息計時
        if self.message_time > 0:
            self.message_time -= 1
        else:
            self.message = ""

    def render(self):
        """渲染遊戲"""
        self.screen.fill((108, 142, 168))  # 藍灰色背景

        if self.show_rules:
            self.render_rules_page()
        else:
            self.render_game()

        pygame.display.flip()

    def render_game(self):
        """渲染遊戲主畫面"""
        # 左側：規則說明
        self.render_left_panel()

        # 中央：遊戲區
        self.render_center_game()

        # 右側：玩家信息
        self.render_right_panel()

    def render_left_panel(self):
        """左側面板：遊戲規則和操作說明"""
        x_start = 15
        y_start = 50
        line_height = 16

         # 標題
         title_text = "遊戲規則"
         title_surf = self.font_large.render(title_text, True, (255, 255, 100))
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
             "",
             "開始：",
             "持梅花3的玩家先出",
             "",
             "操作：",
             "Enter：出牌",
             "P：跳過",
             "R：規則",
             "ESC：退出",
         ]

        y_offset = y_start + 30
        for rule in rules_text:
            if rule:
                text_surf = self.font_small.render(rule, True, (255, 255, 255))
                self.screen.blit(text_surf, (x_start, y_offset))
            y_offset += line_height

     def render_center_game(self):
         """中央遊戲區域"""
         # 標題
         title_text = "大老二撲克牌遊戲"
         title_surf = self.font_large.render(title_text, True, (255, 255, 255))
         title_x = self.screen_width // 2 - title_surf.get_width() // 2
         self.screen.blit(title_surf, (title_x, 15))

         # 當前玩家
         current_idx = self.game.current_player
         if isinstance(current_idx, int) and 0 <= current_idx < len(self.game.players):
             current = self.game.players[current_idx]
             current_text = f"當前玩家：{current.name}"
             current_surf = self.font_medium.render(current_text, True, (255, 200, 100))
             self.screen.blit(current_surf, (350, 50))

         # 上一輪出牌
         if self.game.last_play:
             last_play_str = "上一輪："
             for card in self.game.last_play:
                 last_play_str += str(card) + " "
             last_text = self.font_small.render(last_play_str, True, (200, 200, 200))
             self.screen.blit(last_text, (350, 80))

        # 玩家手牌
        self.render_player_hand()

        # 按鈕
        self.render_buttons()

        # 訊息
        if self.message:
            self.render_message()

         # 遊戲結束訊息
         if self.game.is_game_over() and self.game.winner:
             winner_text = f"遊戲結束！{self.game.winner.name}獲勝！"
             winner_surf = self.font_large.render(winner_text, True, (255, 200, 100))
             winner_x = self.screen_width // 2 - winner_surf.get_width() // 2
             self.screen.blit(winner_surf, (winner_x, 300))

     def render_right_panel(self):
         """右側面板：其他玩家信息"""
         panel_x = self.screen_width - 190
         y_start = 50

         # 標題
         title = self.font_medium.render("其他玩家", True, (255, 255, 100))
         self.screen.blit(title, (panel_x, y_start))

        # 顯示其他玩家信息
        y_offset = y_start + 40
        current_idx = self.game.current_player

        for i, player in enumerate(self.game.players):
            if i == 0:  # 跳過人類玩家
                continue

             player_info = f"{player.name}：{len(player.hand)}張"

            if isinstance(current_idx, int) and current_idx == i:
                color = (255, 200, 0)
                player_info += " *"
            else:
                color = (255, 255, 255)

            text = self.font_small.render(player_info, True, color)
            self.screen.blit(text, (panel_x, y_offset))
            y_offset += 45

    def render_player_hand(self):
        """渲染玩家手牌"""
        hand = self.game.players[0].hand
        hand_y = self.screen_height - 140
        hand_x_start = 100  # 改為更靠左
        card_spacing = 65  # 減小間距

         # 標籤
         label = self.font_small.render("你的手牌：", True, (255, 255, 100))
         self.screen.blit(label, (hand_x_start, hand_y - 35))

        # 渲染卡牌
        for i, card in enumerate(hand):
            card_x = hand_x_start + i * card_spacing
            is_selected = card in self.selected_cards
            self.draw_card(card, card_x, hand_y, selected=is_selected)

    def draw_card(self, card, x, y, selected=False):
        """繪製卡牌"""
        w, h = 70, 100

        if selected:
            bg_color = (150, 200, 255)  # 淺藍色
        else:
            bg_color = (255, 255, 255)

        # 背景
        rect = pygame.Rect(x, y, w, h)
        pygame.draw.rect(self.screen, bg_color, rect)

        # 花色映射 - 使用真正的符號
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

        # 花色顏色
        if card.suit in [1, 2]:  # 鑽石、紅心
            suit_color = (255, 0, 0)
        else:
            suit_color = (0, 0, 0)

        # 渲染花色 - 使用 PIL 以支援 Unicode
        suit_surf = self.pil_render_text(suit_sym, self.pil_font_suit, color=suit_color)
        suit_rect = suit_surf.get_rect(center=(x + w // 2, y + h // 3))
        self.screen.blit(suit_surf, suit_rect)

        # 渲染點數 - 使用 PIL
        rank_surf = self.pil_render_text(
            rank_sym, self.pil_font_medium, color=(0, 0, 0)
        )
        rank_rect = rank_surf.get_rect(center=(x + w // 2, y + 2 * h // 3))
        self.screen.blit(rank_surf, rank_rect)

    def render_buttons(self):
        """渲染按鈕"""
        button_y = self.screen_height - 40
        button_width = 120
        button_height = 35

         buttons = [
             (240, "出牌(Enter)"),
             (380, "跳過(P)"),
             (530, "重新開始"),
         ]

        for x, label in buttons:
            button_rect = pygame.Rect(x, button_y, button_width, button_height)
            pygame.draw.rect(self.screen, (70, 130, 180), button_rect)

            text = self.font_small.render(label, True, (255, 255, 255))
            text_rect = text.get_rect(center=button_rect.center)
            self.screen.blit(text, text_rect)

    def render_message(self):
        """渲染訊息"""
        text = self.font_medium.render(self.message, True, (255, 200, 100))
        text_x = self.screen_width // 2 - text.get_width() // 2
        text_y = 300

        # 背景框
        bg_rect = pygame.Rect(
            text_x - 10, text_y - 5, text.get_width() + 20, text.get_height() + 10
        )
        pygame.draw.rect(self.screen, (50, 50, 100), bg_rect)

        self.screen.blit(text, (text_x, text_y))

    def render_rules_page(self):
        """渲染規則頁面"""
        # 標題
        title = self.font_large.render("BIG TWO RULES", True, (255, 255, 100))
        self.screen.blit(title, (50, 30))

        rules = [
            "",
            "OBJECTIVE: Be first to empty your hand",
            "",
            "PLAY TYPES:",
            "- Single card",
            "- Pair: 2 cards of same rank",
            "- Three of a kind: 3 cards of same rank",
            "- Bomb: 4 cards of same rank (always wins)",
            "- Straight: 5+ consecutive ranks (3-A only)",
            "- Double Straight: 3+ consecutive pairs",
            "",
            "RANK ORDER: 3<4<5<6<7<8<9<10<J<Q<K<A<2",
            "",
            "GAME FLOW:",
            "- Player with C3 (Club 3) plays first",
            "- Take turns playing cards or pass",
            "- Must beat the last play to play",
            "- If 4 in a row pass, round resets",
            "",
            "SUITS: C=Clubs  D=Diamonds  H=Hearts  S=Spades",
            "",
            "CONTROLS:",
            "- Click cards to select",
            "- Enter or PLAY button: play cards",
            "- P or PASS button: pass your turn",
            "- R key: view rules (ESC to close)",
            "- ESC: quit game",
            "",
            "Press any key or click to return to game",
        ]

        y_offset = 80
        for rule in rules:
            rule_text = self.font_small.render(rule, True, (255, 255, 255))
            self.screen.blit(rule_text, (50, y_offset))
            y_offset += 14
