from gearpy.units import InertiaMoment, Length, Torque
from hypothesis.strategies import composite, floats, sampled_from
import numpy as np
from tests.conftest import types_to_check
from pytest import fixture


basic_torque = Torque(1, 'Nm')


@composite
def torques(draw, min_value=-1000, max_value=1000, unit=None):
    value = draw(
        floats(
            allow_nan=False,
            allow_infinity=False,
            min_value=min_value,
            max_value=max_value
        )
    )
    if unit is None:
        unit = draw(sampled_from(elements=list(Torque._Torque__UNITS.keys())))

    return Torque(value=value, unit=unit)


torque_init_type_error_1 = [
    {'value': type_to_check, 'unit': 'unit'}
    for type_to_check in types_to_check
    if not isinstance(type_to_check, float) and
    not isinstance(type_to_check, int)
]

torque_init_type_error_2 = [
    {'value': 1, 'unit': types_to_check} for type_to_check in types_to_check
    if not isinstance(type_to_check, str)
]


@fixture(params=[*torque_init_type_error_1, *torque_init_type_error_2])
def torque_init_type_error(request):
    return request.param


@fixture(
    params=[
        type_to_check for type_to_check in types_to_check
        if not isinstance(type_to_check, Torque)
    ]
)
def torque_add_type_error(request):
    return request.param


@fixture(
    params=[
        type_to_check for type_to_check in types_to_check
        if not isinstance(type_to_check, Torque)
    ]
)
def torque_sub_type_error(request):
    return request.param


@fixture(
    params=[
        type_to_check for type_to_check in types_to_check
        if not isinstance(type_to_check, float) and
        not isinstance(type_to_check, int)
    ]
)
def torque_mul_type_error(request):
    return request.param


@fixture(
    params=[
        type_to_check for type_to_check in types_to_check
        if not isinstance(type_to_check, float) and
        not isinstance(type_to_check, int) and
        not isinstance(type_to_check, np.ndarray)
    ]
)
def torque_rmul_type_error(request):
    return request.param


@fixture(
    params=[
        type_to_check for type_to_check in types_to_check
        if not isinstance(type_to_check, float) and
        not isinstance(type_to_check, int) and
        not isinstance(type_to_check, InertiaMoment) and
        not isinstance(type_to_check, Torque) and
        not isinstance(type_to_check, Length)
    ]
)
def torque_truediv_type_error(request):
    return request.param


@fixture(params=[0, 0.0, Torque(0, 'Nm')])
def torque_truediv_zero_division_error(request):
    return request.param


@fixture(
    params=[
        type_to_check for type_to_check in types_to_check
        if not isinstance(type_to_check, Torque)
    ]
)
def torque_eq_type_error(request):
    return request.param


@fixture(
    params=[
        type_to_check for type_to_check in types_to_check
        if not isinstance(type_to_check, Torque)
    ]
)
def torque_ne_type_error(request):
    return request.param


@fixture(
    params=[
        type_to_check for type_to_check in types_to_check
        if not isinstance(type_to_check, Torque)
    ]
)
def torque_gt_type_error(request):
    return request.param


@fixture(
    params=[
        type_to_check for type_to_check in types_to_check
        if not isinstance(type_to_check, Torque)
    ]
)
def torque_ge_type_error(request):
    return request.param


@fixture(
    params=[
        type_to_check for type_to_check in types_to_check
        if not isinstance(type_to_check, Torque)
    ]
)
def torque_lt_type_error(request):
    return request.param


@fixture(
    params=[
        type_to_check for type_to_check in types_to_check
        if not isinstance(type_to_check, Torque)
    ]
)
def torque_le_type_error(request):
    return request.param


torque_to_type_error_1 = [
    {'target_unit': type_to_check, 'inplace': True}
    for type_to_check in types_to_check if not isinstance(type_to_check, str)
]

torque_to_type_error_2 = [
    {'target_unit': 'target_unit', 'inplace': type_to_check}
    for type_to_check in types_to_check
    if not isinstance(type_to_check, bool) and
    not isinstance(type_to_check, int)
]


@fixture(params=[*torque_to_type_error_1, *torque_to_type_error_2])
def torque_to_type_error(request):
    return request.param
