from gearpy.mechanical_objects import MotorBase, RotatingObject
from gearpy.sensors import AbsoluteRotaryEncoder
from gearpy.powertrain import Powertrain
from gearpy.units import AngularPosition, Angle
from pytest import fixture
from tests.conftest import (
    types_to_check,
    basic_powertrain,
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


reach_angular_position_init_type_error_1 = [
    {
        'encoder': type_to_check, 'powertrain': basic_powertrain,
        'target_angular_position': AngularPosition(1, 'rad'),
        'braking_angle': Angle(1, 'rad')
    } for type_to_check in types_to_check
    if not isinstance(type_to_check, AbsoluteRotaryEncoder)
]

reach_angular_position_init_type_error_2 = [
    {
        'encoder': basic_encoder, 'powertrain': type_to_check,
        'target_angular_position': AngularPosition(1, 'rad'),
        'braking_angle': Angle(1, 'rad')
    } for type_to_check in types_to_check
    if not isinstance(type_to_check, Powertrain)
]

reach_angular_position_init_type_error_3 = [
    {
        'encoder': basic_encoder,
        'powertrain': PowertrainFake([type_to_check, basic_spur_gear_1]),
        'target_angular_position': AngularPosition(1, 'rad'),
        'braking_angle': Angle(1, 'rad')
    } for type_to_check in types_to_check
    if not isinstance(type_to_check, MotorBase)
]

reach_angular_position_init_type_error_4 = [
    {
        'encoder': basic_encoder,
        'powertrain': PowertrainFake([basic_dc_motor_1, type_to_check]),
        'target_angular_position': AngularPosition(1, 'rad'),
        'braking_angle': Angle(1, 'rad')
    } for type_to_check in types_to_check
    if not isinstance(type_to_check, RotatingObject)
]

reach_angular_position_init_type_error_5 = [
    {
        'encoder': basic_encoder,
        'powertrain': basic_powertrain,
        'target_angular_position': type_to_check,
        'braking_angle': Angle(1, 'rad')
    } for type_to_check in types_to_check
    if not isinstance(type_to_check, AngularPosition)
]

reach_angular_position_init_type_error_6 = [
    {
        'encoder': basic_encoder,
        'powertrain': basic_powertrain,
        'target_angular_position': AngularPosition(1, 'rad'),
        'braking_angle': type_to_check
    } for type_to_check in types_to_check
    if not isinstance(type_to_check, Angle)
]


@fixture(
    params=[
        *reach_angular_position_init_type_error_1,
        *reach_angular_position_init_type_error_2,
        *reach_angular_position_init_type_error_3,
        *reach_angular_position_init_type_error_4,
        *reach_angular_position_init_type_error_5,
        *reach_angular_position_init_type_error_6
    ]
)
def reach_angular_position_init_type_error(request):
    return request.param
