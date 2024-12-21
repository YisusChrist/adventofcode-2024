import math
from collections import Counter
from pathlib import Path

cache: dict[int, int | tuple[int, int]] = {}


def read_input() -> list[int]:
    # Read the input data
    input_data: str = Path("input.txt").resolve().read_text().strip()

    # Parse the input data
    return list(map(int, input_data.split(" ")))


def convert_number(n: int) -> list[int]:
    if n == 0:
        return [1]

    if n in cache:
        return cache[n]

    digits: int = int(math.log10(n)) + 1 if n > 0 else 1

    if digits % 2 == 0:
        # Compute half and the divisor to split the number
        half: int = digits // 2
        divisor: int = 10**half
        num1: int = n // divisor
        num2: int = n % divisor
        result: list[int] = [num1, num2]
    else:
        result = [2024 * n]

    cache[n] = result
    return result


def find_solution(step: int) -> None:
    # Read the input data
    input_data: list[int] = read_input()

    # https://realpython.com/python-counter
    stones: Counter = Counter(input_data)

    for i in range(1, 76):
        new_stones = Counter()
        for n, num_stone in stones.items():
            for element in convert_number(n):
                new_stones[element] += num_stone
        stones = new_stones
        if i == step:
            print(sum(new_stones.values()))


def solution1() -> None:
    find_solution(25)


def solution2() -> None:
    find_solution(75)


if __name__ == "__main__":
    solution1()
    solution2()
