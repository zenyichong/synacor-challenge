#!/usr/bin/env python3

import sys
import json
from python_vm import VirtualMachine

DEFAULT_BIN_PATH = 'challenge.bin'


def main():
    if len(sys.argv) == 3:
        bin_path = sys.argv[1]
        with open(sys.argv[2]) as f:
            tmp = json.load(f)
        registers = tmp['registers']
        stack = tmp['stack']
        curr_idx = tmp['curr_idx']
        vm = VirtualMachine(bin_path, registers=registers,
                            stack=stack, curr_idx=curr_idx)
    elif len(sys.argv) == 1:
        bin_path = DEFAULT_BIN_PATH
        vm = VirtualMachine(bin_path)
    else:
        sys.exit("Usage:\n./main.py <path to binary> <path to saved config>")
    vm.execute()


if __name__ == '__main__':
    main()
