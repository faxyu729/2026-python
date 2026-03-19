# AI_USAGE.md

## Questions Asked to AI
1. How to structure unit tests in Python using unittest for multiple test cases?
2. How to implement deduplication without using set in Python?
3. How to sort a list with multiple criteria in Python?
4. How to use Counter and defaultdict for counting in Python?

## Suggestions Adopted from AI
- Used unittest.TestCase for organizing test methods.
- Adopted sorted() with key parameter for multi-criteria sorting in Task 2.
- Used Counter for action counting in Task 3 to find the most common action.
- Suggested refactoring code into smaller functions for better readability.

## Suggestions Rejected from AI
- Rejected using set() for deduplication in Task 1 because the problem explicitly forbids it to ensure order preservation understanding.
- Rejected using manual loops for sorting in Task 2, sticking to sorted() as required.

## Case of AI Misleading and Self-Correction
- AI initially suggested a sorting key that didn't handle name sorting correctly in ties; I corrected it by ensuring the key tuple includes name in ascending order, as 'b' < 'i' for bob vs ian, but verified against the example output to match expectations.