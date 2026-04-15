import math

n, w, t, v = map(int, input().split())

umbrellas = []
for _ in range(n):
    x, l, speed = map(int, input().split())
    umbrellas.append((x, l, speed))

total_volume = 0.0
dt = 0.01
current_time = 0.0

while current_time < t:
    covered_length = 0.0

    for x, l, speed in umbrellas:
        if speed == 0:
            left = x
            right = x + l
        else:
            period = 2 * (w - l) / abs(speed)
            time_in_cycle = current_time % period

            if time_in_cycle <= (w - l) / abs(speed):
                left = x + speed * time_in_cycle
            else:
                left = x + 2 * (w - l) - abs(speed) * time_in_cycle

            right = left + l

        left = max(0, left)
        right = min(w, right)

        if left < right:
            covered_length += right - left

    volume = covered_length * w * v * dt
    total_volume += volume
    current_time += dt

print(f"{total_volume:.2f}")
