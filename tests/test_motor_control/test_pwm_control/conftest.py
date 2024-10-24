from gearpy.mechanical_objects import MotorBase, RotatingObject
from gearpy.motor_control import RuleBase
from gearpy.powertrain import Powertrain
from pytest import fixture
from tests.conftest import types_to_check, basic_spur_gear_1, basic_dc_motor_1


class PowertrainFake(Powertrain):

    def __init__(self, elements: list):
        self.__elements = elements

    @property
    def elements(self):
        return self.__elements

    @elements.setter
    def elements(self, elements):
        self.__elements = elements


pwm_control_init_type_error_1 = [
    {'powertrain': type_to_check} for type_to_check in types_to_check
    if not isinstance(type_to_check, Powertrain)
]

pwm_control_init_type_error_2 = [
    {'powertrain': PowertrainFake([type_to_check, basic_spur_gear_1])}
    for type_to_check in types_to_check
    if not isinstance(type_to_check, MotorBase)
]

pwm_control_init_type_error_3 = [
    {'powertrain': PowertrainFake([basic_dc_motor_1, type_to_check])}
    for type_to_check in types_to_check
    if not isinstance(type_to_check, RotatingObject)
]


@fixture(
    params=[
        *pwm_control_init_type_error_1,
        *pwm_control_init_type_error_2,
        *pwm_control_init_type_error_3
    ]
)
def pwm_control_init_type_error(request):
    return request.param


@fixture(
    params=[
        type_to_check for type_to_check in types_to_check
        if not isinstance(type_to_check, RuleBase)
    ]
)
def pwm_control_add_rule_type_error(request):
    return request.param
