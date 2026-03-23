from gearpy.units import (
    AngularPosition,
    AngularSpeed,
    AngularAcceleration,
    Time
)
from gearpy.motor_control.utils import SCurveTrajectory
from hypothesis.strategies import composite
from pytest import fixture
from tests.conftest import types_to_check
from tests.test_units.test_angular_position.conftest import angular_positions
from tests.test_units.test_angular_speed.conftest import angular_speeds
from tests.test_units.test_angular_acceleration.conftest import \
    angular_accelerations
from tests.test_units.test_time.conftest import times


s_curve_trajectory_init_type_error_1 = [
    {
        'start_position': type_to_check,
        'stop_position': AngularPosition(2, 'rad'),
        'maximum_velocity': AngularSpeed(1, 'rad/s'),
        'maximum_acceleration': AngularAcceleration(1, 'rad/s^2'),
        'maximum_deceleration': AngularAcceleration(1, 'rad/s^2'),
        'start_velocity': AngularSpeed(0, 'rad/s'),
        'stop_velocity': AngularSpeed(0, 'rad/s'),
        'start_time': Time(1, 'sec')
    } for type_to_check in types_to_check
    if not isinstance(type_to_check, AngularPosition)
]

s_curve_trajectory_init_type_error_2 = [
    {
        'start_position': AngularPosition(1, 'rad'),
        'stop_position': type_to_check,
        'maximum_velocity': AngularSpeed(1, 'rad/s'),
        'maximum_acceleration': AngularAcceleration(1, 'rad/s^2'),
        'maximum_deceleration': AngularAcceleration(1, 'rad/s^2'),
        'start_velocity': AngularSpeed(0, 'rad/s'),
        'stop_velocity': AngularSpeed(0, 'rad/s'),
        'start_time': Time(1, 'sec')
    } for type_to_check in types_to_check
    if not isinstance(type_to_check, AngularPosition)
]

s_curve_trajectory_init_type_error_3 = [
    {
        'start_position': AngularPosition(1, 'rad'),
        'stop_position': AngularPosition(2, 'rad'),
        'maximum_velocity': types_to_check,
        'maximum_acceleration': AngularAcceleration(1, 'rad/s^2'),
        'maximum_deceleration': AngularAcceleration(1, 'rad/s^2'),
        'start_velocity': AngularSpeed(0, 'rad/s'),
        'stop_velocity': AngularSpeed(0, 'rad/s'),
        'start_time': Time(1, 'sec')
    } for type_to_check in types_to_check
    if not isinstance(type_to_check, AngularSpeed)
]

s_curve_trajectory_init_type_error_4 = [
    {
        'start_position': AngularPosition(1, 'rad'),
        'stop_position': AngularPosition(2, 'rad'),
        'maximum_velocity': AngularSpeed(1, 'rad/s'),
        'maximum_acceleration': type_to_check,
        'maximum_deceleration': AngularAcceleration(1, 'rad/s^2'),
        'start_velocity': AngularSpeed(0, 'rad/s'),
        'stop_velocity': AngularSpeed(0, 'rad/s'),
        'start_time': Time(1, 'sec')
    } for type_to_check in types_to_check
    if not isinstance(type_to_check, AngularAcceleration)
]

s_curve_trajectory_init_type_error_5 = [
    {
        'start_position': AngularPosition(1, 'rad'),
        'stop_position': AngularPosition(2, 'rad'),
        'maximum_velocity': AngularSpeed(1, 'rad/s'),
        'maximum_acceleration': AngularAcceleration(1, 'rad/s^2'),
        'maximum_deceleration': type_to_check,
        'start_velocity': AngularSpeed(0, 'rad/s'),
        'stop_velocity': AngularSpeed(0, 'rad/s'),
        'start_time': Time(1, 'sec')
    } for type_to_check in types_to_check
    if not isinstance(type_to_check, AngularAcceleration)
]

s_curve_trajectory_init_type_error_6 = [
    {
        'start_position': AngularPosition(1, 'rad'),
        'stop_position': AngularPosition(2, 'rad'),
        'maximum_velocity': AngularSpeed(1, 'rad/s'),
        'maximum_acceleration': AngularAcceleration(1, 'rad/s^2'),
        'maximum_deceleration': AngularAcceleration(1, 'rad/s^2'),
        'start_velocity': type_to_check,
        'stop_velocity': AngularSpeed(0, 'rad/s'),
        'start_time': Time(1, 'sec')
    } for type_to_check in types_to_check
    if not isinstance(type_to_check, AngularSpeed) and
    type_to_check is not None
]

s_curve_trajectory_init_type_error_7 = [
    {
        'start_position': AngularPosition(1, 'rad'),
        'stop_position': AngularPosition(2, 'rad'),
        'maximum_velocity': AngularSpeed(1, 'rad/s'),
        'maximum_acceleration': AngularAcceleration(1, 'rad/s^2'),
        'maximum_deceleration': AngularAcceleration(1, 'rad/s^2'),
        'start_velocity': AngularSpeed(0, 'rad/s'),
        'stop_velocity': type_to_check,
        'start_time': Time(1, 'sec')
    } for type_to_check in types_to_check
    if not isinstance(type_to_check, AngularSpeed) and
    type_to_check is not None
]

