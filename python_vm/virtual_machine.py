import struct
import sys

from .operations import Operations
from .opcode import Opcode


class VirtualMachine:
    def __init__(self, bin_path: str):
        self._bin = self._decode_binary_from_file(bin_path)
        self._registers = [0] * 8
        self._stack = []
        self._ops = Operations(self._bin, self._registers, self._stack)
        self._curr_idx = 0

    @staticmethod
    def _decode_binary_from_file(bin_path: str) -> list:
        with open(bin_path, 'rb') as f:
            data = f.read()

        # decode binary from 16-bit little-endians into ints
        num_elems = len(data) // 2
        try:
            data = struct.unpack('<{}H'.format(num_elems), data)
        except struct.error:
            print(
                "Error while decoding: Make sure the input file provided is 'challenge.bin'")
            sys.exit(1)

        # struct.unpack returns tuple, convert to list for mutability
        return list(data)

    def execute(self):
        while True:
            try:
                op_val = self._bin[self._curr_idx]
                opcode = Opcode(op_val)
                operation = getattr(self._ops, opcode.name.lower())
            except ValueError:
                print(
                    f"Error in binary at index{self._curr_idx}: {op_val} is not listed as a valid opcode")
            except AttributeError:
                print(
                    f"Error in binary at index {self._curr_idx}: Operation {opcode.name} not implemented.")
                sys.exit(1)

            self._curr_idx = operation(self._curr_idx)
