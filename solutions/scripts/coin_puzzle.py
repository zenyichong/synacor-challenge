#!/usr/bin/env python3
from itertools import permutations


def main():
    coin_dict = {
        2: 'red coin',
        3: 'corroded coin',
        5: 'shiny coin',
        7: 'concave coin',
        9: 'blue coin'
    }
    for a, b, c, d, e in permutations([2, 3, 5, 7, 9]):
        if (a + b * (c ** 2) + (d ** 3) - e) == 399:
            break

    sol = [coin_dict.get(key) for key in (a, b, c, d, e)]
    print(', '.join(sol))


if __name__ == '__main__':
    main()
