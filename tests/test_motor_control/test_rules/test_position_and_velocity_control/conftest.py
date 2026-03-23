from gearpy.powertrain import Powertrain
from gearpy.motor_control.utils import SCurveTrajectory, PIDController
from gearpy.sensors import AbsoluteRotaryEncoder, Tachometer
from pytest import fixture
from tests.conftest import (
    types_to_check,
    basic_encoder,
    basic_tachometer,
    basic_powertrain,
    basic_s_trajectory,
    basic_pid
)


position_and_velocity_control_init_type_error_1 = [
    {
        'encoder': type_to_check,
        'tachometer': basic_tachometer,
        'powertrain': basic_powertrain,
        'position_PID': basic_pid,
        'velocity_PID': basic_pid,
        'trajectory': basic_s_trajectory
    } for type_to_check in types_to_check
    if not isinstance(type_to_check, AbsoluteRotaryEncoder)
]

position_and_velocity_control_init_type_error_2 = [
    {
        'encoder': basic_encoder,
        'tachometer': type_to_check,
        'powertrain': basic_powertrain,
        'position_PID': basic_pid,
        'velocity_PID': basic_pid,
        'trajectory': basic_s_trajectory
    } for type_to_check in types_to_check
    if not isinstance(type_to_check, Tachometer)
]

position_and_velocity_control_init_type_error_3 = [
    {
        'encoder': basic_encoder,
        'tachometer': basic_tachometer,
        'powertrain': type_to_check,
        'position_PID': basic_pid,
        'velocity_PID': basic_pid,
        'trajectory': basic_s_trajectory
    } for type_to_check in types_to_check
    if not isinstance(type_to_check, Powertrain)
]

position_and_velocity_control_init_type_error_4 = [
    {
        'encoder': basic_encoder,
        'tachometer': basic_tachometer,
        'powertrain': basic_powertrain,
        'position_PID': type_to_check,
        'velocity_PID': basic_pid,
        'trajectory': basic_s_trajectory
    } for type_to_check in types_to_check
    if not isinstance(type_to_check, PIDController)
]

position_and_velocity_control_init_type_error_5 = [
    {
        'encoder': basic_encoder,
        'tachometer': basic_tachometer,
        'powertrain': basic_powertrain,
        'position_PID': basic_pid,
        'velocity_PID': type_to_check,
        'trajectory': basic_s_trajectory
    } for type_to_check in types_to_check
    if not isinstance(type_to_check, PIDController)
]

position_and_velocity_control_init_type_error_6 = [
    {
        'encoder': basic_encoder,
        'tachometer': basic_tachometer,
        'powertrain': basic_powertrain,
        'position_PID': basic_pid,
        'velocity_PID': basic_pid,
        'trajectory': type_to_check
    } for type_to_check in types_to_check
    if not isinstance(type_to_check, SCurveTrajectory)
]


@fixture(
    params=[
        *position_and_velocity_control_init_type_error_1,
        *position_and_velocity_control_init_type_error_2,
        *position_and_velocity_control_init_type_error_3,
        *position_and_velocity_control_init_type_error_4,
        *position_and_velocity_control_init_type_error_5,
        *position_and_velocity_control_init_type_error_6
    ]
)
def position_and_velocity_control_init_type_error(request):
    return request.param
