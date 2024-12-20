import time
import random
import statistics
from typing import Callable


# Helper function to generate test sizes
def generate_test_sizes(start_size: int, end_size: int, multiplier: float) -> list[int]:
    sizes: list[int] = []
    current_size: int = start_size

    while current_size <= end_size:
        sizes.append(int(current_size))
        current_size *= multiplier

    return sizes


# Function to measure the performance of different test functions
def measure_performance(
    test_functions: list[Callable],
    start_size: int,
    end_size: int,
    multiplier: float,
    num_runs: int = 5,
) -> None:
    test_sizes: list[int] = generate_test_sizes(start_size, end_size, multiplier)
    random.shuffle(test_sizes)  # Shuffle the test sizes to avoid CPU cache effects

    # Store results for each test function
    all_results: dict[str, list] = {
        test_func.__name__: [] for test_func in test_functions
    }

    print("Running performance tests...\n")
    for size in test_sizes:
        # Generate random test data
        test_result: int = random.randint(1000, 10000)
        nums: list[int] = random.sample(range(1, 100), size)

        for test_func in test_functions:
            func_results = []

            for _ in range(num_runs):
                # Measure execution time for each test function
                start_time = time.perf_counter()
                test_func(test_result, nums)
                result = time.perf_counter() - start_time
                func_results.append(result)

            avg_result = statistics.mean(func_results)
            all_results[test_func.__name__].append(avg_result)

            # Print results for each test function
            print(f"Test size: {size}")
            print(
                f"{test_func.__name__.upper()} (average of {num_runs} runs): {avg_result:.6f} seconds"
            )
            print()

    # Print statistical analysis for all results
    def print_stats(label: str, results: list[float]) -> None:
        print(f"\n{label} Execution Time Stats:")
        print(f"  Average: {statistics.mean(results):.6f} seconds")
        print(f"  Min: {min(results):.6f} seconds")
        print(f"  Max: {max(results):.6f} seconds")
        print(f"  Std Dev: {statistics.stdev(results):.6f} seconds")

    # Print stats for each function
    for func_name, results in all_results.items():
        print_stats(func_name, results)
