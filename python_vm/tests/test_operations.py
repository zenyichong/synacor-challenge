import pytest
from ..operations import Operations
from ..virtual_machine import VirtualMachine


@pytest.fixture(autouse=True)
def setup_mocks(mocker):
    global mocked_exit, mocked_print, mocked_input
    mocked_exit = mocker.patch('sys.exit', return_value=None)
    mocked_print = mocker.patch('builtins.print')
    mocked_input = mocker.patch('builtins.input', return_value='a')


def setup_vm_and_ops_module(binary, curr_idx, stack=[]):
    vm = VirtualMachine(binary, curr_idx, stack)
    ops = Operations(vm._read_from_mem, vm._write_to_mem,
                     vm._push_stack, vm._pop_stack, vm._save_state)
    return ops


@pytest.mark.parametrize(
    "op,curr_idx,input_bin,next_idx,side_effect",
    [
        ('halt', 0, [0], None, 'mocked_exit'),
        ('noop', 0, [21, 1], 1, None)
    ]
)
def test_no_args_ops(op, curr_idx, input_bin, side_effect, next_idx):
    ops_module = setup_vm_and_ops_module(input_bin, curr_idx)
    operation = getattr(ops_module, op)
    result = operation(curr_idx)
    if side_effect:
        (eval(side_effect)).assert_called_once()
    assert result == next_idx


@pytest.mark.parametrize(
    "op,curr_idx,input_bin,next_idx, res_bin",
    [
        ('set', 0, [1, 2, 3], 3, [1, 3, 3])
    ]
)
def test_set_op(op, curr_idx, input_bin, next_idx, res_bin):
    ops_module = setup_vm_and_ops_module(input_bin, curr_idx)
    operation = getattr(ops_module, op)
    result = operation(curr_idx)
    assert result == next_idx
    assert input_bin == res_bin


@pytest.mark.parametrize(
    "op,curr_idx,input_bin,input_stack,next_idx,res_bin,res_stack",
    [
        ('push', 0, [2, 4], [], 2, [2, 4], [4]),
        ('pop', 0, [3, 4], [6], 2, [3, 6], []),
        ('call', 0, [17, 5], [], 5, [17, 5], [2]),
        ('ret', 0, [18], [10], 10, [18], [])
    ]

)
def test_stack_ops(op, curr_idx, input_bin, input_stack, next_idx, res_bin, res_stack):
    ops_module = setup_vm_and_ops_module(input_bin, curr_idx, input_stack)
    operation = getattr(ops_module, op)
    result = operation(curr_idx)
    assert result == next_idx
    assert input_bin == res_bin
    assert input_stack == res_stack


@pytest.mark.parametrize(
    "op,curr_idx,input_bin,next_idx, res_bin",
    [
        ('eq', 0, [4, 2, 3, 3], 4, [4, 1, 3, 3]),
        ('eq', 0, [4, 2, 5, 1], 4, [4, 0, 5, 1]),
        ('gt', 0, [5, 2, 4, 2], 4, [5, 1, 4, 2]),
        ('gt', 0, [5, 2, 2, 2], 4, [5, 0, 2, 2]),
        ('gt', 0, [5, 2, 2, 4], 4, [5, 0, 2, 4]),
    ]
)
def test_comparison_ops(op, curr_idx, input_bin, next_idx, res_bin):
    ops_module = setup_vm_and_ops_module(input_bin, curr_idx)
    operation = getattr(ops_module, op)
    result = operation(curr_idx)
    assert result == next_idx
    assert input_bin == res_bin


@pytest.mark.parametrize(
    "op,curr_idx,input_bin,next_idx",
    [
        ('jmp', 0, [6, 10], 10),
        ('jt', 0, [7, 1, 10], 10),
        ('jt', 0, [7, 0, 10], 3),
        ('jf', 0, [8, 0, 10], 10),
        ('jf', 0, [8, 1, 10], 3)
    ]
)
def test_jump_ops(op, curr_idx, input_bin, next_idx):
    ops_module = setup_vm_and_ops_module(input_bin, curr_idx)
    operation = getattr(ops_module, op)
    result = operation(curr_idx)
    assert result == next_idx


@pytest.mark.parametrize(
    "op,curr_idx,input_bin,next_idx,res_bin",
    [
        ('add', 0, [9, 1, 4, 3], 4, [9, 7, 4, 3]),
        ('add', 0, [9, 1, 32758, 15], 4, [9, 5, 32758, 15]),
        ('mult', 0, [10, 1, 5, 4], 4, [10, 20, 5, 4]),
        ('mult', 0, [10, 1, 8192, 5], 4, [10, 8192, 8192, 5]),
        ('mod', 0, [11, 1, 15, 8], 4, [11, 7, 15, 8])
    ]
)
def test_arithmetic_ops(op, curr_idx, input_bin, next_idx, res_bin):
    ops_module = setup_vm_and_ops_module(input_bin, curr_idx)
    operation = getattr(ops_module, op)
    result = operation(curr_idx)
    assert result == next_idx
    assert input_bin == res_bin


@pytest.mark.parametrize(
    "op,curr_idx,input_bin,next_idx,res_bin",
    [
        ('and_', 0, [12, 1, 2, 3], 4, [12, 2, 2, 3]),
        ('or_', 0, [13, 1, 3, 4], 4, [13, 7, 3, 4]),
        ('not_', 0, [14, 1, 100], 3, [14, 32667, 100])
    ]
)
def test_bitwise_ops(op, curr_idx, input_bin, next_idx, res_bin):
    ops_module = setup_vm_and_ops_module(input_bin, curr_idx)
    operation = getattr(ops_module, op)
    result = operation(curr_idx)
    assert result == next_idx
    assert input_bin == res_bin


@pytest.mark.parametrize(
    "op,curr_idx,input_bin,next_idx,res_bin",
    [
        ('rmem', 0, [15, 1, 4, 7, 10], 3, [15, 10, 4, 7, 10]),
        ('wmem', 0, [16, 4, 10, 7, 1], 3, [16, 4, 10, 7, 10])
    ]
)
def test_mem_manip_ops(op, curr_idx, input_bin, next_idx, res_bin):
    ops_module = setup_vm_and_ops_module(input_bin, curr_idx)
    operation = getattr(ops_module, op)
    result = operation(curr_idx)
    assert result == next_idx
    assert input_bin == res_bin


@pytest.mark.parametrize(
    "op,curr_idx,input_bin,next_idx,res_bin,side_effect",
    [
        ('out', 0, [19, 97], 2, [19, 97], 'mocked_print'),
        ('in_', 0, [20, 10], 2, [20, 97], 'mocked_input')
    ]
)
def test_io_ops(op, curr_idx, input_bin, next_idx, res_bin, side_effect):
    ops_module = setup_vm_and_ops_module(input_bin, curr_idx)
    operation = getattr(ops_module, op)
    result = operation(curr_idx)
    (eval(side_effect)).assert_called_once()
    assert result == next_idx
    assert input_bin == res_bin
