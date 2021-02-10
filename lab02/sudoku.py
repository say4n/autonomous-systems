#!/usr/bin/env python3

import argparse
import collections
import itertools
import math
import sys

from utils import save_dimacs_cnf, solve


def parse_arguments(argv):
    parser = argparse.ArgumentParser(description='Solve Sudoku problems.')
    parser.add_argument("board", help="A string encoding the Sudoku board, with all rows concatenated,"
                                      " and 0s where no number has been placed yet.")
    parser.add_argument('-q', '--quiet', action='store_true',
                        help='Do not print any output.')
    parser.add_argument('-c', '--count', action='store_true',
                        help='Count the number of solutions.')
    return parser.parse_args(argv)


def print_solution(solution):
    """ Print a (hopefully solved) Sudoku board represented as a list of 81 integers in visual form. """
    print(f'Solution: {"".join(map(str, solution))}')
    print('Solution in board form:')
    Board(solution).print()


def compute_solution(sat_assignment, variables, size):
    solution = []

    for row in range(1, size + 1):
        for col in range(1, size + 1):
            for number in range(1, 10):
                v = 100 * row + 10 * col + number
                if sat_assignment[v]:
                    solution.append(number)
                    break

    return solution


def generate_theory(board, verbose):
    """ Generate the propositional theory that corresponds to the given board. """
    size = board.size()
    clauses = []
    variables = set()

    # Variable representation is as follows: if the cell in the i-th row, and
    # the j-th column has the number n, it is represented as:
    # v := 100 * i + 10 * j + n
    # and, if it does not have the number, it is represented as -v.
    for row in range(1, size + 1):
        for col in range(1, size + 1):
            for n in range(1, 10):
                variables.add(100 * row + 10 * col + n)

    # Ensure that each cell has one and only one possible value allocated to it.
    at_least_one_value = []
    for r in range(1, size + 1):
        for c in range(1, size + 1):
            value_per_cell = []
            for n in range(1, 10):
                value_per_cell.append(100 * r + 10 * c + n)
            at_least_one_value.append(value_per_cell)

    # if verbose: print(f"at_least_one_value: {at_least_one_value}", end="\n\n")
    clauses.extend(at_least_one_value)

    at_most_one_value = []
    for r in range(1, size + 1):
        for c in range(1, size + 1):
            for n1 in range(1, 10):
                for n2 in range(n1 + 1, 10):
                    v1 = 100 * r + 10 * c + n1
                    v2 = 100 * r + 10 * c + n2
                    at_most_one_value.append([-v1, -v2])

    # if verbose: print(f"at_most_one_value: {at_most_one_value}", end="\n\n")
    clauses.extend(at_most_one_value)


    # Ensure that each column has all numbers in 1...9 only once.
    # ie. for the first column: 11n 21n 31n 41n 51n 61n 71n 81n 91n
    # and only once: -11n -12n
    all_columns = []
    for col in range(1, size + 1):
        single_column = []
        for number in range(1, 10):
            # At least once in a column.
            single_column.append(list([100 * row + 10 * col + number for row in range(1, size + 1)]))

            # Only once in a column.
            for r1 in range(1, size + 1):
                for r2 in range(r1 + 1, size + 1):
                    v1 = r1 * 100 + col * 10 + number
                    v2 = r2 * 100 + col * 10 + number
                    single_column.append([-v1, -v2])

        all_columns.extend(single_column)

    # if verbose: print(f"all_columns: {all_columns}", end="\n\n")
    clauses.extend(all_columns)

    # Ensure that each row has all numbers in 1...9 only once. Similar to
    # columns (above).
    all_rows = []
    for row in range(1, size + 1):
        single_row = []
        for number in range(1, 10):
            # At least once in a row.
            single_row.append(list([100 * row + 10 * col + number for col in range(1, size + 1)]))

            # Only once in a row.
            for c1 in range(1, size + 1):
                for c2 in range(c1 + 1, size + 1):
                    v1 = row * 100 + c1 * 10 + number
                    v2 = row * 100 + c2 * 10 + number
                    single_row.append([-v1, -v2])

        all_rows.extend(single_row)

    # if verbose: print(f"all_rows: {all_rows}", end="\n\n")
    clauses.extend(all_rows)

    # Ensure that each sub-grid has all numbers in 1...9 only once.
    all_subgrids = []
    for superrow in range (3):
        for supercol in range(3):
            subgrid = []
            for number in range(1, 10):
                # Number appears once in the subgrid.
                single_number = []
                for r in range(1, 4):
                    for c in range(1, 4):
                        row = superrow * 3 + r
                        col = supercol * 3 + c

                        single_number.append(100 * row + 10 * col + number)

                subgrid.append(single_number)

                # Number appears only once in sub-grid.
                for i1, v1 in enumerate(single_number):
                    for i2, v2 in enumerate(single_number):
                        if i2 > i1:
                            subgrid.append([-v1, -v2])

            all_subgrids.extend(subgrid)

    # if verbose: print(f"all_subgrids: {all_subgrids}", end="\n\n")
    clauses.extend(all_subgrids)

    # Initialize conditions for given board.
    initialization = []
    for cell in board.all_coordinates():
        if board.value(*cell) != 0:
            r, c = cell
            v = 100 * (r + 1) + 10 * (c + 1) + board.value(*cell)
            initialization.append([v])

    # if verbose: print(f"initialization: {initialization}", end="\n\n")
    clauses.extend(initialization)

    return clauses, variables, size


