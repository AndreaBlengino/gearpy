from gearpy.mechanical_objects import (
    MotorBase,
    RotatingObject,
    DCMotor,
    SpurGear
)
from gearpy.sensors import AbsoluteRotaryEncoder
from gearpy.powertrain import Powertrain
from gearpy.units import (
    AngularPosition,
    AngularSpeed,
    Current,
    InertiaMoment,
    Torque
)
from gearpy.utils import add_fixed_joint
from pytest import fixture
from tests.conftest import (
    types_to_check,
    basic_encoder,
    basic_spur_gear_1,
    basic_dc_motor_1
)


class PowertrainFake(Powertrain):

    def __init__(self, elements: list):
        self.__elements = elements

    @property
    def elements(self):
        return self.__elements

    @elements.setter
    def elements(self, elements):
        self.__elements = elements


motor = DCMotor(
    name='motor',
    inertia_moment=InertiaMoment(1, 'kgm^2'),
    no_load_speed=AngularSpeed(1000, 'rad/s'),
    maximum_torque=Torque(1, 'Nm'),
    no_load_electric_current=Current(0, 'A'),
    maximum_electric_current=Current(1, 'A')
)
gear = SpurGear(
    name='gear',
    n_teeth=20,
    inertia_moment=InertiaMoment(1, 'kgm^2')
)
add_fixed_joint(master=motor, slave=gear)
powertrain = Powertrain(motor=motor)

start_proportional_to_angular_position_init_type_error_1 = [
    {
        'encoder': type_to_check,
        'powertrain': powertrain,
        'target_angular_position': AngularPosition(1, 'rad'),
        'pwm_min_multiplier': 2
    } for type_to_check in types_to_check
    if not isinstance(type_to_check, AbsoluteRotaryEncoder)
]

start_proportional_to_angular_position_init_type_error_2 = [
    {
        'encoder': basic_encoder, 'powertrain': type_to_check,
        'target_angular_position': AngularPosition(1, 'rad'),
        'pwm_min_multiplier': 2
    } for type_to_check in types_to_check
    if not isinstance(type_to_check, Powertrain)
]

start_proportional_to_angular_position_init_type_error_3 = [
    {
        'encoder': basic_encoder,
        'powertrain': PowertrainFake([type_to_check, basic_spur_gear_1]),
        'target_angular_position': AngularPosition(1, 'rad'),
        'pwm_min_multiplier': 2
    } for type_to_check in types_to_check
    if not isinstance(type_to_check, MotorBase)
]

start_proportional_to_angular_position_init_type_error_4 = [
    {
        'encoder': basic_encoder,
        'powertrain': PowertrainFake([motor, type_to_check]),
        'target_angular_position': AngularPosition(1, 'rad'),
        'pwm_min_multiplier': 2
    } for type_to_check in types_to_check
    if not isinstance(type_to_check, RotatingObject)
]

start_proportional_to_angular_position_init_type_error_5 = [
    {
        'encoder': basic_encoder,
        'powertrain': powertrain,
        'target_angular_position': type_to_check,
        'pwm_min_multiplier': 2
    } for type_to_check in types_to_check
    if not isinstance(type_to_check, AngularPosition)
]

start_proportional_to_angular_position_init_type_error_6 = [
    {
        'encoder': basic_encoder, 'powertrain': powertrain,
        'target_angular_position': AngularPosition(1, 'rad'),
        'pwm_min_multiplier': type_to_check
    } for type_to_check in types_to_check
    if not isinstance(type_to_check, float | int)
]

start_proportional_to_angular_position_init_type_error_7 = [
    {
        'encoder': basic_encoder,
        'powertrain': powertrain,
        'target_angular_position': AngularPosition(1, 'rad'),
        'pwm_min_multiplier': 2,
        'pwm_min': type_to_check
    } for type_to_check in types_to_check
    if not isinstance(type_to_check, float | int) and type_to_check is not None
]


@fixture(
    params=[
        *start_proportional_to_angular_position_init_type_error_1,
        *start_proportional_to_angular_position_init_type_error_2,
        *start_proportional_to_angular_position_init_type_error_3,
        *start_proportional_to_angular_position_init_type_error_4,
        *start_proportional_to_angular_position_init_type_error_5,
        *start_proportional_to_angular_position_init_type_error_6,
        *start_proportional_to_angular_position_init_type_error_7
    ]
)
def start_proportional_to_angular_position_init_type_error(request):
    return request.param


@fixture(
    params=[
        {
            'encoder': basic_encoder,
            'powertrain': PowertrainFake([]),
            'target_angular_position': AngularPosition(1, 'rad'),
            'pwm_min_multiplier': 2
        },
        {
            'encoder': basic_encoder,
            'powertrain': PowertrainFake([basic_dc_motor_1]),
            'target_angular_position': AngularPosition(1, 'rad'),
            'pwm_min_multiplier': 2
        },
        {
            'encoder': basic_encoder,
            'powertrain': powertrain,
            'target_angular_position': AngularPosition(1, 'rad'),
            'pwm_min_multiplier': 1
        },
        {
            'encoder': basic_encoder,
            'powertrain': powertrain,
            'target_angular_position': AngularPosition(1, 'rad'),
            'pwm_min_multiplier': 2, 'pwm_min': 0
        }
    ]
)
def start_proportional_to_angular_position_init_value_error(request):
    return request.param
