from gearpy.mechanical_objects import RotatingObject
from tests.conftest import (
    types_to_check,
    basic_spur_gear_1,
    basic_spur_gear_2,
    basic_helical_gear_1,
    basic_helical_gear_2,
    basic_flywheel,
    basic_worm_gear_1,
    basic_worm_gear_2,
    basic_worm_wheel_1,
    basic_worm_wheel_2
)
from pytest import fixture


basic_slaves = [
    basic_spur_gear_1,
    basic_spur_gear_2,
    basic_flywheel,
    basic_helical_gear_1,
    basic_helical_gear_2,
    basic_worm_gear_1,
    basic_worm_gear_2,
    basic_worm_wheel_1,
    basic_worm_wheel_2
]


@fixture(
    params=[
        type_to_check for type_to_check in types_to_check
        if not isinstance(type_to_check, RotatingObject)
    ]
)
def slave_driven_by_type_error(request):
    return request.param


@fixture(
    params=[
        type_to_check for type_to_check in types_to_check
        if not isinstance(type_to_check, RotatingObject)
    ]
)
def slave_drives_type_error(request):
    return request.param


@fixture(
    params=[
        type_to_check for type_to_check in types_to_check
        if not isinstance(type_to_check, float)
    ]
)
def slave_master_gear_ratio_type_error(request):
    return request.param


@fixture(
    params=[
        type_to_check for type_to_check in types_to_check
        if not isinstance(type_to_check, float)
        and not isinstance(type_to_check, int)
        and not isinstance(type_to_check, bool)
    ]
)
def slave_master_gear_efficiency_type_error(request):
    return request.param


@fixture(params=[-1, 2])
def slave_master_gear_efficiency_value_error(request):
    return request.param
