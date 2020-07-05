#!/usr/bin/env python3

import sys
from python_vm import VirtualMachine

BIN_PATH = 'challenge.bin'


def main():
    if len(sys.argv) == 2:
        bin_path = sys.argv[1]
    else:
        bin_path = BIN_PATH
    vm = VirtualMachine(bin_path)
    vm.execute()


if __name__ == '__main__':
    main()
