from pathlib import Path


def read_input() -> list[int]:
    # Read the input data
    input_data: str = Path("input.txt").resolve().read_text().strip()

    # Parse the input data
    return [[int(x) for x in line] for line in input_data.split("\n")]


def get_list_of_neighbors(
    current_position: tuple[int, int],
    input_data: list[int],
    num_rows: int,
    num_columns: int,
) -> list[tuple[int, int]]:
    current_row, current_column = current_position
    current_value: int = input_data[current_row][current_column]

    directions: list[tuple[int, int]] = [
        (-1, 0),
        (1, 0),
        (0, -1),
        (0, 1),
    ]  # Up, Down, Left, Right
    neighbors: list[tuple[int, int]] = [
        (current_row + dr, current_column + dc)
        for dr, dc in directions
        if 0 <= current_row + dr < num_rows
        and 0 <= current_column + dc < num_columns
        and input_data[current_row + dr][current_column + dc] == current_value + 1
    ]
    return neighbors


def bfs(
    input_data: list[int],
    starting_position: tuple[int, int],
    num_rows: int,
    num_columns: int,
    solution2: bool = False,
) -> list[tuple[int, int]]:
    # Initialize the queue
    queue: list[tuple[int, int]] = [starting_position]

    # Initialize the paths
    paths: list[tuple[int, int]] = []

    # Initialize the visited set
    visited = set()

    # While the queue is not empty
    while queue:
        # Get the current position
        current_position: tuple[int, int] = queue.pop(0)

        # Add the current position to the visited set
        visited.add(current_position)

        # Get the current value
        current_value: int = input_data[current_position[0]][current_position[1]]
        if current_value == 9:
            paths.append(current_position)
            continue

        # Get the neighbors
        neighbors: list[tuple[int, int]] = get_list_of_neighbors(
            current_position,
            input_data,
            num_rows,
            num_columns,
        )

        # For each neighbor
        for neighbor in neighbors:
            # If the neighbor is not in the visited set
            if neighbor not in visited and (solution2 or neighbor not in queue):
                # Add the neighbor to the queue
                queue.append(neighbor)

    return paths


def find_trailheads_scores(
    input_data: list[int],
    starting_position: tuple[int, int],
    num_rows: int,
    num_columns: int,
    solution2: bool = False,
) -> int:
    paths: int = bfs(
        input_data,
        starting_position,
        num_rows,
        num_columns,
        solution2,
    )
    return len(paths)


def find_solution(solution2: bool) -> None:
    # Read the input data
    input_data: list[int] = read_input()

    # Get the number of rows and columns in the input data
    num_rows: int = len(input_data)
    num_columns: int = len(input_data[0])

    # Find how many starting positions are in the input data with their position
    starting_positions: list[tuple[int, int]] = [
        (i, j)
        for i in range(len(input_data))
        for j in range(len(input_data[i]))
        if input_data[i][j] == 0
    ]

    # Use BFS to find the paths to an end from each starting position
    scores: list[int] = [
        find_trailheads_scores(
            input_data,
            starting_position,
            num_rows,
            num_columns,
            solution2,
        )
        for starting_position in starting_positions
    ]

    print(sum(scores))


def solution1() -> None:
    find_solution(solution2=False)


def solution2() -> None:
    find_solution(solution2=True)


solution1()
solution2()
