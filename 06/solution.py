from pathlib import Path
from typing import Literal


def read_input() -> list[str]:
    # Read the input data
    input_data: str = Path("input.txt").resolve().read_text().strip()

    # Parse the input data
    return input_data.split("\n")


def print_current_state(
    input_data: list[str],
    current_pos: tuple[int, int],
    rows: int,
    cols: int,
    direction: tuple[int, int],
) -> None:
    print("Current position:", current_pos)
    try:
        if 0 < current_pos[0] <= rows - 1 and 0 <= current_pos[1] < cols - 1:
            x, y = current_pos
            print(
                input_data[x - 1][y - 1], input_data[x - 1][y], input_data[x - 1][y + 1]
            )
            print(input_data[x][y - 1], input_data[x][y], input_data[x][y + 1])
            print(
                input_data[x + 1][y - 1], input_data[x + 1][y], input_data[x + 1][y + 1]
            )
    except Exception:
        pass

    print("Direction:", direction)


def move_guard(
    input_data: list[str],
    directions: list[tuple[int, int]],
    direction: tuple[int, int],
    number_of_directions: int,
    current_pos: tuple[int, int],
    rows: int,
    cols: int,
) -> tuple[int, int]:
    # Move the guard in the current direction
    new_pos: tuple[int, int] = (
        current_pos[0] + direction[0],
        current_pos[1] + direction[1],
    )
    x, y = new_pos

    # If the new position is out of bounds, stop
    if x < 0 or x >= rows or y < 0 or y >= cols:
        return -1, direction

    if input_data[x][y] == "#":
        # There is a obstacle in the way, turn right
        direction = directions[(directions.index(direction) + 1) % number_of_directions]
    else:
        # Update the current position
        current_pos = new_pos

    return current_pos, direction


def find_exit(
    input_data: list[str],
    directions: list[tuple[int, int]],
    number_of_directions: int,
    current_pos: tuple[int, int],
    rows: int,
    cols: int,
) -> int:
    direction: tuple[int, int] = directions[0]
    visited: set[tuple[int, int]] = set()

    while True:
        print_current_state(
            input_data,
            current_pos,
            rows,
            cols,
            direction,
        )

        # Add the current position to the visited set
        visited.add(current_pos)

        # Move the guard in the current direction
        current_pos, direction = move_guard(
            input_data,
            directions,
            direction,
            number_of_directions,
            current_pos,
            rows,
            cols,
        )

        if current_pos == -1:
            break

    return len(visited)


def solution1() -> None:
    # Read the input data
    input_data: list[str] = read_input()

    rows, cols = len(input_data), len(input_data[0])

    directions: list[tuple[int, int]] = [
        (-1, 0),  # Up
        (0, 1),  # Right
        (1, 0),  # Down
        (0, -1),  # Left
    ]
    number_of_directions: int = len(directions)

    # Find the guard starting position (^)
    for i, row in enumerate(input_data):
        if "^" in row:
            current_pos: tuple[int, int] = (i, row.index("^"))
            break

    result: int = find_exit(
        input_data,
        directions,
        number_of_directions,
        current_pos,
        rows,
        cols,
    )

    print(result)


def is_loop_detected(
    input_data: list[str],
    directions: list[tuple[int, int]],
    number_of_directions: int,
    current_pos: tuple[int, int],
    rows: int,
    cols: int,
    obstruction_pos: tuple[int, int],
) -> bool:
    """
    Simulate the guard's movement with an obstruction added at obstruction_pos.
    Return True if a loop is detected.
    """
    direction: tuple[int, int] = directions[0]
    visited: set[tuple[tuple[int, int], tuple[int, int]]] = set()

    while True:
        print_current_state(
            input_data,
            current_pos,
            rows,
            cols,
            direction,
        )
        # Add current position and direction to the visited set
        if (current_pos, direction) in visited:
            return True
        visited.add((current_pos, direction))

        # Move the guard in the current direction
        x, y = current_pos
        new_pos: tuple[int, int] = (x + direction[0], y + direction[1])

        # Check bounds
        if new_pos[0] < 0 or new_pos[0] >= rows or new_pos[1] < 0 or new_pos[1] >= cols:
            break

        # Check if the obstruction or other obstacle is hit
        if new_pos == obstruction_pos or input_data[new_pos[0]][new_pos[1]] == "#":
            # Turn right
            direction = directions[
                (directions.index(direction) + 1) % number_of_directions
            ]
        else:
            # Move forward
            current_pos = new_pos

    return False


def get_guard_path(
    input_data: list[str],
    directions: list[tuple[int, int]],
    number_of_directions: int,
    start_pos: tuple[int, int],
    rows: int,
    cols: int,
) -> list[tuple[int, int]]:
    """
    Simulate the guard's patrol path and return all visited positions in order.
    """
    direction: tuple[int, int] = directions[0]
    current_pos: tuple[int, int] = start_pos
    path: list[tuple[int, int]] = []

    while True:
        # Add the current position to the path
        path.append(current_pos)

        # Move the guard in the current direction
        x, y = current_pos
        new_pos = (x + direction[0], y + direction[1])

        # Check bounds
        if new_pos[0] < 0 or new_pos[0] >= rows or new_pos[1] < 0 or new_pos[1] >= cols:
            break

        # Check if the guard encounters an obstacle
        if input_data[new_pos[0]][new_pos[1]] == "#":
            # Turn right
            direction = directions[
                (directions.index(direction) + 1) % number_of_directions
            ]
        else:
            # Move forward
            current_pos = new_pos

    return path


def count_valid_obstruction_positions(
    input_data: list[str],
    directions: list[tuple[int, int]],
    number_of_directions: int,
    start_pos: tuple[int, int],
    rows: int,
    cols: int,
    path: list[tuple[int, int]],
) -> int:
    """
    Count the number of positions on the path where adding an obstruction creates a loop.
    """
    valid_positions = 0

    for obstruction_pos in path:
        if obstruction_pos == start_pos:
            continue  # Skip the starting position

        if is_loop_detected(
            input_data,
            directions,
            number_of_directions,
            start_pos,
            rows,
            cols,
            obstruction_pos,
        ):
            valid_positions += 1

    return valid_positions


def solution2() -> None:
    # Read the input data
    input_data: list[str] = read_input()

    rows, cols = len(input_data), len(input_data[0])

    directions: list[tuple[int, int]] = [
        (-1, 0),  # Up
        (0, 1),  # Right
        (1, 0),  # Down
        (0, -1),  # Left
    ]
    number_of_directions: int = len(directions)

    # Find the guard's starting position (^)
    for i, row in enumerate(input_data):
        if "^" in row:
            start_pos: tuple[int, int] = (i, row.index("^"))
            break

    # Get the guard's patrol path
    path = get_guard_path(
        input_data, directions, number_of_directions, start_pos, rows, cols
    )

    # Count valid obstruction positions
    result = count_valid_obstruction_positions(
        input_data, directions, number_of_directions, start_pos, rows, cols, path
    )

    print(result)


solution1()
solution2()
