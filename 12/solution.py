from pathlib import Path

# Constants for movement directions
DIRECTIONS: list[tuple[int, int]] = [
    (-1, 0),
    (1, 0),
    (0, -1),
    (0, 1),
]  # Up, Down, Left, Right

ROWS = COLS = 0


def read_input() -> list[str]:
    # Read the input data
    input_data: str = Path("input.txt").resolve().read_text().strip()

    # Parse the input data
    return input_data.splitlines()


def is_within_bounds(row: int, col: int) -> bool:
    """Check if the given position is within grid bounds."""
    return 0 <= row < ROWS and 0 <= col < COLS


def get_neighbors(
    input_data: list[str],
    current_position: tuple[int, int],
    visited: set[tuple[int, int]],
) -> list[tuple[int, int]]:
    current_row, current_col = current_position
    current_value: int = input_data[current_row][current_col]

    neighbors: list[tuple[int, int]] = [
        (new_row, new_col)
        for dr, dc in DIRECTIONS
        if (
            is_within_bounds(
                new_row := current_row + dr,
                new_col := current_col + dc,
            )
            and input_data[new_row][new_col] == current_value
            and (new_row, new_col) not in visited
        )
    ]

    return neighbors


def explore_garden_plot(
    input_data: list[str],
    current_position: tuple[int, int],
    visited: set[tuple[int, int]],
) -> list[tuple[int, int]]:
    if current_position in visited:
        return []

    visited.add(current_position)
    group: list[tuple[int, int]] = [current_position]

    for neighbor in get_neighbors(
        input_data,
        current_position,
        visited,
    ):
        group.extend(
            explore_garden_plot(
                input_data,
                neighbor,
                visited,
            )
        )

    return group


def get_group_perimeter(
    input_data: list[str],
    current_position: tuple[int, int],
) -> int:
    current_row, current_col = current_position
    current_value: str = input_data[current_row][current_col]

    return sum(
        1
        for dr, dc in DIRECTIONS
        if not (
            is_within_bounds(
                new_row := current_row + dr,
                new_col := current_col + dc,
            )
            and input_data[new_row][new_col] == current_value
        )
    )


def get_contiguous_pairs(
    group: list[tuple[int, int]]
) -> list[tuple[tuple[int, int], tuple[int, int]]]:
    contiguous_pairs: list[tuple[tuple[int, int], tuple[int, int]]] = []

    for i in range(len(group)):
        for j in range(i + 1, len(group)):
            x1, y1 = group[i]
            x2, y2 = group[j]
            if (x1 == x2 and abs(y1 - y2) == 1) or (y1 == y2 and abs(x1 - x2) == 1):
                contiguous_pairs.append((group[i], group[j]))

    return contiguous_pairs


def merge_contiguous_cells(
    group: list[tuple[int, int]],
    contiguous_pairs: list[tuple[tuple[int, int], tuple[int, int]]],
) -> list[tuple[int, int]]:
    # TODO: Find an optimal implementation
    return contiguous_pairs


def get_group_sides(
    input_data: list[str],
    group: list[tuple[int, int]],
) -> int:
    sides = 0

    contiguous_pairs: list[tuple[tuple[int, int], tuple[int, int]]] = (
        get_contiguous_pairs(group)
    )
    print("Contiguous pairs:", contiguous_pairs)

    merged_cells: list[tuple[int, int]] = merge_contiguous_cells(
        group, contiguous_pairs
    )
    print("Merged cells:", merged_cells)
    for cell in merged_cells:
        cells_sides: int = get_group_perimeter(input_data, cell[0]) + 1
        print("Cell:", cell, "Sides:", cells_sides)
        sides += cells_sides

    print("Sides:", sides)
    print()

    return sides


def get_garden_groups(input_data: list[str]) -> list[list[tuple[int, int]]]:
    global ROWS, COLS

    ROWS = len(input_data)
    COLS = len(input_data[0])

    visited: set[tuple[int, int]] = set()

    groups: list[list[tuple[int, int]]] = []
    # Traverse the input data and find groups
    for i in range(ROWS):
        for j in range(COLS):
            group: list[tuple[int, int]] = explore_garden_plot(
                input_data,
                (i, j),
                visited,
            )
            if not group:
                continue

            groups.append(group)

    return groups


def solution1() -> None:
    # Read the input data
    input_data: list[str] = read_input()

    groups: list[list[tuple[int, int]]] = get_garden_groups(input_data)

    result: int = sum(
        len(group)  # Area
        * sum(
            get_group_perimeter(  # Perimeter
                input_data,
                position,
            )
            for position in group
        )
        for group in groups
    )

    print("Result:", result)


def solution2() -> None:
    # Read the input data
    input_data: list[str] = read_input()

    result = 0
    groups: list[list[tuple[int, int]]] = get_garden_groups(input_data)

    for group in groups:
        group_value = input_data[group[0][0]][group[0][1]]
        print("Group:", group, "Value:", group_value)

        area: int = len(group)

        # If there are contiguous cells with the same value, the sides are the same
        sides: int = get_group_sides(input_data, group)

        # print("Area:", area, "Sides:", sides)
        result += area * sides

    print("Result:", result)


solution1()
solution2()
