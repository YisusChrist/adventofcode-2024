from pathlib import Path

DIRECTIONS: dict[str, tuple[int, int]] = [
    (-1, 0),  # Up
    (0, 1),  # Right
    (1, 0),  # Down
    (0, -1),  # Left
]
NUMBER_OF_DIRECTIONS: int = len(DIRECTIONS)
STARTING_DIRECTION: tuple[int, int] = DIRECTIONS[0]

ROWS: int
COLS: int


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


def find_guard_start(input_data: list[str]) -> tuple[int, int]:
    """Finds the guard's starting position marked by '^'."""
    for i, row in enumerate(input_data):
        if "^" in row:
            return i, row.index("^")
    return -1, -1  # Default if not found


def move_guard(
    input_data: list[str],
    direction: tuple[int, int],
    current_pos: tuple[int, int],
    obstruction_pos: tuple[int, int] = (-1, -1),
) -> tuple[tuple[int, int], tuple[int, int]]:
    # Get the target position after moving in the current direction
    new_x, new_y = current_pos[0] + direction[0], current_pos[1] + direction[1]

    # If the new position is out of bounds, stop
    if new_x < 0 or new_x >= ROWS or new_y < 0 or new_y >= COLS:
        return (-1, -1), direction

    if input_data[new_x][new_y] == "#" or (new_x, new_y) == obstruction_pos:
        # There is a obstacle in the way, turn right
        direction = DIRECTIONS[(DIRECTIONS.index(direction) + 1) % NUMBER_OF_DIRECTIONS]
        # Don't move the guard, just change the direction
        return current_pos, direction

    # Update the current position
    return (new_x, new_y), direction


def find_path(
    input_data: list[str], starting_position: tuple[int, int]
) -> set[tuple[int, int]]:
    direction: tuple[int, int] = STARTING_DIRECTION
    visited: set[tuple[int, int]] = set()
    current_pos: tuple[int, int] = starting_position

    while True:
        # print_current_state(input_data, current_pos, rows, cols, direction)

        # Add the current position to the visited set
        visited.add(current_pos)

        # Move the guard in the current direction
        current_pos, direction = move_guard(
            input_data,
            direction,
            current_pos,
        )

        if current_pos == (-1, -1):
            break

    return visited


def solution1() -> None:
    global ROWS, COLS

    # Read the input data
    input_data: list[str] = read_input()
    ROWS, COLS = len(input_data), len(input_data[0])

    # Find the guard starting position (^)
    start_pos: tuple[int, int] = find_guard_start(input_data)
    # Find the path the guard takes to patrol the area
    path: set[tuple[int, int]] = find_path(input_data, start_pos)

    print(len(path))


def is_loop_detected(
    input_data: list[str],
    starting_position: tuple[int, int],
    obstruction_pos: tuple[int, int],
) -> bool:
    """
    Simulate the guard's movement with an obstruction added at obstruction_pos.
    Return True if a loop is detected.
    """
    direction: tuple[int, int] = STARTING_DIRECTION
    visited: set[tuple[tuple[int, int], tuple[int, int]]] = set()
    current_pos: tuple[int, int] = starting_position

    while True:
        # print_current_state(input_data, current_pos, rows, cols, direction)
        # Add current position and direction to the visited set
        if (current_pos, direction) in visited:
            return True
        visited.add((current_pos, direction))

        # Move the guard in the current direction
        current_pos, direction = move_guard(
            input_data,
            direction,
            current_pos,
            obstruction_pos,
        )

        if current_pos == (-1, -1):
            break

    return False


def solution2() -> None:
    global ROWS, COLS

    # Read the input data
    input_data: list[str] = read_input()
    ROWS, COLS = len(input_data), len(input_data[0])

    # Find the guard starting position (^)
    start_pos: tuple[int, int] = find_guard_start(input_data)
    # Find the path the guard takes to patrol the area
    path: set[tuple[int, int]] = find_path(input_data, start_pos)

    # Count valid obstruction positions
    result: int = sum(
        is_loop_detected(input_data, start_pos, obstruction)
        for obstruction in path
        if obstruction != start_pos
    )

    print(result)


solution1()
solution2()
