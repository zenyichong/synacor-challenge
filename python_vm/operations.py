import sys
from typing import Callable
from .opcode import Opcode
from .exceptions import InvalidNumberError, EmptyStackError


class Operations:
    """Class containing operations defined for each opcode"""

    def __init__(
        self,
        read_mem_func: Callable,
        write_mem_func: Callable,
        push_stack_func: Callable,
        pop_stack_func: Callable,
        save_state_func: Callable
    ):
        self._input_cache = []
        self._read = read_mem_func
        self._write = write_mem_func
        self._push = push_stack_func
        self._pop = pop_stack_func
        self._save = save_state_func

    @staticmethod
    def halt(idx: int = None, override: bool = False):
        """
        `halt: 0`
        Stops execution and terminates the program.
        """
        print("Reached opcode 0, terminating program.")
        sys.exit(0)

    def set(self, idx: int):
        """
        `set: 1 a b`
        Sets register `a` to the value of `b`
        """
        val = self._read(idx + 2)
        self._write(val, idx + 1)
        return idx + 3

    def push(self, idx: int) -> int:
        """
        `push: 2 a`
        Pushes `a` onto the stack
        """
        val = self._read(idx + 1)
        self._push(val)
        return idx + 2

    def pop(self, idx: int) -> int:
        """
        `pop: 3 a`
        Removes the top element from the stack and write it into `a`;
        empty stack = error
        """
        val = self._pop()
        self._write(val, idx + 1)
        return idx + 2

    def eq(self, idx: int) -> int:
        """
        `eq: 4 a b c`
        sets `a` to 1 if `b` is equal to `c`; sets it to 0 otherwise
        """
        val_1 = self._read(idx + 2)
        val_2 = self._read(idx + 3)
        if val_1 == val_2:
            self._write(1, idx + 1)
        else:
            self._write(0, idx + 1)
        return idx + 4

    def gt(self, idx: int) -> int:
        """
        `gt: 5 a b c`
        Sets `a` to 1 if `b` is greater than `c`; sets it to 0 otherwise
        """
        val_1 = self._read(idx + 2)
        val_2 = self._read(idx + 3)
        if val_1 > val_2:
            self._write(1, idx + 1)
        else:
            self._write(0, idx + 1)
        return idx + 4

    def jmp(self, idx: int) -> int:
        """
        `jmp: 6 a`
        Jumps to `a`
        """
        return self._read(idx + 1)

    def jt(self, idx: int) -> int:
        """
        `jt: 7 a b`
        If `a` is nonzero, jumps to `b`
        """
        if self._read(idx + 1) != 0:
            return self._read(idx + 2)
        return idx + 3

    def jf(self, idx: int) -> int:
        """
        `jf: 8 a b`
        If `a` is zero, jumps to `b`
        """
        if self._read(idx + 1) == 0:
            return self._read(idx + 2)
        return idx + 3

    def add(self, idx: int) -> int:
        """
        `add: 9 a b c`
        Assigns into `a` the sum of `b` and `c` (modulo 32768)
        """
        val_1 = self._read(idx + 2)
        val_2 = self._read(idx + 3)
        total = (val_1 + val_2) % 32768
        self._write(total, idx + 1)
        return idx + 4

    def mult(self, idx: int) -> int:
        """
        `mult: 10 a b c`
        Stores into `a` the product of `b` and `c` (modulo 32768)
        """
        val_1 = self._read(idx + 2)
        val_2 = self._read(idx + 3)
        product = (val_1 * val_2) % 32768
        self._write(product, idx + 1)
        return idx + 4

    def mod(self, idx: int) -> int:
        """
        `mod: 11 a b c`
        Stores into `a` the remainder of `b` divided by `c`
        """
        val_1 = self._read(idx + 2)
        val_2 = self._read(idx + 3)
        remainder = val_1 % val_2
        self._write(remainder, idx + 1)
        return idx + 4

    def and_(self, idx: int) -> int:
        """
        `and: 12 a b c`
        Stores into `a` the bitwise and of `b` and `c`
        """
        val_1 = self._read(idx + 2)
        val_2 = self._read(idx + 3)
        bw_and = val_1 & val_2
        self._write(bw_and, idx + 1)
        return idx + 4

    def or_(self, idx: int) -> int:
        """
        `or: 13 a b c`
        Stores into `a` the bitwise or of `b` and `c`
        """
        val_1 = self._read(idx + 2)
        val_2 = self._read(idx + 3)
        bw_or = val_1 | val_2
        self._write(bw_or, idx + 1)
        return idx + 4

    def not_(self, idx: int) -> int:
        """
        `not: 14 a b`
        Stores 15-bit bitwise inverse of `b` in `a`
        """
        val = self._read(idx + 2)
        bw_not = (~val) % 32768
        self._write(bw_not, idx + 1)
        return idx + 3

    def rmem(self, idx: int) -> int:
        """
        `rmem: 15 a b`
        Reads memory at address `b` and writes it to `a`
        """
        address = self._read(idx + 2)
        val = self._read(address)
        self._write(val, idx + 1)
        return idx + 3

    def wmem(self, idx: int) -> int:
        """
        `wmem: 16 a b`
        Writes the value from `b` into memory at address `a`
        """
        val = self._read(idx + 2)
        address = self._read(idx + 1)
        self._write(val, address)
        return idx + 3

    def call(self, idx: int) -> int:
        """
        `call: 17 a`
        Writes the address of the next instruction to the stack and jumps to `a`
        """
        self._push(idx + 2)
        return self._read(idx + 1)

    def ret(self, idx: int) -> int:
        """
        ret: 18
        remove the top element from the stack and jump to it; empty stack = halt
        """
        try:
            address = self._pop()
        except EmptyStackError:
            self.halt(override=True)
        return address

    def out(self, idx: int) -> int:
        """
        `out: 19 a`
        Writes the character represented by ascii code `a` to the terminal
        """
        ordinal = self._read(idx + 1)
        print(chr(ordinal), end='')
        return idx + 2

    def in_(self, idx: int) -> int:
        """
        `in: 20 a`
        Reads a character from the terminal and write its ascii code to `a`.

        To streamline this operation, a whole line is captured as input, which
        is then split into ascii chars and each of them fed into memory. Since
        there is a guarantee that once input starts, it will continue until a
        newline is encountered, this approach should pose no issue.
        """
        if not self._input_cache:
            tmp = input('> ')
            if 'rewire teleporter' in tmp:
                self._rewire_teleporter()
                print('Teleporter settings altered!\n')
                return idx
            elif 'save' in tmp:
                if len(tmp.split()) == 1:
                    print(
                        "Please provide a file name. State will be saved into both <filename>.bin and <filename>.json inside data/ \n")
                else:
                    filename = tmp.strip().split()[-1]
                    self._save(filename)
                return idx
            # append a newline char since the one from `input()` is consumed by
            # the program, then convert to a list and reversing it so each char
            # can be popped sequentially and fed into memory
            self._input_cache = list(tmp + '\n')[::-1]
        char = self._input_cache.pop()
        self._write(ord(char), idx + 1)
        return idx + 2

    @staticmethod
    def noop(idx: int) -> int:
        """
        `noop: 21`
        No operation
        """
        return idx + 1

    def _rewire_teleporter(self):
        self._write(0, 5485)
        self._write(5, 5488)
