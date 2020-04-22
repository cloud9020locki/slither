from slither import Slither
from slither.analyses.data_dependency.data_dependency import is_dependent, Access
from slither.slithir.variables import Constant

sl = Slither('simple_storage.sol')

contract_A = sl.get_contract_from_name('A')
assert contract_A


def check_dep(variable, source, context, must_be_true):
    is_dep = is_dependent(variable, source, context)
    print(f'{context}: {variable} is dep of {source} {is_dep}')
    if must_be_true:
        assert is_dep
    else:
        assert not is_dep


st1 = contract_A.get_state_variable_from_name('st1')
st2 = contract_A.get_state_variable_from_name('st2')

test = contract_A.get_function_from_signature('test(uint256,uint256)')

print('#### Test g()')
st1_x = Access(st1, [Constant('x')])
st2_x = Access(st2, [Constant('x')])
st2_y = Access(st2, [Constant('y')])
check_dep(st1_x, test.parameters[0], contract_A, True)
check_dep(st2_x, test.parameters[0], contract_A, True)
check_dep(st2_x, test.parameters[1], contract_A, True)
check_dep(st2_y, test.parameters[0], contract_A, False)
check_dep(st2_y, test.parameters[1], contract_A, False)
