from gearpy.units import AngularAcceleration, AngularSpeed, Time
from hypothesis.strategies import composite, floats, sampled_from
import numpy as np
from tests.conftest import types_to_check
from pytest import fixture


basic_time = Time(1, 'sec')


@composite
def times(draw):
    value = draw(
        floats(
            allow_nan=False,
            allow_infinity=False,
            min_value=-1000,
            max_value=1000
        )
    )
    unit = draw(sampled_from(elements=list(Time._Time__UNITS.keys())))

    return Time(value=value, unit=unit)


time_init_type_error_1 = [
    {'value': type_to_check, 'unit': 'unit'}
    for type_to_check in types_to_check
    if not isinstance(type_to_check, float | int)
]

time_init_type_error_2 = [
    {'value': 1, 'unit': types_to_check} for type_to_check in types_to_check
    if not isinstance(type_to_check, str)
]


@fixture(params=[*time_init_type_error_1, *time_init_type_error_2])
def time_init_type_error(request):
    return request.param


@fixture(
    params=[
        type_to_check for type_to_check in types_to_check
        if not isinstance(type_to_check, Time)
    ]
)
def time_add_type_error(request):
    return request.param


@fixture(
    params=[
        type_to_check for type_to_check in types_to_check
        if not isinstance(type_to_check, Time)
    ]
)
def time_sub_type_error(request):
    return request.param


@fixture(
    params=[
        type_to_check for type_to_check in types_to_check
        if not isinstance(
            type_to_check,
            float | int | AngularSpeed | AngularAcceleration
        )
    ]
)
def time_mul_type_error(request):
    return request.param


@fixture(
    params=[
        type_to_check for type_to_check in types_to_check
        if not isinstance(
            type_to_check,
            float | int | np.ndarray | AngularSpeed | AngularAcceleration
        )
    ]
)
def time_rmul_type_error(request):
    return request.param


@fixture(
    params=[
        type_to_check for type_to_check in types_to_check
        if not isinstance(type_to_check, float | int | Time)
    ]
)
def time_truediv_type_error(request):
    return request.param


@fixture(params=[0, 0.0, Time(0, 'sec')])
def time_truediv_zero_division_error(request):
    return request.param


@fixture(
    params=[
        type_to_check for type_to_check in types_to_check
        if not isinstance(type_to_check, Time)
    ]
)
def time_eq_type_error(request):
    return request.param


@fixture(
    params=[
        type_to_check for type_to_check in types_to_check
        if not isinstance(type_to_check, Time)
    ]
)
def time_ne_type_error(request):
    return request.param


@fixture(
    params=[
        type_to_check for type_to_check in types_to_check
        if not isinstance(type_to_check, Time)
    ]
)
def time_gt_type_error(request):
    return request.param


@fixture(
    params=[
        type_to_check for type_to_check in types_to_check
        if not isinstance(type_to_check, Time)
    ]
)
def time_ge_type_error(request):
    return request.param


@fixture(
    params=[
        type_to_check for type_to_check in types_to_check
        if not isinstance(type_to_check, Time)
    ]
)
def time_lt_type_error(request):
    return request.param


@fixture(
    params=[
        type_to_check for type_to_check in types_to_check
        if not isinstance(type_to_check, Time)
    ]
)
def time_le_type_error(request):
    return request.param


time_to_type_error_1 = [
    {'target_unit': type_to_check, 'inplace': True}
    for type_to_check in types_to_check if not isinstance(type_to_check, str)
]

time_to_type_error_2 = [{
    'target_unit': 'target_unit', 'inplace': type_to_check}
    for type_to_check in types_to_check
    if not isinstance(type_to_check, int | bool)
]


@fixture(params=[*time_to_type_error_1, *time_to_type_error_2])
def time_to_type_error(request):
    return request.param
