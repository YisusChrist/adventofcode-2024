from pathlib import Path


def read_input() -> list[str]:
    # Read the input data
    input_data: str = Path("input.txt").resolve().read_text().strip()

    # Parse the input data
    return input_data.splitlines()


def solution1() -> None:
    # Read the input data
    input_data: list[str] = read_input()

    ...


def solution2() -> None:
    # Read the input data
    input_data: list[str] = read_input()

    ...


solution1()
solution2()
