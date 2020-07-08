import struct
import sys
import json
from typing import Union
from .operations import Operations
from .opcode import Opcode
from .exceptions import InvalidNumberError, EmptyStackError


class VirtualMachine:
    def __init__(self, binary: Union[str, list], registers: list = [], stack: list = [], curr_idx: int = 0):
        self._bin = self._retrieve_binary(binary)
        self._registers = [0] * 8 if not registers else registers
        self._stack = stack
        self._ops = Operations(
            self._read_from_mem,
            self._write_to_mem,
            self._push_stack,
            self._pop_stack,
            self._save_state
        )
        self._curr_idx = curr_idx

    def _read_from_mem(self, idx: int) -> int:
        val = self._bin[idx]
        if val < 32768:
            return val
        elif (32768 <= val) and (val <= 32775):
            return self._registers[val % 32768]
        elif val > 32775:
            raise InvalidNumberError("Encountered invalid number {}", val)

    def _write_to_mem(self, val: int, idx: int):
        temp = self._bin[idx]
        if (32768 <= temp) and (temp <= 32775):
            self._registers[temp % 32768] = val
        else:
            self._bin[idx] = val

    def _push_stack(self, val: int):
        self._stack.append(val)

    def _pop_stack(self) -> int:
        if len(self._stack) == 0:
            raise EmptyStackError("Attempting to pop from empty stack")
        val = self._stack.pop()
        return val

    @staticmethod
    def _retrieve_binary(binary: Union[str, list]) -> list:
        if isinstance(binary, list):
            return binary

        with open(binary, 'rb') as f:
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
                self._curr_idx = operation(self._curr_idx)
            except ValueError:
                sys.exit(
                    f"Error in binary at index {self._curr_idx}: {op_val} is not listed as a valid opcode")
            except AttributeError:
                sys.exit(
                    f"Error in binary at index {self._curr_idx}: Operation {opcode.name} not implemented")
            except InvalidNumberError as e:
                sys.exit(f"Error in binary at index {self._curr_idx}: {e}")
            except EmptyStackError as e:
                sys.exit(f"Error in binary at index {self._curr_idx}: {e}")
            except KeyboardInterrupt:
                print(f"\n\nExiting program...")
                sys.exit(0)

    def _save_state(self, filename: str):
        with open('./data/{}.bin'.format(filename), 'wb') as f:
            data = struct.pack('<{}H'.format(len(self._bin)), *self._bin)
            f.write(data)
        with open('./data/{}.json'.format(filename), 'w') as f:
            tmp = {
                'registers': self._registers,
                'stack': self._stack,
                'curr_idx': self._curr_idx
            }
            json.dump(tmp, f, indent=4)

    def get_byte(self, idx: str):
        return self._bin[idx]
