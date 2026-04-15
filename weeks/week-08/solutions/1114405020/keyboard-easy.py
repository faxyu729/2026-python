"""
鍵盤解碼 (Keyboard Decode) - 簡易版本

簡化說明：
建立鍵盤映射表，通過索引位移進行解碼
"""

# QWERTY 鍵盤佈局
KEYBOARD = "`1234567890-=qwertyuiop[]\\asdfghjkl;'zxcvbnm,./"


def decode_character_easy(encrypted_char):
    """
    解碼單個字符

    簡易思路：
    1. 在鍵盤字符串中找到加密字符的位置
    2. 將位置向左移動 3 位
    3. 返回新位置的字符

    參數：
        encrypted_char: 加密字符

    返回值：
        解碼後的字符，如果無法解碼則返回 '?'
    """

    # 轉小寫以支持大寫字母
    char = encrypted_char.lower()

    # 在鍵盤中查找字符位置
    if char in KEYBOARD:
        encrypted_index = KEYBOARD.index(char)

        # 向左移動 3 位
        original_index = encrypted_index - 3

        # 檢查新位置是否有效
        if 0 <= original_index < len(KEYBOARD):
            return KEYBOARD[original_index]
        else:
            # 超出範圍無法解碼
            return "?"
    else:
        # 非鍵盤字符（如空格）保留原樣
        return encrypted_char


def decode_text_easy(encrypted_text):
    """
    解碼整個文本

    參數：
        encrypted_text: 加密的文本

    返回值：
        解碼後的文本
    """
    decoded = []

    for char in encrypted_text:
        decoded.append(decode_character_easy(char))

    return "".join(decoded)


# 簡易測試
if __name__ == "__main__":
    print("=== 鍵盤解碼簡易版本測試 ===\n")

    print("QWERTY 鍵盤佈局：")
    print("第一排：` 1 2 3 4 5 6 7 8 9 0 - =")
    print("第二排：q w e r t y u i o p [ ] \\")
    print("第三排：a s d f g h j k l ; '")
    print("第四排：z x c v b n m , . /")
    print(f"總計 {len(KEYBOARD)} 個按鍵\n")

    print("解碼原理：")
    print("- 加密：手向右偏移 3 個按鍵，所以打出的字符比原字符靠右 3 位")
    print("- 解碼：對加密字符向左移動 3 位找回原字符")
    print("- 超出邊界時無法解碼，返回 '?'\n")

    print("=" * 50)
    print("測試用例：\n")

    # 測試單個字符
    test_chars = ["4", "7", "a", "d", "q", "t"]

    print("單字符解碼：")
    for encrypted in test_chars:
        decrypted = decode_character_easy(encrypted)

        # 找出索引用於說明
        if encrypted in KEYBOARD:
            enc_idx = KEYBOARD.index(encrypted)
            orig_idx = enc_idx - 3

            if 0 <= orig_idx < len(KEYBOARD):
                print(
                    f"'{encrypted}' (索引 {enc_idx:2d}) -> '{decrypted}' (索引 {orig_idx:2d})"
                )
            else:
                print(f"'{encrypted}' (索引 {enc_idx:2d}) -> '{decrypted}' (越界)")

    print("\n" + "=" * 50)
    print("鍵盤字符串（完整）：")
    print(KEYBOARD)
    print("\n每個字符的索引位置都可以用於計算解碼結果。")
