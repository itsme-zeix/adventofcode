from typing import Optional
from time import perf_counter_ns

def timeit(f):
    def wrap(*args, **kwargs):
        start = perf_counter_ns()
        res = f(*args, **kwargs)
        end = perf_counter_ns()
        print(f"Function {f.__name__} took {(end - start)/1000000:.2f}ms")
        return res
    return wrap

@timeit
def read_input(file_path) -> Optional[list[tuple[int, int]]]:
    try:
        with open(file_path, 'r') as f:
            ranges = f.read().split(',')
            return [(int(a), int(b)) for a, b in (r.split('-', 1) for r in ranges if '-' in r)]
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

def is_invalid(id: str, id_len: int, substr_len: int) -> bool:
    substr = id[0: substr_len]
    repeat_count = id_len // substr_len
    return id == (repeat_count * substr)

@timeit
def part1(input: list[tuple[int, int]]) -> int:
    res = 0

    # Brute force across range. Embarassingly parallel.
    for l, r in input:
        for id_int in range(l, r + 1):
            id_str = str(id_int)
            id_len = len(id_str)
            
            # odd no. of digits is always valid
            if id_len % 2 != 0:
                continue 

            substr_len = id_len // 2
            if is_invalid(id_str, id_len, substr_len):
                res += id_int
                continue
            
    return res

@timeit
def part2(input: list[tuple[int, int]]) -> int:
    res = 0

    # Brute force again. Embarassingly parallel again, but a second fork-join might be ideal
    # for iterating through the various substring lengths.
    for l, r in input:
        for id_int in range(l, r + 1):
            id_str = str(id_int)
            id_len = len(id_str)

            # iterate through half of id string, reducing length by 1 each time
            max_substr_len = len(id_str) // 2
            for substr_len in range(max_substr_len, 0, -1):
                if id_len % substr_len != 0:
                    continue
                if is_invalid(id_str, id_len, substr_len):
                    res += id_int
                    break
            
    return res

if __name__ == "__main__":
    input = read_input("input.txt")
    assert(input)

    print(part1(input))
    print(part2(input))

