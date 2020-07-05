import sys


class Operations:
    """Class containing operations defined for each opcode"""

    def __init__(self, _bin: list = [], registers: list = [], stack: list = []):
        self._bin = _bin
        self._registers = registers
        self._stack = stack

    def halt(self, idx: int):
        """
        halt: 0
        Stops execution and terminates the program.
        """
        print("Reached opcode 0, terminating program.")
        sys.exit(0)

    def out(self, idx: int) -> int:
        """
        out: 19 a
        Writes the character represented by ascii code <a> to the terminal
        """
        print(chr(self._bin[idx + 1]), end='')
        return idx + 2

    def noop(self, idx: int) -> int:
        """
        noop: 21
        No operation
        """
        return idx + 1
