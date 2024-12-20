from pathlib import Path


def read_input() -> str:
    # Read the input data
    input_data: str = Path("input.txt").resolve().read_text().strip()

    # Parse the input data
    return input_data


def create_blocks_map(disk_map: str) -> list[int]:
    """
    Given the disk map, represent the blocks as a list of characters
    """
    return list(map(int, disk_map))


def create_disk_map(blocks_map: list[int]) -> list[int | None]:
    """
    Given the blocks map, create the disk map
    """
    return [
        None if i % 2 else i // 2 for i, n in enumerate(blocks_map) for _ in range(n)
    ]


def compact_disk(start_offset: int, disk_map: list[int | None]) -> None:
    head: int = start_offset
    while head < len(disk_map):
        if disk_map[head]:
            head += 1
            continue

        num: int | None = disk_map.pop()
        if num:
            disk_map[head] = num


def solution1() -> None:
    # Read the input data
    input_data: str = read_input()

    # Odd offsets represent used blocks, even offsets represent free blocks
    blocks_map: list[int | None] = create_blocks_map(input_data)

    # Create the disk map
    disk_map: list[int | None] = create_disk_map(blocks_map)

    # Compact the disk
    start_offset: int = blocks_map[0]
    compact_disk(start_offset, disk_map)
    print(sum(i * n for i, n in enumerate(disk_map)))


def create_disk_map_2(blocks_map: list[int]) -> list[int | None]:
    """
    Given the blocks map, create the disk map
    """
    disk_map: list[int | None] = []
    head = 0
    for i, n in enumerate(blocks_map):
        if not i % 2:
            disk_map.append((i // 2, head, head + n))
        head += n

    return disk_map


def compact_disk_2(length: int, blocks: list[int]) -> list[int | None]:
    for to_move in range(length // 2, -1, -1):
        block: int = next(b for b in blocks if b[0] == to_move)
        _, start, end = block
        space_needed = end - start
        for i, ((_, _, end1), (_, start2, _)) in enumerate(zip(blocks, blocks[1:])):
            if end1 == end:
                break
            if start2 - end1 >= space_needed:
                blocks.insert(i + 1, (to_move, end1, end1 + space_needed))
                blocks.remove(block)
                break


def solution2() -> None:
    # Read the input data
    input_data: str = read_input()

    # Odd offsets represent used blocks, even offsets represent free blocks
    blocks_map: list[int | None] = create_blocks_map(input_data)

    # Create the disk map
    disk_map: list[int | None] = create_disk_map_2(blocks_map)

    # Compact the disk
    compact_disk_2(len(blocks_map), disk_map)
    print(
        sum(
            block_id * index
            for block_id, start, end in disk_map
            for index in range(start, end)
        )
    )


solution1()
solution2()
