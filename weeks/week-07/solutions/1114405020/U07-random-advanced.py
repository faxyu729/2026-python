# U07. 隨機種子與安全亂數（3.11）
# 本程式展示隨機數生成的最佳實踐：
# 1. random 為偽隨機，相同種子產生相同序列
# 2. 密碼學安全場景必須使用 secrets 模組
# 3. 兩者的用途、特性和安全性差異

import random
import secrets

# ── 相同種子產生相同序列（可重現性）──────────────────
# 問題：random 是「偽隨機數生成器」(PRNG, Pseudo-Random Number Generator)
#      這意味著：給定相同的種子，會產生相同的「隨機」序列
# 優點：便於測試、模擬、結果重現
# 缺點：不適合用於安全敏感的場景（密碼、token 等）

print("[相同種子測試]")

# 第一次：使用種子 42 生成 5 個隨機整數
random.seed(42)  # 設定隨機數生成器的種子
seq1 = [random.randint(1, 100) for _ in range(5)]
# randint(a, b)：傳回 [a, b] 之間的隨機整數（包括端點）
print(f"第一次序列：{seq1}")

# 第二次：使用相同的種子 42
random.seed(42)  # 重新設定相同的種子
seq2 = [random.randint(1, 100) for _ in range(5)]
print(f"第二次序列：{seq2}")

# 驗證：兩次序列完全相同
print(f"序列相同？{seq1 == seq2}")  # True（✓ 完全可重現）

# 說明：
#   - 種子決定了整個隨機序列
#   - 相同種子 = 相同序列
#   - 這對於測試、遊戲關卡重現非常有用
#   - 但對於安全用途完全不夠

# ── 不同 Random 實例各自獨立──────────────────────────
# 問題：全域的 random.seed() 會影響所有隨機呼叫
#      在多線程或多功能模塊中可能產生干擾
# 解決：使用 random.Random 建立獨立的隨機數生成器實例

print("\n[獨立隨機數生成器]")

# 建立兩個獨立的隨機數生成器，各自有不同的種子
rng1 = random.Random(1)  # 種子為 1 的獨立隨機數生成器
rng2 = random.Random(2)  # 種子為 2 的獨立隨機數生成器

# 各自產生隨機數，互不影響
val1 = rng1.random()  # rng1.random()：傳回 [0.0, 1.0) 的浮點數
val2 = rng2.random()
print(f"rng1.random()：{val1}")
print(f"rng2.random()：{val2}")

# 說明：
#   - 每個 Random 實例有自己的內部狀態
#   - rng1 和 rng2 的序列完全獨立
#   - 不會互相干擾，適合多線程或多功能模塊


# ── 密碼學安全亂數（secrets 模組）──────────────────────
# 問題：random 模組基於 Mersenne Twister 演算法
#      不適合密碼學用途，會被破譯
# 解決：使用 secrets 模組，基於作業系統的真隨機來源（/dev/urandom）
#      產生不可預測的亂數，適合密碼、token、session key 等

print("\n[密碼學安全亂數]")

# 1. secrets.randbelow(n)：密碼學安全的整數 [0, n)
token_int = secrets.randbelow(100)
print(f"密碼學安全整數 (0-99)：{token_int}")

# 2. secrets.token_hex(nbytes)：密碼學安全的十六進位字串
# nbytes：位元組數，輸出為該位元組數的 2 倍十六進位字元
hex_token = secrets.token_hex(16)  # 16 位元組 = 32 個十六進位字元
print(f"密碼學安全 hex token：{hex_token}")

# 3. secrets.token_bytes(nbytes)：密碼學安全的原始位元組
bytes_token = secrets.token_bytes(16)  # 16 位元組的隨機 bytes
print(f"密碼學安全 bytes token：{bytes_token}")

# 說明：
#   - secrets 使用作業系統的隨機來源（CryptographicallyStrong）
#   - 即使知道部分輸出，也無法預測下一個值
#   - token_hex/token_bytes 適合生成密碼、API key、session ID 等
#   - 無法設定種子（因為來自真隨機，不是偽隨機）


# ── random vs secrets：使用場景選擇─────────────────────
# 重要：random 模組不適合密碼、token、session key 等安全場景
# 只適合遊戲、模擬、測試等非安全用途

print("\n[使用場景對照]")
print("""
┌──────────────────────┬────────────┬─────────────────┐
│ 使用場景             │ random     │ secrets         │
├──────────────────────┼────────────┼─────────────────┤
│ 遊戲隨機數           │ ✓ 可用     │ ✗ 過度設計      │
│ 模擬/數值計算        │ ✓ 可用     │ ✗ 過度設計      │
│ 單元測試             │ ✓ 可用     │ ✗ 過度設計      │
│ 密碼生成             │ ✗ 不安全   │ ✓ 必須使用      │
│ 加密 token           │ ✗ 不安全   │ ✓ 必須使用      │
│ Session ID           │ ✗ 不安全   │ ✓ 必須使用      │
│ API key              │ ✗ 不安全   │ ✓ 必須使用      │
│ 需要可重現性         │ ✓ 支援種子 │ ✗ 不支援        │
│ 效能關鍵             │ ✓ 較快     │ ✗ 較慢          │
└──────────────────────┴────────────┴─────────────────┘
""")

# 快速決策樹：
# ├─ 涉及安全？(密碼、token、加密)
# │  ├─ 是 → 使用 secrets
# │  └─ 否 → 繼續
# └─ 遊戲、測試、模擬？
#    ├─ 是 → 使用 random
#    └─ 否 → 請諮詢安全專家
