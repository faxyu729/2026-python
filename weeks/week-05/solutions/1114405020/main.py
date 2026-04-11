# Big Two Game - Main Entry Point

from ui.app import BigTwoApp


def main():
    print("=" * 60)
    print("    大老二遊戲 - Big Two Card Game")
    print("=" * 60)
    print()
    print("遊戲規則:")
    print("  - 4 位玩家（1 人類，3 個電腦）")
    print("  - 首先出完手牌的玩家獲勝")
    print("  - 遊戲開始時必須出 3 of Clubs")
    print()
    print("出牌規則:")
    print("  - 單張: 任意一張牌")
    print("  - 對子: 相同點數的兩張牌")
    print("  - 三條: 相同點數的三張牌")
    print("  - 順子: 五張連續的牌")
    print("  - 同花: 五張相同花色的牌")
    print("  - 葫蘆: 三張相同點數 + 兩張相同點數")
    print("  - 四條: 四張相同點數 + 一張牌")
    print("  - 同花順: 五張連續的同花牌")
    print()
    print("操作說明:")
    print("  - 點擊牌卡: 選擇/取消選擇牌")
    print("  - Enter 或『出牌』按鈕: 確認出牌")
    print("  - P 或『過牌』按鈕: 過牌")
    print()
    print("=" * 60)
    print()

    try:
        app = BigTwoApp()
        app.run()
    except ImportError as e:
        print(f"Error: {e}")
        print("Please install pygame: pip install pygame")


if __name__ == "__main__":
    main()
