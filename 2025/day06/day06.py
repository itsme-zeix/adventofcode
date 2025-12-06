from time import perf_counter_ns
from math import prod


def timeit(f):
    def wrap(*args, **kwargs):
        start = perf_counter_ns()
        res = f(*args, **kwargs)
        end = perf_counter_ns()
        print(f"Function {f.__name__} took {(end - start) / 1e6:.2f}ms")
        return res

    return wrap


@timeit
def read_input(file_path: str) -> str | None:
    try:
        with open(file_path, "r") as f:
            return f.read()

    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")


@timeit
def part1(input: str) -> int:
    lines = input.strip().split("\n")
    num_rows = [list(map(int, line.split())) for line in lines[:-1]]
    ops = lines[-1].split()

    res = 0
    for col in range(len(num_rows[0])):
        op = ops[col]
        if op != "+" and op != "*":
            raise Exception(f"Unknown op: {op}")
        curr = 0 if op == "+" else 1

        for row in range(len(num_rows)):
            num = num_rows[row][col]
            if op == "+":
                curr += num
            else:
                curr *= num
        res += curr
    return res


def compute(op: str, operands: list[int]) -> int:
    if op == "+":
        return sum(operands)
    elif op == "*":
        return prod(operands)
    else:
        raise Exception(f"Unknown op: {op}")


@timeit
def part2(input: str) -> int:
    lines = input.strip().split("\n")
    ops_raw = lines[-1]  # includes spaces here

    col_starts: set[int] = set()
    for i, op in enumerate(ops_raw):
        if op != " ":
            col_starts.add(i)

    res = 0
    op = None
    operands: list[int] = []
    for col in range(len(lines[0])):
        if col in col_starts:
            if op and operands:
                res += compute(op, operands)
            op = ops_raw[col]
            operands = []

        digits: list[str] = []
        for line in lines[:-1]:
            if col >= len(line) or line[col] == " ":
                continue
            digits.append(line[col])

        # no digits means its a blank column (delimiter used by input)
        if digits:
            operands.append(int("".join(digits)))

    # Add the last group of numbers to results
    if op and operands:
        res += compute(op, operands)

    return res


if __name__ == "__main__":
    input = read_input("input.txt")
    assert input

    print(part1(input))
    print(part2(input))
