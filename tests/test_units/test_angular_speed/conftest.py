from gearpy.units import AngularSpeed, Time
from hypothesis.strategies import composite, floats, sampled_from
import numpy as np
from tests.conftest import types_to_check
from pytest import fixture


basic_angular_speed = AngularSpeed(1, 'rad/s')


@composite
def angular_speeds(draw):
    value = draw(floats(allow_nan = False, allow_infinity = False, min_value = -1000, max_value = 1000))
    unit = draw(sampled_from(elements = list(AngularSpeed._AngularSpeed__UNITS.keys())))

    return AngularSpeed(value = value, unit = unit)


@composite
def times(draw):
    value = draw(floats(allow_nan = False, allow_infinity = False, min_value = -1000, max_value = 1000))
    unit = draw(sampled_from(elements = list(Time._Time__UNITS.keys())))

    return Time(value = value, unit = unit)


angular_speed_init_type_error_1 = [{'value': type_to_check, 'unit': 'unit'} for type_to_check in types_to_check
                                   if not isinstance(type_to_check, float) and not isinstance(type_to_check, int)]

angular_speed_init_type_error_2 = [{'value': 1, 'unit': types_to_check} for type_to_check in types_to_check
                                   if not isinstance(type_to_check, str)]

@fixture(params = [*angular_speed_init_type_error_1,
                   *angular_speed_init_type_error_2])
def angular_speed_init_type_error(request):
    return request.param


@fixture(params = [type_to_check for type_to_check in types_to_check if not isinstance(type_to_check, AngularSpeed)])
def angular_speed_add_type_error(request):
    return request.param


@fixture(params = [type_to_check for type_to_check in types_to_check if not isinstance(type_to_check, AngularSpeed)])
def angular_speed_sub_type_error(request):
    return request.param


@fixture(params = [type_to_check for type_to_check in types_to_check if not isinstance(type_to_check, float)
                   and not isinstance(type_to_check, int) and not isinstance(type_to_check, Time)])
def angular_speed_mul_type_error(request):
    return request.param


@fixture(params = [type_to_check for type_to_check in types_to_check if not isinstance(type_to_check, float)
                   and not isinstance(type_to_check, int) and not isinstance(type_to_check, np.ndarray)
                   and not isinstance(type_to_check, Time)])
def angular_speed_rmul_type_error(request):
    return request.param


@fixture(params = [type_to_check for type_to_check in types_to_check if not isinstance(type_to_check, float)
                   and not isinstance(type_to_check, int) and not isinstance(type_to_check, AngularSpeed)])
def angular_speed_truediv_type_error(request):
    return request.param


@fixture(params = [0, 0.0, AngularSpeed(0, 'rad/s')])
def angular_speed_truediv_zero_division_error(request):
    return request.param


@fixture(params = [type_to_check for type_to_check in types_to_check if not isinstance(type_to_check, AngularSpeed)])
def angular_speed_eq_type_error(request):
    return request.param


@fixture(params = [type_to_check for type_to_check in types_to_check if not isinstance(type_to_check, AngularSpeed)])
def angular_speed_ne_type_error(request):
    return request.param


@fixture(params = [type_to_check for type_to_check in types_to_check if not isinstance(type_to_check, AngularSpeed)])
def angular_speed_gt_type_error(request):
    return request.param


@fixture(params = [type_to_check for type_to_check in types_to_check if not isinstance(type_to_check, AngularSpeed)])
def angular_speed_ge_type_error(request):
    return request.param


@fixture(params = [type_to_check for type_to_check in types_to_check if not isinstance(type_to_check, AngularSpeed)])
def angular_speed_lt_type_error(request):
    return request.param


@fixture(params = [type_to_check for type_to_check in types_to_check if not isinstance(type_to_check, AngularSpeed)])
def angular_speed_le_type_error(request):
    return request.param


angular_speed_to_type_error_1 = [{'target_unit': type_to_check, 'inplace': True} for type_to_check in types_to_check
                                 if not isinstance(type_to_check, str)]

angular_speed_to_type_error_2 = [{'target_unit': 'target_unit', 'inplace': type_to_check} for type_to_check in types_to_check
                                 if not isinstance(type_to_check, bool) and not isinstance(type_to_check, int)]

@fixture(params = [*angular_speed_to_type_error_1,
                   *angular_speed_to_type_error_2])
def angular_speed_to_type_error(request):
    return request.param
