from pathlib import Path


def read_input() -> list[list[int]]:
    # Read the input data
    input_data: str = Path("input.txt").resolve().read_text().strip()

    # Parse the input data
    data: list[int] = [list(map(int, line.split())) for line in input_data.split("\n")]

    return data


def is_report_safe(report: list[int]) -> bool:
    ascending = descending = True  # Assume both until proven otherwise

    for i in range(len(report) - 1):
        difference: int = report[i + 1] - report[i]
        if abs(difference) < 1 or abs(difference) > 3:
            return False
        if difference < 0:
            ascending = False
        if difference > 0:
            descending = False

    return ascending or descending


def solution1() -> None:
    data: list[list[int]] = read_input()
    safe_reports: int = sum(1 for report in data if is_report_safe(report))

    print(safe_reports)


def solution2() -> None:
    data: list[list[int]] = read_input()
    safe_reports = 0

    for report in data:
        if is_report_safe(report):
            safe_reports += 1
            continue

        # Try removing each level and check if the report becomes safe
        if any(
            is_report_safe(report[:i] + report[i + 1 :]) for i in range(len(report))
        ):
            safe_reports += 1

    print(safe_reports)


solution1()
solution2()
