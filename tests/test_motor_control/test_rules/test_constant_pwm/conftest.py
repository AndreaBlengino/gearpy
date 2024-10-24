from gearpy.sensors import Timer
from gearpy.powertrain import Powertrain
from pytest import fixture
from tests.conftest import types_to_check, basic_powertrain, basic_timer


constant_pwm_init_type_error_1 = [
    {
        'timer': type_to_check,
        'powertrain': basic_powertrain,
        'target_pwm_value': 0.8
    }
    for type_to_check in types_to_check if not isinstance(type_to_check, Timer)
]

constant_pwm_init_type_error_2 = [
    {
        'timer': basic_timer,
        'powertrain': type_to_check,
        'target_pwm_value': 0.8
    }
    for type_to_check in types_to_check
    if not isinstance(type_to_check, Powertrain)
]

constant_pwm_init_type_error_3 = [
    {
        'timer': basic_timer,
        'powertrain': basic_powertrain,
        'target_pwm_value': type_to_check
    }
    for type_to_check in types_to_check
    if not isinstance(type_to_check, float | int)
]


@fixture(
    params=[
        *constant_pwm_init_type_error_1,
        *constant_pwm_init_type_error_2,
        *constant_pwm_init_type_error_3
    ]
)
def constant_pwm_init_type_error(request):
    return request.param


@fixture(
    params=[
        {
            'timer': basic_timer,
            'powertrain': basic_powertrain,
            'target_pwm_value': -1.1
        },
        {
            'timer': basic_timer,
            'powertrain': basic_powertrain,
            'target_pwm_value': 1.1
        }
    ]
)
def constant_pwm_init_value_error(request):
    return request.param
