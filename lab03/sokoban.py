#!/usr/bin/env python3

import argparse
import sys


def parse_arguments(argv):
    parser = argparse.ArgumentParser(description='Solve Sudoku problems.')
    parser.add_argument("-i", help="Path to the file with the Sokoban instance.")
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


def main(argv):
    args = parse_arguments(argv)
    with open(args.i, 'r') as file:
        board = SokobanGame(file.read().rstrip('\n'))

    # TODO - Some of the things that you need to do:
    #  1. (Previously) Have a domain.pddl file somewhere in disk that represents the Sokoban actions and predicates.
    #  2. Generate an instance.pddl file from the given board, and save it to disk.
    #  3. Invoke some classical planner to solve the generated instance.
    #  3. Check the output and print the plan into the screen in some readable form.

    # Generate Sokoban instance.

    objects = f"""
(:objects
    player
    {" ".join("crate_" + str(i) for i in range(len(board.boxes)))}
    {" ".join("loc_" + str(r) + str(c) for r in range(board.h) for c in range(board.w))}
)
"""

    init = f"""
(:init
\t(PLAYER player)
"""

    # Initialize crates, player.
    init += f"\t(at player loc_{board.player[0]}{board.player[1]})\n"
    for c_id, crate in enumerate(board.boxes):
        init += f"\n\t(CRATE crate_{c_id})"
        init += f"\n\t(at crate_{c_id} loc_{crate[0]}{crate[1]})\n"

    # Initialize adjacency, alignment.
    for r in range(board.h):
        for c in range(board.w):
            # Adjacency
            if r + 1 < board.h:
                init += f"\n\t(is-adjacent loc_{r}{c} loc_{r+1}{c})"                # (x, y) -> (x+1, y)
                init += f"\n\t(is-adjacent loc_{r+1}{c} loc_{r}{c})"                # (x, y) <- (x+1, y)
            if c + 1 < board.w:
                init += f"\n\t(is-adjacent loc_{r}{c} loc_{r}{c+1})"                # (x, y) -> (x, y+1)
                init += f"\n\t(is-adjacent loc_{r}{c+1} loc_{r}{c})"                # (x, y) <- (x, y+1)

            # Alignment
            if r + 1 < board.h and r + 2 < board.h:
                init += f"\n\t(is-aligned loc_{r}{c} loc_{r+1}{c} loc_{r+2}{c})"    # L to R
                init += f"\n\t(is-aligned loc_{r+2}{c} loc_{r+1}{c} loc_{r}{c})"    # R to L

            if c + 1 < board.w and c + 2 < board.w:
                init += f"\n\t(is-aligned loc_{r}{c} loc_{r}{c+1} loc_{r}{c+2})"    # U to D
                init += f"\n\t(is-aligned loc_{r}{c+2} loc_{r}{c+1} loc_{r}{c})"    # D to U

    # Initialize free cells.
    for r in range(board.h):
        for c in range(board.w):
            if not board.is_box(r, c) and not board.is_wall(r, c) and not (r, c) == board.player:
                init += f"\n\t(is-free loc_{r}{c})"

    init += "\n)"

    goal = """
(:goal (and
"""
    for bt_pair in zip(range(len(board.boxes)), board.goals):
        box, target = bt_pair
        goal += f"\n\t(at crate_{box} loc_{target[0]}{target[1]})"

    goal += "\n)\n)"

    instance = f"""
(define (problem sokoban-instance)

(:domain sokoban-teleport)

{objects}

{init}

{goal}

)
"""
    with open("sokoban-instance.pddl", "wt") as outfile:
        outfile.write(instance)


if __name__ == "__main__":
    main(sys.argv[1:])
