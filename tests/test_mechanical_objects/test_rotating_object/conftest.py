from gearpy.units import (
    AngularAcceleration,
    AngularPosition,
    AngularSpeed,
    Torque
)
from tests.conftest import (
    types_to_check,
    basic_spur_gear_1,
    basic_spur_gear_2,
    basic_dc_motor_1,
    basic_dc_motor_2,
    basic_flywheel,
    basic_worm_gear_1,
    basic_worm_gear_2,
    basic_worm_wheel_1,
    basic_worm_wheel_2
)
from pytest import fixture


basic_rotating_objects = [
    basic_dc_motor_1,
    basic_dc_motor_2,
    basic_spur_gear_1,
    basic_spur_gear_2,
    basic_flywheel,
    basic_worm_gear_1,
    basic_worm_gear_2,
    basic_worm_wheel_1,
    basic_worm_wheel_2
]


@fixture(
    params=[
        type_to_check for type_to_check in types_to_check
        if not isinstance(type_to_check, AngularPosition)
    ]
)
def rotating_object_angular_position_type_error(request):
    return request.param


@fixture(
    params=[
        type_to_check for type_to_check in types_to_check
        if not isinstance(type_to_check, AngularSpeed)
    ]
)
def rotating_object_angular_speed_type_error(request):
    return request.param


@fixture(
    params=[
        type_to_check for type_to_check in types_to_check
        if not isinstance(type_to_check, AngularAcceleration)
    ]
)
def rotating_object_angular_acceleration_type_error(request):
    return request.param


@fixture(
    params=[
        type_to_check for type_to_check in types_to_check
        if not isinstance(type_to_check, Torque)
    ]
)
def rotating_object_torque_type_error(request):
    return request.param


@fixture(
    params=[
        type_to_check for type_to_check in types_to_check
        if not isinstance(type_to_check, Torque)
    ]
)
def rotating_object_driving_torque_type_error(request):
    return request.param


@fixture(
    params=[
        type_to_check for type_to_check in types_to_check
        if not isinstance(type_to_check, Torque)
    ]
)
def rotating_object_load_torque_type_error(request):
    return request.param
