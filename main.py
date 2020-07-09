#!/usr/bin/env python3

import sys
import json
from python_vm import VirtualMachine

DEFAULT_BIN_PATH = 'challenge.bin'


def main():

    def exit_and_print_usage():
        sys.exit(
            "Usage:\n./main.py <path to saved binary> <path to saved json>\n")

    if len(sys.argv) == 3:
        if not(sys.argv[1].endswith('bin')) or not(sys.argv[2].endswith('.json')):
            exit_and_print_usage()
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
        exit_and_print_usage()

    vm.execute()


if __name__ == '__main__':
    main()
