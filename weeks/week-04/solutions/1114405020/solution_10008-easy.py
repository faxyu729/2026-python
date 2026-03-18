import sys


def solve(lines):
    """
    這是一個針對 CPE (UVA 10008) 簡單又容易記憶的版本 (-easy)。
    功能：計算所有英文字母出現的次數並依照題意排序。
    """
    counts = {}

    for line in lines:
        for char in line:
            if char.isalpha():
                upper_char = char.upper()
                if upper_char in counts:
                    counts[upper_char] += 1
                else:
                    counts[upper_char] = 1

    result = list(counts.items())

    result.sort(key=lambda x: (-x[1], x[0]))

    return result


def main():
    input_text = sys.stdin.read().splitlines()
    if not input_text:
        return

    n_str = input_text[0].strip()
    if not n_str.isdigit():
        return

    n = int(n_str)
    lines = input_text[1 : n + 1]

    sorted_letters = solve(lines)

    for char, count in sorted_letters:
        print(f"{char} {count}")


if __name__ == "__main__":
    main()
