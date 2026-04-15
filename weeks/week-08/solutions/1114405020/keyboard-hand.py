KEYBOARD = "`1234567890-=qwertyuiop[]\\asdfghjkl;'zxcvbnm,./"

encrypted_text = input().lower()
decoded = []

for char in encrypted_text:
    if char in KEYBOARD:
        encrypted_index = KEYBOARD.index(char)
        original_index = encrypted_index - 3

        if 0 <= original_index < len(KEYBOARD):
            decoded_char = KEYBOARD[original_index]
            decoded.append(decoded_char)
        else:
            decoded.append("?")
    else:
        decoded.append(char)

print("".join(decoded))
