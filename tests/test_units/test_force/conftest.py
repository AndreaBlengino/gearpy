from gearpy.units import Force, Surface
from hypothesis.strategies import composite, floats, sampled_from
import numpy as np
from tests.conftest import types_to_check
from pytest import fixture


basic_force = Force(1, 'N')


@composite
def forces(draw):
    value = draw(floats(allow_nan = False, allow_infinity = False, min_value = -1000, max_value = 1000))
    unit = draw(sampled_from(elements = list(Force._Force__UNITS.keys())))

    return Force(value = value, unit = unit)


force_init_type_error_1 = [{'value': type_to_check, 'unit': 'unit'} for type_to_check in types_to_check
                           if not isinstance(type_to_check, float) and not isinstance(type_to_check, int)]

force_init_type_error_2 = [{'value': 1, 'unit': types_to_check} for type_to_check in types_to_check
                           if not isinstance(type_to_check, str)]

@fixture(params = [*force_init_type_error_1,
                   *force_init_type_error_2])
def force_init_type_error(request):
    return request.param


@fixture(params = [type_to_check for type_to_check in types_to_check if not isinstance(type_to_check, Force)])
def force_add_type_error(request):
    return request.param


@fixture(params = [type_to_check for type_to_check in types_to_check if not isinstance(type_to_check, Force)])
def force_sub_type_error(request):
    return request.param


@fixture(params = [type_to_check for type_to_check in types_to_check
                   if not isinstance(type_to_check, float) and not isinstance(type_to_check, int)])
def force_mul_type_error(request):
    return request.param


@fixture(params = [type_to_check for type_to_check in types_to_check if not isinstance(type_to_check, float)
                   and not isinstance(type_to_check, int) and not isinstance(type_to_check, np.ndarray)])
def force_rmul_type_error(request):
    return request.param


@fixture(params = [type_to_check for type_to_check in types_to_check if not isinstance(type_to_check, float)
                   and not isinstance(type_to_check, int) and not isinstance(type_to_check, Force)
                   and not isinstance(type_to_check, Surface)])
def force_truediv_type_error(request):
    return request.param


@fixture(params = [0, 0.0, Force(0, 'N')])
def force_truediv_zero_division_error(request):
    return request.param


@fixture(params = [type_to_check for type_to_check in types_to_check if not isinstance(type_to_check, Force)])
def force_eq_type_error(request):
    return request.param


@fixture(params = [type_to_check for type_to_check in types_to_check if not isinstance(type_to_check, Force)])
def force_ne_type_error(request):
    return request.param


@fixture(params = [type_to_check for type_to_check in types_to_check if not isinstance(type_to_check, Force)])
def force_gt_type_error(request):
    return request.param


@fixture(params = [type_to_check for type_to_check in types_to_check if not isinstance(type_to_check, Force)])
def force_ge_type_error(request):
    return request.param


@fixture(params = [type_to_check for type_to_check in types_to_check if not isinstance(type_to_check, Force)])
def force_lt_type_error(request):
    return request.param


@fixture(params = [type_to_check for type_to_check in types_to_check if not isinstance(type_to_check, Force)])
def force_le_type_error(request):
    return request.param


force_to_type_error_1 = [{'target_unit': type_to_check, 'inplace': True}
                         for type_to_check in types_to_check if not isinstance(type_to_check, str)]

force_to_type_error_2 = [{'target_unit': 'target_unit', 'inplace': type_to_check} for type_to_check in types_to_check
                         if not isinstance(type_to_check, bool) and not isinstance(type_to_check, int)]

@fixture(params = [*force_to_type_error_1,
                   *force_to_type_error_2])
def force_to_type_error(request):
    return request.param