s_curve_trajectory_init_type_error_8 = [
    {
        'start_position': AngularPosition(1, 'rad'),
        'stop_position': AngularPosition(2, 'rad'),
        'maximum_velocity': AngularSpeed(1, 'rad/s'),
        'maximum_acceleration': AngularAcceleration(1, 'rad/s^2'),
        'maximum_deceleration': AngularAcceleration(1, 'rad/s^2'),
        'start_velocity': AngularSpeed(0, 'rad/s'),
        'stop_velocity': AngularSpeed(0, 'rad/s'),
        'start_time': type_to_check
    } for type_to_check in types_to_check
    if not isinstance(type_to_check, Time) and type_to_check is not None
]


@fixture(
    params=[
        *s_curve_trajectory_init_type_error_1,
        *s_curve_trajectory_init_type_error_2,
        *s_curve_trajectory_init_type_error_3,
        *s_curve_trajectory_init_type_error_4,
        *s_curve_trajectory_init_type_error_5,
        *s_curve_trajectory_init_type_error_6,
        *s_curve_trajectory_init_type_error_7,
        *s_curve_trajectory_init_type_error_8
    ]
)
def s_curve_trajectory_init_type_error(request):
    return request.param


@fixture(
    params=[
        {
            'start_position': AngularPosition(1, 'rad'),
            'stop_position': AngularPosition(1, 'rad'),
            'maximum_velocity': AngularSpeed(1, 'rad/s'),
            'maximum_acceleration': AngularAcceleration(1, 'rad/s^2'),
            'maximum_deceleration': AngularAcceleration(1, 'rad/s^2'),
        },
        {
            'start_position': AngularPosition(1, 'rad'),
            'stop_position': AngularPosition(2, 'rad'),
            'maximum_velocity': AngularSpeed(-1, 'rad/s'),
            'maximum_acceleration': AngularAcceleration(1, 'rad/s^2'),
            'maximum_deceleration': AngularAcceleration(1, 'rad/s^2'),
        },
        {
            'start_position': AngularPosition(1, 'rad'),
            'stop_position': AngularPosition(2, 'rad'),
            'maximum_velocity': AngularSpeed(1, 'rad/s'),
            'maximum_acceleration': AngularAcceleration(-1, 'rad/s^2'),
            'maximum_deceleration': AngularAcceleration(1, 'rad/s^2'),
        },
        {
            'start_position': AngularPosition(1, 'rad'),
            'stop_position': AngularPosition(2, 'rad'),
            'maximum_velocity': AngularSpeed(1, 'rad/s'),
            'maximum_acceleration': AngularAcceleration(1, 'rad/s^2'),
            'maximum_deceleration': AngularAcceleration(-1, 'rad/s^2'),
        },
        {
            'start_position': AngularPosition(1, 'rad'),
            'stop_position': AngularPosition(2, 'rad'),
            'maximum_velocity': AngularSpeed(1, 'rad/s'),
            'maximum_acceleration': AngularAcceleration(1, 'rad/s^2'),
            'maximum_deceleration': AngularAcceleration(1, 'rad/s^2'),
            'start_velocity': AngularSpeed(2, 'rad/s'),
        },
        {
            'start_position': AngularPosition(1, 'rad'),
            'stop_position': AngularPosition(2, 'rad'),
            'maximum_velocity': AngularSpeed(1, 'rad/s'),
            'maximum_acceleration': AngularAcceleration(1, 'rad/s^2'),
            'maximum_deceleration': AngularAcceleration(1, 'rad/s^2'),
            'stop_velocity': AngularSpeed(2, 'rad/s'),
        },
    ]
)
def s_curve_trajectory_init_value_error(request):
    return request.param


@fixture(
    params=[
        type_to_check for type_to_check in types_to_check
        if not isinstance(type_to_check, Time)
    ]
)
def s_curve_trajectory_compute_type_error(request):
    return request.param


@composite
def s_trajectories(draw):
    start_position = draw(angular_positions())
    position_variation = draw(angular_positions(min_value=1))
    velocity_variation = draw(angular_speeds(min_value=1))
    maximum_acceleration = draw(angular_accelerations(min_value=1))
    maximum_deceleration = draw(angular_accelerations(min_value=1))
    start_velocity = draw(angular_speeds())
    stop_velocity = draw(angular_speeds())
    start_time = draw(times())

    return SCurveTrajectory(
        start_position=start_position,
        stop_position=start_position + position_variation,
        maximum_velocity=max(
            start_velocity,
            stop_velocity,
            AngularSpeed(0, 'rad/s')
        ) + velocity_variation,
        maximum_acceleration=maximum_acceleration,
        maximum_deceleration=maximum_deceleration,
        start_velocity=start_velocity,
        stop_velocity=stop_velocity,
        start_time=start_time
    )
