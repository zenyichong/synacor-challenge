#!/usr/bin/env python3
from python_vm import VirtualMachine
from python_vm.opcode import Opcode


opcode_args = {
    Opcode.HALT: 0,
    Opcode.SET: 2,
    Opcode.PUSH: 1,
    Opcode.POP: 1,
    Opcode.EQ: 3,
    Opcode.GT: 3,
    Opcode.JMP: 1,
    Opcode.JT: 2,
    Opcode.JF: 2,
    Opcode.ADD: 3,
    Opcode.MULT: 3,
    Opcode.MOD: 3,
    Opcode.AND_: 3,
    Opcode.OR_: 3,
    Opcode.NOT_: 2,
    Opcode.RMEM: 2,
    Opcode.WMEM: 2,
    Opcode.CALL: 1,
    Opcode.RET: 0,
    Opcode.OUT: 1,
    Opcode.IN_: 1,
    Opcode.NOOP: 0
}


def sanitize_val(val: int):
    if val < 32768:
        ret = str(val)
    elif 32768 <= val <= 32775:
        ret = 'r{}'.format(val % 32768)
    else:
        raise ValueError("Invalid value in binary: {}".format(val))
    return ret


def main():
    vm = VirtualMachine('challenge.bin')
    with open('data/bin_source.asm', 'w') as f:
        curr_idx = 0
        while curr_idx < len(vm._bin):
            val = vm.get_byte(curr_idx)
            try:
                opcode = Opcode(val)
            except ValueError:
                f.write("{:6} DATA: {}\n".format(str(curr_idx) + ':', val))
                curr_idx += 1
                continue

            num_args = opcode_args[opcode]
            args = [vm.get_byte(curr_idx + i) for i in range(1, num_args + 1)]
            args = [sanitize_val(arg) for arg in args]

            line = "{:6} {:4}".format(
                str(curr_idx) + ':', str(opcode.name.strip('_')))
            for arg in args:
                if opcode.value == 19:
                    try:
                        line += " {}".format(repr(chr(int(arg))))
                    except ValueError:
                        line += " {}".format(arg)
                else:
                    line += " {:5}".format(arg)

            f.write(line + '\n')
            curr_idx += num_args + 1


if __name__ == '__main__':
    main()
