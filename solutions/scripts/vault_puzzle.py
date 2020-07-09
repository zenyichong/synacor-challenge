#!/usr/bin/env python3
from collections import deque


MAZE = [['*', '8', '-', '1'],
        ['4', '*', '11', '*'],
        ['+', '4', '-', '18'],
        ['22', '-', '9', '*']]
START = (0, 3)
TARGET = (3, 0)
TARGET_TOTAL = 30
DIRECTIONS = {
    (0, -1): 'north',
    (0, 1): 'south',
    (-1, 0): 'west',
    (1, 0): 'east',
}


def get_neighbours_coords(coords: tuple) -> list:
    neighbours = []
    for x, y in DIRECTIONS:
        i, j = (coords[0] + x, coords[1] + y)
        if not(0 <= j < len(MAZE)) or not(0 <= i < len(MAZE[0])):
            continue
        neighbours.append((i, j))
    return neighbours


def evaluate_expression(expression: list) -> int:
    """
    Evaluates a list containing elements of an expression and assumes that all
    calculations are from left to right i.e. operator precedence is ignored.

    Usage
    -----
    >>> evaluate_expression(['1', '+', '2'])
    3
    >>> evaluate_expression(['1', '+', '2', '*', '3'])
    9
    """
    if len(expression) % 2 == 0:
        return None
    running_total = 0
    running_expression = str(expression[0])
    for i in range(1, len(expression), 2):
        running_expression += ''.join(expression[i: i + 2])
        running_total = eval(running_expression)
        running_expression = str(running_total)
    return running_total


def bfs():
    """Implementation of breadth-first-search specific to this question."""
    initial_state = (START, [START], ['22'])
    paths = deque([initial_state])
    while len(paths) != 0:
        coords, visited, expression = paths.popleft()
        # Take two steps at a time, so that the expression formed can be
        # evaluated properly
        for x1, y1 in get_neighbours_coords(coords):
            for x2, y2 in get_neighbours_coords((x1, y1)):
                if (x2, y2) == START:
                    continue
                new_visited = visited[:] + [(x1, y1), (x2, y2)]
                new_expression = expression[:] + ([MAZE[y1][x1], MAZE[y2][x2]])
                new_total = evaluate_expression(new_expression)

                # Since there is only one '+', it is unlikely that the total
                # will become negative along the shortest path. 100 is an arbitrary
                # maximum cap.
                if not(0 <= new_total < 100):
                    continue
                if (x2, y2) == TARGET:
                    if new_total == TARGET_TOTAL:
                        return new_visited
                    else:
                        continue
                new_state = ((x2, y2), new_visited, new_expression)
                paths.append(new_state)


def main():
    path = bfs()
    path_as_headings = []
    for i in range(len(path) - 1):
        x = path[i + 1][0] - path[i][0]
        y = path[i + 1][1] - path[i][1]
        path_as_headings.append(DIRECTIONS[(x, y)])
    print(', '.join(path_as_headings))


if __name__ == '__main__':
    main()
