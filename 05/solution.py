from collections import defaultdict, deque
from pathlib import Path


def read_input() -> tuple[list[tuple[int, int]], list[list[int]]]:
    # Read the input data
    input_data: str = Path("input.txt").resolve().read_text().strip()

    # Parse the input data
    rules, updates = input_data.split("\n\n")
    rules: list[tuple[int, int]] = [
        (int(num1), int(num2))
        for rule in rules.split("\n")
        for num1, num2 in [rule.split("|")]
    ]
    updates: list[list[int]] = [
        list(map(int, update.split(","))) for update in updates.split("\n")
    ]

    return rules, updates


def update_is_valid(update: list[int], rules: list[tuple[int, int]]) -> bool:
    """Check if the update is valid according to the rules."""
    # Convert rules to a set for fast lookups
    rules_set = set(rules)

    seen = set()

    # Iterate through the update list
    for num in update:
        # Check for conflicts with previously seen elements
        for prev_num in seen:
            if (num, prev_num) in rules_set:
                return False

        # Add the current number to the set of seen elements
        seen.add(num)

    return True


def solution1() -> None:
    rules, updates = read_input()
    result = 0

    for update in updates:
        if update_is_valid(update, rules):
            result += update[len(update) // 2]

    print(result)


def topological_sort(update: list[int], rules: list[tuple[int, int]]) -> list[int]:
    """Perform a topological sort on the update list, given the rules."""
    # Build graph (adjacency list) and in-degree count for the pages in the update
    graph = defaultdict(list)
    in_degree = defaultdict(int)
    update_set = set(update)

    for x, y in rules:
        if x in update_set and y in update_set:
            graph[x].append(y)
            in_degree[y] += 1

    # Start with nodes that have no dependencies
    queue = deque([node for node in update if in_degree[node] == 0])
    sorted_order: list[int] = []

    while queue:
        node: int = queue.popleft()
        sorted_order.append(node)

        for neighbor in graph[node]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)

    # Check if sorting succeeded (cycle detection)
    if len(sorted_order) != len(update):
        raise ValueError("Cycle detected in the dependencies")

    return sorted_order


def solution2() -> None:
    rules, updates = read_input()
    result = 0

    for update in updates:
        if not update_is_valid(update, rules):
            new_update: list[int] = topological_sort(update, rules)
            result += new_update[len(new_update) // 2]

    print(result)


solution1()
solution2()
