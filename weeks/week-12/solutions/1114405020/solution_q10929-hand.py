def is_multiple_of_11(n):
        odd_sum = sum(int(n[-(i+1)]) for i in range(0, len(n), 2))
        even_sum = sum(int(n[-(i+1)]) for i in range(1, len(n), 2))
        return (odd_sum - even_sum) % 11 == 0           

while True:   
    n = input().strip()
    if n == "0":
         break
    if is_multiple_of_11(n):
        print(f"{n} is a multiple of 11.")  
    else:
        print(f"{n} is not a multiple of 11.")
