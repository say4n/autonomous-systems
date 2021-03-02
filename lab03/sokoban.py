#!/usr/bin/env python3

import argparse
import re
import sys
import subprocess


def parse_arguments(argv):
    parser = argparse.ArgumentParser(description='Solve Sokoban problems.')
    parser.add_argument("-i", help="Path to the file with the Sokoban instance.")
    parser.add_argument("-f", help="Path to the fast-downward.py.")
    parser.add_argument("-a", help="Algorithm to use with fast-downward.py.", default="lama-first")
    parser.add_argument("-t", help="Timeout for fast-downward.py", default="30m")
    return parser.parse_args(argv)


class SokobanGame(object):
    """ A Sokoban Game. """
    def __init__(self, string):
        """ Create a Sokoban game object from a string representation such as the one defined in
            http://sokobano.de/wiki/index.php?title=Level_format
        """
        lines = string.split('\n')
        self.h, self.w = len(lines), max(len(x) for x in lines)
        self.player = None
        self.walls = set()
        self.boxes = set()
        self.goals = set()
        for i, line in enumerate(lines, 0):
            for j, char in enumerate(line, 0):
                if char == '#':  # Wall
                    self.walls.add((i, j))
                elif char == '@':  # Player
                    assert self.player is None
                    self.player = (i, j)
                elif char == '+':  # Player on goal square
                    assert self.player is None
                    self.player = (i, j)
                    self.goals.add((i, j))
                elif char == '$':  # Box
                    self.boxes.add((i, j))
                elif char == '*':  # Box on goal square
                    self.boxes.add((i, j))
                    self.goals.add((i, j))
                elif char == '.':  # Goal square
                    self.goals.add((i, j))
                elif char == ' ':  # Space
                    pass  # No need to do anything
                else:
                    raise ValueError(f'Unknown character "{char}"')

    def is_wall(self, x, y):
        """ Whether the given coordinate is a wall. """
        return (x, y) in self.walls

    def is_box(self, x, y):
        """ Whether the given coordinate has a box. """
        return (x, y) in self.boxes

    def is_goal(self, x, y):
        """ Whether the given coordinate is a goal location. """
        return (x, y) in self.goals

def generate_instance_file(board, outfilename="sokoban-instance.pddl"):
    # Generate Sokoban instance.

    objects = f"""
(:objects
    player
    {" ".join("crate_" + str(i) for i in range(len(board.boxes)))}
    {" ".join("row_" + str(r) + "_col_" + str(c) for r in range(board.h) for c in range(board.w))}
)
"""

    init = f"""
(:init
\t(PLAYER player)
"""

    # Initialize crates, player.
    init += f"\t(at player row_{board.player[0]}_col_{board.player[1]})\n"
    for c_id, crate in enumerate(board.boxes):
        init += f"\n\t(CRATE crate_{c_id})"
        init += f"\n\t(at crate_{c_id} row_{crate[0]}_col_{crate[1]})\n"
        init += f"\n\t(has-crate row_{crate[0]}_col_{crate[1]})\n"

    # Initialize adjacency, alignment.
    for r in range(board.h):
        for c in range(board.w):
            # Adjacency
            if r + 1 < board.h:
                init += f"\n\t(is-adjacent row_{r}_col_{c} row_{r+1}_col_{c})"              # (x, y) -> (x+1, y)
                init += f"\n\t(is-adjacent row_{r+1}_col_{c} row_{r}_col_{c})"              # (x, y) <- (x+1, y)
            if c + 1 < board.w:
                init += f"\n\t(is-adjacent row_{r}_col_{c} row_{r}_col_{c+1})"              # (x, y) -> (x, y+1)
                init += f"\n\t(is-adjacent row_{r}_col_{c+1} row_{r}_col_{c})"              # (x, y) <- (x, y+1)

            # Alignment
            if r + 1 < board.h and r + 2 < board.h:
                init += f"\n\t(is-aligned row_{r}_col_{c} row_{r+1}_col_{c} row_{r+2}_col_{c})"    # L to R
                init += f"\n\t(is-aligned row_{r+2}_col_{c} row_{r+1}_col_{c} row_{r}_col_{c})"    # R to L

            if c + 1 < board.w and c + 2 < board.w:
                init += f"\n\t(is-aligned row_{r}_col_{c} row_{r}_col_{c+1} row_{r}_col_{c+2})"    # U to D
                init += f"\n\t(is-aligned row_{r}_col_{c+2} row_{r}_col_{c+1} row_{r}_col_{c})"    # D to U

    # Initialize free cells.
    for r in range(board.h):
        for c in range(board.w):
            if not board.is_box(r, c) and not board.is_wall(r, c) and not (r, c) == board.player:
                init += f"\n\t(is-free row_{r}_col_{c})"

    init += "\n)"

    goal = """
(:goal (and
"""
    for target in board.goals:
        goal += f"\n\t(has-crate row_{target[0]}_col_{target[1]})"

    goal += "\n)\n)"

    instance = f"""
(define (problem sokoban-instance)

(:domain sokoban-teleport)

{objects}

{init}

{goal}

)
"""
    with open(outfilename, "wt") as outfile:
        outfile.write(instance)

def get_row_col(string):
    row, col = None, None

    match = re.match("row_(\d*)_col_(\d*)", string)
    row = match.group(1)
    col = match.group(2)

    return row, col

def main(argv):
    args = parse_arguments(argv)
    with open(args.i, 'r') as file:
        board = SokobanGame(file.read().rstrip('\n'))

    # TODO - Some of the things that you need to do:
    #  1. (Previously) Have a domain.pddl file somewhere in disk that represents the Sokoban actions and predicates.
    #   Done, see sokoban-domain.pddl

    #  2. Generate an instance.pddl file from the given board, and save it to disk.
    #   Done.
    filename = "sokoban-instance.pddl"
    generate_instance_file(board, filename)

    #  3. Invoke some classical planner to solve the generated instance.
    #   Invoking fast downward.
    subprocess.call([args.f, "--log-level", "warning", "--overall-time-limit",
                        args.t, "--alias", args.a, "sokoban-domain.pddl", filename])

    #  3. Check the output and print the plan into the screen in some readable form.
    #   Checkout output in file named `sas_pan`.
    plan = ""
    try:
        with open("sas_plan", "rt") as planfile:
            plan = planfile.read()
    except FileNotFoundError:
        print("Oops, looks like the plan file does not exist on disk!")
        exit(124)

    actions = []

    for line in plan.split("\n"):
        line = line[1:-1]

        if line.startswith("teleport"):
            _, _, a, b = line.split(" ")
            r1, c1 = get_row_col(a)
            r2, c2 = get_row_col(b)

            actions.append(f"Teleport from ({r1}, {c1}) to ({r2}, {c2}).")
        if line.startswith("move"):
            _, _, a, b = line.split(" ")
            r1, c1 = get_row_col(a)
            r2, c2 = get_row_col(b)

            actions.append(f"Move from ({r1}, {c1}) to ({r2}, {c2}).")
        if line.startswith("push"):
            _, _, _, a, b, c = line.split(" ")
            r1, c1 = get_row_col(a)
            r2, c2 = get_row_col(b)
            r3, c3 = get_row_col(c)

            actions.append(f"Push crate from ({r2}, {c2}) to ({r3}, {c3}).")

    header_size = 40
    print("#" * header_size)
    print(" " * ((header_size - 4)//2),   "PLAN", " " * ((header_size - 4)//2))
    print("#" * header_size)
    print("\n".join(actions))
    print("#" * header_size)


if __name__ == "__main__":
    main(sys.argv[1:])
