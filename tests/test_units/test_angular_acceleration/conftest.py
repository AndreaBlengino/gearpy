from gearpy.units import AngularAcceleration, Time
from hypothesis.strategies import composite, floats, sampled_from
import numpy as np
from tests.conftest import types_to_check
from pytest import fixture


basic_angular_acceleration = AngularAcceleration(1, 'rad/s^2')


@composite
def angular_accelerations(draw):
    value = draw(
        floats(
            allow_nan=False,
            allow_infinity=False,
            min_value=-1000,
            max_value=1000
        )
    )
    unit = draw(
        sampled_from(
            elements=list(
                AngularAcceleration._AngularAcceleration__UNITS.keys()
            )
        )
    )

    return AngularAcceleration(value=value, unit=unit)


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


angular_acceleration_init_type_error_1 = [
    {'value': type_to_check, 'unit': 'unit'}
    for type_to_check in types_to_check
    if not isinstance(type_to_check, float | int)
]

angular_acceleration_init_type_error_2 = [
    {'value': 1, 'unit': types_to_check} for type_to_check in types_to_check
    if not isinstance(type_to_check, str)
]


@fixture(
    params=[
        *angular_acceleration_init_type_error_1,
        *angular_acceleration_init_type_error_2
    ]
)
def angular_acceleration_init_type_error(request):
    return request.param


@fixture(
    params=[
        type_to_check for type_to_check in types_to_check
        if not isinstance(type_to_check, AngularAcceleration)
    ]
)
def angular_acceleration_add_type_error(request):
    return request.param


@fixture(
    params=[
        type_to_check for type_to_check in types_to_check
        if not isinstance(type_to_check, AngularAcceleration)
    ]
)
def angular_acceleration_sub_type_error(request):
    return request.param


@fixture(
    params=[
        type_to_check for type_to_check in types_to_check
        if not isinstance(type_to_check, float | int | Time)
    ]
)
def angular_acceleration_mul_type_error(request):
    return request.param


@fixture(
    params=[
        type_to_check for type_to_check in types_to_check
        if not isinstance(type_to_check, float | int | np.ndarray | Time)
    ]
)
def angular_acceleration_rmul_type_error(request):
    return request.param


@fixture(
    params=[
        type_to_check for type_to_check in types_to_check
        if not isinstance(type_to_check, float | int | AngularAcceleration)
    ]
)
def angular_acceleration_truediv_type_error(request):
    return request.param


@fixture(params=[0, 0.0, AngularAcceleration(0, 'rad/s^2')])
def angular_acceleration_truediv_zero_division_error(request):
    return request.param


@fixture(
    params=[
        type_to_check for type_to_check in types_to_check
        if not isinstance(type_to_check, AngularAcceleration)
    ]
)
def angular_acceleration_eq_type_error(request):
    return request.param


@fixture(
    params=[
        type_to_check for type_to_check in types_to_check
        if not isinstance(type_to_check, AngularAcceleration)
    ]
)
def angular_acceleration_ne_type_error(request):
    return request.param


@fixture(
    params=[
        type_to_check for type_to_check in types_to_check
        if not isinstance(type_to_check, AngularAcceleration)
    ]
)
def angular_acceleration_gt_type_error(request):
    return request.param


@fixture(
    params=[
        type_to_check for type_to_check in types_to_check
        if not isinstance(type_to_check, AngularAcceleration)
    ]
)
def angular_acceleration_ge_type_error(request):
    return request.param


@fixture(
    params=[
        type_to_check for type_to_check in types_to_check
        if not isinstance(type_to_check, AngularAcceleration)
    ]
)
def angular_acceleration_lt_type_error(request):
    return request.param


@fixture(
    params=[
        type_to_check for type_to_check in types_to_check
        if not isinstance(type_to_check, AngularAcceleration)
    ]
)
def angular_acceleration_le_type_error(request):
    return request.param


angular_acceleration_to_type_error_1 = [
    {'target_unit': type_to_check, 'inplace': True}
    for type_to_check in types_to_check if not isinstance(type_to_check, str)
]

angular_acceleration_to_type_error_2 = [
    {'target_unit': 'target_unit', 'inplace': type_to_check}
    for type_to_check in types_to_check
    if not isinstance(type_to_check, int | bool)
]


@fixture(
    params=[
        *angular_acceleration_to_type_error_1,
        *angular_acceleration_to_type_error_2
    ]
)
def angular_acceleration_to_type_error(request):
    return request.param
