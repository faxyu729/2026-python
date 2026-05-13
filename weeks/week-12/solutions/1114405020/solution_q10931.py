"""
UVA 10931 - 奇偶性校驗位（Parity Checker）
標準版本實現

問題描述：
給定一個正整數，將其轉換為二進位，計算二進位中 1 的個數，
輸出該個數的奇偶性（0 表示偶數，1 表示奇數）。

輸入範圍：1 到 2,147,483,647
輸入 0 時停止程式

輸出格式：
"The parity of [二進位] is [個數 mod 2] (mod 2)."

例子：
- 輸入：1，二進位：1，1 的個數：1，奇偶性：1 (奇數)
  輸出：The parity of 1 is 1 (mod 2).

- 輸入：2，二進位：10，1 的個數：1，奇偶性：1 (奇數)
  輸出：The parity of 10 is 1 (mod 2).

- 輸入：3，二進位：11，1 的個數：2，奇偶性：0 (偶數)
  輸出：The parity of 11 is 0 (mod 2).
"""


def count_ones_in_binary(n):
    """
    計算整數的二進位表示中 1 的個數
    
    原理：
    bin() 函數將整數轉換為二進位字符串，格式為 '0b...'
    例如：bin(7) 返回 '0b111'
    我們移除前綴 '0b'，然後計算字符 '1' 的出現次數
    
    時間複雜度：O(log n)（二進位位數）
    空間複雜度：O(log n)（存儲二進位字符串）
    
    Args:
        n: 正整數 (1 <= n <= 2,147,483,647)
    
    Returns:
        整數：二進位中 1 的個數
    
    例子：
        count_ones_in_binary(1) -> 1
        count_ones_in_binary(3) -> 2
        count_ones_in_binary(7) -> 3
    """
    # 使用 bin() 轉換為二進位字符串 '0b...'
    binary_str = bin(n)
    
    # 計算字符 '1' 在二進位字符串中的出現次數
    # bin() 返回格式如 '0b101'，count('1') 直接計算 1 的個數
    ones_count = binary_str.count('1')
    
    return ones_count


def calculate_parity(n):
    """
    計算整數的奇偶性校驗位
    
    奇偶性定義：
    - 若二進位中 1 的個數為偶數，則奇偶性為 0
    - 若二進位中 1 的個數為奇數，則奇偶性為 1
    
    這在計算機科學中常用於錯誤檢測（Parity Check）
    
    Args:
        n: 正整數 (1 <= n <= 2,147,483,647)
    
    Returns:
        整數：0 (偶偶性) 或 1 (奇偶性)
    
    例子：
        calculate_parity(1) -> 1
        calculate_parity(3) -> 0
        calculate_parity(7) -> 1
    """
    # 計算 1 的個數
    ones_count = count_ones_in_binary(n)
    
    # 計算奇偶性：1 的個數 mod 2
    # 若為偶數個 1，則 parity = 0
    # 若為奇數個 1，則 parity = 1
    parity = ones_count % 2
    
    return parity


def format_output(n, parity):
    """
    格式化輸出字符串
    
    格式規範：
    "The parity of [二進位字符串] is [奇偶性] (mod 2)."
    
    Args:
        n: 原始正整數
        parity: 奇偶性（0 或 1）
    
    Returns:
        字符串：格式化的輸出
    
    例子：
        format_output(1, 1) -> "The parity of 1 is 1 (mod 2)."
        format_output(3, 0) -> "The parity of 11 is 0 (mod 2)."
    """
    # 轉換為二進位字符串，移除 '0b' 前綴
    binary_str = bin(n)[2:]
    
    # 按格式構造輸出字符串
    output = f"The parity of {binary_str} is {parity} (mod 2)."
    
    return output


def main():
    """
    主程式：讀取輸入並處理每個數字
    
    流程：
    1. 持續讀取輸入直到遇到 0
    2. 對每個輸入計算奇偶性
    3. 格式化並輸出結果
    4. 輸入 0 時停止
    
    輸入示例：
        1
        2
        3
        7
        0 (停止)
    
    輸出示例：
        The parity of 1 is 1 (mod 2).
        The parity of 10 is 1 (mod 2).
        The parity of 11 is 0 (mod 2).
        The parity of 111 is 1 (mod 2).
    """
    while True:
        try:
            # 讀取一個整數
            n = int(input())
            
            # 檢查是否為停止訊號
            if n == 0:
                # 遇到 0 則停止程式
                break
            
            # 計算奇偶性
            parity = calculate_parity(n)
            
            # 格式化輸出
            output = format_output(n, parity)
            
            # 打印結果
            print(output)
        
        except EOFError:
            # 文件結束或管道關閉
            break
        except ValueError:
            # 輸入不是有效的整數，忽略此行
            continue


if __name__ == '__main__':
    # 程式入口
    main()
