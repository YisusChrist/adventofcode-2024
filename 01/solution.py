from pathlib import Path


def read_input() -> tuple[list[int], list[int]]:
    # Read the input data
    input_data = Path("input.txt").resolve().read_text().strip()
    left_list: list[int] = []
    right_list: list[int] = []

    # Parse the input data
    for line in input_data.split("\n"):
        num1, num2 = line.split("   ")
        left_list.append(int(num1))
        right_list.append(int(num2))

    return left_list, right_list


def solution1() -> None:
    left_list, right_list = read_input()

    # Sort both lists
    left_sorted = sorted(left_list)
    right_sorted = sorted(right_list)

    # Calculate the total distance
    distance = sum(abs(l - r) for l, r in zip(left_sorted, right_sorted))

    print(distance)


def solution2() -> None:
    left_list, right_list = read_input()

    # Count the number of appearances of each number in the right list
    numbers = set(left_list)
    appearances: dict[int, int] = {num: right_list.count(num) for num in numbers}

    # Calculate the total sum
    total_sum = sum(num * appearances[num] for num in numbers)

    print(total_sum)


solution1()
solution2()
