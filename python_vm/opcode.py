from enum import Enum


class Opcode(Enum):
    """
    Class containing the opcode listings for the virtual machine, as defined
    in the `arch-spec`.
    """
    HALT = 0
    SET = 1
    PUSH = 2
    POP = 3
    EQ = 4
    GT = 5
    JMP = 6
    JT = 7
    JF = 8
    ADD = 9
    MULT = 10
    MOD = 11
    AND_ = 12
    OR_ = 13
    NOT_ = 14
    RMEM = 15
    WMEM = 16
    CALL = 17
    RET = 18
    OUT = 19
    IN_ = 20
    NOOP = 21