def count_number_solutions(board, verbose=False):
    count = 0

    clauses, variables, size = generate_theory(board, verbose)

    # Find solutions as long as they exist.
    while True:
        name = "theory_for_counting.cnf"
        save_dimacs_cnf(variables, clauses, name, verbose)
        result, sat_assignment = solve(name, verbose)

        if result != "SAT":
            break
        else:
            count += 1

            eliminate_solution = []
            for v in variables:
                # If the solution needed v, add -v to clauses.
                if sat_assignment[v]:
                    eliminate_solution.append(-v)
                # Else add v to clauses.
                else:
                    eliminate_solution.append(v)

            clauses.append(eliminate_solution)

    print(f'Number of solutions: {count}')


def find_one_solution(board, verbose=False):
    clauses, variables, size = generate_theory(board, verbose)
    return solve_sat_problem(clauses, "theory.cnf", size, variables, verbose)


def solve_sat_problem(clauses, filename, size, variables, verbose):
    save_dimacs_cnf(variables, clauses, filename, verbose)
    result, sat_assignment = solve(filename, verbose)
    if result != "SAT":
        if verbose:
            print("The given board is not solvable")
        return None
    solution = compute_solution(sat_assignment, variables, size)
    if verbose:
        print_solution(solution)
    return sat_assignment


class Board(object):
    """ A Sudoku board of size 9x9, possibly with some pre-filled values. """
    def __init__(self, string):
        """ Create a Board object from a single-string representation with 81 chars in the .[1-9]
         range, where a char '.' means that the position is empty, and a digit in [1-9] means that
         the position is pre-filled with that value. """
        size = math.sqrt(len(string))
        if not size.is_integer():
            raise RuntimeError(f'The specified board has length {len(string)} and does not seem to be square')
        self.data = [0 if x == '.' else int(x) for x in string]
        self.size_ = int(size)

    def size(self):
        """ Return the size of the board, e.g. 9 if the board is a 9x9 board. """
        return self.size_

    def value(self, x, y):
        """ Return the number at row x and column y, or a zero if no number is initially assigned to
         that position. """
        return self.data[x*self.size_ + y]

    def all_coordinates(self):
        """ Return all possible coordinates in the board. """
        return ((x, y) for x, y in itertools.product(range(self.size_), repeat=2))

    def print(self):
        """ Print the board in "matrix" form. """
        assert self.size_ == 9
        for i in range(self.size_):
            base = i * self.size_
            row = self.data[base:base + 3] + ['|'] + self.data[base + 3:base + 6] + ['|'] + self.data[base + 6:base + 9]
            print(" ".join(map(str, row)))
            if (i + 1) % 3 == 0:
                print("")  # Just an empty line


def main(argv):
    args = parse_arguments(argv)
    board = Board(args.board)

    if args.count:
        count_number_solutions(board, verbose=False)
    else:
        find_one_solution(board, verbose=not args.quiet)


if __name__ == "__main__":
    main(sys.argv[1:])
