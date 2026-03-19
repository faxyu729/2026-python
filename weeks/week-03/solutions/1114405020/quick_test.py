#!/usr/bin/env python
# -*- coding: utf-8 -*-

from question100 import calculate_cycle_length, find_max_cycle_length

print("=== Manual Tests ===")
print(f"cycle_length(1) = {calculate_cycle_length(1)} (expect 1)")
print(f"cycle_length(22) = {calculate_cycle_length(22)} (expect 16)")
print(f"find_max_cycle_length(1, 10) = {find_max_cycle_length(1, 10)} (expect 20)")
print(f"find_max_cycle_length(100, 200) = {find_max_cycle_length(100, 200)} (expect 125)")

print("\n=== Test with input/output ===")
test_cases = [
    ("1 10", "1 10 20"),
    ("100 200", "100 200 125"),
    ("201 210", "201 210 89"),
    ("900 1000", "900 1000 174"),
]

for inp, expected_out in test_cases:
    i, j = map(int, inp.split())
    result = find_max_cycle_length(i, j)
    output = f"{i} {j} {result}"
    status = "✓ PASS" if output == expected_out else "✗ FAIL"
    print(f"{status}: {output} (expected {expected_out})")

