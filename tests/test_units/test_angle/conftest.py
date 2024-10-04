from gearpy.units import AngularPosition, Angle
from hypothesis.strategies import composite, floats, sampled_from
import numpy as np
from tests.conftest import types_to_check
from pytest import fixture


basic_angle = Angle(1, 'rad')


@composite
def angles(draw, min_value=0, max_value=1000, unit=None):
    value = draw(
        floats(
            allow_nan=False,
            allow_infinity=False,
            min_value=min_value,
            max_value=max_value
        )
    )
    if unit is None:
        unit = draw(
            sampled_from(elements=list(Angle._AngularPosition__UNITS.keys()))
        )

    return Angle(value=value, unit=unit)


angle_init_type_error_1 = [
    {'value': type_to_check, 'unit': 'unit'}
    for type_to_check in types_to_check
    if not isinstance(type_to_check, float) and
    not isinstance(type_to_check, int)
]

angle_init_type_error_2 = [
    {'value': 1, 'unit': types_to_check} for type_to_check in types_to_check
    if not isinstance(type_to_check, str)
]


@fixture(params=[*angle_init_type_error_1, *angle_init_type_error_2])
def angle_init_type_error(request):
    return request.param


@fixture(
    params=[
        type_to_check for type_to_check in types_to_check
        if not isinstance(type_to_check, AngularPosition) and
        not isinstance(type_to_check, Angle)
    ]
)
def angle_add_type_error(request):
    return request.param


@fixture(
    params=[
        type_to_check for type_to_check in types_to_check
        if not isinstance(type_to_check, AngularPosition) and
        not isinstance(type_to_check, Angle)
    ]
)
def angle_sub_type_error(request):
    return request.param


@fixture(
    params=[
        type_to_check for type_to_check in types_to_check
        if not isinstance(type_to_check, float) and
        not isinstance(type_to_check, int)
    ]
)
def angle_mul_type_error(request):
    return request.param


@fixture(
    params=[
        type_to_check for type_to_check in types_to_check
        if not isinstance(type_to_check, float) and
        not isinstance(type_to_check, int) and
        not isinstance(type_to_check, np.ndarray)
    ]
)
def angle_rmul_type_error(request):
    return request.param


@fixture(
    params=[
        type_to_check for type_to_check in types_to_check
        if not isinstance(type_to_check, float) and
        not isinstance(type_to_check, int) and
        not isinstance(type_to_check, AngularPosition) and
        not isinstance(type_to_check, Angle)
    ]
)
def angle_truediv_type_error(request):
    return request.param


@fixture(params=[0, 0.0])
def angle_truediv_zero_division_error(request):
    return request.param


@fixture(
    params=[
        type_to_check for type_to_check in types_to_check
        if not isinstance(type_to_check, AngularPosition) and
        not isinstance(type_to_check, Angle)
    ]
)
def angle_eq_type_error(request):
    return request.param


@fixture(
    params=[
        type_to_check for type_to_check in types_to_check
        if not isinstance(type_to_check, AngularPosition) and 
        not isinstance(type_to_check, Angle)
    ]
)
def angle_ne_type_error(request):
    return request.param


@fixture(
    params=[
        type_to_check for type_to_check in types_to_check
        if not isinstance(type_to_check, AngularPosition) and
        not isinstance(type_to_check, Angle)
    ]
)
def angle_gt_type_error(request):
    return request.param


@fixture(
    params=[
        type_to_check for type_to_check in types_to_check
        if not isinstance(type_to_check, AngularPosition) and
        not isinstance(type_to_check, Angle)
    ]
)
def angle_ge_type_error(request):
    return request.param


@fixture(
    params=[
        type_to_check for type_to_check in types_to_check
        if not isinstance(type_to_check, AngularPosition) and
        not isinstance(type_to_check, Angle)
    ]
)
def angle_lt_type_error(request):
    return request.param


@fixture(
    params=[
        type_to_check for type_to_check in types_to_check
        if not isinstance(type_to_check, AngularPosition) and
        not isinstance(type_to_check, Angle)
    ]
)
def angle_le_type_error(request):
    return request.param


angle_to_type_error_1 = [
    {'target_unit': type_to_check, 'inplace': True}
    for type_to_check in types_to_check if not isinstance(type_to_check, str)
]

angle_to_type_error_2 = [
    {'target_unit': 'target_unit', 'inplace': type_to_check}
    for type_to_check in types_to_check if not isinstance(type_to_check, bool)
    and not isinstance(type_to_check, int)
]


@fixture(params=[*angle_to_type_error_1, *angle_to_type_error_2])
def angle_to_type_error(request):
    return request.param
