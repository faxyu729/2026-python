class MonotonFunction:
    def __init__(self, n):
        self.functions = [0] * n  # 0=增, 1=減
    def toggle(self, i):
        self.functions[i - 1] = 1 - self.functions[i - 1]
    def query(self, l, r):
        decreasing_count = sum(self.functions[l - 1 : r])
        return decreasing_count % 2

if __name__ == "__main__":
    n, q = map(int, input().split())
    mf = MonotonFunction(n)

    for _ in range(q):
        operation = list(map(int, input().split()))
        v = operation[0]

        if v == 1:
            mf.toggle(operation[1])
        else:
            print(mf.query(operation[1], operation[2]))
