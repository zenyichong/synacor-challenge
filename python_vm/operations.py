import sys
from .opcode import Opcode
from .exceptions import InvalidNumberError, EmptyStackError


class Operations:
    """Class containing operations defined for each opcode"""

    def __init__(self, _bin: list = [], registers: list = [], stack: list = []):
        self._bin = _bin
        self._registers = registers
        self._stack = stack
        self._input_cache = []

    def _validate_read(self, value: int) -> int:
        """Ensures values are read from the correct storage region."""
        if value < 32768:
            return value
        elif (32768 <= value) and (value <= 32775):
            return self._registers[value % 32768]
        elif value > 32775:
            raise InvalidNumberError("Encountered invalid number {}", value)

    def _validate_write(self, value: int, address: int):
        """Ensures values are written to the correct storage region."""
        temp = self._bin[address]
        if (32768 <= temp) and (temp <= 32775):
            self._registers[temp % 32768] = value
        else:
            self._bin[address] = value

    def halt(self, idx: int = None, override: bool = False):
        """
        `halt: 0`
        Stops execution and terminates the program.
        """
        if not override:
            assert self._bin[idx] == Opcode.HALT.value
        print("Reached opcode 0, terminating program.")
        sys.exit(0)

    def set(self, idx: int):
        """
        `set: 1 a b`
        Sets register `a` to the value of `b`
        """
        assert self._bin[idx] == Opcode.SET.value
        value = self._validate_read(self._bin[idx + 2])
        self._validate_write(value, idx + 1)
        return idx + 3

    def push(self, idx: int) -> int:
        """
        `push: 2 a`
        Pushes `a` onto the stack
        """
        assert self._bin[idx] == Opcode.PUSH.value
        val = self._validate_read(self._bin[idx + 1])
        self._stack.append(val)
        return idx + 2

    def pop(self, idx: int) -> int:
        """
        `pop: 3 a`
        Removes the top element from the stack and write it into `a`;
        empty stack = error
        """
        assert self._bin[idx] == Opcode.POP.value
        if len(self._stack) == 0:
            raise EmptyStackError("Attempting to pop from empty stack")
        else:
            val = self._stack.pop()
            self._validate_write(val, idx + 1)
        return idx + 2

    def eq(self, idx: int) -> int:
        """
        `eq: 4 a b c`
        sets `a` to 1 if `b` is equal to `c`; sets it to 0 otherwise
        """
        assert self._bin[idx] == Opcode.EQ.value
        val_1 = self._validate_read(self._bin[idx + 2])
        val_2 = self._validate_read(self._bin[idx + 3])
        if val_1 == val_2:
            self._validate_write(1, idx + 1)
        else:
            self._validate_write(0, idx + 1)
        return idx + 4

    def gt(self, idx: int) -> int:
        """
        `gt: 5 a b c`
        Sets `a` to 1 if `b` is greater than `c`; sets it to 0 otherwise
        """
        assert self._bin[idx] == Opcode.GT.value
        val_1 = self._validate_read(self._bin[idx + 2])
        val_2 = self._validate_read(self._bin[idx + 3])
        if val_1 > val_2:
            self._validate_write(1, idx + 1)
        else:
            self._validate_write(0, idx + 1)
        return idx + 4

    def jmp(self, idx: int) -> int:
        """
        `jmp: 6 a`
        Jumps to `a`
        """
        assert self._bin[idx] == Opcode.JMP.value
        return self._validate_read(self._bin[idx + 1])

    def jt(self, idx: int) -> int:
        """
        `jt: 7 a b`
        If `a` is nonzero, jumps to `b`
        """
        assert self._bin[idx] == Opcode.JT.value
        if self._validate_read(self._bin[idx + 1]) != 0:
            return self._validate_read(self._bin[idx + 2])
        return idx + 3

    def jf(self, idx: int) -> int:
        """
        `jf: 8 a b`
        If `a` is zero, jumps to `b`
        """
        assert self._bin[idx] == Opcode.JF.value
        if self._validate_read(self._bin[idx + 1]) == 0:
            return self._validate_read(self._bin[idx + 2])
        return idx + 3

    def add(self, idx: int) -> int:
        """
        `add: 9 a b c`
        Assigns into `a` the sum of `b` and `c` (modulo 32768)
        """
        assert self._bin[idx] == Opcode.ADD.value
        val_1 = self._validate_read(self._bin[idx + 2])
        val_2 = self._validate_read(self._bin[idx + 3])
        total = (val_1 + val_2) % 32768
        self._validate_write(total, idx + 1)
        return idx + 4

    def mult(self, idx: int) -> int:
        """
        `mult: 10 a b c`
        Stores into `a` the product of `b` and `c` (modulo 32768)
        """
        assert self._bin[idx] == Opcode.MULT.value
        val_1 = self._validate_read(self._bin[idx + 2])
        val_2 = self._validate_read(self._bin[idx + 3])
        product = (val_1 * val_2) % 32768
        self._validate_write(product, idx + 1)
        return idx + 4

    def mod(self, idx: int) -> int:
        """
        `mod: 11 a b c`
        Stores into `a` the remainder of `b` divided by `c`
        """
        assert self._bin[idx] == Opcode.MOD.value
        val_1 = self._validate_read(self._bin[idx + 2])
        val_2 = self._validate_read(self._bin[idx + 3])
        remainder = val_1 % val_2
        self._validate_write(remainder, idx + 1)
        return idx + 4

    def and_(self, idx: int) -> int:
        """
        `and: 12 a b c`
        Stores into `a` the bitwise and of `b` and `c`
        """
        assert self._bin[idx] == Opcode.AND_.value
        val_1 = self._validate_read(self._bin[idx + 2])
        val_2 = self._validate_read(self._bin[idx + 3])
        bw_and = val_1 & val_2
        self._validate_write(bw_and, idx + 1)
        return idx + 4

    def or_(self, idx: int) -> int:
        """
        `or: 13 a b c`
        Stores into `a` the bitwise or of `b` and `c`
        """
        assert self._bin[idx] == Opcode.OR_.value
        val_1 = self._validate_read(self._bin[idx + 2])
        val_2 = self._validate_read(self._bin[idx + 3])
        bw_or = val_1 | val_2
        self._validate_write(bw_or, idx + 1)
        return idx + 4

    def not_(self, idx: int) -> int:
        """
        `not: 14 a b`
        Stores 15-bit bitwise inverse of `b` in `a`
        """
        assert self._bin[idx] == Opcode.NOT_.value
        val = self._validate_read(self._bin[idx + 2])
        bw_not = (~val) % 32768
        self._validate_write(bw_not, idx + 1)
        return idx + 3

    def rmem(self, idx: int) -> int:
        """
        `rmem: 15 a b`
        Reads memory at address `b` and writes it to `a`
        """
        assert self._bin[idx] == Opcode.RMEM.value
        address = self._validate_read(self._bin[idx + 2])
        val = self._validate_read(self._bin[address])
        self._validate_write(val, idx + 1)
        return idx + 3

    def wmem(self, idx: int) -> int:
        """
        `wmem: 16 a b`
        Writes the value from `b` into memory at address `a`
        """
        assert self._bin[idx] == Opcode.WMEM.value
        val = self._validate_read(self._bin[idx + 2])
        address = self._validate_read(self._bin[idx + 1])
        self._validate_write(val, address)
        return idx + 3

    def call(self, idx: int) -> int:
        """
        `call: 17 a`
        Writes the address of the next instruction to the stack and jumps to `a`
        """
        assert self._bin[idx] == Opcode.CALL.value
        self._stack.append(idx + 2)
        return self._validate_read(self._bin[idx + 1])

    def ret(self, idx: int) -> int:
        """
        ret: 18
        remove the top element from the stack and jump to it; empty stack = halt
        """
        assert self._bin[idx] == Opcode.RET.value
        if len(self._stack) == 0:
            self.halt(override=True)
        address = self._stack.pop()
        return address

    def out(self, idx: int) -> int:
        """
        `out: 19 a`
        Writes the character represented by ascii code `a` to the terminal
        """
        assert self._bin[idx] == Opcode.OUT.value
        ordinal = self._validate_read(self._bin[idx + 1])
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
        assert self._bin[idx] == Opcode.IN_.value
        if not self._input_cache:
            tmp = input()
            # append a newline char since the one from `input()` is consumed by
            # the program, then convert to a list and reversing it so each char
            # can be popped sequentially and fed into memory
            self._input_cache = list(tmp + '\n')[::-1]
        char = self._input_cache.pop()
        self._validate_write(ord(char), idx + 1)
        return idx + 2

    def noop(self, idx: int) -> int:
        """
        `noop: 21`
        No operation
        """
        assert self._bin[idx] == Opcode.NOOP.value
        return idx + 1
