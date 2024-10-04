from gearpy.units import AngularPosition
from hypothesis.strategies import composite, floats, sampled_from
import numpy as np
from tests.conftest import types_to_check
from pytest import fixture


basic_angular_position = AngularPosition(1, 'rad')


@composite
def angular_positions(draw, min_value=-1000, max_value=1000, unit=None):
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
            sampled_from(
                elements=list(AngularPosition._AngularPosition__UNITS.keys())
            )
        )

    return AngularPosition(value=value, unit=unit)


angular_position_init_type_error_1 = [
    {'value': type_to_check, 'unit': 'unit'}
    for type_to_check in types_to_check
    if not isinstance(type_to_check, float | int)
]

angular_position_init_type_error_2 = [
    {'value': 1, 'unit': types_to_check} for type_to_check in types_to_check
    if not isinstance(type_to_check, str)
]


@fixture(
    params=[
        *angular_position_init_type_error_1,
        *angular_position_init_type_error_2
    ]
)
def angular_position_init_type_error(request):
    return request.param


@fixture(
    params=[
        type_to_check for type_to_check in types_to_check
        if not isinstance(type_to_check, AngularPosition)
    ]
)
def angular_position_add_type_error(request):
    return request.param


@fixture(
    params=[
        type_to_check for type_to_check in types_to_check
        if not isinstance(type_to_check, AngularPosition)
    ]
)
def angular_position_sub_type_error(request):
    return request.param


@fixture(
    params=[
        type_to_check for type_to_check in types_to_check
        if not isinstance(type_to_check, float | int)
    ]
)
def angular_position_mul_type_error(request):
    return request.param


@fixture(
    params=[
        type_to_check for type_to_check in types_to_check
        if not isinstance(type_to_check, float | int | np.ndarray)
    ]
)
def angular_position_rmul_type_error(request):
    return request.param


@fixture(
    params=[
        type_to_check for type_to_check in types_to_check
        if not isinstance(type_to_check, float | int | AngularPosition)
    ]
)
def angular_position_truediv_type_error(request):
    return request.param


@fixture(params=[0, 0.0, AngularPosition(0, 'rad')])
def angular_position_truediv_zero_division_error(request):
    return request.param


@fixture(
    params=[
        type_to_check for type_to_check in types_to_check
        if not isinstance(type_to_check, AngularPosition)
    ]
)
def angular_position_eq_type_error(request):
    return request.param


@fixture(
    params=[
        type_to_check for type_to_check in types_to_check
        if not isinstance(type_to_check, AngularPosition)
    ]
)
def angular_position_ne_type_error(request):
    return request.param


@fixture(
    params=[
        type_to_check for type_to_check in types_to_check
        if not isinstance(type_to_check, AngularPosition)
    ]
)
def angular_position_gt_type_error(request):
    return request.param


@fixture(
    params=[
        type_to_check for type_to_check in types_to_check
        if not isinstance(type_to_check, AngularPosition)
    ]
)
def angular_position_ge_type_error(request):
    return request.param


@fixture(
    params=[
        type_to_check for type_to_check in types_to_check
        if not isinstance(type_to_check, AngularPosition)
    ]
)
def angular_position_lt_type_error(request):
    return request.param


@fixture(
    params=[
        type_to_check for type_to_check in types_to_check
        if not isinstance(type_to_check, AngularPosition)
    ]
)
def angular_position_le_type_error(request):
    return request.param


angular_position_to_type_error_1 = [
    {'target_unit': type_to_check, 'inplace': True}
    for type_to_check in types_to_check if not isinstance(type_to_check, str)
]

angular_position_to_type_error_2 = [
    {'target_unit': 'target_unit', 'inplace': type_to_check}
    for type_to_check in types_to_check
    if not isinstance(type_to_check, int | bool)
]


@fixture(
    params=[
        *angular_position_to_type_error_1,
        *angular_position_to_type_error_2
    ]
)
def angular_position_to_type_error(request):
    return request.param
