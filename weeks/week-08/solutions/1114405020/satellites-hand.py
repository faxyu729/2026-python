import math

EARTH_RADIUS = 6440

while True:
    try:
        line = input().split()
        s = int(line[0])
        angle = int(line[1])
        unit = line[2]
    except:
        break

    r = EARTH_RADIUS + s

    if unit == "deg":
        theta = angle * math.pi / 180
    else:
        theta = angle * math.pi / 10800

    arc = r * theta
    chord = 2 * r * math.sin(theta / 2)

    print(f"{arc:.6f} {chord:.6f}")
