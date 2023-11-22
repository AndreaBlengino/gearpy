from gearpy.units import Current
from hypothesis.strategies import composite, floats, sampled_from
import numpy as np
from tests.conftest import types_to_check
from pytest import fixture


basic_current = Current(1, 'A')


@composite
def currents(draw):
    value = draw(floats(allow_nan = False, allow_infinity = False, min_value = -1000, max_value = 1000))
    unit = draw(sampled_from(elements = list(Current._Current__UNITS.keys())))

    return Current(value = value, unit = unit)


current_init_type_error_1 = [{'value': type_to_check, 'unit': 'unit'} for type_to_check in types_to_check
                             if not isinstance(type_to_check, float) and not isinstance(type_to_check, int)]

current_init_type_error_2 = [{'value': 1, 'unit': types_to_check} for type_to_check in types_to_check
                             if not isinstance(type_to_check, str)]

@fixture(params = [*current_init_type_error_1,
                   *current_init_type_error_2])
def current_init_type_error(request):
    return request.param


@fixture(params = [type_to_check for type_to_check in types_to_check if not isinstance(type_to_check, Current)])
def current_add_type_error(request):
    return request.param


@fixture(params = [type_to_check for type_to_check in types_to_check if not isinstance(type_to_check, Current)])
def current_sub_type_error(request):
    return request.param


@fixture(params = [type_to_check for type_to_check in types_to_check
                   if not isinstance(type_to_check, float) and not isinstance(type_to_check, int)])
def current_mul_type_error(request):
    return request.param


@fixture(params = [type_to_check for type_to_check in types_to_check if not isinstance(type_to_check, float)
                   and not isinstance(type_to_check, int) and not isinstance(type_to_check, np.ndarray)])
def current_rmul_type_error(request):
    return request.param


@fixture(params = [type_to_check for type_to_check in types_to_check if not isinstance(type_to_check, float)
                   and not isinstance(type_to_check, int) and not isinstance(type_to_check, Current)])
def current_truediv_type_error(request):
    return request.param


@fixture(params = [0, 0.0, Current(0, 'A')])
def current_truediv_zero_division_error(request):
    return request.param


@fixture(params = [type_to_check for type_to_check in types_to_check if not isinstance(type_to_check, Current)])
def current_eq_type_error(request):
    return request.param


@fixture(params = [type_to_check for type_to_check in types_to_check if not isinstance(type_to_check, Current)])
def current_ne_type_error(request):
    return request.param


@fixture(params = [type_to_check for type_to_check in types_to_check if not isinstance(type_to_check, Current)])
def current_gt_type_error(request):
    return request.param


@fixture(params = [type_to_check for type_to_check in types_to_check if not isinstance(type_to_check, Current)])
def current_ge_type_error(request):
    return request.param


@fixture(params = [type_to_check for type_to_check in types_to_check if not isinstance(type_to_check, Current)])
def current_lt_type_error(request):
    return request.param


@fixture(params = [type_to_check for type_to_check in types_to_check if not isinstance(type_to_check, Current)])
def current_le_type_error(request):
    return request.param


current_to_type_error_1 = [{'target_unit': type_to_check, 'inplace': True}
                           for type_to_check in types_to_check if not isinstance(type_to_check, str)]

current_to_type_error_2 = [{'target_unit': 'target_unit', 'inplace': type_to_check} for type_to_check in types_to_check
                           if not isinstance(type_to_check, bool) and not isinstance(type_to_check, int)]

@fixture(params = [*current_to_type_error_1,
                   *current_to_type_error_2])
def current_to_type_error(request):
    return request.param
