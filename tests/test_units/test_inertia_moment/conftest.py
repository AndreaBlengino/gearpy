from gearpy.units import InertiaMoment
from hypothesis.strategies import composite, floats, sampled_from
import numpy as np
from tests.conftest import types_to_check
from pytest import fixture


basic_inertia_moment = InertiaMoment(1, 'kgm^2')


@composite
def inertia_moments(draw):
    value = draw(
        floats(
            allow_nan=False,
            allow_infinity=False,
            min_value=1e-10,
            exclude_min=True,
            max_value=1000
        )
    )
    unit = draw(
        sampled_from(elements=list(InertiaMoment._InertiaMoment__UNITS.keys()))
    )

    return InertiaMoment(value=value, unit=unit)


inertia_moment_init_type_error_1 = [
    {'value': type_to_check, 'unit': 'unit'}
    for type_to_check in types_to_check
    if not isinstance(type_to_check, float | int)
]

inertia_moment_init_type_error_2 = [
    {'value': 1, 'unit': types_to_check} for type_to_check in types_to_check
    if not isinstance(type_to_check, str)
]


@fixture(
    params=[
        *inertia_moment_init_type_error_1,
        *inertia_moment_init_type_error_2
    ]
)
def inertia_moment_init_type_error(request):
    return request.param


@fixture(
    params=[
        type_to_check for type_to_check in types_to_check
        if not isinstance(type_to_check, InertiaMoment)
    ]
)
def inertia_moment_add_type_error(request):
    return request.param


@fixture(
    params=[
        type_to_check for type_to_check in types_to_check
        if not isinstance(type_to_check, InertiaMoment)
    ]
)
def inertia_moment_sub_type_error(request):
    return request.param


@fixture(
    params=[
        type_to_check for type_to_check in types_to_check
        if not isinstance(type_to_check, float | int)
    ]
)
def inertia_moment_mul_type_error(request):
    return request.param


@fixture(
    params=[
        type_to_check for type_to_check in types_to_check
        if not isinstance(type_to_check, float | int | np.ndarray)
    ]
)
def inertia_moment_rmul_type_error(request):
    return request.param


@fixture(
    params=[
        type_to_check for type_to_check in types_to_check
        if not isinstance(type_to_check, float | int | InertiaMoment)
    ]
)
def inertia_moment_truediv_type_error(request):
    return request.param


@fixture(params=[0, 0.0])
def inertia_moment_truediv_zero_division_error(request):
    return request.param


@fixture(
    params=[
        type_to_check for type_to_check in types_to_check
        if not isinstance(type_to_check, InertiaMoment)
    ]
)
def inertia_moment_eq_type_error(request):
    return request.param


@fixture(
    params=[
        type_to_check for type_to_check in types_to_check
        if not isinstance(type_to_check, InertiaMoment)
    ]
)
def inertia_moment_ne_type_error(request):
    return request.param


@fixture(
    params=[
        type_to_check for type_to_check in types_to_check
        if not isinstance(type_to_check, InertiaMoment)
    ]
)
def inertia_moment_gt_type_error(request):
    return request.param


@fixture(
    params=[
        type_to_check for type_to_check in types_to_check
        if not isinstance(type_to_check, InertiaMoment)
    ]
)
def inertia_moment_ge_type_error(request):
    return request.param


@fixture(
    params=[
        type_to_check for type_to_check in types_to_check
        if not isinstance(type_to_check, InertiaMoment)
    ]
)
def inertia_moment_lt_type_error(request):
    return request.param


@fixture(
    params=[
        type_to_check for type_to_check in types_to_check
        if not isinstance(type_to_check, InertiaMoment)
    ]
)
def inertia_moment_le_type_error(request):
    return request.param


inertia_moment_to_type_error_1 = [
    {'target_unit': type_to_check, 'inplace': True}
    for type_to_check in types_to_check if not isinstance(type_to_check, str)
]

inertia_moment_to_type_error_2 = [
    {'target_unit': 'target_unit', 'inplace': type_to_check}
    for type_to_check in types_to_check
    if not isinstance(type_to_check, int | bool)
]


@fixture(
    params=[*inertia_moment_to_type_error_1, *inertia_moment_to_type_error_2]
)
def inertia_moment_to_type_error(request):
    return request.param
