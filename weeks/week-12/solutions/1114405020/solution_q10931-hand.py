def solve():
    while True:
        n = int(input())
        if n == 0:
            break
        binary = bin(n)[2:]  
        ones = binary.count('1')  
        parity = ones % 2  

        print(f"The parity of {binary} is {parity} (mod 2).")

if __name__ == '__main__':
    solve()