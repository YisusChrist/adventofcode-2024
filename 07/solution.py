from functools import lru_cache
from pathlib import Path
from typing import Callable


def read_input() -> list[tuple[int, list[int]]]:
    # Read the input data
    input_data: str = Path("input.txt").resolve().read_text().strip()

    data: list[tuple[int, int, int]] = []

    # Parse the input data
    for line in input_data.split("\n"):
        num1, line = line.split(":")
        num1 = int(num1)
        nums = list(map(int, line.strip().split(" ")))
        data.append((num1, nums))

    # Parse the input data
    return data


def passes_test(
    test_result: int, nums: list[int], operators: list[Callable[[int, int], int]]
) -> bool:
    """
    Determines if the target value (test_result) can be achieved using
    '+' and '*' operators left-to-right among the numbers in nums.
    Optimizations:
        - Memoization to avoid redundant calculations
        - Pruning paths that exceed the target value
        - Using bitmasks to represent operator combinations
    """
    n: int = len(nums)  # Number of numbers

    # Memoization for storing intermediate states
    @lru_cache(None)
    def dfs(index: int, current_result: int) -> bool:
        """
        Recursive DFS function to explore operator combinations.
        Parameters:
            index: The current position in the numbers list
            current_result: The result so far
        """
        # Base case: If we reach the last number, check the final result
        if index == n:
            return current_result == test_result

        # Pruning: If the result already exceeds the test result (and all numbers are positive)
        if current_result > test_result and all(num > 0 for num in nums):
            return False

        # Next number to process
        next_num: int = nums[index]

        # Iterate over the list of operators and apply them recursively
        if any(
            dfs(index + 1, operator(current_result, next_num)) for operator in operators
        ):
            return True

        return False

    # Start the search from the first number and position 1
    return dfs(1, nums[0])


def concatenate(left: int, right: int) -> int:
    return int(f"{left}{right}")


def solution1() -> None:
    # Read the input data
    input_data: list[tuple[int, list[int]]] = read_input()

    operators: list[Callable[[int, int], int]] = [
        lambda x, y: x + y,
        lambda x, y: x * y,
    ]

    result: int = sum(
        test_result
        for test_result, nums in input_data
        if passes_test(test_result, nums, operators)
    )

    print(result)


def solution2() -> None:
    # Read the input data
    input_data: list[str] = read_input()

    operators: list[Callable[[int, int], int]] = [
        lambda x, y: x + y,
        lambda x, y: x * y,
        concatenate,
    ]

    result: int = sum(
        test_result
        for test_result, nums in input_data
        if passes_test(test_result, nums, operators)
    )

    print(result)


solution1()
solution2()
