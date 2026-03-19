# Week 02 Solutions - 1114405020

## Completed Tasks
- Task 1: Sequence Clean
- Task 2: Student Ranking
- Task 3: Log Summary

## Execution Environment
- Python Version: 3.12.1

## Program Execution Instructions
Run each task individually:
- Task 1: `python task1_sequence_clean.py` (Note: This is a module, call the function in code)
- Task 2: `python task2_student_ranking.py`
- Task 3: `python task3_log_summary.py`

## Test Execution Instructions
`python -m unittest discover -s tests -p "test_*.py" -v`

## Data Structure Choices
- **Task 1:** Used list and set for deduplication to preserve order without violating constraints; strings for output formatting.
- **Task 2:** Used list of tuples for students and sorted() with key for efficient multi-criteria sorting.
- **Task 3:** Used defaultdict for user counts and Counter for actions to handle dynamic counting efficiently.

## One Error Encountered and Fix
In Task 2, initially misunderstood the tie-breaking order for names; fixed by correcting the sorting key to ensure name ascending order when scores and ages are equal.

## Red → Green → Refactor Summary

### Task 1: Sequence Clean
- **Red:** Wrote tests for normal, empty, and no-evens cases; all failed due to missing implementation.
- **Green:** Implemented sequence_clean function with deduplication loop, sorting, and even filtering; tests passed.
- **Refactor:** Split into helper functions (remove_duplicates_preserve_order, get_even_numbers) for better modularity and readability.

### Task 2: Student Ranking
- **Red:** Created tests for normal ranking, k=0, and tie-breaking; failed as function was undefined.
- **Green:** Added student_ranking with input parsing and sorted() using correct key; all tests passed after fixing expected output.
- **Refactor:** Broke down into parse_input, sort_students, and format_output functions for separation of concerns.

### Task 3: Log Summary
- **Red:** Defined tests for normal logs, empty logs, and same actions; import error due to missing function.
- **Green:** Implemented log_summary using defaultdict and Counter; handled edge cases like m=0.
- **Refactor:** Divided into parse_logs, get_sorted_user_counts, and get_top_action for cleaner code structure.