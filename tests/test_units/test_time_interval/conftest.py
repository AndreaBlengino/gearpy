from gearpy.units import AngularAcceleration, AngularSpeed, Time, TimeInterval
from hypothesis.strategies import composite, floats, sampled_from
import numpy as np
from tests.conftest import types_to_check
from pytest import fixture


basic_time_interval = TimeInterval(1, 'sec')


@composite
def time_intervals(draw):
    value = draw(floats(allow_nan = False, allow_infinity = False, min_value = 1e-10, exclude_min = True, max_value = 1000))
    unit = draw(sampled_from(elements = list(TimeInterval._Time__UNITS.keys())))

    return TimeInterval(value = value, unit = unit)


time_interval_init_type_error_1 = [{'value': type_to_check, 'unit': 'unit'} for type_to_check in types_to_check
                                   if not isinstance(type_to_check, float) and not isinstance(type_to_check, int)]

time_interval_init_type_error_2 = [{'value': 1, 'unit': types_to_check} for type_to_check in types_to_check
                                   if not isinstance(type_to_check, str)]

@fixture(params = [*time_interval_init_type_error_1,
                   *time_interval_init_type_error_2])
def time_interval_init_type_error(request):
    return request.param


@fixture(params = [type_to_check for type_to_check in types_to_check
                   if not isinstance(type_to_check, Time) and not isinstance(type_to_check, TimeInterval)])
def time_interval_add_type_error(request):
    return request.param


@fixture(params = [type_to_check for type_to_check in types_to_check
                   if not isinstance(type_to_check, Time) and not isinstance(type_to_check, TimeInterval)])
def time_interval_sub_type_error(request):
    return request.param


@fixture(params = [type_to_check for type_to_check in types_to_check
                   if not isinstance(type_to_check, float) and not isinstance(type_to_check, int)
                   and not isinstance(type_to_check, AngularSpeed) and not isinstance(type_to_check, AngularAcceleration)])
def time_interval_mul_type_error(request):
    return request.param


@fixture(params = [type_to_check for type_to_check in types_to_check if not isinstance(type_to_check, float)
                   and not isinstance(type_to_check, int) and not isinstance(type_to_check, np.ndarray)
                   and not isinstance(type_to_check, AngularSpeed) and not isinstance(type_to_check, AngularAcceleration)])
def time_interval_rmul_type_error(request):
    return request.param


@fixture(params = [type_to_check for type_to_check in types_to_check if not isinstance(type_to_check, float)
                   and not isinstance(type_to_check, int) and not isinstance(type_to_check, Time)
                   and not isinstance(type_to_check, TimeInterval)])
def time_interval_truediv_type_error(request):
    return request.param


@fixture(params = [0, 0.0])
def time_interval_truediv_zero_division_error(request):
    return request.param


@fixture(params = [type_to_check for type_to_check in types_to_check
                   if not isinstance(type_to_check, Time) and not isinstance(type_to_check, TimeInterval)])
def time_interval_eq_type_error(request):
    return request.param


@fixture(params = [type_to_check for type_to_check in types_to_check
                   if not isinstance(type_to_check, Time) and not isinstance(type_to_check, TimeInterval)])
def time_interval_ne_type_error(request):
    return request.param


@fixture(params = [type_to_check for type_to_check in types_to_check
                   if not isinstance(type_to_check, Time) and not isinstance(type_to_check, TimeInterval)])
def time_interval_gt_type_error(request):
    return request.param


@fixture(params = [type_to_check for type_to_check in types_to_check
                   if not isinstance(type_to_check, Time) and not isinstance(type_to_check, TimeInterval)])
def time_interval_ge_type_error(request):
    return request.param


@fixture(params = [type_to_check for type_to_check in types_to_check
                   if not isinstance(type_to_check, Time) and not isinstance(type_to_check, TimeInterval)])
def time_interval_lt_type_error(request):
    return request.param


@fixture(params = [type_to_check for type_to_check in types_to_check
                   if not isinstance(type_to_check, Time) and not isinstance(type_to_check, TimeInterval)])
def time_interval_le_type_error(request):
    return request.param


time_interval_to_type_error_1 = [{'target_unit': type_to_check, 'inplace': True}
                                 for type_to_check in types_to_check if not isinstance(type_to_check, str)]

time_interval_to_type_error_2 = [{'target_unit': 'target_unit', 'inplace': type_to_check}
                                 for type_to_check in types_to_check if not isinstance(type_to_check, bool)
                                 and not isinstance(type_to_check, int)]

@fixture(params = [*time_interval_to_type_error_1,
                   *time_interval_to_type_error_2])
def time_interval_to_type_error(request):
    return request.param