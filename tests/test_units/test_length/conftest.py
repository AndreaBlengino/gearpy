from gearpy.units import Length
from hypothesis.strategies import composite, floats, sampled_from
import numpy as np
from tests.conftest import types_to_check
from pytest import fixture


basic_length = Length(1, 'm')


@composite
def lengths(draw):
    value = draw(floats(allow_nan = False, allow_infinity = False, min_value = 1e-10, exclude_min = True, max_value = 1000))
    unit = draw(sampled_from(elements = list(Length._Length__UNITS.keys())))

    return Length(value = value, unit = unit)


length_init_type_error_1 = [{'value': type_to_check, 'unit': 'unit'} for type_to_check in types_to_check
                            if not isinstance(type_to_check, float) and not isinstance(type_to_check, int)]

length_init_type_error_2 = [{'value': 1, 'unit': types_to_check} for type_to_check in types_to_check
                            if not isinstance(type_to_check, str)]

@fixture(params = [*length_init_type_error_1,
                   *length_init_type_error_2])
def length_init_type_error(request):
    return request.param


@fixture(params = [type_to_check for type_to_check in types_to_check if not isinstance(type_to_check, Length)])
def length_add_type_error(request):
    return request.param


@fixture(params = [type_to_check for type_to_check in types_to_check if not isinstance(type_to_check, Length)])
def length_sub_type_error(request):
    return request.param


@fixture(params = [type_to_check for type_to_check in types_to_check if not isinstance(type_to_check, float)
                   and not isinstance(type_to_check, int) and not isinstance(type_to_check, Length)])
def length_mul_type_error(request):
    return request.param


@fixture(params = [type_to_check for type_to_check in types_to_check if not isinstance(type_to_check, float)
                   and not isinstance(type_to_check, int) and not isinstance(type_to_check, np.ndarray)
                   and not isinstance(type_to_check, Length)])
def length_rmul_type_error(request):
    return request.param


@fixture(params = [type_to_check for type_to_check in types_to_check if not isinstance(type_to_check, float)
                   and not isinstance(type_to_check, int) and not isinstance(type_to_check, Length)])
def length_truediv_type_error(request):
    return request.param


@fixture(params = [0, 0.0])
def length_truediv_zero_division_error(request):
    return request.param


@fixture(params = [type_to_check for type_to_check in types_to_check if not isinstance(type_to_check, Length)])
def length_eq_type_error(request):
    return request.param


@fixture(params = [type_to_check for type_to_check in types_to_check if not isinstance(type_to_check, Length)])
def length_ne_type_error(request):
    return request.param


@fixture(params = [type_to_check for type_to_check in types_to_check if not isinstance(type_to_check, Length)])
def length_gt_type_error(request):
    return request.param


@fixture(params = [type_to_check for type_to_check in types_to_check if not isinstance(type_to_check, Length)])
def length_ge_type_error(request):
    return request.param


@fixture(params = [type_to_check for type_to_check in types_to_check if not isinstance(type_to_check, Length)])
def length_lt_type_error(request):
    return request.param


@fixture(params = [type_to_check for type_to_check in types_to_check if not isinstance(type_to_check, Length)])
def length_le_type_error(request):
    return request.param


length_to_type_error_1 = [{'target_unit': type_to_check, 'inplace': True}
                          for type_to_check in types_to_check if not isinstance(type_to_check, str)]

length_to_type_error_2 = [{'target_unit': 'target_unit', 'inplace': type_to_check}
                          for type_to_check in types_to_check if not isinstance(type_to_check, bool)
                          and not isinstance(type_to_check, int)]

@fixture(params = [*length_to_type_error_1,
                   *length_to_type_error_2])
def length_to_type_error(request):
    return request.param
